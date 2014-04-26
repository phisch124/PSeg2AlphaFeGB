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
#   Date:     24/10/2013
#
#-----------------------------------------------------------------------------

if ((len(sys.argv) != 3) and (len(sys.argv) != 4) and (len(sys.argv) != 5)):
    print " "
    print "Usage: "+str(sys.argv[0])+" Input_file Output_file [x_column] [vx_column]"
    print " "
    print "      Note that atom_id and atom_type are assumed to be in cols 1 and 2"
    print "      Default is to assume that x coordinate is in column 3"
    print " "
else:
    print ''
    print '-----------------------------------------------------------'
    print '    File conversion utility: lammps dump -> lammps input   '
    print '-----------------------------------------------------------'
    print '-----------------------------------------------------------'
    print ''
    infile = sys.argv[1]
    outfile = sys.argv[2]
    numcol = 1
    typecol = 2
    xcol = 3
    usevel = False
    if (len(sys.argv) == 4):
        xcol = int(sys.argv[3])
    if (len(sys.argv) == 5):
        vxcol = int(sys.argv[4])
        usevel = True


    bounds = np.zeros((3,2), dtype=float)
    skew = np.zeros((3), dtype=float)
    isskew = False

    # First check number of atom types
    fin = open(infile,'r')
    done = False
    while not done:
        line = fin.readline()
        words = string.split(line)
        if (len(words)>2):
            if (words[3].lower() == 'atoms'):
                line = fin.readline()
                words = string.split(line)
                natoms = int(words[0])
            elif (words[1].lower() == 'atoms'):
                done = True
    numtypes = 0
    for i in range(natoms):
        line = fin.readline()
        words = string.split(line)
        if (int(words[typecol-1])>numtypes):
            numtypes = int(words[typecol-1])
    fin.close()


    fin = open(infile,'r')
    fout = open(outfile,'w')


    done = False
    while not done:
        line = fin.readline()
        words = string.split(line)
        if (len(words)>2):
            if (words[3].lower() == 'atoms'):
                line = fin.readline()
                words = string.split(line)
                natoms = int(words[0])
                done = True

    done = False
    while not done:
        line = fin.readline()
        words = string.split(line)
        if (len(words)>2):
            if (words[2].lower() == 'bounds'):
                done = True
    if (words[3].lower() == 'xy'):
        isskew = True
    else:
        line = fin.readline()
        words = string.split(line)
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
    if (isskew):
        bounds[0,0] = bounds[0,0] - min(0.0,skew[0],skew[1],skew[0]+skew[1])
        bounds[0,1] = bounds[0,1] - max(0.0,skew[0],skew[1],skew[0]+skew[1])
        bounds[1,0] = bounds[1,0] - min(0.0,skew[2])
        bounds[1,1] = bounds[1,1] - max(0.0,skew[2])

    done = False
    while not done:
        line = fin.readline()
        words = string.split(line)
        if (len(words)>0):
            if (words[1].lower() == 'atoms'):
                done = True

    # Write header
    fout.write('#Header\n')
    fout.write('\n')
    fout.write(str(natoms) + ' atoms\n')
    fout.write('\n')
    fout.write(str(numtypes) + ' atom types\n')
    fout.write('\n')

    fout.write(str(bounds[0,0]) + ' ' +str(bounds[0,1]) + ' xlo xhi\n')
    fout.write(str(bounds[1,0]) + ' ' +str(bounds[1,1]) + ' ylo yhi\n')
    fout.write(str(bounds[2,0]) + ' ' +str(bounds[2,1]) + ' zlo zhi\n')
    if (isskew):
        fout.write(str(skew[0]) + ' ' + str(skew[1]) + ' ' + str(skew[2]) + ' xy xz yz\n')
    else:
        fout.write('\n')
    fout.write('\n')
    fout.write('Atoms\n')
    fout.write('\n')

    for i in range(natoms):
        line = fin.readline()
        words = string.split(line)
        if (usevel):
            fout.write(words[numcol-1] + ' ' + words[typecol-1] + ' ' + words[xcol-1] + ' ' + words[xcol] + ' ' + words[xcol+1] + ' ' + words[vxcol-1] + ' ' + words[vxcol] + ' ' + words[vxcol+1] + '\n')
        else:
            fout.write(words[numcol-1] + ' ' + words[typecol-1] + ' ' + words[xcol-1] + ' ' + words[xcol] + ' ' + words[xcol+1] + '\n')


    fin.close()
    fout.flush()
    fout.close()








