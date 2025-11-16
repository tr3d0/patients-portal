#!/bin/bash

# Get the directory where the script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

request_payload_path="$SCRIPT_DIR/payloads/create_patients.json"

payload=$(cat "$request_payload_path")

curl -X POST -H "Content-Type: application/json" -d "$payload" "127.0.0.1:5001/patients"