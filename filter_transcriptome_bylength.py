#!/usr/bin/python3
# -*- coding: iso-8859-1 -*-


import sys, fileinput
from Bio import SeqIO


f = sys.argv[1]
g = sys.argv[2]

o = open('filtered_'+sys.argv[2]+'bp_'+sys.argv[1],'w')

sum = 0
N = 0

for record in SeqIO.parse(f, "fasta"):
	if len(record.seq) > int(g):
		o.write(record.id+"\n")
		o.write(str(record.seq)+"\n")
		N += 1
	else:
		pass
	
print("Transcript_number: "+str(N))
o.close()		
	

