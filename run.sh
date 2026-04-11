#!/bin/bash

cd /home/shaun/Bioteck

export DISPLAY=:0
export XAUTHORITY=/home/shaun/.Xauthority

# kill old Flask if it exists (prevents port conflict)
pkill -f main.py

# start Flask
python3 main.py > flask.log 2>&1 &

# wait for server
until curl -s http://127.0.0.1:5001 > /dev/null; do
  sleep 0.5
done

# start Chromium in REAL GUI session
chromium --kiosk \
  --noerrdialogs \
  --disable-infobars \
  http://127.0.0.1:5001