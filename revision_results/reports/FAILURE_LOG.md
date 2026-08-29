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

## F007 — modality block diagnostic NumPy API mismatch

首次 block-diagnostic 汇总调用 `np.linalg.vector_norm`，但环境 NumPy 1.26.4 不提供该 API。失败 manifest 保留为带 `_FAILED_numpy_vector_norm` 后缀的配置证据。处理：改用 `np.linalg.norm` 后以新 config ID 重跑；属于诊断统计兼容性修复，不改变 GARQ 数值路径。

## F008 — interrupted run was incorrectly marked PASS

一次人工中断暴露 CLI 原先只捕获 `Exception`，导致 `KeyboardInterrupt` 在 `finally` 中被写成 `PASS` 并生成错误 done sentinel。原 manifest 已复制为 `_INTERRUPTED_FALSE_PASS` 证据，错误 sentinel 已精确移除。CLI 改为捕获 `BaseException` 后重跑成功；这是运行状态审计修复，不改变算法语义。

## F009 — GitHub push authentication unavailable

服务器 HTTPS remote 没有 GitHub credential；本机 Git Credential Manager 也没有可复用的 HTTPS credential，GitHub SSH key 未授权。提交 `22b7a7cd242b37b43334b85c119f02a4e61ffe9e` 已安全保存在服务器实验分支，但首次增量 push 被认证阻塞。临时 clone/bundle 已回收或移除；未创建 PR，未把凭据写入文件或日志。

## F010 — direct pytest invocation collection failure recurred

新增 E8 instrumentation 后直接执行 `pytest -q revision_exp/tests`，9 个模块在 collection 阶段因仓库根目录未进入 import path 而失败，与 F002 同因。立即使用 `python -m pytest -q revision_exp/tests`，结果为 `14 passed, 13 warnings`。本次失败未通过删除测试规避。
