#!/bin/bash

cd /home/shaun/Bioteck

pkill -f main.py

export DISPLAY=:0

python3 main.py > flask.log 2>&1 &

until curl -s http://127.0.0.1:5001 > /dev/null; do
  sleep 0.5
done

chromium --kiosk --noerrdialogs --disable-infobars http://127.0.0.1:5001