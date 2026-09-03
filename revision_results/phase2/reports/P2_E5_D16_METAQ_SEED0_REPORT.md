# P2-E5 D16 MetaQ seed 0

## Status and reviewer mapping

**PASS in the established `MetqQ2` environment.** This adds the official MetaQ seed-0 assignment prerequisite for Reviewer 1 Major 5's unified D13/D16 multi-batch MOFA+ comparison. It does not complete that reviewer comment.

## Frozen experiment and exact results

Corrected D16 GSE140203 RNA+ATAC, 32,231 paired cells; official `metaq-sc` 1.0.6; seed 0; requested K=645; labels excluded from construction and used only in the external common evaluator.

- Requested/realized K: 645/645; empty metacells: 0.
- Wall time: 2,842.65 s; peak CPU RSS: 191,147,056 KiB.
- Size median/mean/max: 53/49.971/65; Gini: 0.096881.
- Macro cell-type F1: 0.821613.
- Schwann Cell: 163 cells (abundance 0.005057); precision 0.912698, recall 0.705521, F1 0.795848; majority retention 0.705521; high-purity recovery 0.066667.

MetaQ exceeded the seed-0 KMeans and SEACells Schwann-cell recall/F1, but one seed and one method arm cannot establish superiority.

## Compatibility disclosures and failed attempt

The accepted run uses the previously documented MetaQ 1.0.6 package-directory import shim, verified invariant row-order cell-ID restoration, and disabled broken label-only plotting; labels remain external to construction.

A separate invocation in the older `MetaQ` environment **FAILed before assignment** because its `anndata/h5py` stack could not read the D16 `/obs/domain` dataset (`TypeError: Unsupported integer size (0)`). This is an engineering compatibility failure, not a scientific result. It did not change the accepted run's data, seed, K, method, or evaluator. The older attempt reused the same log pathname while the established job was active, so the log contains the old-environment traceback and is not the sole PASS evidence. Acceptance is based on the independent status file `0`, 32,231-cell assignment, `summary.json` status PASS, K=645/645, and complete common-evaluator outputs. This logging collision is disclosed rather than hidden.

## Evidence paths

- Outputs: `/data/zhangpeiru/GARQ_revision/revision_results/phase2/01_size_resolution/D16/MetaQ/full_seed0_K002/`
- Status: `/data/zhangpeiru/GARQ_revision/revision_results/phase2/logs/P2_E5_D16_MetaQ_seed0.status`
- Mixed/failed-attempt log: `/data/zhangpeiru/GARQ_revision/revision_results/phase2/logs/P2_E5_D16_MetaQ_seed0.driver.log`
- Adapter: `revision_exp/methods/metaq_adapter.py`
- Evaluator: `revision_exp/methods/common_assignment_evaluator.py`

## Safe wording and limitations

Safe interim wording: “The official MetaQ seed-0 control completed on corrected D16 at K=645 and recovered Schwann Cells with recall 0.706 and F1 0.796. This is one assignment arm; common MOFA+ and global-versus-batch-stratified analyses are still required before addressing the full batch-workflow comment.”

Do not claim MetaQ or GARQ superiority from this seed. Do not describe these assignment metrics as MOFA+ integration performance. Retain the older-environment failure and log-collision disclosure.

