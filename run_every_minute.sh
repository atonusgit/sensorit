#!/bin/bash

. ~/sensorit/.env

kappe_ip="$ROOT_DIRECTORY/status_files/kappe_ip"
hostname=$(hostname)

reset_switch=$(ssh $KAPPE_USERNAME@$(cat $kappe_ip) -p $KAPPE_SSH_PORT "cat $KAPPE_ROOT_DIRECTORY/switches/reset_$hostname")
if [[ $reset_switch -eq 1 ]]; then
    ssh $KAPPE_USERNAME@$(cat $kappe_ip) -p $KAPPE_SSH_PORT "echo 2 > $KAPPE_ROOT_DIRECTORY/switches/reset_$hostname"
    killall -9 ssh
    killall -9 bash # notice - script dies here
fi

ssh_tunnel_switch=$(ssh $KAPPE_USERNAME@$(cat $kappe_ip) -p $KAPPE_SSH_PORT "cat $KAPPE_ROOT_DIRECTORY/switches/ssh_tunnel_$hostname")
if [[ $ssh_tunnel_switch -eq 1 ]]; then
    echo $ssh_tunnel_switch
    ssh $KAPPE_USERNAME@$(cat $kappe_ip) -p $KAPPE_SSH_PORT "echo 2 > $KAPPE_ROOT_DIRECTORY/switches/ssh_tunnel_$hostname"
    killall -9 ssh
    /usr/bin/bash $ROOT_DIRECTORY/ssh_tunnel.sh
fi

reboot_switch=$(curl http://valle.fi/reboot_switch.php)
if [[ $reboot_switch -eq 1 ]]; then
    curl http://valle.fi/reboot_switch.php?set=2
    sudo reboot
fi
