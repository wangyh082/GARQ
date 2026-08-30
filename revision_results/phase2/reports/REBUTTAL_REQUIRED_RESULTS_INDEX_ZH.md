# 回复信所需结果交付索引

本文件是回复信结果的权威进度索引。每个实验必须标记 `PASS`、`FAIL`、`BLOCKED` 或 `RUNNING`；只有 `PASS` 且完成复核的结果才能作为正式回复证据。失败实验必须链接原始日志、根因和 retry 方案。

| 所需结果 | 对应审稿意见 | 状态 | 当前权威文件或运行证据 | 回复信可用性 |
|---|---|---|---|---|
| Final realized-K table | R1 Major 1；R2 Major 2 | PASS | `01_size_resolution/full_benchmark_long.csv`、`metacell_size_summary.csv` | 可用于主分辨率回复；0.01/0.05 sensitivity 尚缺 |
| Final method-input table | R2 Major 2 | PARTIAL | `reports/BASELINE_IMPLEMENTATION_TABLE_PHASE2.md`、resolved configs、representation provenance | 需整理为统一 method × input × representation 表 |
| D17/D18 modality combination | R1 Major 2；R2 Major 1 | NOT STARTED | 仅有 GARQ block contribution 和 Phase-1 smoke | 不可作为最终回复 |
| D17/D18 neighborhood retention/homogeneity | R2 Major 1 | NOT STARTED | 仅有早期 smoke `02_modality/neighborhood_anchor_mapping.csv` | 不可作为最终回复 |
| D17/D18 thinning/permutation | R1 Major 2；R2 Major 1 | NOT STARTED | Phase-1 smoke 存在，但不是 corrected full-data multi-seed | 不可作为最终回复 |
| Fixed-representation GARQ quantizer-only | R2 Major 2 | NOT STARTED | KMeans/SEACells fixed representation 已完成 | 不可完成 aggregation-only 归因 |
| Final realized-K controlled benchmark | R2 Major 2 | PARTIAL | 四方法 48 runs 均在 target K ±5%；GARQ quantizer-only 尚缺 | 可报告 K 控制，不能声称完全去除 representation confounding |
| D17 cross-method trajectory | R2 Major 3 | NOT STARTED | D17 assignments 已具备 | 不可作为最终回复 |
| D18 cross-method MOFA+ | R2 Major 4 | NOT STARTED | assignments 已具备；MOFA+ 0.7.2 环境可导入 | 不可作为最终回复 |
| D18 peak-gene | R2 Major 4 | NOT STARTED | — | 不可作为最终回复 |
| D18 TF-gene | R2 Major 4 | NOT STARTED | — | 不可作为最终回复 |
| D18 RNA-protein | R2 Major 4 | NOT STARTED | — | 不可作为最终回复 |
| D18 feature cross-fitting | R2 Major 4 | NOT STARTED | — | 不可作为最终回复 |
| D13 stage profile | R1 Major 3；R2 Major 5 | NOT STARTED | — | 不可作为最终回复 |
| D16 stage profile | R1 Major 3；R2 Major 5 | RUNNING | server `revision_results/phase2/logs/P2_E8_D16_full_profile_seed0.driver.log` | 完成复核前不可引用 |
| Full-data batch-size/order stability | R2 Major 5 | NOT STARTED | 仅有 Phase-1 smoke；旧 D5/D11 biological mapping 不可用 | 不可作为最终回复 |
| Exact MOFA+ settings | R1 Major 5；R2 Major 4 | NOT STARTED | 仅环境版本已冻结 | 不可作为最终回复 |
| D13–D16 unified batch integration | R1 Major 5 | NOT STARTED | D13/D16 identity 已确认 | 不可作为最终回复 |

## 本地交付结构

- 意见级报告：`phase2_reports/reports/` 及 `phase2_reports/` 根目录。
- 核心小表：`phase2_reports/01_size_resolution/`，后续按 `02_modality`、`03_controlled_benchmark`、`05_multibatch`、`06_kidney`、`07_trimodal`、`08_scalability` 增加。
- 总报告：`PHASE2_EXPERIMENT_REPORT.md`。
- 审稿证据矩阵：`REVIEWER_EVIDENCE_MATRIX_PHASE2.md`。
- 完整性：`run_manifest_phase2.json`、`MANIFEST_PHASE2.sha256`、`GARQ_phase2_handoff_bundle.zip`。

每个 reply-ready 报告均需包含：做了什么、准确结果、可安全声称、不可声称、candidate English paragraph、表格路径、失败/retry 记录、测试和 commit。
