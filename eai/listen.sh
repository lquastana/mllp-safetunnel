#!/bin/sh
# Listen for HL7 messages sent to the local port (22010)
LOGFILE=/app/listen.log

while true; do
  echo "$(date +'%F %T') Waiting on 22010" | tee -a "$LOGFILE"
  nc -l -p 22010 | tee -a "$LOGFILE"
done
