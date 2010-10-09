#!/bin/bash
su cloud -c "Xvfb :1 -cc 4 -screen 0 1024x768x16 &"
sleep 5
x11vnc -display :1 -ssl SAVE -httpdir /usr/share/x11vnc/classes/ssl/ -httpsredir -rfbport 443 -forever -unixpw cloud >/tmp/xll.txt 2>&1 &
su cloud -c "export DISPLAY=:1 ; matchbox-desktop  -use_titlebar yes -use_desktop_mode decorated &"
su cloud -c "export DISPLAY=:1 ; calibre &"
su cloud -c "export DISPLAY=:1 ; matchbox-window-manager -theme Industrial"

