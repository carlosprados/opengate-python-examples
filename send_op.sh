#!/bin/bash
API_KEY="b6d8f262-8fe3-4ef5-a1f4-2c3d5c7fa4cc"
curl -X POST \
    -H "Content-Type: application/json" \
    -H "X-ApiKey: ${API_KEY}" \
    -d @SET_DEVICE_PARAMETERS.json \
    https://api.opengate.es:443/north/v80/operation/jobs
