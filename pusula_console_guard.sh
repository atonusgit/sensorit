#!/usr/bin/bash

. ~/sensorit/.env

echo "$$" > $ROOT_DIRECTORY/status_files/pidof_pusula_console

while true;
do
/bin/pidof /usr/local/bin/python3
	if [[ $? -ne 0 ]]; then
		python3 $ROOT_DIRECTORY/pusula_console.py
	fi
sleep 10
done
