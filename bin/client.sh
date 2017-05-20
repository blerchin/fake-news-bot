#!/usr/bin/env bash

source .tokens
export BOT_SOCKET_URL="wss://fake-news-bot.herokuapp.com/ws?accessToken=${BOT_ACCESS_TOKEN}"
export BOT_GUI_URL="https://fake-news-bot.herokuapp.com/?accessToken=${BOT_ACCESS_TOKEN}"

trap killgroup SIGINT

killgroup(){
	kill 0
}

./button.py &
./speech.py &
./bin/browser.sh
wait

