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
