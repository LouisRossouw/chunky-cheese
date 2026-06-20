#!/bin/bash

export DISPLAY=:0

set -a
source /opt/projects/dev/chunky-cheese/installers/pi/home-pie-electricity-kiosk/.env
set +a

chromium \
--kiosk \
--noerrdialogs \
--disable-infobars \
--disable-session-crashed-bubble \
--disable-translate \
--password-store=basic \
--autoplay-policy=no-user-gesture-required \
--enable-virtual-keyboard \
--load-extension=/opt/dot_squad_bridge,/opt/nav-nav \
--user-data-dir=/home/pi/.config/chromium-kiosk \
"$KIOSK_URL"