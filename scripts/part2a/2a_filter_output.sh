#!/bin/bash

interferences=("none" "cpu" "l1d" "l1i" "l2" "llc" "membw")
jobs=("blackscholes" "canneal" "dedup" "ferret" "freqmine" "radix" "vips")
FILE=meas_real_2a.csv

# remove existing file to avoid appending
if [ -f "$FILE" ]; then
    rm $FILE
    echo deleted previous version of $FILE.
fi


for j in {1..7}; do
    for i in {1..7}; do
        if [ $i -lt 7 ]; then
            cat ${jobs[$j-1]}-${interferences[$i-1]}.txt| grep 'real' | awk '{printf $2 ", "}' >> $FILE
        else
            cat ${jobs[$j-1]}-${interferences[$i-1]}.txt| grep 'real' | awk '{print $2}' >> $FILE
        fi
    done
done
