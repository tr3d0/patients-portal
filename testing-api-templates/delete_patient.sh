#!/bin/bash

if [ -z "$1" ]; then
  echo "Usage: $0 <patient-id>"
  exit 1
fi

id=$1
curl -X DELETE "127.0.0.1:5001/patients/$id"