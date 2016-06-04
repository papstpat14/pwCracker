#!/bin/bash

cd ..
for i in $(seq 1 $1)
do
 gnome-terminal -e "python3 ./worker.py $2"
done
