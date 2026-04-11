#!/bin/bash
# ai has no clue what its doing. im on my own
nohup python3 -m http.server 5001 > /dev/null 2>&1 &
xset s noblank
xset s off
xset -dpms

unclutter -idle 0 &

sed -i 's/"exited_cleanly":false/"exited_cleanly":true/' /home/pi/.config/chromium/Default/Preferences
sed -i 's/"exit_type":"Crashed"/"exit_type":"Normal"/' /home/pi/.config/chromium/Default/Preferences
chromium-browser --kiosk --noerrdialogs --disable-infobars http://127.0.0.1:5001 &
