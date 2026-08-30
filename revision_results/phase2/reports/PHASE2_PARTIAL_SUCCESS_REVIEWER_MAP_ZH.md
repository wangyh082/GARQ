# GARQ Phase 2 已成功实验与审稿意见对应报告

更新时间：2026-08-30。状态：阶段性成功报告；完整 Phase 2 仍为 `PARTIAL`。本报告只列已经完成并核验的实验，同时保留负结果和结论边界。

## 一、已经成功完成的实验

1. **数据身份与输入审计（Gate 0）**
   - 确认 D5 为 BMMC_batch1（12,103 cells，RNA+ADT），D11 为 10Xpbmc10k（9,631 cells，RNA+ATAC）。
   - D5、D11、D13、D16、D17、D18 均完成身份核验；配对模态行顺序和 count 来源通过检查。
   - 6,600 条 Phase 1 中错误标为 D5/D11 的历史文件记录已隔离，不能用于相应生物学结论。

2. **正确数据上的 GARQ 全数据主实验**
   - D5、D11、D17、D18 × seeds 0–2，共 12/12 个 300-epoch 运行成功。
   - 保存 requested/realized K、完整 assignment、metacell size、逐 cell-type 指标、训练阶段耗时、CPU/GPU 峰值和 anchor 动态。

3. **requested-K 公平基线比较**
   - GARQ、KMeans、官方 MetaQ 1.0.6、官方 SEACells 0.3.3。
   - D5、D11、D17、D18 × 3 seeds，共 48/48 个运行通过统一 evaluator。
   - KMeans 与 SEACells 使用同一个固定等权 PCA/LSI/CLR representation；方法兼容性修改和失败重试均已披露并保留。

4. **rare-state 全数据比较（不是下采样实验）**
   - 完成 D5 Treg/cDC2、D11 Plasma/gdT、D17 Mast Cells、D18 DC.Myeloid/Platelets/T.DoubleNegative 的三种子比较。
   - 主要负结果：GARQ 相对 SEACells 的 D18 DC.Myeloid 平均 F1 差为 -0.640；相对 KMeans 的 D5 Treg 为 -0.453；相对 MetaQ 的 D17 Mast Cells 为 -0.345。
   - 局部有利结果：D5 cDC2 相对 MetaQ 为 +0.316；D18 Platelets 相对 MetaQ/SEACells 仅 +0.014/+0.018。
   - D18 T.DoubleNegative 在四种方法、三个 seeds 中均未恢复（F1=0）。因此不能声称 GARQ 一致优于 baseline。

5. **metacell 数量与大小分布**
   - 48 个 dataset-method-seed 组合均有 requested/realized K 和 size summary。
   - GARQ D18 seed0 的 size median/P95/max 为 49/91/572，存在明显长尾；seed2 最大值为 988。

6. **dynamic anchor 全长度运行证据**
   - 正确数据的 full GARQ 运行中，local branch 首次在 quantized step 88 执行；anchor NaN/Inf 为 0。
   - 这纠正了早期 35-step smoke 中“未触发”的短运行局限。

7. **官方 EpiCarousel 对照**
   - 官方 EpiCarousel 0.0.2 在正确 D11 和 D17 的全数据 ATAC assignment 成功。
   - D11 requested/realized K=193/192；D17=323/322。兼容性 shim 和所有失败尝试均已记录。

8. **资源与复杂度实测**
   - 12 个 GARQ full runs 均记录 CPU RSS、GPU allocated/reserved 和 wall time。
   - D18 peak CPU RSS 约 82.45 GB，而 peak GPU allocation 约 1.71 GB；当前实现的主要内存压力来自 CPU/预处理，不能用 GPU 显存代替总内存描述。

9. **测试与可复现性交付**
   - `python -m pytest -q revision_exp/tests`：28 passed、13 warnings。
   - requested-K 基线结果已提交并推送至 `revision/major-review-experiments-phase2`，commit `a322a456e7231b0d0ab1061b4a8509ed25070ac6`，未创建 PR。

## 二、对应回复了哪些审稿意见

