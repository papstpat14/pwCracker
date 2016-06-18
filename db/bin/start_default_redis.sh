#!/bin/bash

screen -d -m ./start_redis.sh
screen -d -m ./start_dbworker.sh 5
