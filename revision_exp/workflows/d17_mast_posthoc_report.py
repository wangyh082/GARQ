"""Render D17 Mast post-hoc figures, report, and rebuttal-ready prose."""
from __future__ import annotations
import argparse
from pathlib import Path
import numpy as np
import pandas as pd
import yaml
import matplotlib.pyplot as plt

COLORS={"GARQ":"#0072B2","MetaQ":"#D55E00","SEACells":"#009E73","KMeans":"#CC79A7"}

def fmt(x,n=3): return "NA" if pd.isna(x) else f"{x:.{n}f}"

def markdown(df):
    def cell(x): return fmt(x,4) if isinstance(x,(float,np.floating)) else str(x)
    head="| " + " | ".join(df.columns) + " |"
    sep="|" + "|".join(["---"]*len(df.columns)) + "|"
    rows=["| " + " | ".join(cell(x) for x in row) + " |" for row in df.itertuples(index=False,name=None)]
    return "\n".join([head,sep,*rows])

def figures(out,run,meta,perm):
    methods=list(run.method.drop_duplicates()); pos={m:i for i,m in enumerate(methods)}
    fig,ax=plt.subplots(2,2,figsize=(10,8)); panels=[("strict_recall","Strict Mast-cell recall"),("max_purity","Maximum Mast-cell purity"),("associated_metacell_count","No. Mast-associated metacells")]
    for a,(col,label) in zip(ax.flat[:3],panels):
      for m,z in run.groupby("method",sort=False):
        x=pos[m]+(z.seed.to_numpy()-1)*.07; a.scatter(x,z[col],color=COLORS.get(m),s=36,zorder=3); a.errorbar(pos[m],z[col].mean(),yerr=z[col].std(ddof=1),fmt="_",color="black",capsize=3)
        if col=="associated_metacell_count": a.scatter(x,z.dominated_metacell_count,facecolors="none",edgecolors=COLORS.get(m),s=45)
      a.set_xticks(range(len(methods)),methods,rotation=20); a.set_ylabel(label); a.grid(axis="y",alpha=.2)
      if col=="strict_recall": a.set_ylim(0,1)
      if col=="max_purity": a.axhline(.5,ls="--",color="gray"); a.axhline(.7,ls=":",color="gray"); a.set_ylim(0,1)
    a=ax.flat[3]
    assoc=meta[meta.is_associated.astype(bool)]
    for m,z in assoc.groupby("method",sort=False): a.scatter([pos[m]]*len(z),z.metacell_size,color=COLORS.get(m),alpha=.7)
    a.set_xticks(range(len(methods)),methods,rotation=20); a.set_ylabel("Number of cells per Mast-associated metacell"); a.grid(axis="y",alpha=.2)
    fig.tight_layout()
    for ext in ["pdf","svg"]: fig.savefig(out/f"Fig4b_mast_quantitative.{ext}",bbox_inches="tight")
    fig.savefig(out/"Fig4b_mast_quantitative.png",dpi=300,bbox_inches="tight"); plt.close(fig)
    fig,ax=plt.subplots(2,2,figsize=(10,7))
    for col,a in zip(["top1_capture","top3_capture","top5_capture"],ax.flat[:3]):
      for m,z in run.groupby("method",sort=False): a.scatter([pos[m]]*len(z),z[col],color=COLORS.get(m)); a.set_title(col.replace("_"," ")); a.set_xticks(range(len(methods)),methods,rotation=20); a.set_ylim(0,1)
    p=perm[perm.metric.isin(["normalized_hhi","top3_capture"])]
    for (m,metric),z in p.groupby(["method","metric"]): ax.flat[3].scatter([pos[m]+(-.05 if metric=="normalized_hhi" else .05)]*len(z),z.empirical_p,label=metric if m==methods[0] else None,color=COLORS.get(m),marker="o" if metric=="normalized_hhi" else "x")
    ax.flat[3].axhline(.05,ls="--",color="gray"); ax.flat[3].set_yscale("log"); ax.flat[3].set_xticks(range(len(methods)),methods,rotation=20); ax.flat[3].set_title("Permutation empirical P"); ax.flat[3].legend(fontsize=8)
    fig.tight_layout(); fig.savefig(out/"FigS_mast_enrichment_capture.pdf",bbox_inches="tight"); plt.close(fig)

