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
#   Date:     16/11/2013
#
#-----------------------------------------------------------------------------

if (len(sys.argv) != 4):
    print " "
    print "Usage: "+str(sys.argv[0])+" Input_file Initial_defects Start_Timestep"
    print " "

else:
    print ''
    print '-----------------------------------------------------------'
    print '    Print average number of defects from a mc_log.txt file   '
    print '-----------------------------------------------------------'
    print '-----------------------------------------------------------'
    print ''
    infile = sys.argv[1]
    i_def = int(sys.argv[2])
    t1 = int(sys.argv[3])


    fin = open(infile,'r')

    line = fin.readline()
    words = string.split(line)
    total = 0

    if(words[0].lower()=='#timestep'):
        for i in range(0,t1):
            line = fin.readline()
        words = string.split(line)
        print ''
        print 'Starting to count at timestep ' + str(int(words[0]) + 1)
        print ''
        print '---------------------------------------------------------'

        t1 = 0

        for line in fin:
            words = string.split(line)
            total += int(words[2]) + i_def
            t1 += 1

        result = float(total)/float(t1)

        print ''
        print 'Average number of defects: ' + str(result)
        print ''
        print '---------------------------------------------------------'

    fin.close()

