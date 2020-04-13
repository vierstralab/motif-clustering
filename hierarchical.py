#!/bin/env python2

import sys
import os.path

import pandas as pd
import numpy as np
import scipy as sp

##

sim_file=sys.argv[1]
outdir=sys.argv[2]

sim = pd.read_csv(sim_file, header=None, delimiter="\t", skiprows=1)

simsq = sim.pivot(index = 0, columns = 1, values = 4)
simsq.fillna(100, inplace=True)

##

from scipy.cluster.hierarchy import fcluster, linkage, dendrogram
from scipy.spatial.distance import squareform

mat = -np.log10(simsq)
mat[np.isinf(mat)]=10

Z = linkage(mat, method = 'complete', metric = 'correlation')

#d = dendrogram(Z, no_plot=True)
#o = d["leaves"]

step=0.1
start=0.5
end=1.0

thresholds=np.arange(start, end+step/100, step)

for thresh in thresholds:

	print "tree height: %0.2f" % (thresh)

	cl = fcluster(Z, thresh, criterion='distance')

	df = pd.DataFrame(cl, index=mat.index, columns=["cluster"])
	df.index.name="motifs"

	df.to_csv(os.path.join(outdir, "clusters.%0.2f.txt" % (thresh)), sep="\t", header=True)

##


