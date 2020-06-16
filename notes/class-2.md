
# Class 2

> If you haven't already, please sign up for Basilica and Twitter API accounts, respectively:
>  + https://developer.twitter.com/en/docs
>  + https://www.basilica.ai/

Topics / Agenda:

  1. Integrating with an example API (bonus)
  2. Integrating with the Twitter API
  3. Integrating with the Basilica API
  4. Storing API data in the database

Lambda Materials:

  + https://learn.lambdaschool.com/ds/module/recVFIbE3mpjpVGrj/
  + https://github.com/LambdaSchool/DS-Unit-3-Sprint-3-Productization-and-Cloud/tree/master/module2-consuming-data-from-an-api

Installing package dependencies:

```sh
pipenv install python-dotenv requests basilica tweepy
```

Example ".env" file:

```sh
# .env
ALPHAVANTAGE_API_KEY="abc123"

BASILICA_API_KEY="_______________________"

TWITTER_API_KEY="_______________________"
TWITTER_API_SECRET="_______________________"
TWITTER_ACCESS_TOKEN="_______________________"
TWITTER_ACCESS_TOKEN_SECRET="_______________________"
```

> IMPORTANT: remember to add a `.env` entry into the ".gitignore" file, to prevent secret creds from being tracked in version control!!

## Part 0 (Bonus / SC Hint)

If you're working with an API that doesn't provide its own Python package interface, one option is to use the `requests` package to directly issue HTTP requests to the given API.

Using the `requests` package to issue HTTP requests:

  + https://github.com/psf/requests
  + https://requests.readthedocs.io/en/master/
  + https://raw.githubusercontent.com/prof-rossetti/intro-to-python/master/data/products.json
  + https://github.com/prof-rossetti/intro-to-python/blob/master/notes/python/packages/requests.md

A simple example API to get started with (can use API KEY "abc123"):

  + https://www.alphavantage.co/
  + https://www.alphavantage.co/documentation/#daily

```py
# web_app/services/stocks_service.py

import requests
import json

request_url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=TSLA&apikey=abc123"
print(request_url)

response = requests.get(request_url)
print(type(response)) #> <class 'requests.models.Response'>
print(response.status_code) #> 200
print(type(response.text)) #> <class 'str'>

parsed_response = json.loads(response.text) # transforms the string response into a usable python datatype (list or dict)
print(type(parsed_response)) #> <class 'dict'>

latest_close = parsed_response["Time Series (Daily)"]["2020-02-25"]["4. close"]
print("LATEST CLOSING PRICE:", latest_close)

#breakpoint()
```

## Part I

The Basilica API:

  + https://www.basilica.ai/quickstart/python/
  + https://www.basilica.ai/api-keys/
  + https://basilica-client.readthedocs.io/en/latest/basilica.html

```py
# web_app/services/basilica_service.py

import basilica
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("BASILICA_API_KEY")

def basilica_api_client():
    connection = basilica.Connection(API_KEY)
    print(type(connection)) #> <class 'basilica.Connection'>
    return connection

if __name__ == "__main__":

    print("---------")
    connection = basilica_api_client()

    print("---------")
    sentence = "Hello again"
    sent_embeddings = connection.embed_sentence(sentence)
    print(list(sent_embeddings))

    print("---------")
    sentences = ["Hello world!", "How are you?"]
    print(sentences)
    # it is more efficient to make a single request for all sentences...
    embeddings = connection.embed_sentences(sentences)
    print("EMBEDDINGS...")
    print(type(embeddings))
    print(list(embeddings)) # [[0.8556405305862427, ...], ...]

```

## Part II

The Twitter API and Tweepy Package:

  + https://developer.twitter.com/en/docs
  + https://github.com/tweepy/tweepy
  + http://docs.tweepy.org/en/latest/
  + http://docs.tweepy.org/en/latest/api.html#API.get_user
  + http://docs.tweepy.org/en/latest/api.html#API.user_timeline
  + https://github.com/prof-rossetti/intro-to-python/blob/master/notes/python/packages/tweepy.md (FYI / BONUS)

Twitter Service:

```py
# web_app/services/twitter_service.py

import tweepy
import os
from dotenv import load_dotenv

load_dotenv()

TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

def twitter_api():
    auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
    auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
    print("AUTH", auth)
    api = tweepy.API(auth)
    print("API", api)
    #print(dir(api))
    return api

if __name__ == "__main__":

    api = twitter_api()
    user = api.get_user("elonmusk")
    print("USER", user)
    print(user.screen_name)
    print(user.name)
    print(user.followers_count)

    #breakpoint()

    #public_tweets = api.home_timeline()
    #
    #for tweet in public_tweets:
    #    print(type(tweet)) #> <class 'tweepy.models.Status'>
    #    #print(dir(tweet))
    #    print(tweet.text)
    #    print("-------------")
```

## Part III

Saving tweets and users in the database.

Twitter Routes (Iteration 1, returning the results as JSON):

