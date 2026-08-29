# Blocked or deferred

| Item | Status | 原因 | 已完成 | 继续条件/命令 |
|---|---|---|---|---|
| 论文/补充/审稿原文抽取 | BLOCKED | 三份权威文件未在附件、仓库或服务器发现；Figshare 403 | 代码证据和计划摘要已索引 | 作者提供文件后重建 traceability/matrix |
| D1–D4/D6–D10/D12–D16 映射 | BLOCKED | 缺 Supplementary 数据表，禁止按目录猜 | D5/D11/D17/D18 已核验 | 取得 Supplementary 后更新 registry |
| published_config | BLOCKED | 仓库无逐数据集原始参数/log | controlled K smoke 已跑 | 作者提供 configs/logs |
| D18 实验 | DEFERRED | obs_names 跨三模态不一致 | shape/label vector 已核验 | 先完成 cell-id reconciliation 审计 |
| 全 P0 baselines | IN PROGRESS | 官方实现、版本与独立环境尚待建立 | common evaluator 与 GARQ smoke 已完成 | 依 E3 adapter 逐个运行 |

资源降级规则当前按计划执行：先完成 2,000-cell smoke，再跑 D5/D11/D17/D18 全量核心任务；任何降级均保留配置和状态，不把 smoke 当主结果。
