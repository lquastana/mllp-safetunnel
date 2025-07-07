#!/bin/sh
# Listen for HL7 messages sent to the local port (21010)
while true; do
  nc -l -p 21010
done
