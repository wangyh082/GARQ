# D18 peak–gene and feature cross-fitting: BLOCKED

## Status and reviewer mapping

- Status: **BLOCKED** (scientific-input blocker; no experiment was silently substituted).
- Phase-2 item: P2-E7, D18 held-out/cross-fit association analysis.
- Reviewer use: the trimodal-specificity evidence requested for the D18 reviewer response. This item is not reply-ready.
- Inspection date: 2026-09-03 (Asia/Shanghai).

## Frozen input inspected

- RNA: `/home/zhangpeiru/data/RNA_ATAC_ADT/GSE158013/GSE158013_rna.h5ad`, shape 25,517 × 17,882.
- ATAC: `/home/zhangpeiru/data/RNA_ATAC_ADT/GSE158013/GSE158013_atac.h5ad`, shape 25,517 × 128,853.
- Phase-2 config: `revision_exp/configs/methods_phase2/p2_D18_full_seed0.yaml`.
- RNA `var_names` are gene symbols and `var` contains only `n_cells`; no chromosome, start, end, Ensembl ID, or genome-build field is present.
- ATAC `var_names` encode coordinates such as `chr1-9965-10465`, but `var` and `uns` contain no genome-build or annotation provenance.
- No GTF or gene-annotation table was found within the inspected project/data locations (`/home/zhangpeiru/data` and `/data/zhangpeiru`, maximum depth five).

## Why execution is blocked

The preregistered odd/even-chromosome cross-fit requires assigning both RNA genes and ATAC peaks to chromosomes, excluding the held-out fold during metacell construction, and evaluating associations only on excluded features. Peak coordinates alone are insufficient: mapping RNA symbols to chromosomes and peaks to genes requires a declared reference genome and a frozen gene annotation. Guessing hg19 versus hg38, or downloading an undeclared annotation, could change the eligible feature/pair universe and therefore changes scientific semantics.

This is not an engineering compatibility failure. It is missing authoritative scientific metadata. A full-feature association, nearest-symbol heuristic, or post-hoc chromosome mapping would not satisfy the planned cross-fit and must not be reported as such.

## Preserved evidence and commands

Read-only inspections were run in the `MetqQ2` environment:

```text
anndata.read_h5ad(<RNA>, backed="r"): shape=(25517, 17882), var columns=[n_cells], uns={}
anndata.read_h5ad(<ATAC>, backed="r"): shape=(25517, 128853), var columns=[], uns={}
RNA examples: AL627309.5, LINC01409, LINC01128
ATAC examples: chr1-9965-10465, chr1-181043-181543, chr1-191296-191796
find /home/zhangpeiru/data /data/zhangpeiru -maxdepth 5 ...: no candidate GTF/annotation returned
```

No assignment, metric, or partial scientific result was generated, so there is no failed numerical output to reinterpret.

## Required author input and retry acceptance criteria

Provide or approve all of the following:

1. the D18 reference genome build (for example, GRCh37/hg19 or GRCh38/hg38);
2. the authoritative GTF/GFF release or an exact immutable annotation file/checksum;
3. the peak-to-gene rule (for example, TSS-window distance and tie handling), unless already fixed elsewhere in the manuscript protocol.

After those inputs are frozen, an acceptable retry must record annotation provenance/checksum, per-fold RNA genes/ATAC peaks/pairs/cells, exclude held-out features before constructing every method's metacells, apply the identical rule to GARQ/SEACells/MetaQ/KMeans, and evaluate associations only on the held-out fold. Odd/even folds must be swapped and merged without using full-feature assignments as a substitute.

## Safe response wording

Do not claim that the D18 peak–gene cross-fit has been completed. Safe interim wording is: “The cross-fitted peak–gene analysis is pending confirmation of the dataset's genome build and authoritative gene annotation; we have not substituted a post-hoc or full-feature analysis.”

