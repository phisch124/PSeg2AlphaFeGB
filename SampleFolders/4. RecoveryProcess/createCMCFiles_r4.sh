#!/bin/sh

#for this github example one of gb of each type has been included, but the code can be arbitrarily extended
#gb types
#gb[2]=S5A
gb[1]=S41A
#gb[3]=S257A


# include as many other GBs as you want, change the number in the for loop accordingly. -> $(seq X);
#gb[4]=S5B
#gb[5]=S5C

# ...

# supercell and potentials
for i in $(seq 1); do
    	echo ${gb[$i]}
        mkdir -p csf/${gb[$i]}
        cp input/Fe-P.eam.fs csf/${gb[$i]}/Fe-P.eam.fs
        cp input/canonical.py csf/${gb[$i]}/canonical.py
        cp input/in.base csf/${gb[$i]}/in.base
        cp input/in.smallcell csf/${gb[$i]}/in.smallcell
        cp input/qsub.txt csf/${gb[$i]}/${gb[$i]}_CMC.qsub
        python code/dump2lammps.py input/dump/dump_${gb[$i]}.250000.txt lammps_in.txt
        mv lammps_in.txt csf/${gb[$i]}/
done


