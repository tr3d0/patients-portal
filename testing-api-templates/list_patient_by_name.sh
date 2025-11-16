#!/bin/bash

if [ -z "$1" ]; then
  echo "Usage: $0 <name-to-search>"
  exit 1
fi

name=$1
curl -X GET "127.0.0.1:5001/patients/search?search_name=$name"