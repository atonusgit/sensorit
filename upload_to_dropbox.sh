#!/bin/bash

. ~/sensorit/.env

date=$(date '+%y%m%d')
files=$(find $ROOT_DIRECTORY/sensor_logs/$date*)

curl -s -X POST https://api.dropboxapi.com/2/files/delete \
    --header "Authorization: Bearer $DROPBOX_AUTH_TOKEN" \
    --header "Content-Type: application/json" \
    --data "{\"path\": \"/container.tar.gz\"}"

tar -czvf container.tar.gz $files

curl -s -X POST https://content.dropboxapi.com/2/files/upload \
    --header "Authorization: Bearer $DROPBOX_AUTH_TOKEN" \
    --header "Dropbox-API-Arg: {\"path\": \"/container.tar.gz\"}" \
    --header "Content-Type: application/octet-stream" \
    --data-binary @container.tar.gz

rm container.tar.gz
