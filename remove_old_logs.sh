#!/bin/bash

. ~/sensorit/.env

sudo find $ROOT_DIRECTORY/sensor_logs/ -mtime +14 -name "*.json" -type f -exec rm -f {} \;
