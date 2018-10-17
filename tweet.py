import os
import markovify
import json
import re
import twitter

tw_api = twitter.Api(consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
        consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
        access_token_key=os.environ['TWITTER_ACCESS_TOKEN_KEY'],
        access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET']
        )

with open('fake-2017-05-02.txt') as f:
    text = f.read()
    model = markovify.Text(text)

def make_tweet():
    return strip_handles(strip_urls(model.make_short_sentence(140)))

def strip_urls(text):
    return re.sub(r"https:\/\/(.*?)[^A-Za-z0-9.\/]", ' ', text);

def strip_handles(text):
    return re.sub(r"(@)", '', text)

def send_tweet(text):
    try:
        tw_api.PostUpdate(text)
    except Exception as e:
        print(e)

def tweet():
    text = make_tweet()
    send_tweet(text)
    return text


