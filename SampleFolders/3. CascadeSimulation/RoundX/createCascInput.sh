#!/bin/sh


#gb types
gb[1]=S5
x[1]=74; y[1]=102; z[1]=89;

gb[2]=S257
x[2]=97; y[2]=57; z[2]=91;
gb[3]=S41
x[3]=74; y[3]=73; z[3]=73;

# different PKA directions
dir[1]=A
vx[1]=2600.88; vy[1]=109.51; vz[1]=-100;
dir[2]=B
vx[2]=2200.88; vy[2]=1401.11; vz[2]=-300;
dir[3]=C
vx[3]=1800; vy[3]=-1210.11; vz[3]=1010;
dir[4]=D
vx[4]=2445.88; vy[4]=331; vz[4]=-114;
dir[5]=E
vx[5]=2700; vy[5]=-335; vz[5]=567


# supercell and potentials
for i in $(seq 3); do
    for j in $(seq 5); do
    	  echo ${gb[$i]}${dir[$j]}
        mkdir -p csf/${gb[$i]}${dir[$j]}
        cp input/Fe_2.eam.fs csf/${gb[$i]}${dir[$j]}/Fe_2.eam.fs
        cp input/Fe-P.eam.fs csf/${gb[$i]}${dir[$j]}/Fe-P.eam.fs
        cp input/${gb[$i]}/lammps_sc.txt csf/${gb[$i]}${dir[$j]}/lammps_sc.txt
        python code/csf_input_files.py ${gb[$i]}${dir[$j]} ${x[$i]} ${y[$i]} ${z[$i]} ${vx[$j]} ${vy[$j]} ${vz[$j]}
        mv in.sim${gb[$i]}${dir[$j]} csf/${gb[$i]}${dir[$j]}/
        mv ${gb[$i]}${dir[$j]}.qsub csf/${gb[$i]}${dir[$j]}/
    done
done


