#!/bin/bash

. ~/sensorit/.env

createTunnel() {
	kappe_ip=$(curl -u $VALLE_DYNDNS_USERNAME:$VALLE_DYNDNS_PASSWORD http://valle.fi/dyndns/)
	ssh -N -R $REVERSE_SSH_PORT:$REVERSE_SSH_HOSTNAME:$DEFAULT_SSH_PORT $KAPPE_USERNAME@$kappe_ip -p $KAPPE_SSH_PORT -o StrictHostKeyChecking=no
}

while true;
do
/bin/pidof ssh
	if [[ $? -ne 0 ]]; then
		echo Creating new tunnel connection
		createTunnel
	fi
sleep 15
done
