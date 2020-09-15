#!/bin/bash
source ./.env
#HOST="api.opengate.es"
HOST="preproapi.opengate.es"
#TOPIC="odm/operationOnDemand/${1}"
TOPIC="odm/iot/${1}"

echo "Host: ${HOST}"
echo "DeviceID: ${1}"
echo "Topic: ${TOPIC}"
echo "Message to publish:"
message_template=`cat ${2}`
message="${message_template/your-device-id/$1}"
echo ${message}

mosquitto_pub \
    -t "${TOPIC}" \
    -u "${1}" \
    -P "${API_KEY}" \
    -h ${HOST} \
    -m "${message}"