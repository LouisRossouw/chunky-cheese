#!/bin/bash

export DISPLAY=:0

set -a
source ~/.config/kiosk/.env
set +a

chromium \
--kiosk \
--incognito \
--noerrdialogs \
--disable-infobars \
--disable-session-crashed-bubble \
--disable-translate \
--password-store=basic \
--autoplay-policy=no-user-gesture-required \
"$KIOSK_URL"