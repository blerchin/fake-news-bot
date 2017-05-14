import markovify
import os
import logging
import redis
import gevent
import json
from flask import Flask, render_template
from flask_sockets import Sockets

REDIS_URL = os.environ['REDIS_URL']
REDIS_CHAN = 'tweets'

app = Flask(__name__)
app.debug = 'DEBUG' in os.environ

sockets = Sockets(app)
redis = redis.from_url(REDIS_URL)

with open('fake-2017-05-02.txt') as f:
    text = f.read()
    model = markovify.Text(text)

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
                yield self.handle_data(data)

    def handle_data(self, message):
        data = json.loads(message)
        if data['evt'] == 'button:pressed':
            return json.dumps({
                'evt': 'new:tweet',
                'tweet': model.make_short_sentence(140)
            })
        else:
            return json


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

@app.route("/")
def render_app():
    return render_template('app.html')

@sockets.route('/ws')
def socket(ws):
    tweets.register(ws)
    while not ws.closed:
        gevent.sleep(0.1)
        message = ws.receive()

        if message:
            app.logger.info(u'inserting message: {}'.format(message))
            redis.publish(REDIS_CHAN, message)
