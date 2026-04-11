#!/bin/bash

cd /home/shaun/Bioteck

export DISPLAY=:0
export XAUTHORITY=/home/shaun/.Xauthority
lxterminal -e "/home/shaun/Bioteck/create_python_server.sh"
sleep 2

chromium --kiosk \
  --noerrdialogs \
  --disable-infobars \
  http://127.0.0.1:5001