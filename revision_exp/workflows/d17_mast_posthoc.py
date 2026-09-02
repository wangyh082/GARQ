"""Quantitative D17 Mast-cell post-hoc analysis of frozen assignments."""
from __future__ import annotations

import argparse, hashlib, json
from pathlib import Path
import numpy as np
import pandas as pd
import yaml
from scipy.stats import fisher_exact


def bh(p):
    p=np.asarray(p,float); n=len(p); order=np.argsort(p); out=np.empty(n); q=1.0
    for rank in range(n-1,-1,-1):
        i=order[rank]; q=min(q,p[i]*n/(rank+1)); out[i]=q
    return out


def group_table(assign, target="Mast Cells"):
    if not assign.cell_id.is_unique: raise ValueError("duplicate assignment cell IDs")
    y=(assign.cell_type.astype(str)==target).to_numpy(); n_target=int(y.sum())
    if not n_target: raise ValueError("no target cells")
    g=assign.assign(_mast=y.astype(int)).groupby("metacell_id",sort=False).agg(metacell_size=("cell_id","size"),mast_count=("_mast","sum")).reset_index()
    n=len(assign); b=n_target/n
    g["mast_purity"]=g.mast_count/g.metacell_size; g["background_abundance"]=b; g["fold_enrichment"]=g.mast_purity/b
    g["fisher_p"]=[fisher_exact([[m,s-m],[n_target-m,n-n_target-(s-m)]],alternative="greater").pvalue for m,s in zip(g.mast_count,g.metacell_size)]
    g["fisher_q"]=bh(g.fisher_p)
    g["is_mast_containing"]=g.mast_count>=1; g["is_associated"]=(g.mast_count>=3)&(g.fold_enrichment>=5)&(g.fisher_q<.05)
    g["is_majority_dominated"]=g.mast_purity>.5; g["is_high_purity"]=g.mast_purity>=.7
    return g,n_target,b


def top_table(g,n_target):
    z=g.sort_values(["fold_enrichment","fisher_q","mast_count","metacell_id"],ascending=[False,True,False,True],kind="mergesort").head(5).copy()
    z["rank"]=np.arange(1,len(z)+1); z["cumulative_capture"]=z.mast_count.cumsum()/n_target
    return z


def summarize(g,n_target,n_cells):
    dom=g[g.is_majority_dominated]; high=g[g.is_high_purity]; assoc=g[g.is_associated]; contain=g[g.is_mast_containing]
    def pooled(z): return (z.mast_count.sum()/z.metacell_size.sum()) if len(z) else np.nan
    sr=dom.mast_count.sum()/n_target; sp=pooled(dom); sf=0 if sr==0 else 2*sr*sp/(sr+sp)
    weights=contain.mast_count/n_target; hhi=float((weights**2).sum()); km=len(contain); nh=1.0 if km<=1 else (hhi-1/km)/(1-1/km)
    top=top_table(g,n_target)
    vals={"strict_recall":sr,"strict_precision":sp,"strict_f1":sf,"high_purity_recall":high.mast_count.sum()/n_target,
      "max_purity":g.mast_purity.max(),"max_fold_enrichment":g.fold_enrichment.max(),"mast_containing_metacell_count":len(contain),
      "associated_metacell_count":len(assoc),"associated_recall":assoc.mast_count.sum()/n_target,"associated_pooled_precision":pooled(assoc),
      "associated_weighted_purity":pooled(assoc),"dominated_metacell_count":len(dom),"high_purity_metacell_count":len(high),
      "top1_capture":top.head(1).mast_count.sum()/n_target,"top3_capture":top.head(3).mast_count.sum()/n_target,"top5_capture":top.mast_count.sum()/n_target,
      "hhi":hhi,"normalized_hhi":nh,"effective_mast_metacells":1/hhi}
    for name,fun in [("min","min"),("q1",lambda x:x.quantile(.25)),("median","median"),("q3",lambda x:x.quantile(.75)),("max","max")]:
        vals["associated_size_"+name]=getattr(assoc.metacell_size,fun)() if isinstance(fun,str) and len(assoc) else (fun(assoc.metacell_size) if len(assoc) else np.nan)
    return vals,top


