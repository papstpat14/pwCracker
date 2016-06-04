#!/bin/bash

gnome-terminal -e "sh start_default_redis.sh"
cd ..
gnome-terminal -e "python3 init.py"
