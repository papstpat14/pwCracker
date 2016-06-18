#!/bin/bash

screen -d -m ./start_default_mongo.sh
cd ..
screen -d -m ./init.py
