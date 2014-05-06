PSeg2AlphaFeGB
==============

Irradiation induced embrittlement of reactor presssure vessel steels - exploring the effect of irradiation on the phosphorus segregation to grain boundaries in alpha iron. Using LAMMPS and python scripts.

----------------------------------------------------------------------------------------------

Python, bash, LAMMPS, atomeye, gnuplot

----------------------------------------------------------------------------------------------

The scripts found is this repository have been used within the scope of a dissertation project in the School of Materials at the University of Manchester. The aim is to provide students that would like to do collision cascade simulations a base to start with.

The repository has three main categories:

- InputFiles: One folder per grain boundary, each containing different files with information on the atom coordinates of the respective GB. Because it is just a lot of data, it could have been better to put it in a dropbox.

- SampelFolders: Examples of the simulations of the different stages of the project. Often the bash script should be run first to create the folder that then can be put on the csf to run the simulation. They can easily be adapted to create a larger amount of simulations at once.
Input: Files which are simply copied from the bash script into the csf folders. Code: python scripts executed by the bash script

- OtherScripts: Other scripts used during the project, which did not find a place in the sample folders.


----------------------------------------------------------------------------------------------

1. GBPopulation

2. BuildingSupercells

3. CascadeSimulation

4. RecoveryProcess

5. DataAnalysis


----------------------------------------------------------------------------------------------

Below several scripts are explained in more details. If you would like to have additonal information, feel free to write me an email.

----------------------------------------------------------------------------------------------

create_supercell_v2.py


Needs as input

- csl_black.txt
- csl_white.txt
- dump/dump_unmin.txt
- dump/dump*.txt; 4 prepopulated dump files if 2x2 supercell, 16 if 4x4

Create a supercell made of i x i prepopulated grain boundaries and bulk bcc iron around.

----------------------------------------------------------------------------------------------

rec_GCMC_v2.py

The grand canonical monte carlo used for the long timescale recovery process. Badly chosen boundary conditions, to be modified before usage.

----------------------------------------------------------------------------------------------

meandefectnumber.py

Takes an mc_log.txt file as input and calculates the mean defect (P atom) number after a certain timestep. Used to get the average stable concentration.

----------------------------------------------------------------------------------------------

create_supercellS257_v2.py

Slightly modified version of the create_supercell_v2.py. Because the grain boundary input cell of the S257 was elongated and the script to build the supercell depending on the size of those, a shrink was used to decrease the length of the cell in x direction.

----------------------------------------------------------------------------------------------

mclog2totallog.py

Takes as an input several mc_log files and combines them to have the full defect/timestep evolution of a grand canonical monte carlo simulation. It was used to create some graphs for the dissertation.

----------------------------------------------------------------------------------------------

Unminimised dump

To create supercells an unminimised dump file is needed, they are found in the InputFiles and were created by using:

- lammps2unmindump.py
- in.base
- Fe-P.eam.fs
- lammps.txt

python lammps2unmindump.py in.base

In case you get:
ERROR: Incorrect args for pair coefficients (pair_eam_fs.cpp:51)
Change the number of atom types in the lammps.txt to 2. (line 5)


----------------------------------------------------------------------------------------------

Dumb_renamer.sh

Renames dumb files from dumb_000000 to dumb_030000 to dumb1.txt to dumb16.txt for building supercells.

1 2 3 4					dumpfile		0' 16' 2' 18'
5 6 7 8						<==				4' 20' 6' 22'
9 10 11 12			in 1000			8' 24' 10' 26'
13 14 15 16									12' 28' 14' 30'

All dumbfiles touching have at least 4000 time steps different.


----------------------------------------------------------------------------------------------

Visualisation of P atoms in a dump file using gnuplot:

gnuplot> splot "< awk '($2==2){print}' dump_004000.txt" u 3:4:5 w p pt 7 ps 2
