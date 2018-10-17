#!/usr/bin/env bash

source .env

export TWITTER_ACCESS_TOKEN_KEY
export TWITTER_ACCESS_TOKEN_SECRET
export TWITTER_CONSUMER_KEY
export TWITTER_CONSUMER_SECRET

python3 button.py
