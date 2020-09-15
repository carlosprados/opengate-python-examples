#!/bin/bash
source ./.env
curl -X POST \
    -H "Content-Type: application/json" \
    -H "X-ApiKey: ${API_KEY}" \
    -d @SET_DEVICE_PARAMETERS.json \
    https://api.opengate.es:443/north/v80/operation/jobs
