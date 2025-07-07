#!/bin/sh
set -e
stunnel /app/stunnel.conf &
python3 /app/server.py 22010 &
wait -n
