#!/bin/bash

# USES AS INPUT (have in same folder!): new_logi.txt (i=1,2,3) and new_tailsi.txt (i=1,2,3) and compute_pause.py script
        # ---> new_logi.txt (i=1,2,3)           // logs from task 4
        # ---> new_tailsi.txt (i=1,2,3)         // mcperf output from task 4
        # ---> compute_pause.py script
# OUTPUTS: 
        # ---> log_i_processed.txt (i=1,2,3)
        # ---> pause_logi.txt (i=1,2,3)
        # ---> memcached_jumps_i.txt (i=1,2,3)
        # ---> 4_3_p95_QPS_i.csv (i=1,2,3)


# ------------------------------DATA FROM LOGS (from new_logi.txt)--------------------------------------
read_files=("measurements/4.3_log1.txt" "measurements/4.3_log2.txt" "measurements/4.3_log3.txt")
pause_files=("pause_log1.txt" "pause_log2.txt" "pause_log3.txt")
write_files=("log_1_processed.txt" "log_2_processed.txt" "log_3_processed.txt")


# pausing happens (from controller.py)
cat1=('dedup' 'radix' 'blackscholes')

# no pausing (dedup also has pausing)
cat2=('ferret' 'freqmine' 'canneal' 'vips')

# create txt file ('processed') with COLUMNS: job name, t_start, t_end, t_pause[s] (= 0 for cat2)
for f in {1..3}
do
    # if write_file alreafy exists, delete it
    if [ -f ${write_files[$f-1]} ]
    then
        rm ${write_files[$f-1]}
    fi
    # if pause file already exists, delete it
    if [ -f ${pause_files[$f-1]} ]
    then
        rm ${pause_files[$f-1]}
    fi


    # for cat2
    for i in {1..4}
    do
        printf "${cat2[$i-1]}, " >> ${write_files[$f-1]} 
        grep_start="start ${cat2[$i-1]}"
        grep_end="end ${cat2[$i-1]}"
        cat ${read_files[$f-1]} | grep "$grep_start" | awk -F"T" '{print $2}' | awk -F" " '{printf $1 ", "}' >> ${write_files[$f-1]}
        cat ${read_files[$f-1]} | grep "$grep_end" | awk -F"T" '{print $2}' | awk -F" " '{printf $1 ", "}' >> ${write_files[$f-1]}
        echo "0" >> ${write_files[$f-1]}
    done
    # for cat1
    for i in {1..3}
    do
        # ---> precompute pause time
        echo "${cat1[$i-1]}" >> ${pause_files[$f-1]} 
        grep_pause=" pause ${cat1[$i-1]}"
        grep_unpause="unpause ${cat1[$i-1]}"
        # cat ${read_files[$f-1]} | grep "$grep_pause" | awk -F"T" '{print $2}' | awk -F" " '{printf $1 ", "}' >> ${pause_files[$f-1]}
        pause=$(cat ${read_files[$f-1]} | grep "$grep_pause" | awk -F"T" '{print $2}' | awk -F" " '{printf $1 ", "}')
        unpause=$(cat ${read_files[$f-1]} | grep "$grep_unpause"  | awk -F"T" '{print $2}' | awk -F" " '{printf $1 ", "}')
        echo $pause >> ${pause_files[$f-1]}
        echo $unpause >> ${pause_files[$f-1]}
        printf "$pause \n$unpause" > pauses_job_i.txt
        # use python to compute pause time (s) from data of cat1 i
        total_pause_i=$(python3 compute_pause.py pauses_job_i.txt)


        # ---> write to files
        printf "${cat1[$i-1]}, " >> ${write_files[$f-1]} 
        grep_start="start ${cat1[$i-1]}"
        grep_end="end ${cat1[$i-1]}"
        cat ${read_files[$f-1]} | grep "$grep_start" | awk -F"T" '{print $2}' | awk -F" " '{printf $1 ", "}' >> ${write_files[$f-1]}
        cat ${read_files[$f-1]} | grep "$grep_end" | awk -F"T" '{print $2}' | awk -F" " '{printf $1 ", "}' >> ${write_files[$f-1]}
        echo $total_pause_i >> ${write_files[$f-1]}
    done
    
    echo "done processing log nr. $f"
    # --------------------------> GET MEMCACHED JUMPS IN CORE USAGE <--------------------------------

    memcached_file="memcached_jumps_${f}.txt"
    # timestamps when computed/jumped with 1 core (FIRST LINE OF FILE = 1 core)
    tail -n +3 ${read_files[$f-1]} | grep memcached | grep -v "0,1" | awk -F"T" '{print $2}' | awk -F" " '{printf $1 ", "}' > $memcached_file
    echo " " >> $memcached_file
    # timestamps when jumped from 1 to 2 cores (SECOND LINE OF FILE = 2 cores)
    cat ${read_files[$f-1]} | grep memcached | grep "0,1" | awk -F"T" '{print $2}' | awk -F" " '{printf $1 ", "}' >> $memcached_file
    
done
echo "done processing memcached core jumps."

rm pauses_job_i.txt


#-------------------------------GET MEMCACHED LATENCIES (from new_tailsi.txt)--------------------------------------------
# collect p95 latencies and QPS from mcperf output and store in .csv files
for i in {1..3}
do
    data_file="measurements/4.3_tails${i}.txt"
    csv_filename="4_3_p95_QPS_${i}.csv"

    # alles fiels stored with tabs, not comma separated
    cat $data_file | grep 'read' | awk '{print $13 ", " $17}' > $csv_filename
   
done
echo "done processing latencies and QPS."
