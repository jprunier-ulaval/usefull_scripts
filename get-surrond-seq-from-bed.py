#!/usr/bin/python3
# -*- coding: iso-8859-1 -*-
# program to select SNPs according to an average distance


import sys, fileinput
import numpy as np
from Bio import SeqIO


def documentation():
    print('''
    Usage:
        python3 get-surround-seq-from-bed.py bedfile refgenome distance
        
    ''')

try:
    bed = sys.argv[1]
    ref = sys.argv[2]
    dist = sys.argv[3]

except:
    documentation()
    sys.exit(1)


dic = {}

for record in SeqIO.parse(ref, "fasta"):
#  print(record.id)
  chr = str(record.id).split(' ')[0].replace('chr','')
  dic[chr] = str(record.seq)
  
o = open(bed[:-4]+str(dist)+"_suroundSeq.csv",'w')
o.write("chromosome,position,seq\n")

h = open(bed,'r')
line = h.readline()

for line in h:
  l = line.strip().split('\t')
#  print(l[1])
  start = int(l[1])-int(dist)
#  print(start)
  if start < 0:
    start = 0
  end = int(l[1])+int(dist)
#  print(end)
  chromo = str(l[0]).replace('chr','')
#  print(chromo)
  if chromo in dic.keys():
    seq = str(dic[chromo][start:end])
    nl=[chromo,l[1],seq]
    if end > len(dic[chromo]):
      end = len(dic[chromo])
  else:
    nl=['not_found','not_found','not_found']

  o.write(','.join(nl)+'\n')

#f.close()
#h.close()
o.close()

