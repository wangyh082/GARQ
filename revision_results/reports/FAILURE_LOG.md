# Failure log

## F001 — CLI 缺 PyYAML

首次运行统一 CLI 时 `import yaml` 失败。环境：MetqQ2/Python 3.11.6。处理：安装 `PyYAML==6.0.2`，仅补运行依赖，不改算法语义。

## F002 — pytest collection import failure

直接调用 `pytest` 时根目录不在预期 import path，collection 失败。原始 JUnit：`revision_results/00_audit/pytest_E0_collection_fail.xml`。处理：使用 `python -m pytest`；随后进入行为测试。

## F003 — anchor test 假设错误

初版测试假设每个 scheduled anchor 每步都有数值位移；实际 beta 在 float32 下可下溢/小到没有有效位移。原始 JUnit：`pytest_E0_behavioral_fail.xml`、`pytest_E0_pre_correction_fail.xml`。处理：测试分别记录 scheduled 与 effective update，不改发布实现。最终 8 tests passed。

## F004 — deterministic CUDA 警告

D5 smoke 未设置 `CUBLAS_WORKSPACE_CONFIG`；D11 设置 `:4096:8` 后，PyTorch 仍报告 memory-efficient attention/cumsum 某些 CUDA 路径没有 deterministic implementation。运行未删除，状态 PASS 但复现强度受限。后续 manifest 显式保存相关环境变量。

## F005 — D11 输入尺度警告

D11 RNA 在 legacy `sc.pp.log1p` 前被 Scanpy 判定“seems to be already log-transformed”。运行继续并保留完整日志。该 smoke 不能视为已确认 raw-count published reproduction；需检查 layers/raw 或恢复作者原始输入说明。

## F006 — remote material retrieval

服务器直连 GitHub HTTPS 两次超时，采用本地浅 clone 后 SCP；传输 SHA/objects 已验证。Figshare API/DOI 返回 HTTP 403；未据此猜测数据集映射。
