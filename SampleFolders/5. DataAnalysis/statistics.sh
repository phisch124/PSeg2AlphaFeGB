#!/bin/sh


#gb types
gb[1]=S5A
gb[2]=S41A
gb[3]=S257A

#again include as many GBs as you need..

for i in $(seq 3); do
    	echo ${gb[$i]}
      mkdir -p stat

      python code/phos_stats_v4.py input/${gb[$i]}_CMC_500000.cfg ${gb[$i]}_C_500000_stat.txt all_stat.txt
      mv ${gb[$i]}_C_500000_stat.txt stat/${gb[$i]}_C_500000_stat.txt

done


