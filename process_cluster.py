#!/bin/env python2
##mkdir -p viz && tail -n+2 ../clusters.0.70.txt | cut -f2 | sort -g  | uniq | xargs -I {} python ../process_cluster.py ../clusters.0.70.txt {}

import sys
import os.path

import pandas as pd
import numpy as np
import scipy as sp

####

import re

def read_meme_file(filepath):
	
	pwms={}

	data = open(filepath).read()

	pos=0
	while(1):

		rec_loc=data.find('\nMOTIF', pos)

		if rec_loc<0:
			break

		nl=data.find('\n', rec_loc+1)

		motif=data[rec_loc+6:nl].strip()
		#print motif

		mat_header_start=data.find('letter-probability', rec_loc)
		mat_header_end=data.find('\n', mat_header_start+1)

		i = data.find(':', mat_header_start)
		kp = data[i+1:mat_header_end]
		r = re.compile(r"(\w+)=\s?([\w.\+]+)\s?")
		attribs=dict(r.findall(kp))

		ist=mat_header_end+1
		iend=-1

		j=0
		z=[]
		while(j<int(attribs["w"])):
			iend = data.find('\n', ist)
			z.append(map(float, data[ist:iend].strip().split()))
			ist = iend+1
			j+=1

		pwms[motif]=np.array(z)

		pos=ist

	return pwms

def relative_info_content(pwm):
	p=pwm/np.sum(pwm, axis = 1)[:,np.newaxis]
	ic=2+np.sum(p*np.nan_to_num(np.log2(p)), axis = 1)
	ric=p*ic[:,np.newaxis]
	return ric

def reverse_complement_pwm(pwm):
	baseorder=[3,2,1,0]
	return pwm[::-1,baseorder]

pwms = read_meme_file("/home/jvierstra/data/motifs/cluster/20181012/all.dbs.meme")

def pwm_widths(pwms, ids):
	return [pwms[i].shape[0] for i in ids]

####

sim_file=sys.argv[1]
cluster_file=sys.argv[2]
cl=int(sys.argv[3])
outdir=sys.argv[4]

sim=pd.read_csv(sim_file, header=None, delimiter="\t", skiprows=1)
clusters=pd.read_csv(cluster_file, header=0, delimiter="\t", index_col=0)

cl_motifs=clusters.index[clusters["cluster"]==cl]

cl_seed_motif=cl_motifs[0]

i=(sim[0]==cl_seed_motif) & (sim[1].isin( cl_motifs))

cl_motifs_info=sim.loc[i]

# motif width
cl_motifs_info["w"]=cl_motifs_info[8].str.len()
#cl_motifs_info.sort_values(by="w", inplace=True, ascending=False)

# cluster left offset
left=np.min(-cl_motifs_info[2])
cl_motifs_info["loffset"]=-left-cl_motifs_info[2]

# cluster right offset
right=np.max(cl_motifs_info["loffset"]+cl_motifs_info["w"])
cl_motifs_info["roffset"]=right-cl_motifs_info["w"]-cl_motifs_info["loffset"]

cl_motifs_info["cluster"]=cl

cl_motifs_info.drop([0, 2, 3, 4, 5, 6, 7], axis = 1, inplace=True)
cl_motifs_info.rename(columns={1: "id", 8: "consensus", 9: "strand"}, inplace=True)

cl_motifs_info.to_csv(os.path.join(outdir, "cluster-motifs.%d.txt" % cl), sep="\t", header=None, index=False)

####

N=cl_motifs_info.shape[0]

total_ic=np.zeros(right)

for i in range(N):
	
	m=cl_motifs_info.iloc[i,:]
	
	pwm=pwms[m["id"]]
	w=m["w"]
	offset=m["loffset"]
	strand=m["strand"]

	ic=relative_info_content(pwm) if strand=="+" else relative_info_content(reverse_complement_pwm(pwm))
	total_ic[offset:offset+w]+=np.sum(ic, axis=1)


cdf=np.cumsum(total_ic)/np.sum(total_ic)
s=np.where(cdf>0.05)[0][0]
e=np.where(cdf>0.95)[0][0]+1

with open(os.path.join(outdir, "cluster-info.%d.txt" % cl), "w") as file:
	file.write('\t'.join(map(str, [cl, cl_seed_motif, right, s, e, N]))+'\n')

sys.exit(0)
