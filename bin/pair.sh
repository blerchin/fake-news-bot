#!/bin/bash

BT_MAC="FC:58:FA:9E:A5:8E"

pulseaudio -D

expect << EOF
set timeout 120
spawn "bluetoothctl"
expect "# "
send "power on\r"
expect "# "
send "agent on\r"
expect "Agent registered"
send "default-agent\r"
expect "Default agent request successful"
send "remove ${BT_MAC}\r"
expect {
	"Device has been removed" {}
	"not available" {}
}
send "scan on\r"
expect "Discovery started"
expect "Device ${BT_MAC}" 
send "pair ${BT_MAC}\r"
expect "Pairing successful"
send "trust ${BT_MAC}\r"
expect "trust succeeded"
send "connect ${BT_MAC}\r"
expect {
	"Connection successful" { send "exit" }
	"Failed to connect: " { send "exit" }
}
send "exit"
EOF

pacmd set-default-sink "bluez_sink.$(echo $BT_MAC | tr : _)"
pactl set-sink-volume "bluez_sink.$(echo $BT_MAC | tr : _)" 80%

espeak -ven+f3 -k5 -s150 "Introducing Fake News Bot"
