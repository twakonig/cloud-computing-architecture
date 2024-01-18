#!/bin/bash

jobs=("blackscholes" "canneal" "dedup" "ferret" "freqmine" "radix" "vips" "x264")
threads=(1 2 4 8)

for j in {1..8}; do
  for t in {1..4}; do
    echo ""
    echo "executing job ${jobs[$j - 1]} with ${threads[$t - 1]} threads"

    # start job
    kubectl create -f parsec-benchmarks/part2b/parsec-${jobs[$j - 1]}-${threads[$t - 1]}.yaml

    # wait for job to finish
    > check.txt
    kubectl get jobs >> check.txt
    while grep -R "0/1" check.txt; do
      sleep 10
      > check.txt
      kubectl get jobs >> check.txt
    done

    # store log
    kubectl logs $(kubectl get pods --selector=job-name=parsec-${jobs[$j - 1]} \
        --output=jsonpath='{.items[*].metadata.name}') \
        >> logs2b/${jobs[$j - 1]}-${threads[$t - 1]}.txt

    # delete job and pod
    kubectl delete jobs --all

    # sleep before starting next iteration
    sleep 30
  done
done