| 审稿意见 | 已完成的对应实验 | 当前可安全回复 | 仍不能声称 |
|---|---|---|---|
| R1 Major 1：metacell size range、median、large metacells | 12 个 GARQ full runs；48 个四方法 size summaries | 已报告 requested/realized K、median、P95、max 和长尾；D18 存在大 metacell | GARQ 的 size 始终均匀，或已完成全部 compression frontier |
| R1 Major 2：modality dominance | 12 个 GARQ full runs 的 modality block contribution trace | 已量化各 block 的贡献，正文应限制为观测到的贡献 | 多模态天然等权或对扰动普遍稳健 |
| R1 Major 3：dense conversion / large-scale memory | D5/D11/D17/D18 stage profile | CPU RSS、GPU allocated、GPU reserved 已分开报告；D18 CPU 内存较高 | 用 GPU-only memory 声称低总内存，或声称已证明大规模可扩展性 |
| R1 Major 4：under/overused anchors、更新频率、split terminology | full-length anchor trace；step 88 首次 local update | released method 是“固定 anchor 集合的 continuous usage-weighted repositioning” | create/split new anchors；matched-K 机制优势 |
| R1 Major 6：加入 scATAC-specific EpiCarousel | 官方 D11/D17 full EpiCarousel | 已加入 ATAC-derived 官方 comparator，并公开兼容处理 | 在尚未完成全部共同下游指标前声称 GARQ 优于 EpiCarousel |
| R2 Major 1：shared multimodal anchors 与 discordance | block contribution + 正确多模态数据 full runs | 可说明共享 anchor 的实测 block contribution | 已证明跨模态忠实性或对 modality noise 稳健 |
| R2 Major 2：representation / aggregation / K 混杂 | fixed-representation KMeans/SEACells；MetaQ；48-run requested-K comparison | 已区分 fixed-representation control 与 native pipeline，并报告 K | 所有差异都来自 aggregation；requested-K 等同严格 realized-K |
| R2 Major 5：attention、batch-local KNN、scalability、实现不一致 | 代码审计、full trace、stage memory profile | 可准确解释 sequence length 1、batch-local graph 和 CPU/GPU memory | 论文复杂度表述已被所有大数据 full profile 完全验证 |
| purity 0.5/0.7 不一致 | common evaluator | majority 定义为 purity >0.5；high-purity 定义为 purity >=0.7 | 将两个阈值混用 |
| Mast Cell retained/lost 缺定义 | D17 三种子、四方法 precision/recall/F1/purity | 用连续指标替代 retained/lost；GARQ/KMeans F1=0，MetaQ/SEACells有有限恢复 | GARQ 保留 Mast Cells或在此状态上占优 |

## 三、阶段性结论

- **Rare-state preservation：广义 superiority claim 不受支持。** requested-K 的四方法证据是 cell-type dependent，并且多个关键状态明显由 baseline 更好恢复。
- **Multimodal fidelity：仍为 INCONCLUSIVE。** 已有 block trace，但缺完整 modality combination/noise grid。
- **Scalability：PARTIALLY SUPPORTED。** 四个中等数据集运行成功，但 D18 CPU RSS 高，D13/D16 scaling series 未完成。
- **GARQ-specific downstream advantage：INCONCLUSIVE。** D17 trajectory 和 D18 held-out/cross-fit 仍未完成。

## 四、正在继续运行和后续顺序

1. 正在运行 MetaQ 标签不可见 realized-K calibration：D5/D11/D18 × seeds 0–2；seed0 映射冻结后用于其他 seeds。
2. 校准完成后更新 realized-K 表和 paired rare-state 对照。
3. 随后依次推进 full-data rare-state subsampling、E4 matched-K、D17 trajectory、D18 MOFA+/cross-fit、D13/D16 profile；每项仍按资源和失败证据要求执行。

核心数据表：`full_benchmark_long.csv`、`metacell_size_summary.csv`、`per_type_metrics_long.csv`、`matchedK_focal_rare_summary.csv`、`matchedK_focal_rare_paired_contrasts.csv`。
