#!/bin/sh
set -e
stunnel /app/stunnel.conf 2>&1 | tee -a /app/stunnel.log &
python3 /app/server.py 21010 | tee -a /app/server.log &
sleep infinity
