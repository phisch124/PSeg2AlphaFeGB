import sys
sys.path.append('/mnt/cr01-home01/shared/lammps-30Sep13/python')
from lammps import lammps
import numpy as np
import sys

nvars = 4
if (len(sys.argv) != nvars):
    print " "
    print "Usage: "+str(sys.argv[0])+" input_file mc_steps write_period"
    print " "
else:
    input_file = str(sys.argv[1])

    steps = int(sys.argv[2])
    period = int(sys.argv[3])

    T = 600.0

    beta = 11605.0/T
    pad = int(np.log10([steps]))+1  # Determines padding of dump file filenames

    np.random.seed(21694) # Initialise seed

    # Open logfile
    flog='mc_log.txt'
    f=open(flog,'w')
    f.write('#Timestep'.rjust(16) + 'Energy'.rjust(24)  + 'Action'.rjust(8) + 'Init_energy'.rjust(24) + 'Final_energy'.rjust(24) + 'Energy_change'.rjust(24) + 'Boltz_factor'.rjust(24) + 'Random_number'.rjust(24)  + '\n')

    lmp = lammps()
    lmp.file(input_file)

    # Relaxation
    #lmp.command("minimize 0 0 10 10") # test minimisation
    lmp.command("minimize 0 0 1000 10000")

    xlo = lmp.extract_global("boxxlo",1)
    xhi = lmp.extract_global("boxxhi",1)
    ylo = lmp.extract_global("boxylo",1)
    yhi = lmp.extract_global("boxyhi",1)
    zlo = lmp.extract_global("boxzlo",1)
    zhi = lmp.extract_global("boxzhi",1)

    xmid = (xlo + xhi)/2
    ymid = (ylo + yhi)/2
    zmid = (zlo + zhi)/2

    print xmid, ymid, zmid

    reg1 = 100.0
    reg2 = 90.0
    reg3 = 70.0

    #shrinkfactor for y and z side of box - accelerate the simulation
    sf1 = 80.0/100.0
    sf2 = 70.0/90.0
    sf3 = 50.0/70.0

    print sf1, sf2, sf3

    #make simulating box smaller, delete unwanted atoms.
    lmp.command("region del block " + str(xmid-reg1/2) + " " + str(xmid+reg1/2) + " " + str(ymid-reg1/2*sf1) + " " + str(ymid+reg1/2*sf1) + " " + str(zmid-reg1/2*sf1) + " " + str(zmid+reg1/2*sf1) + " side out")
    lmp.command("delete_atoms region del")

    natoms = lmp.get_natoms()


    # write lammps input file

    fdump='lmp_smallcell.txt'

    f1=open(fdump,'w')
    x = lmp.extract_atom("x",3)   # obtain a POINTER! to atom coords
    atomtype = lmp.extract_atom("type",0)  # we already have atom types
    atomid = lmp.extract_atom("id",0)  # ditto ids

    f1.write('#Header\n\n')
    f1.write(str(natoms) + ' atoms\n\n')
    f1.write('2 atom types \n\n')
    f1.write(str(0.0) + ' ' + str(reg1)  + ' xlo xhi\n')
    f1.write(str(0.0) + ' ' + str(reg1*sf1)  + ' ylo yhi\n')
    f1.write(str(0.0) + ' ' + str(reg1*sf1)  + ' zlo zhi\n\n\n')
    f1.write('Atoms\n\n')

    for s in range(natoms):
        # move the box to have the corner at 0 0 0.
        f1.write(str(atomid[s]) + ' ' + str(atomtype[s]) + ' ' + str(x[s][0]-(xmid-reg1/2)) + ' ' + str(x[s][1]-(ymid-reg1/2*sf1)) + ' ' + str(x[s][2]-(zmid-reg1/2*sf1)) + '\n')
    f1.close()

    lmp.close()

    #works perfectly until here see smallcell.cfg

    lmp = lammps()

    lmp.file("in.smallcell")

    xlo = lmp.extract_global("boxxlo",1)
    xhi = lmp.extract_global("boxxhi",1)
    ylo = lmp.extract_global("boxylo",1)
    yhi = lmp.extract_global("boxyhi",1)
    zlo = lmp.extract_global("boxzlo",1)
    zhi = lmp.extract_global("boxzhi",1)

    xmid = (xlo + xhi)/2
    ymid = (ylo + yhi)/2
    zmid = (zlo + zhi)/2

    #outer atoms force = 0
    #check1.cfg - ok

    #fdump='check2.txt'

    #check 2 - ok

    lmp.command("region outer block " + str(xmid-reg2/2) + " " + str(xmid+reg2/2) + " " + str(ymid-reg2/2*sf2) + " " + str(ymid+reg2/2*sf2) + " " + str(zmid-reg2/2*sf2) + " " + str(zmid+reg2/2*sf2) + " side out")
    lmp.command("group force0 region outer")
    lmp.command("fix 1 force0 setforce 0.0 0.0 0.0")


    #fdump='check3.txt'

    #check 3 - ok

    #fdump='check4.txt'

    # check4 - ok

    # Build a MC Simulation.

    #lmp.command("minimize 0 0 10 10") # test
    lmp.command("minimize 0 0 100 1000")


    Ef = lmp.extract_compute("thermo_pe",0,0)


    for t in range(steps):

        xsave = lmp.gather_atoms("x",1,3)   # obtain a COPY! of atom coords in a ctype array
        typesave = lmp.gather_atoms("type",0,1)
        idsave = lmp.gather_atoms("id",0,1)

        atomtype = lmp.extract_atom("type",0)
        x = lmp.extract_atom("x",3)   # obtain a POINTER! to atom coords
        atomid = lmp.extract_atom("id",0)

        pcounter = 0
        fecounter = 0
        r3counter = 0
        patoms = []
        featoms = []
        region3 = []

        for i in range(natoms):
            # check if atom is in region 3
            if abs(x[atomid[i]][0]-xmid) <= reg3/2 and abs(x[atomid[i]][1]-ymid) <= reg3/2*sf3 and abs(x[atomid[i]][2]-zmid) <= reg3/2*sf3:

                region3.append(atomid[i])
                r3counter = r3counter + 1

                #if (type_atoms[i-1] == 2):
                if atomtype[atomid[i]] == 2:
                    pcounter = pcounter + 1
                    patoms.append(atomid[i])
                else:
                    fecounter = fecounter + 1
                    featoms.append(atomid[i])
        print r3counter, pcounter, fecounter

        # Directly a lammps input file..
        if (t%period == 0):
            # Open dumpfile
            fdump= 'lammpsdump_'+ str(t).rjust(pad, '0') +'.txt'
            f1=open(fdump,'w')
            x = lmp.extract_atom("x",3)   # obtain a POINTER! to atom coords
            atomtype = lmp.extract_atom("type",0)  # we already have atom types
            atomid = lmp.extract_atom("id",0)  # ditto ids

            #lmp.command("compute pote all pe/atom")
            #pote = lmp.extract_compute("pote",1,1)

            f1.write('#Header\n\n')
            f1.write(str(r3counter) + ' atoms\n\n')
            f1.write('2 atom types \n\n')
            f1.write(str(0.0) + ' ' + str(reg1)  + ' xlo xhi\n')
            f1.write(str(0.0) + ' ' + str(reg1*sf1)  + ' ylo yhi\n')
            f1.write(str(0.0) + ' ' + str(reg1*sf1)  + ' zlo zhi\n\n\n')
            f1.write('Atoms\n\n')

            for s in range(r3counter):
                f1.write(str(s+1) + ' ' + str(atomtype[region3[s]]) + ' ' + str(x[region3[s]][0]) + ' ' + str(x[region3[s]][1]) + ' ' + str(x[region3[s]][2]) +'\n')
            f1.close()

        E0 = Ef     # Initial potential energy

        pswapnr = np.random.randint(0,pcounter) #randomly choose a P atom
        ptarget= patoms[pswapnr] #get id
        atomtype[ptarget] = 1 #change type

        #neighbouring - restrict the swap to a radius around the P atom, 0 => swap in whole region 3
        neigh_r = 20 # in A
        ncounter = 0
        neigh = []

        if neigh_r > 0:
            for i in range(r3counter):
                r = ((x[region3[i]][0] - x[ptarget][0])**2 + (x[region3[i]][1] - x[ptarget][1])**2 + (x[region3[i]][2] - x[ptarget][2])**2)**(0.5)
                if r <= neigh_r and atomtype[region3[i]]==1:
                    neigh.append(region3[i])
                    ncounter = ncounter + 1

            feswapnr = np.random.randint(0,ncounter) #randomly choose a Fe atom
            fetarget = neigh[feswapnr] # get id

        else:
            feswapnr = np.random.randint(0,fecounter) #randomly choose a Fe atom
            fetarget = featoms[feswapnr] # get id

        atomtype[fetarget] = 2 #change type


        #Relax system
        lmp.command("minimize 1.0e-4 1.0e-6 100 1000")

        E1 = lmp.extract_compute("thermo_pe",0,0) # Final potential energy
        # amount of p and fe atoms stays constant -> take away mu
        boltz = np.exp( -beta*(E1-E0) )
        prob = np.random.random()

        if boltz >= 1.0 or boltz > prob:  # Accept move?
            action = 'Swap'
            print ' Swap '
            Ef = E1 # Record final energy
        else:
            action = 'None'
            print ' None '
            Ef = E0 # Record final energy
            # Reset atom positions and types(These were COPIED with gather_Atoms, so must be "scattered" back)
            lmp.scatter_atoms("x",1,3,xsave)
            lmp.scatter_atoms("type",0,1,typesave)

        # Write MC history
        f.write(str(t).rjust(16) + str(Ef).rjust(24) + action.rjust(8) + str(E0).rjust(24) + str(E1).rjust(24) + str(E1-E0).rjust(24) + str(boltz).rjust(24) + str(prob).rjust(24) + '\n')
        f.flush()

    f.close()

    fdump= 'endlammps_'+ str(t).rjust(pad, '0') +'.txt'
    f1=open(fdump,'w')
    x = lmp.extract_atom("x",3)   # obtain a POINTER! to atom coords
    atomtype = lmp.extract_atom("type",0)  # we already have atom types
    atomid = lmp.extract_atom("id",0)  # ditto ids

    #lmp.command("compute pote all pe/atom")
    #pote = lmp.extract_compute("pote",1,1)

    f1.write('#Header\n\n')
    f1.write(str(natoms) + ' atoms\n\n')
    f1.write('2 atom types \n\n')
    f1.write(str(0.0) + ' ' + str(reg1)  + ' xlo xhi\n')
    f1.write(str(0.0) + ' ' + str(reg1*sf1)  + ' ylo yhi\n')
    f1.write(str(0.0) + ' ' + str(reg1*sf1)  + ' zlo zhi\n\n\n')
    f1.write('Atoms\n\n')

    for s in range(natoms):
        f1.write(str(s+1) + ' ' + str(atomtype[s]) + ' ' + str(x[s][0]) + ' ' + str(x[s][1]) + ' ' + str(x[s][2]) +'\n')
    f1.close()




