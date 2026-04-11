#!/bin/bash
# ai has no clue what its doing. im on my own

LOGFILE="/home/shaun/Bioteck/run.log"

echo "----- START $(date) -----" >> "$LOGFILE"

sleep 3
nohup python3 -m http.server 5001 >> "$LOGFILE" 2>&1 &

echo "HTTP server started (PID $!)" >> "$LOGFILE"

sleep 1
/bin/chromium-browser \
  --kiosk \
  --ozone-platform=wayland \
  --start-maximized \
  --noerrdialogs \
  --disable-infobars \
  --enable-features=OverlayScrollbar \
  https://time.is/ >> "$LOGFILE" 2>&1 &

echo "Chromium launched (PID $!)" >> "$LOGFILE"

echo "----- END SCRIPT $(date) -----" >> "$LOGFILE"