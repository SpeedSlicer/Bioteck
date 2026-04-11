#!/bin/bash

sleep 10

cd /home/shaun/Bioteck

nohup /home/shaun/venv/bin/python main.py > /home/shaun/app.log 2>&1 &

DISPLAY=:0 nohup /usr/bin/chromium --kiosk http://127.0.0.1:5001 > /home/shaun/browser.log 2>&1 &