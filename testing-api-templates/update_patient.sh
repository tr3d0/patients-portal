#!/bin/bash

if [ -z "$1" ]; then
  echo "Usage: $0 <patient-id>"
  exit 1
fi

# Get the directory where the script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

request_payload_path="$SCRIPT_DIR/payloads/update_patient.json"

payload=$(cat "$request_payload_path")
id=$1

curl -X PUT -H "Content-Type: application/json" -d "$payload" "127.0.0.1:5001/patients/$id"