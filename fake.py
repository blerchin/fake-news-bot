#!/usr/bin/env python

from __future__ import print_function

import time

import twitter
import json

config = json.loads(open('config.json').read())

api = twitter.Api(consumer_key=config['TWITTER_CONSUMER_KEY'],
        consumer_secret=config['TWITTER_CONSUMER_SECRET'],
        access_token_key=config['TWITTER_ACCESS_TOKEN_KEY'],
        access_token_secret=config['TWITTER_ACCESS_TOKEN_SECRET']
        )

tweets = {}

fpath = 'fake.txt'
max_id = None
with open(fpath, 'r') as f:
    line = '\n'
    while(line != ''):
        line = f.readline().decode('utf-8')
        if line != '\n':
            print(line)
            tweets[line] = True
    print('parsed file')
    time.sleep(1)
for i in range(200):
    results = api.GetSearch('#fake', count=200, max_id=max_id)

    if len(results) < 1:
         break

    for status in results:
        tweets[status.text] = True 
        print(status.text)
        
        if not max_id:
            max_id = status.id - 1
        elif status.id < max_id:
            max_id = status.id - 1

    time.sleep(1)
    with open(fpath, 'w') as f:
        for tweet in tweets:
            print(tweet.encode('utf-8') + '\n\n\n', file=f)

