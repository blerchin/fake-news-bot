#!/bin/bash

BT_MAC="FC:58:FA:1A:90:92"

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
send "scan on\r"
expect "Discovery started"
expect "Device ${BT_MAC}" 
send "pair ${BT_MAC}\r"
expect "Pairing successful"
send "trust ${BT_MAC}\r"
expect "trust succeeded"
send "connect ${BT_MAC}\r"
expect "Connection successful"
send "exit"
EOF
