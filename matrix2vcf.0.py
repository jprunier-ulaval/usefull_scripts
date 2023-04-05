#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
# prg to make a vcf file from variant matrix.



def documentation():
	print('''

	Usage:
		python3 matrix2vcf.py matrix-file1.csv output-name option prefix sep


		option: either write 'coord' or 'ID'.
                	If coord : the genome coordinates are expected in col names of variants
                		Then:
                			- prefix option should provide the prefix before coordinates 
                				(chrom)
                			- sep option is the separator used between chrom and 
                				position (often '_')
                		
                	If ID: the output vcf file will only have the variant ID in the 'ID' column, 
                		coordinate will be fictive
        
	''')

import sys, fileinput
import time
import sys
import pandas as pd
from datetime import date

try:
    file = sys.argv[1]
    output = sys.argv[2]
    option = sys.argv[3]

except:
    documentation()
    sys.exit(1)

if option == 'coord':
	try:
		prefix = sys.argv[4]
		sep = sys.argv[5]
	except:
		print('        prefix and/or separator are missing')
		documentation()
		sys.exit(1)


#reading csv file
df = pd.read_csv(file, header = None)

#transposing
df = df.transpose()

#setting the column names using the first row; row of sample names

df.columns = df.iloc[0]
df = df[1:]
df.reset_index(drop=True, inplace=True)

o = open(output,'w')


#writting first lines of the vcf
o.write('##fileformat=VCF'+'\n')
today = date.today()
o.write('##fileDate='+str(today)+'\n')
o.write('##source=matrix2vcf from J.Prunier, Laval University, Canada'+'\n')
o.write('##chosen option='+option+'\n')

#getting list of column names and writing headings of the vcf
col = list(df.columns.values)

nl = ['#CHROM','POS','ID','REF','ALT','QUAL','FILTER','INFO','FORMAT']
nl.extend(col[1:]) 

o.write('\t'.join(nl)+'\n')


a = 1
#iterate over index of rows
for index, row in df.iterrows():
	l = row[0:]
	if option == 'coord':
		#setting first columns in the output vcf
		full_name = l[0]
		short_name = full_name.replace(prefix,'')
		chrom = short_name.split(sep)[0]
		pos = short_name.split(sep)[1]
		nl = [chrom,pos,full_name]
		
		#get allele frequencies
		dic={}
		dic['A'] = sum(i.count('A') for i in l[1:])
		dic['T'] = sum(i.count('T') for i in l[1:])
		dic['C'] = sum(i.count('C') for i in l[1:])
		dic['G'] = sum(i.count('G') for i in l[1:])
		
		#get the most frequent allele		
		first = max(dic, key=dic.get)
		#get the second most frequent allele
		del dic[first]
		second = max(dic, key=dic.get)

		nl.append(first)
		nl.append(second)
		nl2 = ['.','.','.','GT']
		nl.extend(nl2)
		#get genotypes and change for x/x format
		for i in l[1:]:
			i = i.replace(first,'0')
			i = i.replace(second,'1')
			i = i.replace('N','.')
			ngeno = i[0]+'/'+i[1]
			nl.append(ngeno)
		
		#writting entire line in the output	
		o.write('\t'.join(nl)+'\n')

	else:
		#setting first columns in the output vcf
		nl = ['Unknwon', str(a), l[0]]
		
		#get allele frequencies
		dic={}
		dic['A'] = sum(i.count('A') for i in l[1:])
		dic['T'] = sum(i.count('T') for i in l[1:])
		dic['C'] = sum(i.count('C') for i in l[1:])
		dic['G'] = sum(i.count('G') for i in l[1:])

		#get the most frequent allele
		first = max(dic, key=dic.get)
		#get the second most frequent allele
		del dic[first]
		second = max(dic, key=dic.get)
#               print(second)
		nl.append(first)
		nl.append(second)
		nl2 = ['.','.','.','GT']
		nl.extend(nl2)
		for i in l[1:]:
			i = i.replace(first,'0')
			i = i.replace(second,'1')
			i = i.replace('N','.')
			ngeno = i[0]+'/'+i[1]
			nl.append(ngeno)
		#writting entire line in the output vcf
		o.write('\t'.join(nl)+'\n')
		a += 1


o.close()

	

