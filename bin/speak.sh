#!/bin/bash

export BT_MAC="FC:58:FA:1A:90:92"

pulseaudio -D

expect << EOF
set timeout 30
spawn "bluetoothctl"
expect "# "
send "power on\r"
expect "# "
send "agent on\r"
expect "Agent registered"
send "default-agent\r"
expect "Default agent request successful"
send "connect ${BT_MAC}\r"
expect {
	"Connection successful" { send "exit" }
	"Failed to connect: " { send "exit" }
}
EOF

pacmd set-default-sink "bluez_sink.$(echo $BT_MAC | tr : _)"
pactl set-sink-volume "bluez_sink.$(echo $BT_MAC | tr : _)" 80%


pico2wave -w ttl.wav "$1" && alsaplayer ttl.wav 
