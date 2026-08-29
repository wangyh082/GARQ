# GARQ 代码—方法一致性审计（E0）

状态：`PARTIAL`。发布代码与运行时行为已经审计；`GARQ.pdf`、`Supplementary.pdf` 和审稿意见原文尚未取得，因此“论文陈述”列目前仅使用实验计划中列出的待核查主张，不能替代逐页论文核对。

## 版本与边界

- Base commit: `5da45adcd62f1be8ee318d8742c80c59cb242ca2`
- 分支：`revision/major-review-experiments`
- E0 instrumentation 不修改根目录 GARQ 数值路径，只增加 hook、追踪、独立评估与报告。
- 源码 SHA256 见 `revision_results/00_audit/source_sha256.json`。

## 逐项审计

| 论文/计划待核查陈述 | 发布代码行为 | 证据 | 建议处理方式 |
|---|---|---|---|
| 预处理可扩展 | 稀疏矩阵先整体 `toarray()`，随后保留 `raw`、normalized `adata`、`adata_`，并物化 float tensor | `data_utils.py:38-73, 8-21`；D11 2,000-cell preprocessing peak RSS 5,466,956,928 B | 如实报告 CPU peak；sparse-safe 版本仅列为 diagnostic variant |
| Transformer 建模跨细胞关系 | encoder/decoder 对每个细胞 `unsqueeze(1)`，实际 sequence length=1 | `model.py:125-140,143-180,182-225`；`tensor_shapes.json` | 不应声称 Transformer self-attention 在细胞间传播信息 |
| graph-aware smoothing 稳定表达全局拓扑 | 图只在当前 mini-batch 内构造，显式形成 dense `B×B`；同一目标细胞换 context 可改变 assignment | `model.py:32-67`；`batch_local_graph_dependency.json` trial 4: assignment 1→0 | 完成 batch size/order 稳定性；global graph 只能标 diagnostic variant |
| alpha 是可学习权重 | `encode_relation()` 每次新建 `nn.Parameter(0.2)`；optimizer 已先构造；每次 forward object id 不同 | `model.py:59-61`；`parameter_registration_before_after.csv` | 原实现中 alpha 不可由 optimizer 学习；候选修复不得冒充 legacy |
| GPU FAISS 初始化 | `faiss.Kmeans(..., gpu=True)` 在 warm-up 前调用，输入为前两个 shuffled training batches | `model.py:19-29`; `engine.py:16-42`; `GARQ.py:42-73` | 当前 faiss-cpu 1.11.0 仍成功但 index 为 CPU `IndexFlatIP`；应披露实际 backend |
| dynamic anchor 使用 under/overused thresholds 并 split | 无显式离散阈值；每个 training forward 对全部 anchor 安排连续更新；第二分支条件为 usage sum；不会创建新 anchor | `model.py:82-114`; `anchor_dynamics_step.csv` | 使用“continuous usage-weighted repositioning”，避免 split/create 表述 |
| graph smoothing 做尺度控制 | 邻接只 `(A+A.T)/2`，未 row normalize；`A @ raw_sim` 随 degree/k 改变尺度 | `model.py:32-61` | 报告 k 敏感性；归一化只能作为诊断版本 |
| 输出为 raw count metacells | `compute_metacell` 平均的是 normalize_total+log1p 后、HVG/scale 前的 `adata_` | `data_utils.py:43-73,124-161`; `metacell_output_scale.json` | 明确输出是 log-normalized profile，而非 raw counts |
| 环境说明一致且可移植 | README 的 sklearn 0.22.1 与 environment 的 1.1.3 不同；`requirement.ymal` 含绝对 prefix | `README.md`; `requirement.ymal` | 发布 portable lockfile，并列出本次实际环境 |
| 仓库可生成全部论文结果 | 仓库仅含 tutorial/root scripts，无完整 figure/baseline configs/raw logs | repository inventory | published config 标 `NOT_RECOVERED`，禁止反推 |

## 最小运行证据

- Tests: `python -m pytest -q` → 8 passed；JUnit: `pytest_E0_after_runner.xml`。
- D5 controlled smoke: 2,000 cells, requested K=40, realized K=34, 6 empty anchors, wall 15.95 s。
- D11 controlled smoke: 2,000 cells, requested K=40, realized K=40, wall 17.04 s；preprocessing peak RSS 5.47 GB。
- D11 loader 发出“RNA seems already log-transformed”警告，说明当前文件可能被 legacy pipeline 再次 normalize/log；在确认原始 counts layer 前不能把该输出当作无歧义 published reproduction。

## Dynamic anchor 数学等价伪代码

```text
for each quantized training forward:
    p_j = mean_i 1[argmax(sim_i) == j]
    usage_j <- 0.9 * usage_j + 0.1 * p_j
    beta_s_j = exp(-100*K*usage_j - 1e-3)
    anchor_j <- (1-beta_s_j)*anchor_j + beta_s_j*sampled_cell_j
    if sum_j(usage_j) + 1e-4 >= 1:
        beta_l_j = exp(-mean(usage)/(10*usage_j) - 1e-3)
        anchor_j <- (1-beta_l_j)*anchor_j + beta_l_j*local_sample_j
```

注意：当 `usage_j=0` 时第二个表达式包含除零风险（通常产生 exponent `-inf` 而 beta 为 0）；没有显式 NaN guard。确定性 trace 中 long update 每步对 6 个 anchor 都“被安排”，但从 step 5 到 87 float32 的有效位移为 0；local branch 于 step 88 首次满足条件。它是 repositioning，不是新建/split anchor。

## 候选 Methods 修订文本（未采用）

> In the released implementation, each cell is encoded independently by a TransformerEncoderLayer with sequence length one. Graph-aware interactions are introduced subsequently through a dense cosine k-nearest-neighbor graph constructed within each mini-batch. The symmetric adjacency is not row-normalized. The released anchor update continuously repositions existing anchors using an exponential function of exponentially smoothed assignment usage; it does not create new anchors or apply explicit underuse/overuse thresholds.

依赖证据：A02/A03/A06/A07。`[AUTHOR DECISION REQUIRED]` 是否修正文稿以匹配 released implementation，或采用经完整实验验证的候选修复。

## 尚缺证据

1. 缺论文与补充材料原文件，无法核查 Eq. (15)、Eq. (19)–(21) 的精确原文与维度。
2. 缺 published per-dataset configs/logs，D5/D11 的 published K 与 epochs 暂为 `NOT_RECOVERED`。
3. smoke 只用于数值/资源路径核验，不支持性能优越性主张。
