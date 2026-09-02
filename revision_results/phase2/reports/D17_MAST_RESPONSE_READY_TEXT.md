# D17 Mast-cell response-ready text

## Response Letter

We thank the reviewer for raising this point. Under the strict majority criterion, GARQ did not achieve complete Mast-cell recovery. Nevertheless, the existing assignments showed partial localized preservation (mean associated recall 61.7%; maximum purity 0.153–0.270; maximum enrichment 33.3–59.0-fold). We therefore removed the binary superiority statement and now report strict majority recovery, enrichment-based associated recall, top-k capture, metacell sizes, and fixed-assignment permutation tests across three seeds. Comparative superiority was not supported under our preregistered same-seed criterion. [AUTHOR INPUT REQUIRED: MetaCell V2 assignment not available] [AUTHOR INPUT REQUIRED: SuperCell assignment not available]

## Changes in the revised manuscript

We replaced the qualitative Mast-cell retained/lost panel with a quantitative four-panel display of strict recall, maximum purity, the number of associated metacells, and associated-metacell size. We added complete seed-level and permutation results to the Supplementary Tables and explicitly separated strict majority recovery from partial enrichment.

## Revised Results paragraph

Mast Cells comprised 74 of 16143 cells (0.46%). Under the strict majority criterion, GARQ did not achieve complete Mast-cell recovery. Nevertheless, the existing assignments showed partial localized preservation (mean associated recall 61.7%; maximum purity 0.153–0.270; maximum enrichment 33.3–59.0-fold). Across GARQ seeds, mean strict recall was 0.000, mean associated recall was 0.617, maximum purity ranged from 0.153 to 0.270, and maximum enrichment ranged from 33.3- to 59.0-fold. The normalized-HHI permutation P values were 0.0001, 0.0001, 0.0001. These measurements do not support a claim that GARQ uniquely retained Mast Cells.

## Revised Figure 4b legend

Quantitative evaluation of Mast-cell organization in existing D17 assignments. Points denote seeds (0–2) and bars denote mean ± SD. Panels show strict majority-level recall, maximum Mast-cell purity (dashed lines at 0.5 and 0.7), the number of enrichment-defined associated metacells (open symbols: majority-dominated count), and sizes of associated metacells. No zero size is plotted when no associated metacell exists.

## Supplementary Methods paragraph

For metacell $M_k$, Mast-cell purity was defined as $p_{Mast}(M_k)=\sum_{i\in M_k}\mathbb{I}(y_i=\mathrm{Mast})/|M_k|$. A metacell was Mast-cell dominated when $p_{Mast}>0.5$ and high purity when $p_{Mast}\geq0.7$. We tested over-representation by one-sided Fisher exact tests with Benjamini--Hochberg correction within each method and seed. Associated metacells contained at least three Mast Cells, showed at least five-fold enrichment, and had adjusted $P<0.05$. We report associated recall, number and size, maximum purity and enrichment, top-one/three/five capture, and concentration. Label-permutation tests with 10,000 repetitions preserved the assignments, metacell sizes, and total Mast-cell count.
