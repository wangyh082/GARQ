# Anchor operational definition（released implementation）

实现标签：`legacy_main` / `instrumented_legacy`。本文只描述 commit `5da45ad` 的真实行为。

- 初始化发生于 optimizer 构造后、warm-up 前。
- `init_gart_anchors` 只读取 shuffled train loader 的前两个 batch；`drop_last=True`，因此名义样本数为 `2 × batch_size`。
- 初始化 encoder 未训练。FAISS 调用写作 `gpu=True`，但本环境为 `faiss-cpu==1.11.0`，实际 index 是 `IndexFlatIP`。
- KMeans 后代码重新按 assignment 求中心；空簇会对空 slice 求 mean，存在 NaN 风险，且没有 guard。
- usage 是 hard argmax assignment 比例的 EMA：`u_t=0.9u_(t-1)+0.1p_t`。
- 每个 quantized training batch 都运行动态更新；warm-up decode-only 阶段不运行 quantizer update。
- “long”分支对所有 anchors 计算 `exp(-100*K*u-0.001)`，但高 usage 时可数值下溢为无有效位移。
- 第二分支条件不是 per-anchor threshold，而是 `sum(u)+1e-4>=1`；更新仍针对已有 anchors。
- 不存在增加 anchor 数量、复制 anchor 或真正 split/create 的代码路径。

因此准确术语为：**continuous usage-weighted repositioning of a fixed anchor set**。

## Runtime trace

确定性 6-anchor/100-step trace：

- step 1：6/6 anchors 有可测位移；
- step 5–87：scheduled=6，但 float32 effective displacement=0；
- step 88：第二分支首次触发；5/6 anchors 有可测位移；
- 完整记录：`revision_results/00_audit/anchor_dynamics_step.csv`。

## 归因限制

该 trace 证明代码机制和数值触发，不证明机制改善 rare-state preservation。该因果归因仍需 E4 matched-realized-K、5 seeds 的 `no_dynamic_update`、interval、初始化时点/样本量对照。

## D5/D11/D17 actual-training smoke trace

配置均为 2,000 cells、seed 0、requested K=40、6 epochs（1 warm-up + 5 quantized epochs），每个 quantized epoch 7 个 drop-last batches，共 35 个被记录 step。`instrumented_legacy` 的 interval=1 trace 与改动前相同配置的 assignments 完全一致（D5 ARI=1；D11 ARI=1），说明启用 trace 本身没有改变默认数值结果。

| Dataset | Variant | realized K | size Gini | ARI vs legacy | reposition steps | final usage perplexity |
|---|---|---:|---:|---:|---:|---:|
| D5 | legacy continuous | 34 | 0.683 | 1.000 | 35 | 15.73 |
| D5 | no manual reposition | 30 | 0.618 | 0.311 | 0 | 15.15 |
| D5 | interval 5 | 20 | 0.711 | 0.513 | 7 | 8.74 |
| D5 | interval 10 | 17 | 0.720 | 0.392 | 3 | 8.06 |
| D11 | legacy continuous | 40 | 0.704 | 1.000 | 35 | 14.76 |
| D11 | no manual reposition | 36 | 0.631 | 0.170 | 0 | 16.94 |
| D11 | interval 5 | 28 | 0.671 | 0.178 | 7 | 10.23 |
| D11 | interval 10 | 31 | 0.814 | 0.163 | 3 | 7.78 |
| D17 | legacy continuous | 40 | 0.672 | 1.000 | 35 | 16.30 |
| D17 | no manual reposition | 36 | 0.676 | 0.252 | 0 | 15.54 |
| D17 | interval 5 | 39 | 0.715 | 0.265 | 7 | 14.22 |
| D17 | interval 10 | 33 | 0.728 | 0.312 | 3 | 12.75 |

所有 12 个 runs 的 `anchor_nan_count` 与 `anchor_inf_count` 均为 0。35 steps 内第二个 local branch 执行次数均为 0；因为每 batch 的 hard-assignment proportions 求和为 1，usage sum 从 0 开始满足 `sum(u_t)=1-0.9^t`，条件 `sum(u)+1e-4>=1` 最早约在 step 88 才成立。因而这些 6-epoch smoke 中所谓动态行为仅包含第一个 continuous usage-weighted reposition expression。

`no manual reposition` 保留 usage EMA 记录，也保留 optimizer 对 `anchors.weight` 的正常梯度更新，只关闭发布实现中通过 `.data` 执行的两段手工重定位。interval 5/10 同样每 batch 更新 usage EMA，但只在预注册间隔执行手工重定位。因此这些是隔离的 `diagnostic_variant`，不得冒充原始 GARQ。

结果说明手工重定位频率会显著改变 partition 与 realized K，但当前并未匹配 realized K，也只有一个 seed；不能据此声称 legacy schedule 改善 biological quality 或 rare-state preservation。D17 Mast Cells 在四个 schedule 中均为 8 cells 且 recall/F1=0。D17 Stressed Tumor (p53+) 的 F1 在 0–0.233 间非单调变化，Tumor Epithelial F1 在 0.577–0.766 间变化，同样不能用标签择优选择 schedule。正式归因仍需 D5/D11/D17、5 seeds、matched-realized-K，以及初始化时点/样本量对照。

统一原始表：`revision_results/04_anchor/anchor_dynamics_step.csv`、`revision_results/04_anchor/anchor_schedule_ablation.csv`。
