#!/bin/bash

interferences=("none" "cpu" "l1d" "l1i" "l2" "llc" "membw")
EXTERNAL_CLIENT_IP=34.159.207.176

for i in {1..7}; do
  if [ $i != 1 ]; then
    echo ""
    echo "start interference ${interferences[$i - 1]}"

    # introduce interference
    kubectl create -f /home/luca/study/FS23/cca/cloud-comp-arch-project/interference/ibench-${interferences[$i - 1]}.yaml

    # wait for interference to start
    kubectl get pods > check.txt
    while grep -R "0/1" check.txt; do
      sleep 5
      kubectl get pods > check.txt
    done
  fi

  # ssh onto client-measure
  gcloud compute ssh --ssh-key-file ~/.ssh/cloud-computing ubuntu@client-measure-hxk9 --zone europe-west3-a << EOF
    cd memcache-perf/
    bash measure.sh
    exit
EOF

  # get results over scp
  for r in {1..3}; do
    scp ubuntu@$EXTERNAL_CLIENT_IP:/home/ubuntu/memcache-perf/meas_p95_QPS_${r}.csv \
        /home/luca/study/FS23/cca/cca_project/results/1/meas_p95_QPS_${interferences[$i - 1]}_${r}.csv
  done

  # kill interference
  if [ $i != 1 ]; then
    kubectl delete pods ibench-${interferences[$i - 1]}
  fi

  sleep 30
done
