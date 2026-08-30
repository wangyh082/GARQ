# R1 Major 1 — Metacell size、range 与 large metacells

状态：**READY FOR REPLY（主分辨率证据完成）**。本报告回答审稿人关于 metacell 数量、典型大小、范围和异常大 metacell 的问题。0.01/0.05 resolution sensitivity 仍属于后续补充，不应描述为已完成的全 compression frontier。

## 做了什么

- 数据：身份纠正后的 D5、D11、D17、D18，全量细胞。
- 方法：GARQ、KMeans、官方 MetaQ 1.0.6、官方 SEACells 0.3.3。
- 重复：每个 dataset-method 三个 seeds，共 48 个通过统一 evaluator 的运行。
- 主目标：K/n≈0.02。
- 分辨率控制：KMeans/SEACells 使用目标 K；GARQ 使用原预注册 K；MetaQ 使用 seed0 的 requested/realized K 映射进行标签不可见校准，并将新 requested K 冻结用于 seeds 1–2。
- realized-K 结果全部在各数据集目标 K 的 ±5% 内：D5 GARQ 237/239/236、MetaQ 244/237/244、其余 242；D11 MetaQ 196/196/185、其余 193；D17 四方法均 323；D18 GARQ 497/493/486、MetaQ 511/505/517、KMeans/SEACells 510。

## 三种子 size 结果

下表的 median、P95 和 CV 为三种子均值；max 给出三个 seeds 的最小–最大值。

| Dataset | Method | realized K | median | P95 | max range | mean CV |
|---|---|---:|---:|---:|---:|---:|
| D5 | GARQ | 237/239/236 | 48.8 | 75.8 | 158–1131 | 0.72 |
| D5 | KMeans | 242/242/242 | 48.0 | 75.3 | 108–134 | 0.28 |
| D5 | MetaQ | 244/237/244 | 35.8 | 63.1 | 2832–2897 | 3.83 |
| D5 | SEACells | 242/242/242 | 31.2 | 155.3 | 205–357 | 0.96 |
| D11 | GARQ | 193/193/193 | 55.0 | 69.8 | 75–92 | 0.33 |
| D11 | KMeans | 193/193/193 | 47.3 | 80.4 | 121–144 | 0.36 |
| D11 | MetaQ | 196/196/185 | 42.0 | 64.0 | 2147–3052 | 3.83 |
| D11 | SEACells | 193/193/193 | 37.3 | 114.1 | 173–194 | 0.67 |
| D17 | GARQ | 323/323/323 | 53.7 | 71.6 | 85–167 | 0.33 |
| D17 | KMeans | 323/323/323 | 47.7 | 77.6 | 114–142 | 0.32 |
| D17 | MetaQ | 323/323/323 | 54.0 | 68.0 | 73–75 | 0.28 |
| D17 | SEACells | 323/323/323 | 47.3 | 102.2 | 139–164 | 0.59 |
| D18 | GARQ | 497/493/486 | 48.3 | 93.8 | 147–988 | 0.73 |
| D18 | KMeans | 510/510/510 | 48.0 | 78.0 | 118–145 | 0.31 |
| D18 | MetaQ | 511/505/517 | 41.7 | 69.8 | 2318–3415 | 2.85 |
| D18 | SEACells | 510/510/510 | 41.0 | 114.5 | 189–199 | 0.66 |

## 发现与边界

1. 大多数方法的典型 metacell size 与目标 compression ratio 一致，median 约 31–55 cells，但 tail behavior 差异很大。
2. GARQ 并非始终生成窄 size distribution。D5 和 D18 存在 seed-dependent 大 metacell；D18 已观察到最大 988，D5 最大 1131。
3. MetaQ 在 D5、D11、D18 出现极长尾，最大 metacell 达 2897、3052、3415；这不是 K 不匹配造成，因为 realized K 已在目标 ±5% 内。
4. SEACells 的 P95 和 CV 通常高于 KMeans；KMeans 在四个数据集上的 size distribution 最稳定。
5. D17 是例外：MetaQ size 最均匀，GARQ 也相对稳定。
6. 因此可回答“范围和大 metacell 是否存在”，但不能声称 GARQ 或任一方法在所有数据集上始终控制得最好。

## 可直接用于回复的英文段落

> We now report the requested and realized metacell numbers together with the full metacell-size distributions across three seeds on the corrected D5, D11, D17, and D18 datasets. At the preregistered primary compression level (K/n approximately 0.02), the median metacell size was generally 31–55 cells, but the upper tails were method- and dataset-dependent. GARQ produced relatively compact distributions on D11 and D17, whereas seed-dependent large metacells occurred on D5 and D18 (maximum observed sizes 1,131 and 988, respectively). MetaQ showed substantially longer upper tails on D5, D11, and D18 despite realized K being within 5% of the target. We therefore added median, P95, maximum, CV, outlier, and requested/realized-K statistics and avoid claiming uniformly bounded metacell sizes.

## 不应声称

- 不应写“GARQ 在所有数据集上产生最均匀或最小的 metacells”。
- 不应隐藏 D5/D18 的 GARQ 大 metacell，或 MetaQ 的极长尾。
- 不应把 requested K 当作 realized K；两者必须同时报告。
- 不应声称 0.01/0.05 的完整 compression-quality frontier 已完成。

## 核查路径

- `revision_results/phase2/01_size_resolution/metacell_size_summary.csv`
- `revision_results/phase2/01_size_resolution/full_benchmark_long.csv`
- `revision_results/phase2/01_size_resolution/D*/<method>/full_seed*_K002*/summary.json`
- MetaQ calibration provenance：各 `full_seed*_K002_realizedmatched/calibration_provenance.json`
- 失败与兼容处理：`revision_results/phase2/reports/FAILURE_LOG_PHASE2.md`

统一测试：`28 passed, 13 warnings`。统计单位为 dataset-method-seed，不把细胞当作独立生物重复。
