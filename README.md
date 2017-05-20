# Fake News Bot

This is a bot that generates tweets about #fake news, and general #fakeness.

## Usage:
### Server:
First, create `.env` with the following:
```
ACCESS_TOKEN="some_token"
REDIS_URL="redis://some_redis"
```
Then run:
```
pip install -r requirements.txt

heroku local web
```

### Client:
```
sudo apt-get install python3 python3-pip \
  pulseaudio pulseaudio-module-bluetooth \
  espeak expect python3-rpi.gpio
sudo pip3 install -r requirements.txt
sudo pip3 install websockets asyncio
```
Then create `.tokens` with the following:
```
export BOT_ACCESS_TOKEN="your_same_token"
```


Run with:
```
./bin/client.py
```

## Add to Corpus
`fake.py` accesses the twitter API to download recent tweets and is
intended to run locally. There's no reason it couldn't run in the cloud,
but since you'll have to do a bunch of cleanup on the corpus... better to do
this at home.

Create `config.json` with your Twitter API credentials:
```
{
    "TWITTER_CONSUMER_KEY": "XXXXXXXXXXXXXXXXXXXXXXXXX",
    "TWITTER_CONSUMER_SECRET":"XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "TWITTER_ACCESS_TOKEN_KEY": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "TWITTER_ACCESS_TOKEN_SECRET": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
}
```

Run:
```
python fake.py
```
