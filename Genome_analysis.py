#!/usr/bin/python3
# -*- coding: iso-8859-1 -*-

import sys, fileinput
from Bio import SeqIO
import numpy as np

f = sys.argv[1]

o = open('Assembly_analysis_'+sys.argv[1],'w')

total = 0
scaf_list = []
N = 0

for record in SeqIO.parse(f, "fasta"):
	scaf_list.append(int(len(record.seq)))
	total += int(len(record.seq))
	N += 1

o.write("total assembly: "+str(total)+'\n')
o.write("Sequence_number: "+str(N)+'\n')
print("total assembly: "+str(total))
print("Sequence_number: "+str(N))


#print(scaf_list[-10:-1])

scaf_list.sort(reverse=True)

#print(scaf_list[-10:-1])

avg = np.average(scaf_list)
med = np.median(scaf_list)

o.write("Average_seq_length: "+str(avg)+'\n')
o.write("Median_seq_length: "+str(med)+'\n')
print("Average_seq_length: "+str(avg))
print("Median_seq_length: "+str(med))

cum = 0
L = 0
for scaf in scaf_list:
	if cum <= float(total*0.5):
		cum += int(scaf)
		#print(cum)
		L += 1
		#print(L)
		pre_scaf = scaf
	else:
		N50 = pre_scaf
		break

print("N50: "+str(N50))
o.write("N50: "+str(N50)+'\n')
print("L50: "+str(L))
o.write("L50: "+str(L)+'\n')		
		
cum = 0
L = 0
for scaf in scaf_list:
	if cum <= float(total*0.9):
                cum += int(scaf)
                L += 1
                pre_scaf = scaf
	else:
		N90 = pre_scaf
		break

print("N90: "+str(N90))
o.write("N90: "+str(N90)+'\n')
print("L90: "+str(L))
o.write("L90: "+str(L)+'\n')

o.close()
