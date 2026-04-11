#!/bin/bash

cd /home/shaun/Bioteck

export DISPLAY=:0
export XAUTHORITY=/home/shaun/.Xauthority

lxterminal -e "bash -c 'python3 main.py'" &

# wait for server
until curl -s http://127.0.0.1:5001 > /dev/null; do
  sleep 0.5
done

chromium --kiosk \
  --noerrdialogs \
  --disable-infobars \
  http://127.0.0.1:5001