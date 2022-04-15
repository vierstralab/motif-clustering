#!/bin/env python

import sys
import re

import numpy as np

meme_file=sys.argv[1]
output_dir=sys.argv[2]


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
			z.append(list(map(float, data[ist:iend].strip().split())))
			ist = iend+1
			j+=1

		pwms[motif]=np.array(z)

		pos=ist

	return pwms

pwms=read_meme_file(meme_file)

for k, p in pwms.items():
	np.savetxt("%s/%s.pfm" % (output_dir, k), p.T, delimiter='\t', fmt='%0.5f')
