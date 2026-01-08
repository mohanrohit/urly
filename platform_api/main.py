import string
import time
import logging

from functools import wraps

from flask import Flask
from flask import request
from flask import redirect


links = {}

app = Flask(__name__)


def generate_shortcode():
    # use base62 to generate a shortcode using the current timestamp
    number = int(time.time())

    alphabet = string.ascii_lowercase + string.ascii_uppercase + string.digits

    shortcode = ""

    while number > 0:
        remainder = number % 62

        shortcode = alphabet[remainder] + shortcode

        number //= 62


    return shortcode


@app.get("/")
def index():
    return { "message": "Hello, Urly!" }


@app.post("/shorten")
def shorten_url():
    payload = request.json

    if "url" not in payload:
        return { "error": "Please provide the URL to shorten "}, 422

    shortcode = generate_shortcode()

    links[shortcode] = payload["url"]

    return { "url": f"http://localhost:5000/{shortcode}" }


@app.get("/<shortcode>")
def redirect_to_url(shortcode):
    link = links.get(shortcode) or ""

    if not link:
        return {"error": f"There's no URL for {shortcode}"}, 404

    return redirect(links[shortcode], code=301)
