#!/bin/env python2
##mkdir -p viz && tail -n+2 ../clusters.0.70.txt | cut -f2 | sort -g  | uniq | xargs -I {} python ../process_cluster.py ../clusters.0.70.txt {}

import sys
import os.path

import pandas as pd
import numpy as np
import scipy as sp

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

from pylab import rcParams
rcParams['pdf.fonttype'] = 42
rcParams['svg.fonttype'] = 'none'

from genome_tools.plotting import pwm


cl_info_file=sys.argv[1]
cl_motifs_file=sys.argv[2]
outfile=sys.argv[3]

cluster_info=pd.read_csv(cl_info_file, delimiter="\t", header=None)
cluster_info.columns=["cl", "seed_motif", "roffset", "s", "e", "N"]

cl_motifs_info=pd.read_csv(cl_motifs_file,  delimiter="\t", header=None)
cl_motifs_info.columns=["id", "consensus", "strand", "w", "loffset", "roffset", "cluster"]

N=cl_motifs_info.shape[0]
right=np.max(cl_motifs_info["loffset"]+cl_motifs_info["w"])

s=cluster_info["s"][0]
e=cluster_info["e"][0]

padding=2

fig=plt.figure()

width=(right+padding*2)*0.15
label_size=2.0

fig.set_size_inches(width+label_size, N*0.35)

gs=gridspec.GridSpec(N, 2, wspace=0, width_ratios=[1, label_size/width])

plt.subplots_adjust(left=0, top=1, bottom=0)

for i in range(N):

    ax=fig.add_subplot(gs[i,0])

    m=cl_motifs_info.iloc[i,:]

    pssm=np.loadtxt("/home/jvierstra/data/motifs/moods/GRCh38_no_alts.alldbs.1e-4/pfm/%s.pfm" % m["id"])
    w=m["w"]
    offset=m["loffset"]
    strand=m["strand"]

    #ic=relative_info_content(pwm) if strand=="+" else relative_info_content(reverse_complement_pwm(pwm))

    
    pwm(pssm).render(fig, ax, type="ic", xoffset=offset, xlim=(0-padding, right+padding), rc=True if strand=="-" else False)

    #stackedbar(ic.T, ax, sorted=True, xoffset=offset)
    ax.axvline(s, color='black', ls='--')
    ax.axvline(e, color='black', ls='--')

    ax.text(0.90, 0.5, m["id"], transform = ax.transAxes, ha = 'left', va = 'center')

    #ax.xaxis.set_visible(True)

    #ax.set_xlim(0-padding, right+padding)
    #ax.set_ylim(0, 2.25)
    

    
    #ax.set_ylabel("Bits")

    [ax.spines[loc].set_color("none") for loc in ["top", "right"]]

plt.savefig(outfile + ".pdf")
plt.savefig(outfile + ".png")