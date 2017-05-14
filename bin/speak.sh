#!/bin/bash

export BT_MAC="FC:58:FA:1A:90:92"

pulseaudio -D

expect << EOF
spawn "bluetoothctl"
expect "# "
send "power on\r"
expect "# "
send "agent on\r"
expect "Agent registered"
send "default-agent\r"
expect "Default agent request successful"
send "connect ${BT_MAC}\r"
expect "Connection successful"
send "exit"
EOF

pacmd set-default-sink "bluez_sink.$(echo $BT_MAC | tr : _)"


pico2wave -w ttl.wav "$1" && aplay ttl.wav