```py
# web_app/routes/twitter_routes.py

from flask import Blueprint, render_template, jsonify
from web_app.services.twitter_service import twitter_api_client

twitter_routes = Blueprint("twitter_routes", __name__)

@twitter_routes.route("/users/<screen_name>")
def get_user(screen_name=None):
    print(screen_name)
    api = twitter_api_client()
    user = api.get_user(screen_name)
    statuses = api.user_timeline(screen_name, tweet_mode="extended", count=150, exclude_replies=True, include_rts=False)
    return jsonify({"user": user._json, "tweets": [s._json for s in statuses]})

```

Twitter Routes (Iteration 2, storing users in the database, first need to implement the respective [`User` and `Tweet` model classes](/reference_code/models.py)):

```py
# web_app/routes/twitter_routes.py

from flask import Blueprint, render_template, jsonify
from web_app.models import db, User, Tweet, parse_records
from web_app.services.twitter_service import twitter_api_client
from web_app.services.basilica_service import basilica_api_client

twitter_routes = Blueprint("twitter_routes", __name__)

@twitter_routes.route("/users/<screen_name>")
def get_user(screen_name=None):
    print(screen_name)

    api = twitter_api_client()

    twitter_user = api.get_user(screen_name)
    statuses = api.user_timeline(screen_name, tweet_mode="extended", count=150, exclude_replies=True, include_rts=False)
    print("STATUSES COUNT:", len(statuses))
    #return jsonify({"user": user._json, "tweets": [s._json for s in statuses]})

    # get existing user from the db or initialize a new one:
    db_user = User.query.get(twitter_user.id) or User(id=twitter_user.id)
    db_user.screen_name = twitter_user.screen_name
    db_user.name = twitter_user.name
    db_user.location = twitter_user.location
    db_user.followers_count = twitter_user.followers_count
    db.session.add(db_user)
    db.session.commit()
    #breakpoint()
    return "OK"
    #return render_template("user.html", user=db_user, tweets=statuses) # tweets=db_tweets
```


Twitter Routes (Iteration 3, storing users and tweets and embeddings in the database):

```py
# web_app/routes/twitter_routes.py

from flask import Blueprint, render_template, jsonify
from web_app.models import db, User, Tweet, parse_records
from web_app.services.twitter_service import twitter_api_client
from web_app.services.basilica_service import basilica_api_client

twitter_routes = Blueprint("twitter_routes", __name__)

@twitter_routes.route("/users/<screen_name>")
def get_user(screen_name=None):
    print(screen_name)

    api = twitter_api_client()

    twitter_user = api.get_user(screen_name)
    statuses = api.user_timeline(screen_name, tweet_mode="extended", count=150, exclude_replies=True, include_rts=False)
    print("STATUSES COUNT:", len(statuses))
    #return jsonify({"user": user._json, "tweets": [s._json for s in statuses]})

    # get existing user from the db or initialize a new one:
    db_user = User.query.get(twitter_user.id) or User(id=twitter_user.id)
    db_user.screen_name = twitter_user.screen_name
    db_user.name = twitter_user.name
    db_user.location = twitter_user.location
    db_user.followers_count = twitter_user.followers_count
    db.session.add(db_user)
    db.session.commit()
    #return "OK"
    #breakpoint()

    basilica_api = basilica_api_client()

    all_tweet_texts = [status.full_text for status in statuses]
    embeddings = list(basilica_api.embed_sentences(all_tweet_texts, model="twitter"))
    print("NUMBER OF EMBEDDINGS", len(embeddings))

    # TODO: explore using the zip() function maybe...
    counter = 0
    for status in statuses:
        print(status.full_text)
        print("----")
        #print(dir(status))
        # get existing tweet from the db or initialize a new one:
        db_tweet = Tweet.query.get(status.id) or Tweet(id=status.id)
        db_tweet.user_id = status.author.id # or db_user.id
        db_tweet.full_text = status.full_text
        #embedding = basilica_client.embed_sentence(status.full_text, model="twitter") # todo: prefer to make a single request to basilica with all the tweet texts, instead of a request per tweet
        embedding = embeddings[counter]
        print(len(embedding))
        db_tweet.embedding = embedding
        db.session.add(db_tweet)
        counter+=1
    db.session.commit()
    #breakpoint()
    return "OK"
    #return render_template("user.html", user=db_user, tweets=statuses) # tweets=db_tweets
```


```html
<!-- web_app/templates/user.html -->

{% extends "layout.html" %}

{% block content %}
    <h2>Twitter User: {{ user.screen_name }} </h2>

    <p>Name: {{ user.name }}</p>
    <p>Location: {{ user.location }}</p>
    <p>Followers: {{ user.followers_count }}</p>

    {% if tweets %}
        <ul>
        {% for status in tweets %}
            <li>{{ status.full_text }}</li>
        {% endfor %}
        </ul>

    {% else %}
        <p>No tweets found.</p>
    {% endif %}

{% endblock %}
```

> CHALLENGE: Can you display the tweets in a twitter bootstrap table, instead of a list?
