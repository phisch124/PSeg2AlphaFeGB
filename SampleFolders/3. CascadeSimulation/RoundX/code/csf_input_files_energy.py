#!/usr/bin/python

import numpy as np
import sys
import string

#-----------------------------------------------------------------------------
#
#   Author:   P Schwaller
#
#   Contact:  philippe.schwaller@student.manchester.ac.uk
#
#   Date:     04/03/2014
#
#-----------------------------------------------------------------------------


if (len(sys.argv) != 8):
    print " "
    print "Usage: "+str(sys.argv[0])+" SimulationType PKa_x y z vx vy vz"
    print
    print " "
else:
    print ''
    print '-----------------------------------------------------------'
    print '    Generates the csf input files: qsub and in.sim '
    print '-----------------------------------------------------------'
    print '-----------------------------------------------------------'
    print ''
    symtype = sys.argv[1]
    x = sys.argv[2]
    y = sys.argv[3]
    z = sys.argv[4]
    vx = sys.argv[5]
    vy = sys.argv[6]
    vz = sys.argv[7]

    out1 = "in.sim" + symtype
    out2 = symtype + ".qsub"

    in1 = "input/part1.txt"
    in2 = "input/part2.txt"
    in3 = "input/part3.txt"
    in4 = "input/qsub.txt"

    fout = open(out1,'w')
# Initialisation
    fout.write("#Initialisation\n\n")
    fout.write("log log." + symtype + "\n\n")

    fin = open(in1, 'r')

    for line in fin:
        fout.write(line)
    fin.close()

    fout.write("region rPKA sphere " + x + " " + y + " " + z + " 1.3\n")

    fin = open(in2, 'r')
    for line in fin:
        fout.write(line)
    fin.close()

    fout.write("velocity PKA set " + vx + " " + vy + " " + vz + " # " + symtype + "\n")

# Cascade
    fout.write("restart  50000 " +symtype+".tmp.restart\n")
    fout.write("dump 1 all custom 50000 dump_"+ symtype +".*.txt id type x y z vx vy vz\n")
    fout.write("dump 3 all cfg 1000 all_"+ symtype+ ".*.cfg id type xs ys zs vx vy vz fx fy fz c_kine1 c_pote1 v_cokp v_cokp1\n")

    fin = open(in3, 'r')

    for line in fin:
        fout.write(line)

    fin.close()
    fout.close()

# write qsub file

    fout = open(out2, 'w')

    fin = open(in4, 'r')

    for line in fin:
        fout.write(line)

    fout.write("mpirun -np $NSLOTS lmp_linux < in.sim" + symtype +" \n")

    fout.close()
    fin.close()





