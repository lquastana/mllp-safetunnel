#!/bin/sh
FILE=${1:-/app/message.hl7}
while true; do
  /app/send.sh "$FILE"
  sleep 20
done
