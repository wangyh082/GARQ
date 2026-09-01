# R2 Major 1 — D18 corrected full-data RNA cell permutation

## Status and reviewer mapping

**PASS for corrected retry1 seeds 0–2; negative for strong perturbation robustness.** This is the first completed condition in the D18 thinning/permutation grid supporting Reviewer 2 Major 1 and Reviewer 1 Major 2.

## Preserved invalid first attempt

The initial seed-0 and seed-1 processes exited with status 0 but are scientifically **FAIL/INVALID**: their assignment hashes were byte-identical to the corresponding unperturbed baselines. Root cause was an engineering control-flow defect: `modality_perturbations` was only materialized when `cell_limit` was set, while corrected full-data configs omit `cell_limit`. Original outputs, logs, and status files remain under `noise_full`; they are excluded from every scientific summary.

The compatibility-equivalent fix materializes the complete 25,517-cell dataset whenever a perturbation is configured, even without subsampling. A full-size permutation regression test was added. Corrected runs use independent `retry1` output directories. Provenance confirms `subset_applied=true`, RNA `cell_permutation`, and perturbation seeds 8104/9104/10104; assignment hashes differ from baseline.

## Frozen corrected experiment and exact results

D18 RNA+ATAC+ADT, 25,517 cells; RNA rows permuted while ATAC/ADT and cell identifiers remain fixed; requested K=510; resolution approximately 0.02; 300 epochs; batch 256; kNN5.

| seed | realized K | empty | macro F1 | precision | recall | purity | median/max size | ARI vs baseline | NMI vs baseline | VI (nats) | wall | peak RSS |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 510 | 0 | 0.676858 | 0.718688 | 0.657405 | 0.862426 | 51/123 | 0.037044 | 0.473379 | 6.454182 | 45:16.93 | 80,993,060 KiB |
| 1 | 510 | 0 | 0.673422 | 0.705443 | 0.658773 | 0.846531 | 51/92 | 0.033632 | 0.479079 | 6.419563 | 46:41.30 | 81,037,712 KiB |
| 2 | 508 | 2 | 0.662972 | 0.701823 | 0.645096 | 0.842188 | 50/165 | 0.040146 | 0.474270 | 6.370578 | 45:42.59 | 80,993,268 KiB |

Label-based macro-F1 changed only moderately, but clustering identity changed radically: same-seed ARI was only 0.034–0.040. The high Rand-style coassignment agreement (0.994–0.996) is not interpreted as robustness because at K approximately 510 almost all random cell pairs are negative in both partitions.

## Evidence, commands, tests, and limitations

- Corrected results: `/data/zhangpeiru/GARQ_revision/revision_results/phase2/02_modality/noise_full_retry1/D18/RNA_cell_permutation/seed{0,1,2}`
- Invalid first attempt: `/data/zhangpeiru/GARQ_revision/revision_results/phase2/02_modality/noise_full/D18/RNA_cell_permutation/seed{0,1}`
- Corrected configs: `revision_exp/configs/noise_full/p2_D18_noise_RNA_cell_permutation_seed{0,1,2}.yaml`
- Workflow fix: `revision_exp/workflows/legacy.py`
- Test: `revision_exp/tests/test_modality_perturbation.py::test_full_size_cell_permutation_is_materialized`
- Standard tests: 29 passed, 13 warnings

Safe wording: “Permuting RNA while holding the other modalities fixed produced similar label-level macro-F1 but a nearly complete reorganization of metacell membership (ARI 0.034–0.040), indicating that apparently stable aggregate label metrics should not be interpreted as assignment robustness.”

Do not claim robustness to RNA corruption, and do not treat cell permutation as a realistic measurement-noise model. It is a destructive negative control. Other modality permutations and count-thinning levels remain in progress.
