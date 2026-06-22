# GARQ

Graph-Aware Residual Quantization model (GARQ v1.0)

We develop a deep learning framework based on graph-aware residual quantization (GARQ) to efficiently construct metacell representations for single-cell data. GARQ effectively captures topological relationships between cells and learns compact metacell representations through dynamic anchor mechanisms and graph-aware smoothing. Extensive experiments demonstrate that GARQ exhibits superior performance in metacell construction tasks, outperforming existing metacell construction methods across various single-cell multimodal datasets including RNA+ADT, RNA+ATAC, and RNA+ATAC+ADT datasets.

## Table of contents

- [Framework diagram](#diagram)
- [Datasets](#Datasets)
- [Dependencies](#Dependencies)
- [Usage](#Usage)
- [Output](#Output)

## <a name="diagram">Framework diagram</a>



## <a name="Datasets">Datasets</a>

Example datasets used in the article can be downloaded from https://doi.org/10.6084/m9.figshare.32751672, and the downloaded datasets should be placed in the "datasets" folder.

## <a name="Dependencies">Dependencies</a>

Python 3.11.6

Pytorch 2.1.1

Pytorch Geometric 2.6.1

Scanpy 1.9.6

Scipy 1.11.3

Sklearn 0.22.1

Numpy 1.26.0

Pandas 2.3.2

All experiments of GARQ in this study are conducted on Nvidia 4090 (24G) GPU. 

## <a name="Dependencies">Usage</a>

**GARQ Input Data Format**
GARQ accepts paired multi-omics single-cell data in h5ad format as input, supporting the following data types:

+ Dual-modal data: RNA+ADT, RNA+ATAC
+  Triple-modal data: RNA+ATAC+ADT

**Required contents in h5ad file:**

1. Count matrices for each omics modality (including RNA, ADT, and/or ATAC depending on data type)
2. Cell type annotation labels (for evaluating metacell construction quality)

**Usage steps:**

1. Prepare paired multi-omics data in h5ad format

2. Run scripts to perform metacell construction

3. Results will be saved to the specified output path

    

## <a name="Dependencies">Output</a>

1. GARQ outputs metacell count matrices, which can be used for further downstream analyses;
2. GARQ outputs cell-to-metacell assignment results, which can be used to trace the cellular composition of metacells;
3. GARQ outputs latent representations of metacells, which can be visualized through Umap and used to evaluate metacell quality.






