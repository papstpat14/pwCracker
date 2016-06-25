#!/bin/bash

cd ..
for i in $(seq 1 $1)
do
screen -d -m ./worker.py $2
done
