# P2-E5 D16 SEACells seed 0

## Status and reviewer mapping

**PASS on compatibility-equivalent retry1.** This adds the official SEACells seed-0 assignment prerequisite for the unified D13/D16 multi-batch MOFA+ comparison requested by Reviewer 1 Major 5. The reviewer comment is not complete until the remaining method/dataset assignments, common MOFA+ fits, and global-versus-batch-stratified diagnostic are complete.

## Frozen experiment and exact results

Corrected D16 GSE140203 RNA+ATAC, 32,231 paired cells; fixed equal-weight RNA-PCA/ATAC-LSI representation; official SEACells 0.3.3; seed 0; requested K=645; labels excluded from construction and used only by the common evaluator.

- Requested/realized K: 645/645; empty metacells: 0.
- Wall time: 3,865.20 s; peak CPU RSS: 19,164,200 KiB.
- Size median/mean/max: 46/49.971/159; Gini: 0.350546.
- Macro cell-type F1: 0.763452.
- Schwann Cell: 163 cells (abundance 0.005057); precision 0.590909, recall 0.239264, F1 0.340611; majority retention 0.239264; high-purity recovery 0.021505.

The Schwann-cell result is unfavorable: it is lower than the matched fixed-representation KMeans seed-0 recall/F1 (0.349693/0.478992). This does not support uniformly strong rare-state preservation.

## Failure and retry evidence

The initial attempt **FAILed before data loading** because it invoked the `MetqQ2` environment, which does not contain SEACells (`ModuleNotFoundError: No module named 'SEACells'`). This was an engineering environment-selection error, not a scientific result. The complete initial stderr is retained at:

`/data/zhangpeiru/GARQ_revision/revision_results/phase2/logs/P2_E5_D16_SEACells_seed0.driver.log`

Retry1 used the pre-existing official environment `/home/zhangpeiru/.conda/envs/seacells/bin/python` without changing data, representation, seed, K, SEACells settings, or evaluator. During monitoring, an accidental duplicate invocation of the identical retry was detected writing to the same destination; only the later project-owned duplicate PID was terminated after exact command inspection, and the earlier run continued to completion. The shared retry log can therefore contain interleaved/truncated progress text and is not used as sole acceptance evidence. Acceptance instead requires the completed assignment (32,231 unique input cells), `summary.json` status PASS, K=645/645, complete size/per-type outputs, and successful common-evaluator terminal line.

## Evidence paths

- Successful outputs: `/data/zhangpeiru/GARQ_revision/revision_results/phase2/01_size_resolution/D16/SEACells/full_seed0_K002_retry1/`
- Retry log: `/data/zhangpeiru/GARQ_revision/revision_results/phase2/logs/P2_E5_D16_SEACells_seed0_retry1.driver.log`
- Adapter: `revision_exp/methods/seacells_adapter.py`
- Common evaluator: `revision_exp/methods/common_assignment_evaluator.py`

## Safe response wording and limitations

Safe interim wording: “Official SEACells completed the corrected D16 seed-0 assignment at the requested K. Schwann-cell recall was 0.239 (F1 0.341), so this result does not support uniformly strong rare-state preservation. Unified MOFA+ and batch-workflow sensitivity remain in progress.”

Do not claim that SEACells or GARQ is superior from one seed. Do not call this a batch-integration or MOFA+ result. The process-launch incident did not alter the accepted assignment, but its logging limitation must remain disclosed.

