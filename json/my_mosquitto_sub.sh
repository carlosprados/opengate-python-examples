#!/bin/bash
source ./.env
#HOST="api.opengate.es"
HOST="preproapi.opengate.es"
echo "Host: ${HOST}"
echo "DeviceID: ${1}"
mosquitto_sub \
    -t "odm/request/${1}" \
    -u "${1}" \
    -P "${API_KEY}" \
    -h ${HOST}
