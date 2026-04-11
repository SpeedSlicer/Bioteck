#!/bin/bash
source /home/shaun/venv/bin/activate
cd /home/shaun/Bioteck

nohup python3 main.py > app.log 2>&1 &
nohup chromium --kiosk http://127.0.0.1:5001 > browser.log 2>&1 &