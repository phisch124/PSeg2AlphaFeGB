#!/bin/bash

dump_array=(dump_000000.txt dump_002000.txt dump_004000.txt
dump_006000.txt
dump_008000.txt
dump_010000.txt
dump_012000.txt
dump_014000.txt
dump_016000.txt
dump_018000.txt
dump_020000.txt
dump_022000.txt
dump_024000.txt
dump_026000.txt
dump_028000.txt
dump_030000.txt
)

mv "${dump_array[0]}" "dump1.txt"
mv "${dump_array[1]}" "dump3.txt"
mv "${dump_array[2]}" "dump5.txt"
mv "${dump_array[3]}" "dump7.txt"
mv "${dump_array[4]}" "dump9.txt"
mv "${dump_array[5]}" "dump11.txt"
mv "${dump_array[6]}" "dump13.txt"
mv "${dump_array[7]}" "dump15.txt"
mv "${dump_array[8]}" "dump2.txt"
mv "${dump_array[9]}" "dump4.txt"
mv "${dump_array[10]}" "dump6.txt"
mv "${dump_array[11]}" "dump8.txt"
mv "${dump_array[12]}" "dump10.txt"
mv "${dump_array[13]}" "dump12.txt"
mv "${dump_array[14]}" "dump14.txt"
mv "${dump_array[15]}" "dump16.txt"



