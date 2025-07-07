#!/bin/sh
# Send an HL7 message to the local Stunnel port (21010)
FILE=${1:-/app/message.hl7}
if [ ! -f "$FILE" ]; then
  echo "Message file $FILE not found" >&2
  exit 1
fi
nc 127.0.0.1 21010 < "$FILE"
