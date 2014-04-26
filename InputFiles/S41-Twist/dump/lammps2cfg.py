#!/usr/bin/python

import numpy as np
import sys
import string

#-----------------------------------------------------------------------------
#
#   Author:   C P Race
#
#   Address:  Materials Science Centre, University of Manchester
#   Contact:  christopher.race@manchester.ac.uk
#
#   Date:     09/08/2013
#
#-----------------------------------------------------------------------------

if (len(sys.argv) < 5):
    print " "
    print "Usage: "+str(sys.argv[0])+" Input_file Output_file Mass Symbol [..... Mass Symbol]"
    print "Fe 55.845 P 30.9738 "
    print " "
else:
    infile = sys.argv[1]
    outfile = sys.argv[2]
    mass = []
    element = []
    giventypes = (len(sys.argv)-3)/2
    for i in range(giventypes):
        mass.append(sys.argv[3+2*i])
        element.append(sys.argv[4+2*i])

    print ''
    print '-----------------------------------------------------------'
    print '     File conversion utility: lammps input -> cfg'
    print '-----------------------------------------------------------'
    print '-----------------------------------------------------------'
    print ''

    bounds = np.zeros((3,2), dtype=float)
    skew = np.zeros((3), dtype=float)
    isskew = False

    fin = open(infile,'r')
    fout = open(outfile,'w')


    done = False
    while not done:
        line = fin.readline()
        words = string.split(line)
        if (len(words)>1):
            if (words[1].lower() == 'atoms'):
                natoms = int(words[0])
                done = True

    done = False
    while not done:
        line = fin.readline()
        words = string.split(line)
        if (len(words)>2):
            if(words[2].lower() == 'types'):
                ntypes = int(words[0])
                done = True
    if ntypes != giventypes:
        print 'Possible problem with insufficent atom types specified'

    done = False
    while not done:
        line = fin.readline()
        words = string.split(line)
        if (len(words)>2):
            if (words[2].lower() == 'xlo'):
                bounds[0,0] = float(words[0])
                bounds[0,1] = float(words[1])
                line = fin.readline()
                words = string.split(line)
                bounds[1,0] = float(words[0])
                bounds[1,1] = float(words[1])
                line = fin.readline()
                words = string.split(line)
                bounds[2,0] = float(words[0])
                bounds[2,1] = float(words[1])
                done = True

    done = False
    while not done:
        line = fin.readline()
        words = string.split(line)
        if (len(words)>3):
            if (words[3].lower() == 'xy'):
                isskew = True
                skew[0] = float(words[0])
                skew[1] = float(words[1])
                skew[2] = float(words[2])
        if (len(words)>0):
            if (words[0].lower() == 'atoms'):
                done = True
    H0 = np.zeros((3,3),dtype=float)
    H0[0,0] = bounds[0,1]-bounds[0,0]
    H0[1,0] = skew[0]
    H0[1,1] = bounds[1,1]-bounds[1,0]
    H0[2,0] = skew[1]
    H0[2,1] = skew[2]
    H0[2,2] = bounds[2,1]-bounds[2,0]

    # Write header
    fout.write('Number of particles = ' + str(natoms) + '\n')
    fout.write('\n')
    fout.write('A = 1.0 Angstrom\n')
    fout.write('\n')
    fout.write('H0(1,1) = ' + str(bounds[0,1]-bounds[0,0]) + ' A\n')
    fout.write('H0(1,2) = 0 A\n')
    fout.write('H0(1,3) = 0 A\n')
    fout.write('\n')
    fout.write('H0(2,1) = ' + str(skew[0]) + ' A\n')
    fout.write('H0(2,2) = ' + str(bounds[1,1]-bounds[1,0]) + ' A\n')
    fout.write('H0(2,3) = 0 A\n')
    fout.write('\n')
    fout.write('H0(3,1) = ' + str(skew[1]) + ' A\n')
    fout.write('H0(3,2) = ' + str(skew[2]) + ' A\n')
    fout.write('H0(3,3) = ' + str(bounds[2,1]-bounds[2,0]) + ' A\n')
    fout.write('\n')

    line = fin.readline()

    for i in range(natoms):
        line = fin.readline()
        words = string.split(line)
        pos = np.array([float(words[2]),float(words[3]),float(words[4])])
        spos = np.dot(np.linalg.inv(np.transpose(H0)),pos)
        fout.write(mass[int(words[1])-1] + ' ' + element[int(words[1])-1] + ' ' + str(spos[0]) + ' ' + str(spos[1]) + ' ' + str(spos[2]) + ' 0.0 0.0 0.0\n')










