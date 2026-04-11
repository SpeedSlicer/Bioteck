#!/bin/bash

cd /home/shaun/Bioteck

python3 main.py &
chromium --kiosk --incognito --password-store=basic http://127.0.0.1:5001 &