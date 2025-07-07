#!/bin/sh
FILE=${1:-/app/message.hl7}
LOGFILE=/app/send.log

if [ ! -f "$FILE" ]; then
  echo "Message file $FILE not found" >&2
  exit 1
fi

python3 /app/client.py 127.0.0.1 22010 "$FILE" | tee -a "$LOGFILE"
