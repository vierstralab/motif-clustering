#!/bin/env python2

import sys
import pandas as pd

clusters=pd.read_csv(sys.argv[1], index_col=0)

for line in sys.stdin:
	fields=line.strip().split('\t')
	cl_id, cl_seed_motif=fields[3].split(":")
	cl_id=int(cl_id)

	rgb = "%d,%d,%d" % (clusters.loc[cl_id]['R'], clusters.loc[cl_id]['G'], clusters.loc[cl_id]['B'])
	name = clusters.loc[cl_id]['Name']
	dbd = clusters.loc[cl_id]['DBD']

	fields[3]=name


	print '\t'.join(fields[:4] + ["0"] + [fields[5]] + fields[1:3] + [rgb] + [fields[6],  fields[4], dbd, fields[7]] ) 