import markovify
import os
import logging
import redis
import gevent
import json
import re
from flask import Flask, request, render_template, Response
from flask_sockets import Sockets
from functools import wraps

REDIS_URL = os.environ['REDIS_URL']
REDIS_CHAN = 'tweets'
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']

app = Flask(__name__)
app.debug = 'DEBUG' in os.environ

sockets = Sockets(app)
redis = redis.from_url(REDIS_URL)

with open('fake-2017-05-02.txt') as f:
    text = f.read()
    model = markovify.Text(text)

def make_tweet():
    return strip_urls(model.make_short_sentence(140))

def strip_urls(text):
    return re.sub(r"https:\/\/(.*?)[^A-Za-z0-9.\/]", ' ', text);

def authenticate(token):
    return token == ACCESS_TOKEN

def authenticated(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not authenticate(request.args.get('accessToken')):
            return Response('Authentication failed.', 403)
        return f(*args, **kwargs)
    return decorated

class TweetBackend(object):
    def __init__(self):
        self.clients = list()
        self.pubsub = redis.pubsub()
        self.pubsub.subscribe(REDIS_CHAN)

    def __iter_data(self):
        for message in self.pubsub.listen():
            data = message.get('data')
            if message['type'] == 'message':
                app.logger.info(u'sending: {}'.format(data))
                yield data

    def register(self, client):
        self.clients.append(client)

    def send(self, client, data):
        try:
            client.send(data)
        except Exception:
            self.clients.remove(client)

    def run(self):
        for data in self.__iter_data():
            for client in self.clients:
                gevent.spawn(self.send, client, data)

    def start(self):
        gevent.spawn(self.run)

tweets = TweetBackend()
tweets.start()


def handle_message(message):
    data = json.loads(message)
    if data['evt'] == 'button:pressed':
        result = json.dumps({
            'evt': 'new:tweet',
            'tweet': make_tweet()
        })
        redis.publish(REDIS_CHAN, result)
    else:
        redis.publish(REDIS_CHAN, json.dumps(data))


@app.route("/")
@authenticated
def render_app():
    return render_template('app.html')

@sockets.route('/ws')
@authenticated
def socket(ws):
    tweets.register(ws)
    while not ws.closed:
        gevent.sleep(0.1)
        message = ws.receive()

        if message:
            handle_message(message)
