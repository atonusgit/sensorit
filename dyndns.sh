#!/bin/bash

. ~/sensorit/.env

curl -u $VALLE_DYNDNS_USERNAME:$VALLE_DYNDNS_PASSWORD http://valle.fi/dyndns/ > ~/sensorit/status_files/kappe_ip
