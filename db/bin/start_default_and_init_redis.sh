#!/bin/bash

screen -d -m ./start_default_redis.sh
cd ..
screen -d -m ./init.py
