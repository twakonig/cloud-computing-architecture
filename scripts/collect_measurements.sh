#!/bin/bash
################################################################################
#                        Script for 1st graded project.                        #
#                                                                              #
# Use this script to collect relevant data from ./mcperf output.               #
# Naming convention of output files: meas_p95_QPS_c{CONFIG_NR}_r{RUN_NR}.csv   #
# Example: Output file for config 5, run 2 = meas_p95_QPS_c5_r2.csv            #
#                                                                              #
# Run script with: bash collect_measurements.sh                                #
#                                                                              #
################################################################################
################################################################################
################################################################################


# just for testing purposes
take_measurements="python3 simulate_meas_output.py"

# TODO: fill out configs_list with configuration specific parts of command
configs_list=("config1" "config2" "config3" "config4" "config5" "config6" "config7")

# loop over configurations
for c in {1..7}
do
    # TODO: set 'take_measurements' variable using ${config}
    config=${configs_list[${c}-1]}
    # take_measurements=...

    # loop over runs
    for r in {1..3}
    do
        file_name="meas_p95_QPS_c${c}_r${r}.csv"
        $take_measurements | grep 'read' | awk '{print $13 ", " $17}' > $file_name
        echo "done with config ${c}, run ${r}."
    done
done
echo "completed all measurements."