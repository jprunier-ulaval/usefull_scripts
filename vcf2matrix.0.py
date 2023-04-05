#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
# prg to make a matrix from vcf files.
# works only for two-alleles SNP data



def documentation():
	print('''

	Usage:
		python vcf2matrix.py vcf-file1 output-name option


		option: either write 'coord' or 'ID'.
                	If coord : the output name for each variant will be based on chromosome and position
                	If ID: the output name for each variant will be based on variant ID
        
	''')

import sys, fileinput
import time
import sys
import pandas as pd

try:
    file = sys.argv[1]
    output = sys.argv[2]
    option = sys.argv[3]

except:
    documentation()
    sys.exit(1)


f = open(file,'r')

data = []


for line in f:
	# pass header lines
	if line[0:2] == '##':
		pass
	# getting line of sample names
	elif line[0:2] == '#C':
		header = line.strip().split('\t')
		nl = ['Samples']
		nl.extend(header[9:])
		data.append(nl)
	
	# getting genotypes and changing for nucleotides		
	else:
		l= line.strip().split('\t')
		if option == 'coord':
			#varname contains prefix + chrom + pos + allel1 + allel2
			varname = 'Var'+l[0]+'_'+l[1]+'_'+l[3]+l[4]
			nl = [varname]
			for sample in l[9:]:
#				print(sample)
				geno = sample[0:3]
				geno = geno.replace('/','')
				geno = geno.replace('0',l[3])
				geno = geno.replace('1',l[4])
				geno = geno.replace('.','N')
				nl.append(geno)
			data.append(nl)
				
				
		else:
                        #varname contains prefix + ID + allel1 + allel2
                        varname = 'Var'+l[2]+'_'+l[3]+l[4]
                        nl = [varname]
                        for sample in l[9:]:
                                geno = sample[0:3]
                                geno = geno.replace('/','')
                                geno = geno.replace('0',l[3])
                                geno = geno.replace('1',l[4])
                                geno = geno.replace('.','N')
                                nl.append(geno)
                        data.append(nl)

#make a dataframe easily transposed
df  = pd.DataFrame(data)

df = df.transpose()

#writing output
df.to_csv(output, index = False, header = False) 
	

f.close()

	

