#!/bin/bash

gnome-terminal -e "sh start_redis.sh"
sh start_dbworker.sh 5
