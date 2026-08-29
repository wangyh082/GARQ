# Source traceability

## 已取得

- 用户指定代码仓库：`https://github.com/wangyh082/GARQ.git`
- base commit：`5da45adcd62f1be8ee318d8742c80c59cb242ca2`（2026-07-08）
- README 数据 DOI：`10.6084/m9.figshare.32751672`
- 权威执行计划：本地附件，SHA256 `64E186F2E811631A6B6CFD5ADEE567A9365092744ACEFD4A564E54B22920AFC1`
- 用户澄清的数据根：`/home/zhangpeiru/data` 下 RNA+ADT、RNA+ATAC、RNA_ATAC_ADT。

## 未取得

`GARQ.pdf`、`Supplementary.pdf`、`审稿意见.docx` 未出现在仓库或已检查的服务器 home tree。Figshare DOI/API 在 2026-08-29 检索时返回 403，不能从其元数据恢复 D1–D18 表。计划中的 reviewer 摘要可用于规划，但不能伪装为原始评论全文。

## 数据映射状态

- D5、D11、D17：路径、shape、label、paired row order 已核验。
- D18：三模态 shape 和 label vector 一致，但 obs_names 不一致，状态为 `needs_cell_id_reconciliation`。
- D1–D4、D6–D10、D12–D16：`NOT_RECOVERED`，不根据目录名猜测。
- 权威 YAML：`revision_exp/data_registry/datasets.yaml`。

## 代码证据

根目录源码未改。SHA256 和字节数在 `revision_results/00_audit/source_sha256.json`。所有新增 workflow 必须带 `implementation_tag`；涉及算法语义的版本不得标为 legacy。
