import sys
sys.path.append('/mnt/cr01-home01/shared/lammps-30Sep13/python')
from lammps import lammps
import numpy as np
import sys

nvars = 6
if (len(sys.argv) != nvars):
    print " "
    print "Usage: "+str(sys.argv[0])+" input_file temperature chem_pot mc_steps write_period"
    print " "
else:
    input_file = str(sys.argv[1])
    T = float(sys.argv[2])
    mu = float(sys.argv[3])
    steps = int(sys.argv[4])
    period = int(sys.argv[5])
    
    beta = 11605.0/T
    pad = int(np.log10([steps]))+1  # Determines padding of dump file filenames

    np.random.seed(21694) # Initialise seed
    
    # Open logfile
    flog='mc_log.txt'
    f=open(flog,'w')
    f.write('#Timestep'.rjust(16) + 'Energy'.rjust(24) + 'N_defects'.rjust(12) + 'Action'.rjust(8) + 'Init_energy'.rjust(24) + 'Final_energy'.rjust(24) + 'Energy_change'.rjust(24) + 'Boltz_factor'.rjust(24) + 'Random_number'.rjust(24) + 'Trial_action'.rjust(24)  + '\n')
    
    
    lmp = lammps()
    lmp.file(input_file)
    
    natoms = lmp.get_natoms()
    
    #lmp.command("variable mype equal pe")
    #Ef = lmp.extract_variable("mype","all",0)     # Get initial energy
    #lmp.command("variable mype equal thermo_pe")
    lmp.command("minimize 0 0 1000 10000")
    Ef = lmp.extract_compute("thermo_pe",0,0)     # Get initial energy
    ndefects = 0  # Variable to record number of defect atoms added in
    
    for t in range(steps):
        xsave = lmp.gather_atoms("x",1,3)   # obtain a COPY! of atom coords in a ctype array
        atomtype = lmp.extract_atom("type",0)   # POINTER! to vector of atom types
        atomid = lmp.extract_atom("id",0)   # POINTER! to vector of atom IDs
        E0 = Ef     # Initial potential energy
        swapid = np.random.randint(0,natoms)
        targetatom = atomid[swapid]
        # Implement MC move (here a change of atom type)
        if (atomtype[swapid] == 1):
            atomtype[swapid] = 2
            ndefects = ndefects + 1 # Add trial defect to count
            trialaction = 'Atom_' + str(targetatom) + '_1->2'
            actioncode = '1'
        else:
            atomtype[swapid] = 1
            ndefects = ndefects - 1 # Remove trial defect from count
            trialaction = 'Atom_' + str(targetatom) + '_2->1'
            actioncode = '-1'
        # Relax system and extract new energy
        #lmp.command(minimize 1.0e-12 1.0e-14 1000 10000)
        lmp.command("minimize 0 0 1000 10000")
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
                lmp.command('set atom ' + str(targetatom) + ' type 2')
                ndefects = ndefects + 1  # Add back rejected defect removal to count
            else:
                lmp.command('set atom ' + str(targetatom) + ' type 1')
                ndefects = ndefects - 1  # Remove rejected defect from count    
            # Reset atom positions (These were COPIED with gather_Atoms, so must be "scattered" back)
            lmp.scatter_atoms("x",1,3,xsave)
            
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
            atomid = lmp.extract_atom("id",0)  # ditto ids

            f1.write('ITEM: TIMESTEP\n')
            f1.write(str(t) + '\n')
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
            
    f.close()


