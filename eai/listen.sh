#!/bin/sh
LOGFILE=/app/listen.log
python3 /app/server.py 22010 | tee -a "$LOGFILE"