def permute(assign,g,n_target,b,R,seed):
    codes,_=pd.factorize(assign.metacell_id,sort=False); sizes=np.bincount(codes); rng=np.random.default_rng(seed); K=len(sizes)
    out=np.empty((R,6))
    for r in range(R):
        m=np.bincount(codes[rng.choice(len(codes),n_target,replace=False)],minlength=K); p=m/sizes; fold=p/b
        order=np.lexsort((np.arange(K),-m,-fold)); w=m[m>0]/n_target; h=(w*w).sum(); km=len(w); nh=1 if km<=1 else (h-1/km)/(1-1/km)
        out[r]=[p.max(),fold.max(),m[order[:1]].sum()/n_target,m[order[:3]].sum()/n_target,h,nh]
    return out


def sha256(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for x in iter(lambda:f.read(1024*1024),b""): h.update(x)
    return h.hexdigest()


def main(config,dry_run=False):
    cfg=yaml.safe_load(Path(config).read_text()); out=Path(cfg["result_dir"]); out.mkdir(parents=True,exist_ok=True)
    import anndata as ad
    a=ad.read_h5ad(cfg["metadata_path"],backed="r"); ids=pd.Index(a.obs_names.astype(str)); labels=a.obs[cfg["label_key"]].astype(str); a.file.close()
    exact=int((labels==cfg["target_label"]).sum()); variants=sorted({x for x in labels.unique() if x.strip().lower()==cfg["target_label"].strip().lower()})
    if exact==0 or variants!=[cfg["target_label"]]: raise ValueError(f"target mismatch: exact={exact}, variants={variants}")
    inventory=[]; checks=[]; runs=[]; allg=[]; allt=[]; perml=[]; quant=[]
    for mi,(method,pattern) in enumerate(cfg["methods"].items()):
      for seed in cfg["seeds"]:
        path=Path(pattern.format(seed=seed)); df=pd.read_csv(path); aset=pd.Index(df.cell_id.astype(str)); missing=ids.difference(aset); extra=aset.difference(ids)
        check={"method":method,"seed":seed,"n_metadata":len(ids),"n_assignment":len(df),"n_matched":len(ids.intersection(aset)),"n_missing":len(missing),"n_extra":len(extra),"duplicate_count":int(aset.duplicated().sum()),"id_set_equal":len(missing)==len(extra)==0,"order_equal":ids.equals(aset)}; checks.append(check)
        inventory.append({"dataset":cfg["dataset"],"method":method,"seed":seed,"path":str(path.resolve()),"sha256":sha256(path),"available":True})
        if not check["id_set_equal"] or check["duplicate_count"]: raise ValueError(f"ID mismatch {method} seed {seed}: {check}")
        df=df.set_index(df.cell_id.astype(str)).loc[ids].reset_index(drop=True); df["cell_type"]=labels.to_numpy()
        if dry_run: continue
        g,nt,b=group_table(df,cfg["target_label"]); vals,top=summarize(g,nt,len(df)); rk=int(df.requested_K.iloc[0]) if "requested_K" in df else cfg["requested_k"]; real=len(g)
        base={"dataset":cfg["dataset"],"method":method,"seed":seed,"n_cells":len(df),"mast_count":nt,"mast_abundance":b,"requested_K":rk,"realized_K":real,"empty_count":max(0,rk-real),"compression_ratio":len(df)/real}
        obs=[vals[x] for x in ["max_purity","max_fold_enrichment","top1_capture","top3_capture","hhi","normalized_hhi"]]
        null=permute(df,g,nt,b,int(cfg["permutations"]),int(cfg["random_seed"])+mi*100+seed)
        metrics=["max_purity","max_fold_enrichment","top1_capture","top3_capture","hhi","normalized_hhi"]
        pvals=[]
        for j,m in enumerate(metrics):
            p=(1+int((null[:,j]>=obs[j]-1e-15).sum()))/(len(null)+1); pvals.append(p); sd=null[:,j].std(ddof=1)
            perml.append({**{k:base[k] for k in ["dataset","method","seed"]},"metric":m,"observed":obs[j],"null_mean":null[:,j].mean(),"null_sd":sd,"null_q95":np.quantile(null[:,j],.95),"empirical_p":p,"z_score":((obs[j]-null[:,j].mean())/sd if sd else np.nan)})
            for q in [.01,.05,.5,.95,.99]: quant.append({"dataset":cfg["dataset"],"method":method,"seed":seed,"metric":m,"quantile":q,"value":np.quantile(null[:,j],q)})
        level="A" if vals["strict_recall"]>0 else ("B" if vals["associated_metacell_count"]>=1 and vals["associated_recall"]>=.2 and vals["max_fold_enrichment"]>=5 and pvals[5]<.05 and pvals[3]<.05 else ("C" if vals["associated_metacell_count"]>=1 else "D"))
        runs.append({**base,**vals,"evidence_level":level}); g=pd.concat([pd.DataFrame({"dataset":[cfg["dataset"]]*len(g),"method":[method]*len(g),"seed":[seed]*len(g),"requested_K":[rk]*len(g),"realized_K":[real]*len(g)}),g.reset_index(drop=True)],axis=1); allg.append(g)
        top=top.rename(columns={"metacell_size":"size","mast_purity":"purity","fisher_q":"q_value"}); top.insert(0,"seed",seed); top.insert(0,"method",method); top.insert(0,"dataset",cfg["dataset"]); allt.append(top[["dataset","method","seed","rank","metacell_id","size","mast_count","purity","fold_enrichment","q_value","cumulative_capture"]])
    pd.DataFrame(inventory).to_csv(out/"input_inventory.csv",index=False); pd.DataFrame(checks).to_csv(out/"id_alignment_checks.csv",index=False)
    resolved={**cfg,"metadata_sha256":sha256(cfg["metadata_path"]),"target_count":exact,"target_abundance":exact/len(ids),"exact_label_variants":variants}; (out/"resolved_config.yaml").write_text(yaml.safe_dump(resolved,sort_keys=False))
    if dry_run: return
    run=pd.DataFrame(runs); run.to_csv(out/"mast_run_level_summary.csv",index=False); pd.concat(allg).to_csv(out/"mast_metacell_level_metrics.csv",index=False); pd.concat(allt).to_csv(out/"mast_top_metacells.csv",index=False)
    perm=pd.DataFrame(perml); perm["empirical_p_bh_within_run"]=perm.groupby(["method","seed"]).empirical_p.transform(bh); perm.to_csv(out/"mast_permutation_summary.csv",index=False); pd.DataFrame(quant).to_csv(out/"mast_permutation_null_quantiles.csv",index=False)
    metrics=["strict_recall","strict_f1","max_purity","max_fold_enrichment","associated_recall","associated_metacell_count","top1_capture","top3_capture","top5_capture","normalized_hhi","associated_size_median"]
    rows=[]
    for method,z in run.groupby("method",sort=False):
        x={"dataset":cfg["dataset"],"method":method,"number_of_valid_seeds":len(z),"strict_recovery_seed_count":int((z.strict_recall>0).sum()),"partial_localized_seed_count":int((z.evidence_level=="B").sum()),"evidence_level":("A" if (z.evidence_level=="A").any() else ("B" if (z.evidence_level=="B").sum()>=2 else ("C" if (z.evidence_level=="C").any() else "D")))}
        for m in metrics:
            x.update({m+"_mean":z[m].mean(),m+"_sd":z[m].std(ddof=1),m+"_median":z[m].median(),m+"_min":z[m].min(),m+"_max":z[m].max()})
        rows.append(x)
    pd.DataFrame(rows).to_csv(out/"mast_method_summary.csv",index=False)
    print(json.dumps({"runs":len(run),"target_count":exact,"output":str(out)},indent=2))

if __name__=="__main__":
    p=argparse.ArgumentParser(); p.add_argument("--config",required=True); p.add_argument("--dry-run",action="store_true"); a=p.parse_args(); main(a.config,a.dry_run)
