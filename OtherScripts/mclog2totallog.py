#!/usr/bin/python

import numpy as np
import sys
import string

#-----------------------------------------------------------------------------
#
#	 Author:	 P Schwaller
#
#	 Contact: philippe.schwaller@student.manchester.ac.uk
#
#	 Date:		 16/11/2013
#
#-----------------------------------------------------------------------------

if (len(sys.argv) < 4):
	print " "
	print "Usage: "+str(sys.argv[0])+" GB-Type(folder) | logfile amount | Number of timesteps logfile2 in 1000 | logfile3 | etc .."
	print " "

else:
	print ''
	print '-----------------------------------------------------------'
	print '	 Make a total mc_log	'
	print '-----------------------------------------------------------'
	print '-----------------------------------------------------------'
	print ''
	gbtype = sys.argv[1]
	n = int(sys.argv[2])

	dumpnr = []

	outfile = gbtype + '/' +gbtype + '_mc_tot.txt'

	for i in range(0, n-1):
		dumpnr.append(int(sys.argv[3+i])*1000)

	fin = open(gbtype + '/mc_log.txt','r')

	input_mc = [gbtype + '/mc_log ' + str(i)+ '.txt' for i in range(2,n+1)]

	fout = open(outfile,'w')

	for i in range(0, 10001):
		line = fin.readline()
		fout.write(line)

	words = string.split(line)
	defects = int(words[2])
	fin.close()
	'''
	line = fin.readline()
	fout.write(line)

	fin.close()
	'''
	k = 10000
	'''
	defects = 0
	k = 1
	'''
	for i in range(0, n-1):
		fin = open(input_mc[i],'r')
		line = fin.readline()

		for j in range(0, dumpnr[i]):
			line = fin.readline()
			words = string.split(line)
			words[0] = str(k)
			words[2] = str(int(words[2]) + defects)
			line = string.join(words, '    ')

			fout.write(line + '\n')
			k = k+1

		words = string.split(line)
		defects = int(words[2])
		fin.close()

	fout.close()