def main(result_dir,output):
    out=Path(result_dir); run=pd.read_csv(out/"mast_run_level_summary.csv"); method=pd.read_csv(out/"mast_method_summary.csv"); meta=pd.read_csv(out/"mast_metacell_level_metrics.csv"); perm=pd.read_csv(out/"mast_permutation_summary.csv"); cfg=yaml.safe_load((out/"resolved_config.yaml").read_text())
    figures(out,run,meta,perm); garq=run[run.method=="GARQ"]; gm=method[method.method=="GARQ"].iloc[0]; level=gm.evidence_level
    superiority=True
    for seed in sorted(run.seed.unique()):
      g=run[(run.method=="GARQ")&(run.seed==seed)].iloc[0]; c=run[(run.method!="GARQ")&(run.seed==seed)]
      if not all((g[x]>c[x]).all() for x in ["strict_recall","associated_recall","top3_capture","max_purity"]): superiority=False
    p_hhi=perm[(perm.method=="GARQ")&(perm.metric=="normalized_hhi")].sort_values("seed").empirical_p.tolist()
    strict=garq.strict_recall.mean(); assoc=garq.associated_recall.mean(); maxp=(garq.max_purity.min(),garq.max_purity.max()); fold=(garq.max_fold_enrichment.min(),garq.max_fold_enrichment.max())
    if level=="B": core=f"Under the strict majority criterion, GARQ did not achieve complete Mast-cell recovery. Nevertheless, the existing assignments showed partial localized preservation (mean associated recall {assoc:.1%}; maximum purity {maxp[0]:.3f}–{maxp[1]:.3f}; maximum enrichment {fold[0]:.1f}–{fold[1]:.1f}-fold)."
    elif level=="C": core="GARQ retained detectable Mast-cell enrichment in a small number of metacells, but the enrichment-based recall and permutation evidence did not support robust population-level preservation."
    elif level=="D": core="The existing assignments did not support Mast-cell preservation under either the strict majority or the enrichment-based criteria."
    else: core=f"GARQ achieved strict majority-level recovery in {int((garq.strict_recall>0).sum())}/3 seeds (mean strict recall {strict:.3f})."
    table=markdown(run[["method","seed","realized_K","strict_recall","strict_f1","associated_metacell_count","associated_recall","max_purity","max_fold_enrichment","top3_capture","normalized_hhi","evidence_level"]])
    ptable=markdown(perm[perm.metric.isin(["top3_capture","normalized_hhi"])][["method","seed","metric","observed","null_mean","null_q95","empirical_p"]])
    report=f"""# D17 Mast Cells Existing-Assignment Post-hoc Analysis

## Executive summary

{core} GARQ's evidence level is **{level}**. Comparative superiority is **{'supported' if superiority else 'not supported'}** under the preregistered all-comparator, same-seed rule. The original binary/unique-retention wording should therefore be replaced by quantitative strict, enrichment, and permutation results.

## Inputs and provenance

This analysis used frozen assignments only; it did not retrain, tune, or alter assignments. Dataset: `{cfg['dataset']}`; exact label: `{cfg['target_label']}`; target count: {cfg['target_count']}/{sum(run.n_cells.unique())} ({cfg['target_abundance']:.4%}); requested K: {cfg['requested_k']}; seeds: 0–2. Metadata SHA256: `{cfg['metadata_sha256']}`. Assignment paths and SHA256 hashes are recorded in `input_inventory.csv`; exact ID-set checks are in `id_alignment_checks.csv`. Available methods were GARQ, MetaQ, SEACells, and KMeans. MetaCell V2 and SuperCell assignments were unavailable.

## Definitions

Strict majority recovery uses purity >0.5; high purity uses purity >=0.7. An associated metacell requires at least 3 Mast Cells, >=5-fold enrichment, and within-run Fisher/BH q<0.05. Top-k capture ranks by enrichment, q-value, Mast count, and stable metacell ID. Fixed-assignment label permutations (10,000 per method/seed) test concentration using maximum purity/enrichment, top-1/top-3 capture, HHI, and normalized HHI.

## Results

{table}

Permutation results for the two evidence-gating concentration measures:

{ptable}

All six permutation statistics are in `mast_permutation_summary.csv`; metacell-level Fisher/BH results and sizes are in `mast_metacell_level_metrics.csv`.

## Interpretation

Visual detectability in a UMAP, strict majority recovery, and partial localized preservation are distinct. The evidence level above was assigned automatically from the preregistered thresholds. Enrichment or concentration does not by itself establish strict recovery. No UMAP-only conclusion was used.

## Figure and table mapping

Replace the Mast-cell portion of Figure 4b with `Fig4b_mast_quantitative` and place the enrichment/capture panel in a Supplementary Figure. Use `mast_run_level_summary.csv` and `mast_metacell_level_metrics.csv` as the source for a new Supplementary Table. Replace any binary statement that GARQ uniquely retained Mast Cells with: “{core}”

## Limitations

D17 annotations are study-derived. This post-hoc analysis did not retrain or optimize assignments. UMAP is qualitative and was not used as a retention criterion. Enrichment evidence is not equivalent to strict recovery. MetaCell V2 and SuperCell assignments were unavailable. Only three seeds were available. Comparator claims are restricted to matched existing assignments and do not establish trajectory superiority.
"""
    Path(output).parent.mkdir(parents=True,exist_ok=True); Path(output).write_text(report)
    response=f"""# D17 Mast-cell response-ready text

## Response Letter

We thank the reviewer for raising this point. {core} We therefore removed the binary superiority statement and now report strict majority recovery, enrichment-based associated recall, top-k capture, metacell sizes, and fixed-assignment permutation tests across three seeds. Comparative superiority was not supported under our preregistered same-seed criterion. [AUTHOR INPUT REQUIRED: MetaCell V2 assignment not available] [AUTHOR INPUT REQUIRED: SuperCell assignment not available]

## Changes in the revised manuscript

We replaced the qualitative Mast-cell retained/lost panel with a quantitative four-panel display of strict recall, maximum purity, the number of associated metacells, and associated-metacell size. We added complete seed-level and permutation results to the Supplementary Tables and explicitly separated strict majority recovery from partial enrichment.

## Revised Results paragraph

Mast Cells comprised {cfg['target_count']} of {int(run.n_cells.iloc[0])} cells ({cfg['target_abundance']:.2%}). {core} Across GARQ seeds, mean strict recall was {strict:.3f}, mean associated recall was {assoc:.3f}, maximum purity ranged from {maxp[0]:.3f} to {maxp[1]:.3f}, and maximum enrichment ranged from {fold[0]:.1f}- to {fold[1]:.1f}-fold. The normalized-HHI permutation P values were {', '.join(fmt(x,4) for x in p_hhi)}. These measurements do not support a claim that GARQ uniquely retained Mast Cells.

## Revised Figure 4b legend

Quantitative evaluation of Mast-cell organization in existing D17 assignments. Points denote seeds (0–2) and bars denote mean ± SD. Panels show strict majority-level recall, maximum Mast-cell purity (dashed lines at 0.5 and 0.7), the number of enrichment-defined associated metacells (open symbols: majority-dominated count), and sizes of associated metacells. No zero size is plotted when no associated metacell exists.

## Supplementary Methods paragraph

For metacell $M_k$, Mast-cell purity was defined as $p_{{Mast}}(M_k)=\\sum_{{i\\in M_k}}\\mathbb{{I}}(y_i=\\mathrm{{Mast}})/|M_k|$. A metacell was Mast-cell dominated when $p_{{Mast}}>0.5$ and high purity when $p_{{Mast}}\\geq0.7$. We tested over-representation by one-sided Fisher exact tests with Benjamini--Hochberg correction within each method and seed. Associated metacells contained at least three Mast Cells, showed at least five-fold enrichment, and had adjusted $P<0.05$. We report associated recall, number and size, maximum purity and enrichment, top-one/three/five capture, and concentration. Label-permutation tests with 10,000 repetitions preserved the assignments, metacell sizes, and total Mast-cell count.
"""
    (Path(output).parent/"D17_MAST_RESPONSE_READY_TEXT.md").write_text(response)

if __name__=="__main__":
 p=argparse.ArgumentParser(); p.add_argument("--result-dir",required=True); p.add_argument("--output",required=True); a=p.parse_args(); main(a.result_dir,a.output)
