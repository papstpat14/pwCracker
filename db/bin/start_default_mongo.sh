#!/bin/bash

screen -d -m ./start_mongo.sh
screen -d -m ./start_dbworker.sh 5
