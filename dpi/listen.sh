#!/bin/sh
LOGFILE=/app/listen.log
python3 /app/server.py 21010 | tee -a "$LOGFILE"
