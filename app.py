import markovify

from flask import Flask
app = Flask(__name__)


with open('fake.txt') as f:
    text = f.read()

@app.route("/")
def generate_tweet():
    model = markovify.Text(text)
    return model.make_short_sentence(140)

