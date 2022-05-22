#!/bin/bash

. ~/sensorit/.env

sunrise=$(date --date=$(cat $ROOT_DIRECTORY/sunrise_sunset_logs/$(date '+%y%m%d')_sunrise_sunset.json | jq -r '.results.sunrise') +"%s")
sunset=$(date --date=$(cat $ROOT_DIRECTORY/sunrise_sunset_logs/$(date '+%y%m%d')_sunrise_sunset.json | jq -r '.results.sunset') +"%s")
now=$(date +"%s")

if [[ $now -gt $sunrise ]]; then
        if [[ $(cat $ROOT_DIRECTORY/status_files/all_status.json | jq -r ".G.status") = "is_read_on" ]]; then
		ssh $PISTORASIAT_USERNAME@$PISTORASIAT_ADDRESS python3 $PISTORASIAT_ROOT_DIRECTORY/remote_control.py G off
        fi
fi

if [[ $now -gt $sunset ]]; then
        if [[ $(cat $ROOT_DIRECTORY/status_files/all_status.json | jq -r ".G.status") = "is_read_off" ]]; then
		ssh $PISTORASIAT_USERNAME@$PISTORASIAT_ADDRESS python3 $PISTORASIAT_ROOT_DIRECTORY/remote_control.py G on
	fi
fi
