#!/usr/bin/python3
# -*- coding: iso-8859-1 -*-
# program to obtain closest annotation for a genome position
# from a gtf/gff/gff3 file

'''

Usage:
  python3 get-closest-annotation.py position-list gff-file
  
  gff-file that may be downsized to select feature such as gene or mRNA...
'''


import sys, fileinput
import numpy as np


def documentation():
    print('''
    Usage:
        python3 get-closest-annotation.py position-list gff-file
    
    position-list: can be any csv file with the chromosome and the position
    in the first and second columns as well as a header - carefull:
    from the R output, you may need to remove line numbers, change tab for coma.
    
    gff-file: is a gff3-like file that may be downsized to select 
    feature such as gene or mRNA...
    
    ''')

try:
    pos = sys.argv[1]
    gff = sys.argv[2]

except:
    documentation()
    sys.exit(1)

f = open(gff,'r')

dic1 = {}
dic2 = {}
for line in f:
  if line[0] != "#":
    l = line.strip().split('\t')
    dic2[(l[0],l[3])] = l
    dic2[(l[0],l[4])] = l
    if l[0] in dic1.keys():
      dic1[l[0]].append(int(l[3]))
      dic1[l[0]].append(int(l[4]))
    else:
      dic1[l[0]] = [int(l[3])]
      dic1[l[0]].append(int(l[4]))

#print(dic2[(1,int(6112447))])
#print(dic2.keys())

o = open(pos[:-4]+"_closest_annotations.0.csv",'w')

g = open(pos,'r')
line = g.readline()
l=line.strip().split()
o.write(','.join(line.strip().split())+"chrom,pos,distance,type,start_annot,end_annot,annot_strand,annotation"+'\n')


for line in g:
  l = line.strip().split('\t')  
  a=int("10000000000000000000000000000000000")
#  print(l[0])
  if l[0] in dic1.keys():
#    print(l[0])
    list = dic1[l[0]]
    list.sort()
#    print(list[0:386])
    for i in list:
      diff=abs(int(i)-int(l[1]))
#      print("diff:"+str(diff))
      if abs(int(i)-int(l[1])) < int(a):
        a = abs(int(i)-int(l[1]))
#        print("a:"+str(a))
        c = str(i)
#        print("i:"+str(i))
#        print("c:"+str(c))
      elif int(diff) == int(a):
        pass
      else:
        m = dic2[(l[0],c)]
#        print(l[1])
#        print(m[3])
#        print(m[4])
        if m[3] < l[1] < m[4]:
          l.append("within")
        else:
          l.append(str(a))
        nm = m[2:5]
        nm.append(m[6])
        nm.append(m[8])
        l.extend(nm)
#        print(l)
        o.write(','.join(l)+'\n')
        break
  else:
    pass
f.close()
g.close()
o.close()  