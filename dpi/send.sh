#!/bin/sh
# Send an HL7 message to the local Stunnel port (22010)
FILE=${1:-/app/message.hl7}
LOGFILE=/app/send.log

if [ ! -f "$FILE" ]; then
  echo "Message file $FILE not found" >&2
  exit 1
fi

echo "$(date +'%F %T') Sending $FILE" | tee -a "$LOGFILE"
nc 127.0.0.1 22010 < "$FILE"
