#!/bin/bash

gnome-terminal -e "sh start_default_mongo.sh"
cd ..
gnome-terminal -e "python3 init.py"
