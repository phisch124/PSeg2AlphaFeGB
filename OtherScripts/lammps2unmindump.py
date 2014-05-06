import sys
#sys.path.append('/mnt/cr01-home01/shared/lammps-30Sep13/python')
from lammps import lammps
import numpy as np
import sys

nvars = 2
if (len(sys.argv) != nvars):
    print " "
    print "Usage: "+str(sys.argv[0])+" input_file "
    print "The input file is in.base, it creates an unminimised dump file at timestep 0 "
else:
    input_file = str(sys.argv[1])
#    T = float(sys.argv[2])
#    mu = float(sys.argv[3])

#    beta = 11605.0/T

 #   np.random.seed(21694) # Initialise seed

    # Open logfile


    lmp = lammps()
    lmp.file(input_file)

    natoms = lmp.get_natoms()

    #lmp.command("variable mype equal pe")
    #Ef = lmp.extract_variable("mype","all",0)     # Get initial energy
    #lmp.command("variable mype equal thermo_pe")


        # Also write a dump file? I'm writing this in a lammps dump style so that my conversion scripts can be used

            # Open dumpfile
    fdump='dump_unmin.txt'
    print' writing dump'
    f1=open(fdump,'w')
    x = lmp.extract_atom("x",3)   # obtain a POINTER! to atom coords
    #atomtype = lmp.extract_atom("type",0)  # we already have atom types
    atomid = lmp.extract_atom("id",0)  # ditto ids
    atomtype = lmp.extract_atom("type",0)   # POINTER! to vector of atom types

    f1.write('ITEM: TIMESTEP\n')
    f1.write(str(0) + '\n')
    f1.write('ITEM: NUMBER OF ATOMS\n')
    f1.write(str(natoms) + '\n')
    f1.write('ITEM: BOX BOUNDS pp pp pp\n')
    f1.write(str(lmp.extract_global("boxxlo",1)) + ' ' + str(lmp.extract_global("boxxhi",1)) + '\n')
    f1.write(str(lmp.extract_global("boxylo",1)) + ' ' + str(lmp.extract_global("boxyhi",1)) + '\n')
    f1.write(str(lmp.extract_global("boxzlo",1)) + ' ' + str(lmp.extract_global("boxzhi",1)) + '\n')
    f1.write('ITEM: ATOMS id type x y z\n')

    for s in range(natoms):
        f1.write(str(atomid[s]) + ' ' + str(atomtype[s]) + ' ' + str(x[s][0]) + ' ' + str(x[s][1]) + ' ' + str(x[s][2]) + '\n')
    f1.close()




