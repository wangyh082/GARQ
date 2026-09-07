# Rebuttal Evidence Draft — Phase 2

Status: VERIFIED EVIDENCE DRAFT; not the final rebuttal.

## Rare-state and matched-resolution concern

**What we did.** We reran corrected D5, D11, D17 and D18 at requested K/n=0.02 for three seeds with GARQ, official SEACells 0.3.3, official MetaQ 1.0.6 and KMeans. SEACells and KMeans share a fixed equal-weight PCA/LSI/CLR representation. All 48 assignments used the same evaluator and explicit majority (>0.5) and high-purity (>=0.7) definitions.

**What we found.** Results were cell-type dependent and often unfavorable to GARQ. GARQ mean F1 was lower than SEACells for D18 DC.Myeloid by 0.640, lower than KMeans for D5 Treg by 0.453, and lower than MetaQ for D17 Mast Cells by 0.345. GARQ exceeded MetaQ for D5 cDC2 by 0.316, while D18 Platelet differences versus MetaQ/SEACells were only +0.014/+0.018. All methods had F1=0 for D18 T.DoubleNegative.

**What we can safely say.** Full-data requested-K comparisons were added and show heterogeneous preservation rather than a consistent winner.

**What we cannot say.** GARQ consistently or significantly outperforms competing metacell methods, or that requested-K matching removes realized-K confounding.

**Candidate English paragraph.** “We added three-seed, full-data comparisons on the corrected D5, D11, D17, and D18 datasets using GARQ, SEACells, MetaQ, and a fixed-representation KMeans control at the same requested compression level. Rare-state recovery was heterogeneous across datasets and cell types, and several focal states were recovered better by a baseline. We therefore narrowed the manuscript claim and report all favorable, unfavorable, and null outcomes.”

Tables: `matchedK_focal_rare_summary.csv`, `matchedK_focal_rare_paired_contrasts.csv`, `full_benchmark_long.csv`.

## R1 Major 3 / R2 Major 5 — implementation-scale and batch/order concern

**What we did.** We added a five-point, 300-epoch D13 scaling series (10k,
25k, 50k, 100k and full 161,764 cells; seed 0), a corrected full D16 profile,
four training batch sizes × three seeds on corrected D5/D11, and five frozen
inference batch sizes with ten pre-specified order permutations on each of D5
and D11. All planned rows completed with the common evaluator; original D13
and D16 compatibility failures and their compatibility-equivalent retries are
retained.

**What we found.** D13 full completed at K=3,234/3,235 in about 119 minutes
with peak CPU RSS 202.9 GiB and GPU allocated/reserved 5.25/7.13 GiB, but the
25k/50k points had 28/238 empty anchors and size Gini 0.261/0.670. D16 full
completed at K=645/645 with peak CPU RSS 207.84 GiB during preprocessing and
GPU allocated/reserved 1.58/2.29 GB during inference. Training membership was
not batch-size invariant (mean ARI versus batch 256: D5 0.1302 at batch 2048;
D11 0.0412), and order permutations at inference batch 1,024 gave mean ARI
0.5746 (D5) and 0.6942 (D11).

**What we can safely say.** “The added experiments establish implementation
feasibility at the tested sizes and expose CPU preprocessing and the released
batch-local graph as important limitations. We therefore report qualified
scalability evidence rather than uniform runtime, size or batch/order
invariance.”

**What we cannot say.** We cannot claim linear scaling, uniformly stable
metacell sizes, low total memory from GPU values alone, a global-graph result,
or a completed unified D13–D16 batch-integration/MOFA+ benchmark. D13/D16
scaling uses one seed each.

Dedicated report: `R1_MAJOR3_R2_MAJOR5_SCALABILITY_REPORT.md`; exact CSVs and
server log paths are indexed in `RESULT_FILE_INDEX_PHASE2.md`.

## R2 Minor Comment 4 — Figure 4b Mast Cells

**What we did.** We audited the canonical D17 `celltype` labels (74 Mast Cells
of 16,143 cells) and quantified five frozen assignment files using the same
nominal compression input. We pre-specified associated-group criteria,
majority/high-purity thresholds, a seven-gene Mast marker panel, and 10,000
fixed-label permutations (seed 20260907). The author explicitly approved
retaining non-exact realized K for MetaCell V2 and SuperCell.

**What we found.** Realized K was GARQ/MetaQ/SEACells/MetaCell V2/SuperCell =
403/403/403/429/404. GARQ associated recall was 0.5676 and maximum purity
0.3016; top-three capture was 0.4865 (permutation P=0.0001). Strict majority
and high-purity recovery were zero for every method. MetaQ associated recall
was 0.5811; SEACells 0.2297; MetaCell V2 0.1622; SuperCell 0.2297.

**What we can safely say.** “Mast-cell-associated metacells remained
identifiable in the GARQ space; localized enrichment and strict majority
recovery varied across methods.”

**What we cannot say.** This is not an exact-K=403 comparison for MetaCell V2
or SuperCell; it does not support exclusive GARQ detection, majority Mast-cell
recovery, superiority, causal regulation, or independent ground truth.

**Candidate English paragraph.** “For Figure 4b, we re-evaluated the frozen
assignments using the exact D17 Mast-cell label (74/16,143 cells), a
pre-specified enrichment definition, and 10,000 fixed-label permutations.
GARQ showed localized enrichment (associated recall 0.568; maximum purity
0.302), but strict majority and high-purity recovery were zero. The other
methods showed method-dependent enrichment under the same nominal compression
input, with realized K values retained explicitly (403, 403, 403, 429 and 404).
We therefore do not claim exclusive GARQ recovery or superiority.”

Tables/figures: `fig4b/reviewer_mast_quantification/`; detailed delivery report:
`R2_MINOR4_FIG4B_MAST_REPORT.md`.
