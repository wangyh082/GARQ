# P2-E5 D13 MetaQ seed 0

## Status and reviewer mapping

**PASS for execution and common evaluation; realized-K matching is NOT yet acceptable.** This is the official MetaQ seed-0 assignment prerequisite for Reviewer 1 Major 5's D13/D16 multi-batch MOFA+ comparison. A label-free requested-K calibration is required before the assignment can enter the final controlled cross-method benchmark.

## Frozen experiment and exact results

Corrected D13 GSE164378 RNA+ADT, 161,764 paired cells; official `metaq-sc` 1.0.6; seed 0; requested K=3,235; labels excluded from construction and used only by the common evaluator.

- Requested/realized K: 3,235/3,065; 170 empty anchor IDs (5.255%).
- Realized K is 5.255% below requested K, narrowly outside the preregistered ±5% acceptance band.
- Wall time: 3,454.68 s; peak CPU RSS: 176,081,576 KiB.
- Size median/mean/max: 45/52.778/14,340; Gini: 0.396859; max/median ratio: 318.667.
- Macro cell-type F1: 0.903263 across 31 numeric input labels; minimum per-type F1: 0.659595.

The extreme 14,340-cell tail is an unfavorable aggregation result and must not be hidden. D13 labels are numeric in the frozen H5AD, so no biological label names are inferred.

## Compatibility and evidence

The accepted run uses the documented MetaQ 1.0.6 package-directory import shim, verified invariant row-order cell-ID restoration, and disabled broken label-only plotting. These compatibility steps do not change assignments or use labels for construction.

- Outputs: `/data/zhangpeiru/GARQ_revision/revision_results/phase2/01_size_resolution/D13/MetaQ/full_seed0_K002/`
- Status: `/data/zhangpeiru/GARQ_revision/revision_results/phase2/logs/P2_E5_D13_MetaQ_seed0.status` (`0`)
- Log: `/data/zhangpeiru/GARQ_revision/revision_results/phase2/logs/P2_E5_D13_MetaQ_seed0.driver.log`
- Adapter: `revision_exp/methods/metaq_adapter.py`
- Evaluator: `revision_exp/methods/common_assignment_evaluator.py`

## Retry plan and acceptance evidence

Run the existing label-free monotone requested-K calibration protocol without examining cell-type performance. Freeze the calibrated requested K before the controlled retry. Acceptance requires realized K within 3,235 ±5%, all 161,764 assignments, unchanged data/representation/seed/method settings, status 0, and common-evaluator completion. Both the current PASS and any calibration attempts must remain preserved.

## Safe wording and limitations

Safe interim wording: “MetaQ completed the full corrected D13 seed-0 run, but realized K=3,065 was 5.26% below the target and the size distribution had a 14,340-cell maximum. We therefore retain this run as execution evidence while performing label-free K calibration before the controlled MOFA+ comparison.”

Do not use the current run for a matched-K superiority claim. Do not describe assignment F1 as MOFA+ integration performance. Do not infer biological identities for D13's numeric cell-type codes.
