#!/bin/bash
# ai has no clue what its doing. im on my own

LOGFILE="/home/shaun/Bioteck/run.log"

echo "----- START $(date) -----" >> "$LOGFILE"

PORT=5001

if ss -tulpn | grep -q ":$PORT "; then
    echo "Port $PORT is in use, switching..." >> "$LOGFILE"
    PORT=5002
fi

sleep 3
nohup python3 -m http.server $PORT >> "$LOGFILE" 2>&1 &
SERVER_PID=$!

echo "HTTP server started on port $PORT (PID $SERVER_PID)" >> "$LOGFILE"

sleep 1
chromium-browser \
  --kiosk \
  --ozone-platform=wayland \
  --start-maximized \
  --noerrdialogs \
  --disable-infobars \
  --enable-features=OverlayScrollbar \
  https://time.is/ >> "$LOGFILE" 2>&1 &

echo "Chromium launched (PID $!)" >> "$LOGFILE"

echo "----- END SCRIPT $(date) -----" >> "$LOGFILE"