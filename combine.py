#!/bin/env python3

import sys
import math

for line in sys.stdin:
	(ref, mapped) = line.strip().split('|')

	scores={}
	strands={}
	motifs={}
	n={}
	for elem in mapped.split(';'):
		(chr, start, end, name, score, strand, motif)=elem.split('\t')
		score=float(score)

		best = scores.get(name, 1.0)
		
		n[name] = n.get(name, 0) + 1

		if score>best:
			scores[name]=score
			strands[name]=strand
			motifs[name]=motif

	for name, score in scores.items():
		print "%s\t%s\t%s\t%s\t%s\t%d" % (ref, name, '{:.4f}'.format(score), strands[name], motifs[name], n[name])
		#print "%s\t%s\t%s\t%s" % (ref, name, '{:d}'.format(int(math.floor(-math.log10(score)))), strands[name])