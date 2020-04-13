#!/bin/env python2

import sys

def read_cluster_info(filepath):

	names = {}
	widths = {}
	loffsets = {}
	roffsets = {}
	
	with open(filepath) as file:
		for line in file:
			
			(c, name, w, l, r, n) = line.strip().split('\t')

			names[c]=name
			widths[c]=int(w)
			loffsets[c]=int(l)
			roffsets[c]=int(r)

	return (loffsets, roffsets, widths, names)


def read_motif_info(filepath):
	
	loffsets = {}
	roffsets = {}
	widths = {}
	strands = {}
	cl = {}

	with open(filepath) as file:
		for line in file:
			
			(motif, seq, s, w, l, r, c) = line.strip().split('\t')

			loffsets[motif]=int(l)
			roffsets[motif]=int(r)
			widths[motif]=int(w)
			strands[motif]=s
			cl[motif]=c

	return (loffsets, roffsets, strands, widths, cl)


(clo, cro, cw, cn) = read_cluster_info("/home/jvierstra/data/motifs/cluster/20181012/height0.70/combined.cluster-info.txt")
(mlo, mro, ms, mw, mcl) = read_motif_info("/home/jvierstra/data/motifs/cluster/20181012/height0.70/combined.cluster-motifs.txt")

for line in sys.stdin:
	(chrom, start, end, motif, score, strand, seq)=line.strip().split('\t')
	start=int(start)
	end=int(end)

	try:
		cl=mcl[motif]
		l=mlo[motif]
		r=mro[motif]
		s=ms[motif]
		w=mw[motif]

		cl_name=cn[cl]
		cl_w=cw[cl]
		cl_l=clo[cl]
		cl_r=cro[cl]

		cl_lo=cl_l
		cl_ro=cl_w-cl_r

		if strand==s:
			nstart=start-l+(cl_lo)
			nend=end+r-(cl_ro)
			nstrand="+"
		else:
			nstart=start-r+cl_ro
			nend=end+l-cl_lo
			nstrand="-"

		# bit of a hack for small chromosomes
		if nstart<0:
			continue
	
		print "%s\t%d\t%d\t%s:%s\t%s\t%s\t%s" % (chrom, nstart, nend, cl, cl_name, score, nstrand, motif)
	
		#DEBUG	
		#print "%s\t%d\t%d\t%s:%s\t%s\t%s\t%s" % (chrom, nstart, nend, cl, cl_name, score, nstrand, motif),
		#print start, end, l, r, cl_w, cl_l, cl_r, cl_lo, cl_ro, strand
	
	except KeyError, e:
		pass	
