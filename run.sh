#!/bin/bash
# ai has no clue what its doing. im on my own
nohup python3 -m http.server 5001 > /dev/null 2>&1 &
/bin/chromium-browser  --kiosk --ozone-platform=wayland --start-maximized --noerrdialogs --disable-infobars --enable-features=OverlayScrollbar  https://time.is/ &