#!/usr/bin/python3
# -*- coding: iso-8859-1 -*-


import sys, fileinput
from Bio import SeqIO


f = sys.argv[1]

o = open('scafsize_'+sys.argv[1],'w')

sum = 0
N = 0

for record in SeqIO.parse(f, "fasta"):
	o.write(record.id+"\t")
	o.write(str(len(record.seq))+"\n")
	sum += len(record.seq)
	N += 1

print("total assembly: "+str(sum))
print("Sequence_number: "+str(N))
o.close()		
	

