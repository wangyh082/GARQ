# P2-E8 D16 full scalability/profile — failure report

Status: **FAIL / AUTHOR DIRECTION REQUIRED FOR RETRY**  
Reviewer mapping: **R1 Major 3** (dense conversion and large-scale memory) and **R2 Major 5** (batch-local graph, scalability, implementation consistency).

## Experiment

- Config: `revision_exp/configs/methods_phase2/p2_D16_full_profile_seed0.yaml`
- Dataset: authoritative D16 GSE140203, 32,231 cells, paired RNA+ATAC.
- Source shapes: RNA 32,231×21,478; ATAC 32,231×340,341.
- Preprocessed shapes reached before failure: RNA 32,231×2,202; ATAC 32,231×30,000.
- Requested K: 645 (K/n≈0.02); seed 0; 300 epochs; configured batch size 256; instrumented legacy.
- Server driver log: `/data/zhangpeiru/GARQ_revision/revision_results/phase2/logs/P2_E8_D16_full_profile_seed0.driver.log`
- Exit status file: `/data/zhangpeiru/GARQ_revision/revision_results/phase2/logs/P2_E8_D16_full_profile_seed0.status` (`1`).

## Exact failure

The run completed loading and high-variable-feature preprocessing, then failed during legacy FAISS KMeans anchor initialization:

```text
RuntimeError: ... 'nx >= k' failed: Number of training points (512)
should be at least as large as number of clusters (645)
```

The released initializer trains KMeans from a 512-cell initialization batch, which is smaller than requested K=645. This is not an OOM and not a corrupted-data failure.

## Resource evidence retained from the failed run

- Wall time to failure: 14 min 48.09 s.
- Peak CPU RSS: 212,123,112 KiB (approximately 202.3 GiB).
- GPU memory at observed preprocessing stage: approximately 384 MiB.
- Swap: 0.
- System still had substantial available RAM; the run exited from the explicit FAISS constraint.

This failed run is already informative for the review: feature preprocessing alone is CPU-memory-heavy, and the legacy initializer cannot represent K/n=0.02 on D16 without changing initialization behavior or batch size.

## Root-cause classification

- Data identity/input: PASS.
- Resource preflight: PASS.
- Engineering cause: legacy anchor initialization uses fewer points than requested clusters.
- Scientific impact: a retry is not semantics-neutral unless initialization sampling or batch size changes. Because released GARQ uses a batch-local graph, increasing training batch size also changes inter-cell dependence.

## Adjustment options

### Option A — diagnostic large-sample anchor initialization (recommended)

Collect at least 645 label-free hidden representations for FAISS initialization while retaining the configured training batch size. This corresponds to the preregistered `diagnostic_large_sample_or_full_initialization` variant. It answers whether D16 is computationally runnable, but must not be labelled unmodified legacy GARQ.

Acceptance criteria: initialization sample ≥645; no labels used; 32,231 assignments; requested/realized K reported; full stage CPU/GPU profile; implementation tag explicitly diagnostic.

### Option B — batch_size 1024 retry

Use the preregistered E8 batch-size grid value 1024 so a single initialization batch exceeds K. This also changes the batch-local training graph and therefore is a batch-size sensitivity experiment, not a numerical compatibility retry.

Acceptance criteria: same data/seed/K/epochs, explicit `batch_size_1024` tag, full resource and quality comparison, no claim that it reproduces default-batch legacy behavior.

### Option C — preserve legacy failure only

Do not alter the method. Report D16 K/n=0.02 as blocked by the released initialization constraint and proceed to D13/scaling diagnostics or sparse-safe candidates.

## Safe reply wording now

> On the full D16 dataset, preprocessing reached 32,231 cells with 2,202 RNA and 30,000 ATAC features and consumed approximately 202 GiB peak CPU RSS. The released initialization then stopped because its 512-cell initialization sample was smaller than the requested 645 anchors. We retain this failed run as scalability evidence and distinguish any larger-sample initialization retry as a diagnostic variant rather than unmodified legacy behavior.

## What must not be claimed

- Do not report the D16 full legacy run as successful.
- Do not call this an OOM.
- Do not silently increase batch size or initialization sample and label the result `instrumented_legacy`.
- Do not delete the failed log or partial provenance files.
