import numpy as np, pandas as pd, pytest
from revision_exp.workflows.d17_mast_posthoc import bh, group_table, summarize, top_table, permute

def frame(groups,labels): return pd.DataFrame({"cell_id":[f"c{i}" for i in range(len(groups))],"metacell_id":groups,"cell_type":labels})
def test_pure_target_metacell():
 g,n,_=group_table(frame(["a"]*3+["b"]*3,["Mast Cells"]*3+["Other"]*3)); s,_=summarize(g,n,6); assert s["strict_recall"]==s["strict_precision"]==s["strict_f1"]==1
def test_enriched_without_majority():
 g,n,_=group_table(frame(["a"]*20+["b"]*80,["Mast Cells"]*5+["Other"]*15+["Mast Cells"]*5+["Other"]*75)); s,_=summarize(g,n,100); assert s["strict_recall"]==0 and g.fold_enrichment.max()>1
def test_no_target_errors():
 with pytest.raises(ValueError): group_table(frame([1,1],["Other","Other"]))
def test_no_associated_is_nan():
 g,n,_=group_table(frame([1,1,2,2],["Mast Cells","Other","Other","Other"])); s,_=summarize(g,n,4); assert np.isnan(s["associated_size_median"])
def test_bh_standard(): assert np.allclose(bh([.01,.04,.03]),[.03,.04,.04])
def test_top_tie_stable():
 g,n,_=group_table(frame(["b","a","b","a"],["Mast Cells","Mast Cells","Other","Other"])); assert top_table(g,n).metacell_id.tolist()==["a","b"]
def test_permutation_reproducible():
 d=frame([1,1,2,2],["Mast Cells","Other","Other","Other"]); g,n,b=group_table(d); assert np.array_equal(permute(d,g,n,b,20,4),permute(d,g,n,b,20,4))
def test_arbitrary_labels_invariant():
 d=frame([1,1,2,2],["Mast Cells","Other","Other","Other"]); g,n,_=group_table(d); d.metacell_id=d.metacell_id.map({1:"x",2:"y"}); h,nn,_=group_table(d); assert summarize(g,n,4)[0]["hhi"]==summarize(h,nn,4)[0]["hhi"]
