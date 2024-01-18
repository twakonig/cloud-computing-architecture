#!/bin/bash
kubectl create -f parsec-ferret.yaml
kubectl create -f parsec-freqmine.yaml
kubectl create -f parsec-canneal.yaml
kubectl create -f parsec-dedup.yaml
kubectl create -f parsec-vips.yaml
kubectl create -f parsec-blackscholes.yaml
kubectl create -f parsec-radix.yaml

kubectl get jobs > check.txt
while grep -R "0/1" check.txt; do
  sleep 5
  kubectl get jobs > check.txt
done

kubectl get pods -o json > results$1.json
python3 ../../get_time.py results$1.json > times$1.txt
