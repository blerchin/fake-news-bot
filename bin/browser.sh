#!/usr/bin/env bash

startx `which chromium-browser` --app=$BOT_GUI_URL --window-position=0,0 --window-size=1824,984 --aggressive-cache-discard -- -s 0 dpms -nocursor
