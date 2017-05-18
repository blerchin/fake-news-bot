#!/usr/bin/env bash

trap killgroup SIGINT

killgroup(){
	kill 0
}

./button.py &
./speech.py
wait

