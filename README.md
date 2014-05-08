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

Before starting:


1. Download Python - https://www.python.org/downloads/
Python 2 has been used during the project.

2. Build lammps - http://lammps.sandia.gov/download.html

If there is any problem, try to google it first.

For the visualisation

Atomeye - http://li.mit.edu/Archive/Graphics/A/#download

Gnuplot - http://www.gnuplot.info


It is very handy to have access to a computer cluster and not to have to run the simulations locally.

At the University of Manchester for example it would be the Computational Shared Facility, short csf.

----------------------------------------------------------------------------------------------

The 5 main steps:

/SampleFolders

----------------------------------------------------------------------------------------------

/1. GBPopulation

The grain boudaries found in the inputfiles were populated with phosphorus atoms using a Grand Canonical Monte Carlo simulation.

/S41
- grand_canonical.py, runs the GCMC simulation using lammps ,for N time steps dumping an image of the cell every D time steps
- Fe-P.eam.fs, interatomic potential, http://www.ctcms.nist.gov/potentials/Fe-P.html
- lammps_in.txt, contains all atom information (position, type) of the S41 grain boundary
- in.base, lammps input file, read by the python script
- S41-Twist.qsub, used to add it to the CSF queue, alternatively line 9 (sample usage) could be run in the terminal (makes no sense to run it locally, as it takes weeks to populate a cell)

----------------------------------------------------------------------------------------------

2. BuildingSupercells

Before simulation cascade could be run, bigger computational cells were needed. Again the S41 is used as example.

/S41-Twist_4x4
- create_supercell_v2.py, takes all the other files in the folder and builds a supercell. The supercell parameter (line 33: sc_par = 4) defines how big the cell will be.
It takes an amount of sc_par x sc_par GB files as input.
- csl_black.txt
- csl_white.txt
- dump/dump_unmin.txt
- dump/dump*.txt; 4 prepopulated dump files if 2x2 supercell, 16 if 4x4


|		csl_black		|		GB 4x4		|		csl_white 	|

----------------------------------------------------------------------------------------------

/3. CascadeSimulation

This folder does not contain directly an input folder for a cascade simulation, it first has to be created by running one of the bash scripts:

/RoundX
bash createCascInput.sh, creates 15 different cascade folders at ones
or
bash createCascInputEnergy.sh, creates 18 different cascade folders at ones

Take those scripts as example how to use bash scripts to generate a whole folder structure using one terminal command. It will safe you a lot of time.

A typical cascade folder looks like following:

/S41A
- S41A.qsub, to submit it to the queue, because no python script is used, the simulations are run in parallel
- in.simS41A, lammps input file, contains all lammps commands
- Fe_2.eam.fs and Fe-P.eam.fs, interatomic potentials, combinded because the Fe-P.eam.fs doesn't support short atomic distances
- lammps_sc.txt, atom data of the supercell

----------------------------------------------------------------------------------------------

4. RecoveryProcess

After the cascade a short and a long timescale segregation process were planned. The canonical.py has a bug and should be modified before usage.
Again same principle as with the cascade simulations, the bash script has to be run to create csf input folders.

Sample csf input folder:

- canonical.py, runs the CMC simulation, be careful few P atoms change their type to Fe during the simulation, boundary condition should be improved
- Fe-P.eam.fs, interatomic potential
- in.base
- in.smallcell
- lammmps_in.txt
_ S41A_CMC.qsub


----------------------------------------------------------------------------------------------

5. DataAnalysis

Running the bash scripts, the input file are analysed and a file containing

'Name mean standard_deviation m3 m4 skewness kurtosis'

of the grain boundaries using the x-coordinate of the P atoms will be created.
In addition, the total number of P atoms is printed.

----------------------------------------------------------------------------------------------

Below the other scripts are explained in more details. If you would like to have additonal information, feel free to write me an email.

/OtherScripts

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
