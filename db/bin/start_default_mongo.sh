#!/bin/bash

gnome-terminal -e "sh start_mongo.sh"
sh start_dbworker.sh 5
