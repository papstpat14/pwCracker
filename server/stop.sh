#!/bin/bash
PROCESS="SCREEN -d -m npm start"
PIDS=`ps ax | grep "$PROCESS" | grep -o '^[ ]*[0-9]*'`
if [ -z "$PIDS" ]; then
	echo "Process not running."
	exit 1
else
	
	for PID in $PIDS; do
		echo "Stopping Server..."		
		kill $PID
		echo "Done."
		exit 0
	done
fi
