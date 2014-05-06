import sys
sys.path.append('/mnt/cr01-home01/shared/lammps-30Sep13/python')
from lammps import lammps
import numpy as np
import sys

nvars = 3
if (len(sys.argv) != nvars):
    print " "
    print "Usage: "+str(sys.argv[0])+" mc_steps write_period"
    print " "
else:
    T = 600.0
    mu = 2.175
    steps = int(sys.argv[1])
    period = int(sys.argv[2])

    beta = 11605.0/T
    pad = int(np.log10([steps]))+1  # Determines padding of dump file filenames

    np.random.seed(21694) # Initialise seed

    reg1 = 100.0
    reg2 = 60.0
    reg3 = 40.0

    #shrinkfactor for y and z side of box - accelerate the simulation
    sf1 = 80.0/100.0
    sf2 = 70.0/90.0
    sf3 = 50.0/70.0

    # Open logfile
    flog='mc_log.txt'
    f=open(flog,'w')
    f.write('#Timestep'.rjust(16) + 'Energy'.rjust(24) + 'N_defects'.rjust(12) + 'Action'.rjust(8) + 'Init_energy'.rjust(24) + 'Final_energy'.rjust(24) + 'Energy_change'.rjust(24) + 'Boltz_factor'.rjust(24) + 'Random_number'.rjust(24) + 'Trial_action'.rjust(24)  + '\n')


    lmp = lammps()
    lmp.file("in.smallcellGCMC")

    xlo = lmp.extract_global("boxxlo",1)
    xhi = lmp.extract_global("boxxhi",1)
    ylo = lmp.extract_global("boxylo",1)
    yhi = lmp.extract_global("boxyhi",1)
    zlo = lmp.extract_global("boxzlo",1)
    zhi = lmp.extract_global("boxzhi",1)

    xmid = (xlo + xhi)/2
    ymid = (ylo + yhi)/2
    zmid = (zlo + zhi)/2

    lmp.command("region outer block " + str(xmid-reg2/2) + " " + str(xmid+reg2/2) + " " + str(ymid-reg2/2*sf2) + " " + str(ymid+reg2/2*sf2) + " " + str(zmid-reg2/2*sf2) + " " + str(zmid+reg2/2*sf2) + " side out")
    lmp.command("group force0 region outer")
    lmp.command("fix 1 force0 setforce 0.0 0.0 0.0")

    natoms = lmp.get_natoms()

    #lmp.command("variable mype equal pe")
    #Ef = lmp.extract_variable("mype","all",0)     # Get initial energy
    #lmp.command("variable mype equal thermo_pe")
    #lmp.command("minimize 0 0 1000 10000")
    lmp.command("minimize 0 0 10 10") #test
    Ef = lmp.extract_compute("thermo_pe",0,0)     # Get initial energy
    ndefects = 0  # Variable to record number of defect atoms added in

    for t in range(steps):
        xsave = lmp.gather_atoms("x",1,3)   # obtain a COPY! of atom coords in a ctype array
        typesave = lmp.gather_atoms("type",0,1)
        idsave = lmp.gather_atoms("id",0,1)

        atomtype = lmp.extract_atom("type",0)
        x = lmp.extract_atom("x",3)   # obtain a POINTER! to atom coords
        atomid = lmp.extract_atom("id",0)

        E0 = Ef     # Initial potential energy

        r3counter = 0
        region3 = []


        for i in range(natoms):
            # check if atom is in region 3

            if (abs(x[i][0]-xmid) <= reg3/2) and (abs(x[i][1]-ymid) <= reg3/2*sf3) and (abs(x[i][2]-zmid) <= reg3/2*sf3):
                region3.append(i)
                r3counter = r3counter + 1


        swapid = np.random.randint(0,r3counter)
        targetatom = region3[swapid]
        # Implement MC move (here a change of atom type)
        if (atomtype[region3[swapid]] == 1):
            atomtype[region3[swapid]] = 2
            ndefects = ndefects + 1 # Add trial defect to count
            trialaction = 'Atom_' + str(targetatom) + '_1->2'
            actioncode = '1'
        else:
            atomtype[region3[swapid]] = 1
            ndefects = ndefects - 1 # Remove trial defect from count
            trialaction = 'Atom_' + str(targetatom) + '_2->1'
            actioncode = '-1'
        # Relax system and extract new energy
        #lmp.command(minimize 1.0e-12 1.0e-14 1000 10000)
        #lmp.command("minimize 0 0 100 1000")
        #lmp.command("minimize 1.0e-4 1.0e-6 100 1000")
        lmp.command("minimize 0 0 10 10") #test
        #E1 = lmp.extract_variable("mype","all",0) # Final potential energy
        E1 = lmp.extract_compute("thermo_pe",0,0) # Final potential energy
        boltz = np.exp( -beta*(E1-E0-mu) )
        prob = np.random.random()
        if ((boltz >= 1.0) or (boltz > prob)):  # Accept move?
            action = 'Swap'
            Ef = E1 # Record final energy
        else:
            action = 'None'
            Ef = E0 # Record final energy
            # Swap atom type back to original
            if (actioncode == -1):
                ndefects = ndefects + 1  # Add back rejected defect removal to count
            else:
                ndefects = ndefects - 1  # Remove rejected defect from count
            # Reset atom positions (These were COPIED with gather_Atoms, so must be "scattered" back)
            lmp.scatter_atoms("x",1,3,xsave)
            lmp.scatter_atoms("type",0,1,typesave)

        # Write MC history
        f.write(str(t).rjust(16) + str(Ef).rjust(24) + str(ndefects).rjust(12) + action.rjust(8) + str(E0).rjust(24) + str(E1).rjust(24) + str(E1-E0).rjust(24) + str(boltz).rjust(24) + str(prob).rjust(24) + trialaction.rjust(24) + '\n')
        f.flush()

        # Also write a dump file? I'm writing this in a lammps dump style so that my conversion scripts can be used
        if (t%period == 0):
            # Open dumpfile
            fdump='dump_'+ str(t).rjust(pad, '0') +'.txt'
            f1=open(fdump,'w')
            x = lmp.extract_atom("x",3)   # obtain a POINTER! to atom coords
            #atomtype = lmp.extract_atom("type",0)  # we already have atom types
            atomtype = lmp.extract_atom("type",0) # ditto ids

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

    f.close()

    fdump= 'endlmpGCMC_'+ str(t).rjust(pad, '0') +'.txt'
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


