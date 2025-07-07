#!/bin/sh
# Listen for HL7 messages sent to the local port (22010)
while true; do
  nc -l -p 22010
done
