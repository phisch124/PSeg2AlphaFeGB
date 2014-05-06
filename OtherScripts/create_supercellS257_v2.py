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
#   Date:     08/12/2013
#
#   Modifications: 24/03/2014 ID changes with lammps minimize,
#   would be better to use atom coordinates for placement
#-----------------------------------------------------------------------------


numargs = 5
if (len(sys.argv) != numargs):
    print " "
    print "Usage: "+str(sys.argv[0])+" x_reps y_reps z_reps w_reps"
    print " "
    print "      x,y,z_reps for number of repeats of black lattice"
    print "      w_reps for number of repeats of white lattice parallel to gb normal"
    print "      Take the same values as used for the creation of the prepopulation input file"
    print "      atom_type should be an integer for lammps (1,2,3,..) -> 1"
    print "      lattice parameter in whatever units software will assume (probably angstrom) -> 2.855"
    print "      Smallest atom separation to tolerate (fractions of lattice param distance) -> 0.3"
    print " "
else:
    #supercell parameter - scales the cell - set to 1 here, to get a better view of the problem..
    sc_par = 4

    # Inputs

    # One small standart cell as created for the GB Prepopulation
    numrepsb = np.array([int(sys.argv[1]),int(sys.argv[3]),int(sys.argv[2])])
    repsw = int(sys.argv[4])
    atomtype = str(1)
    alatt = 2.855
    olap = 0.3


    #supercell
    sc_numrepsb = sc_par * numrepsb
    sc_repsw = sc_par * repsw

    input_file_b = 'csl_black.txt'
    input_file_w = 'csl_white.txt'

    #needs sc_par * sc_par dump_files as input to create the gbs -> dump1.txt to dump16.txt
    #access the names with input_gb[0] to input_gb[15]
    input_gb = ['dump/dump' + str(i)+ '.txt' for i in range(1,1+(sc_par*sc_par))]

    output_file = 'lammps_sc.txt'
    fo = open(output_file, 'w')

    cslbasis = np.zeros((3,3), dtype=float)

    #small cell
    numrepsw = np.copy(numrepsb)
    numrepsall = np.copy(numrepsb)

    #supercell
    sc_numrepsw = np.copy(sc_numrepsb)
    sc_numrepsall = np.copy(sc_numrepsb)
    sc_bulkrepsall = np.copy(sc_numrepsb)



    print ''
    print '-----------------------------------------------------------'
    print '       Cubic grain boundary supercell file creator'
    print '-----------------------------------------------------------'
    print '-----------------------------------------------------------'
    print ''



    numrepsw[0] = repsw
    numrepsall[0] = numrepsb[0] + numrepsw[0]

    # only insert half of bulk to make cell a bit smaller !!!
    sc_numrepsb[0] = sc_par/2 * numrepsw[0]
    sc_numrepsw[0] = sc_par/2 * numrepsw[0]
    sc_numrepsall[0] = (sc_par/2 +1) * numrepsall[0]
    sc_bulkrepsall[0] = (sc_par)/2 * numrepsall[0]

    #offset
    #setting white offset sc_par + 2 cells away (sc_par * black + 2 for the gb)
    offsetw = np.array([(sc_par/2+2)* numrepsb[0],0,0])
    #offset for the b to w gb = sc_par
    offsetbw = np.array([(sc_par/2)* numrepsb[0],0,0])
    #offset for the w to b gb = 2* sc_par + 2
    offsetwb = np.array([(2*sc_par/2+2)* numrepsb[0],0,0])



    #taken from create_inputfile.py

    fb = open(input_file_b, 'r')
    fw = open(input_file_w, 'r')

    # Get number of atoms in minimal cell
    fb.readline()
    line = fb.readline()
    words = string.split(line)
    natoms = int(float(words[1]))
    for i in range(3):
        line = fb.readline()
        words = string.split(line)
        cslbasis[i,i]=float(words[1])
    #print cslbasis

    # positions of the black atoms in posb array
    posb = np.zeros((natoms,3), dtype=float)
    for s in range(natoms):
        line = fb.readline()
        words = string.split(line)
        #print words
        for t in range(3):
            posb[s,t] = float(words[t])
    fb.close()

    # positions of the white atoms in posw array
    fw.readline()
    fw.readline()
    fw.readline()
    fw.readline()
    fw.readline()
    posw = np.zeros((natoms,3), dtype=float)
    for s in range(natoms):
        line = fw.readline()
        words = string.split(line)
        for t in range(3):
            posw[s,t] = float(words[t])
    fw.close()

    # Now find overlapping atoms in minimal cells
    olapb = np.zeros([natoms], dtype = int)
    olapw = np.zeros([natoms], dtype = int)
    # Black cell first
    nolapb = 0
    for i in range(natoms):
        for j in range(natoms):
            if((np.linalg.norm(posb[i] - (cslbasis[0,:] + posw[j]) ) < olap) and (olapb[i] == 0)):
                olapb[i] = 1
                nolapb = nolapb + 1
    # Now white cell
    nolapw = 0
    for i in range(natoms):
        for j in range(natoms):
            if((np.linalg.norm(posw[i] - (cslbasis[0,:] + posb[j]) ) < olap) and (olapw[i] == 0)):
                olapw[i] = 1
                nolapw = nolapw + 1

    # small cell
    bounds = np.zeros([3], dtype = float)
    for s in range(3):
        bounds[s] = numrepsall[s]*cslbasis[s,s]*alatt
        print bounds[s]

    # bounds supercell
    sc_bounds = np.zeros([3], dtype = float)
    for s in range(3):
        sc_bounds[s] = sc_numrepsall[s]*cslbasis[s,s]*alatt


    n_small = natoms*numrepsall[0]*numrepsall[1]*numrepsall[2]
    n_small_dump = natoms*numrepsall[0]*numrepsall[1]*numrepsall[2]- (nolapb + nolapw)*numrepsall[1]*numrepsall[2]

    #Here we should insert code for GB-creation... for i in range(1,16): etc.
    posbw = np.zeros((sc_par* sc_par * n_small,4), dtype=float)

    counter = 0
    filecount = 1

    #go through all dump files i->y; j->z
    for i in range(sc_par):
        for j in range(sc_par):
            #open file
            fivar = open('dump/dump' + str(filecount) + '.txt', 'r')
            fi = open('dump/dump_unmin.txt','r')
            # There should be n_small atoms in the file
            for t in range(9):
                line = fi.readline()
                line = fivar.readline()

            # get all atom-ids of the phosphorus atoms, save them in phos (dictionary)

            atomt = {}

            #first put iron atoms ('1') on every position:

            for t in range(n_small_dump):
                atomt[t] = '1'

            # search for P atoms in the right region and get the nearest atom in the dump file and give it the atomtype 2


            for t in range(n_small_dump):

                line = fivar.readline()
                words = string.split(line)
                x = float(words[2])
                y = float(words[3])
                z = float(words[4])
                if words[1] == '2' and x>0.25*bounds[0] and x<=0.75*bounds[0]:
                    print words[0]
                    testd = 15.0
                    for s in range(n_small_dump):
                        line = fi.readline()
                        words = string.split(line)
                        dist = ((x-float(words[2]))**2+(y-float(words[3]))**2+(z-float(words[4]))**2)**(0.5)
                        if dist < testd:
                            idd = s
                            testd = dist
                    atomt[idd] = '2'
                    print idd
                    fi.close()
                    fi = open('dump/dump_unmin.txt','r')

                    for s in range(9):
                        line = fi.readline()




            for s in range(n_small_dump):
                line = fi.readline()
                words = string.split(line)
                xpos = float(words[2])

                # 0,1,2 -> x,y,z, 3 = atom type

                if (xpos <= 0.25 * bounds[0]):
                    posbw[counter, 3] = 1
                    posbw[counter,0] = float(words[2])/alatt
                    posbw[counter,1] = float(words[3])/alatt + j * numrepsall[1]*cslbasis[1,1]
                    posbw[counter,2] = float(words[4])/alatt + i * numrepsall[2]*cslbasis[2,2]
                    counter = counter + 1

                elif (xpos <= 0.75 * bounds[0]):
                    posbw[counter, 3] = int(atomt[int(words[0])-1])
                    posbw[counter,0] = float(words[2])/alatt
                    posbw[counter,1] = float(words[3])/alatt + j * numrepsall[1]*cslbasis[1,1]
                    posbw[counter,2] = float(words[4])/alatt + i * numrepsall[2]*cslbasis[2,2]
                    counter = counter + 1
                else:
                    posbw[counter, 3] = 1
                    posbw[counter,0] = float(words[2])/alatt
                    posbw[counter,1] = float(words[3])/alatt + j * numrepsall[1]*cslbasis[1,1]
                    posbw[counter,2] = float(words[4])/alatt + i * numrepsall[2]*cslbasis[2,2]
                    counter = counter + 1

            filecount = filecount + 1
            fi.close()
            fivar.close()



    #our supercell

    n_sc = natoms*sc_bulkrepsall[0]*sc_bulkrepsall[1]*sc_bulkrepsall[2]

    print'Number of atoms:'
    print str(n_sc + sc_par * sc_par * n_small_dump+ sc_numrepsw[1]*sc_numrepsw[2]*nolapw)
    print ''
    print n_small
    print n_small_dump

    fo = open(output_file, 'w')
    fo.write('#Header\n')
    fo.write('\n')
    # n_sc are the white and black atoms // 16 n_small the atoms that come from the gb_files
    #fo.write(str(n_sc/2 + 8* n_small) + ' atoms'+'\n')
    fo.write(str(n_sc + sc_par * sc_par * n_small_dump + sc_numrepsw[1]*sc_numrepsw[2]*nolapw ) + ' atoms'+'\n')
    fo.write('\n')
    fo.write('2 atom types'+'\n')
    fo.write('\n')
    fo.write('0.0 ' + str(sc_numrepsall[0]*cslbasis[0,0]*alatt) + ' xlo xhi' + '\n')
    fo.write('0.0 ' + str(sc_numrepsall[1]*cslbasis[1,1]*alatt) + ' ylo yhi' + '\n')
    fo.write('0.0 ' + str(sc_numrepsall[2]*cslbasis[2,2]*alatt) + ' zlo zhi' + '\n')
    #fo.write(str(numrepsall[]*cslbasis[,]) + ' 0.0 0.0 xy xz yz' + '\n')
    fo.write('\n')
    fo.write('\n')
    fo.write('Atoms\n')
    fo.write('\n')

    count = 1
    olapcount = 0

    counter = 0

    #insert black atoms

    for i in range(sc_numrepsb[0]):
      for j in range(sc_numrepsb[1]):
          for k in range(sc_numrepsb[2]):
              corner = i*cslbasis[0,:] + j*cslbasis[1,:] + k*cslbasis[2,:]
              for s in range(natoms):
                  fo.write(str(count) + ' ' + atomtype + ' ')
                  for t in range(3):
                      fo.write(str((corner[t]+posb[s,t])*alatt) + ' ')
                  fo.write('\n')
                  count = count + 1
                  counter = counter + 1
    print counter, n_sc/2
    counter = 0


    #insert black to white gb

    corner = offsetbw[0]*cslbasis[0,:] + offsetbw[1]*cslbasis[1,:] + offsetbw[2]*cslbasis[2,:]
    for s in range(sc_par* sc_par * n_small_dump):
        fo.write(str(count) + ' ' + str(int(posbw[s,3])) + ' ')
        for t in range(3):
            fo.write(str((corner[t]+posbw[s,t])*alatt) + ' ')
        fo.write('\n')
        count = count + 1
        counter = counter + 1

    #insert atoms which had been removed because of overlapping

    print counter, sc_par * sc_par * n_small_dump
    counter = 0

    i = numrepsall[0]-1

    for j in range(sc_numrepsw[1]):
            for k in range(sc_numrepsw[2]):
                corner = i*cslbasis[0,:] + j*cslbasis[1,:] + k*cslbasis[2,:]
                corner = corner + offsetbw[0]*cslbasis[0,:] + offsetbw[1]*cslbasis[1,:] + offsetbw[2]*cslbasis[2,:]
                for s in range(natoms):
                    if (olapw[s] != 0):
                        fo.write(str(count) + ' ' + atomtype + ' ')
                        for t in range(3):
                            fo.write(str((corner[t]+posw[s,t])*alatt) + ' ')
                        fo.write('\n')
                        count = count + 1
                        counter = counter +1

    print counter, sc_numrepsw[1]*sc_numrepsw[2]*nolapw
    counter = 0


    #insert white atoms
    for i in range(sc_numrepsw[0]):
        for j in range(sc_numrepsw[1]):
            for k in range(sc_numrepsw[2]):
                corner = i*cslbasis[0,:] + j*cslbasis[1,:] + k*cslbasis[2,:]
                corner = corner + offsetw[0]*cslbasis[0,:] + offsetw[1]*cslbasis[1,:] + offsetw[2]*cslbasis[2,:]
                for s in range(natoms):
                    fo.write(str(count) + ' ' + atomtype + ' ')
                    for t in range(3):
                        fo.write(str((corner[t]+posw[s,t])*alatt) + ' ')
                    fo.write('\n')
                    count = count + 1
                    counter = counter +1

    print counter, n_sc/2
    counter = 0



    fo.close()

    print count-1
