# motif-clustering
Clustering motif models to remove redundancy

## Requirements

- Python 2.7
  - numpy, scipy
  - genome-tools (http://www.github.com/jvierstra/genome-tools)
- Tomtom (http://meme-suite.org/doc/download.html)

## Included motif databases

- Jolma et al., Cell 2013 (Supplemental Table 2) 
- JASPAR 2018
- HOCOMOCO version 11

## Step 1: Compute pair-wise motif similarity

Here we TOMTOM to determine the similarity between all motif models (all pairwise) with the following code:

```
meme2meme databases/*/*.meme > tomtom/all.dbs.meme

tomtom \
	-bfile /net/seq/data/projects/motifs/hg19.K36.mappable_only.5-order.markov \
	-dist kullback \
	-motif-pseudo 0.1 \
	-text \
	-min-overlap 1 \
	tomtom/all.dbs.meme tomtom/all.dbs.meme \
> tomtom/tomtom.all.txt
```

I have a provided a script that will load this operation up on a SLURM parallel compute cluster (see [e](runall))

## Step 2: Hierarchically cluster motifs by similarity

```
python2 hierarchical.py tomtom/tomtom.all.txt tomtom
```

This script performs hierarchical clustering (distance: correlation, complete linkage) and provides an output of cluster assignments at a range of tree heights (0.5-1). Below is a heatmap representation of motifs clustered by simililarity and clusters identified cutting the dendrogram at height 0.7.

![Clustered heatmap cut at height 0.7](tomtom/height.0.70/heatmap.png)

## Step 3: Process each cluster to build a motif archetype

```
mkdir -p tomtom/height.0.70/viz

python2 process_cluster.py \
  tomtom/tomtom.all.txt \
  tomtom/clusters.0.70.txt \
  62 \
  tomtom/height.0.70
```

This command generates two files (per motif cluster).

```
python2 viz_cluster.py \
  tomtom/height.0.70/cluster-info.62.txt \
  tomtom/height.0.70/cluster-motifs.62.txt \
  tomtom/height.0.70/viz/cluster.62 
 ```

This wiil create a PDF and PNG with visualizing motif cluster #62 corresponding to the basic helix-loop-helix DBD containing OLIG/NEUROG. Dashed lines demarcate the boundaries of the "archetypal" motif position. The motif matches for the constituent models have will have their coordinates adjusted to match.


C62:OLIG (bHLH)|  C69:RUNX (RUNX domain)
:-------------------------:|:-------------------------:
![C62:OLIG](tomtom/height.0.70/viz/cluster.62.png)| ![C69:MEIS](tomtom/height.0.70/viz/cluster.179.png)
