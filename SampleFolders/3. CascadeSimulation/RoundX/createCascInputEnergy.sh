#!/bin/sh


#gb types
gb[1]=S5
x[1]=74; y[1]=102; z[1]=89;

gb[2]=S257
x[2]=97; y[2]=57; z[2]=91;
gb[3]=S41
x[3]=74; y[3]=73; z[3]=73;

# Energies
ener[1]=E1
vx[1]=1312.3; vy[1]=55.3; vz[1]=-55.5;
ener[2]=E2
vx[2]=1855.8; vy[2]=78.1; vz[2]=-71.4;
ener[3]=E3
vx[3]=2272.9; vy[3]=95.7; vz[3]=-87.4;
ener[4]=E4
vx[4]=2624.5; vy[4]=110.5; vz[4]=-100.9;
ener[5]=E5
vx[5]=2934.3; vy[5]=123.5; vz[5]=-112.8;
ener[6]=E6
vx[6]=3214.4; vy[6]=135.3; vz[6]=-123.6;


# supercell and potentials
for i in $(seq 3); do
    for j in $(seq 6); do
    	echo ${gb[$i]}${ener[$j]}
        mkdir -p csf/${gb[$i]}${ener[$j]}
        cp input/Fe_2.eam.fs csf/${gb[$i]}${ener[$j]}/Fe_2.eam.fs
        cp input/Fe-P.eam.fs csf/${gb[$i]}${ener[$j]}/Fe-P.eam.fs
        cp input/${gb[$i]}/lammps_sc.txt csf/${gb[$i]}${ener[$j]}/lammps_sc.txt
        python code/csf_input_files_energy.py ${gb[$i]}${ener[$j]} ${x[$i]} ${y[$i]} ${z[$i]} ${vx[$j]} ${vy[$j]} ${vz[$j]}
        mv in.sim${gb[$i]}${ener[$j]} csf/${gb[$i]}${ener[$j]}/
        mv ${gb[$i]}${ener[$j]}.qsub csf/${gb[$i]}${ener[$j]}/
    done
done


