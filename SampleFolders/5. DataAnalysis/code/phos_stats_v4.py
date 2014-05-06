#!/usr/bin/python

import numpy as np
import sys
import string

#-----------------------------------------------------------------------------
#
#   Author:   P Schwaller
#
#   Contact: philippe.schwaller@student.manchester.ac.uk
#
#   Date:     28/02/2014
#
#-----------------------------------------------------------------------------


if (len(sys.argv) != 4):
    print " "
    print "Usage: "+str(sys.argv[0])+" Input_file Output_file Output_file2"
    print " "

else:
    #print ''
    #print '-----------------------------------------------------------'
    #print ' Reads with lammps2cfg.py created cfg files and outputs the phosphorus distribution  '
    #print '-----------------------------------------------------------'
    #print '-----------------------------------------------------------'
    #print ''
    infile = sys.argv[1]
    outfile = sys.argv[2]
    out2 = sys.argv[3]


    fin = open(infile,'r')
    line = fin.readline()
    words = string.split(line)

    #Define the precision you want to look at the phosphorus distribution
    prec = 100.0

    #Make a dictionary to save the P distribution, putting every position to 0
    distr = {}

    # dictionary to save x values of P atoms

    x_phos = {}

    for i in range(int(prec)+1):
        distr[i] = 0

    #delete all iron lines

    counter = 0

    mean = 0

    for i in range(17):
        line = fin.readline()
        words = string.split(line)

#change this get a better stop, read until the end of the file.. how?!
    while True:
        #Assingments are not allowed in expressions in Python -> while(line=fin.readline()): -> syntax error. Improvised end of file test:
        if not line: break
        if words[1] and words[1] == 'P':
            distr[int(float(words[2])*prec)] = distr[int(float(words[2])*prec)] + 1
            x_phos[counter] = float(words[2])
            mean = mean + float(words[2])

            counter = counter + 1
        line = fin.readline()
        words = string.split(line)

    print counter

    fin.close()

    # statistical calculations:

    mean = mean / counter

    #standard deviation

    s = 0
    m3 = 0
    m4 = 0

    for i in range(counter):
        s = s + (x_phos[i]-mean)**2
        m3 = m3 + (x_phos[i]-mean)**3
        m4 = m4 + (x_phos[i]-mean)**4


    s = (s/(counter))**(0.5)
    m3 = (m3/(counter))
    m4 = (m4/(counter))

#    print mean
#    print s
#    print m3
#    print m4
#    print m3/s**3
#    print m4/s**4 - 3

    fout2 = open(out2, 'a')

    print 'Name mean standard_deviation m3 m4 skewness kurtosis'

    fout2.write(infile[4:infile.rfind('_C')] + ' ' + str(mean) + ' ' + str(s) + ' ' + str(m3) + ' ' + str(m4) + ' ' + str(m3/s**3) + ' ' + str(m4/s**4 - 3) + '\n')

    fout2.close()


    fout = open(outfile, 'w')

 #   fout.write('Standard deviation: s = ' + str(s) + ' Mean value: mean = ' + str(mean) + '\n')

    for i in range(int(prec)+1):
        fout.write(str(i) + ' ' + str(distr[i]) + '\n')

    fout.close()



