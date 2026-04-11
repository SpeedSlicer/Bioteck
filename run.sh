#!/bin/bash

source /home/shaun/venv/bin/activate
cd /home/shaun/Bioteck

nohup python main.py > app.log 2>&1 &
SERVER_PID=$!

until curl -s http://127.0.0.1:5001 > /dev/null; do
  sleep 1
done

nohup chromium --kiosk http://127.0.0.1:5001 > browser.log 2>&1 &

wait $SERVER_PID