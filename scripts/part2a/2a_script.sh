#!/bin/bash

interferences=("none" "cpu" "l1d" "l1i" "l2" "llc" "membw")
jobs=("blackscholes" "canneal" "dedup" "ferret" "freqmine" "radix" "vips" "x264")

for j in {1..8}; do
  for i in {1..7}; do
    echo ""
    echo "executing job ${jobs[$j - 1]} with interference ${interferences[$i - 1]}"

    if [ $i != 1 ]; then
      # introduce interference
      kubectl create -f interference/ibench-${interferences[$i - 1]}.yaml

      # wait for interference to start
      > check.txt
      kubectl get pods >> check.txt
      while grep -R "0/1" check.txt; do
        sleep 5
        > check.txt
        kubectl get pods >> check.txt
      done
    fi

    # start job
    kubectl create -f parsec-benchmarks/part2a/parsec-${jobs[$j - 1]}.yaml

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
        >> logs2a/${jobs[$j - 1]}-${interferences[$i - 1]}.txt

    # delete job and pod
    kubectl delete jobs --all
    kubectl delete pods --all

    # sleep before starting next iteration
    sleep 30
  done
done
