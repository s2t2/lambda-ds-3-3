
# Class 2

> If you haven't already, please sign up for Basilica and Twitter API accounts, respectively:
>  + https://developer.twitter.com/en/docs
>  + https://www.basilica.ai/

Topics / Agenda:

  1. Integrating with an example API
  2. Integrating with the Twitter API
  3. Integrating with the Basilica API

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

## Part I

Using the requests package to issue HTTP requests (BONUS):

  + https://github.com/psf/requests
  + https://requests.readthedocs.io/en/master/
  + https://raw.githubusercontent.com/prof-rossetti/intro-to-python/master/data/products.json
  + (BONUS) https://github.com/prof-rossetti/intro-to-python/blob/master/notes/python/packages/requests.md

A simple example API to get started with (can use API KEY "abc123") (BONUS):

  + https://www.alphavantage.co/
  + https://www.alphavantage.co/documentation/#daily

```py
# web_app/stocks_service.py
import requests
import json

request_url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=TSLA&apikey=abc123"
print(request_url)

response = requests.get(request_url)
print(type(response)) #> <class 'requests.models.Response'>
print(response.status_code) #> 200
print(type(response.text)) #> <class 'str'>

parsed_response = json.loads(response.text)
print(type(parsed_response)) #> <class 'dict'>

latest_close = parsed_response["Time Series (Daily)"]["2020-02-25"]["4. close"]
print("LATEST CLOSING PRICE:", latest_close)

#breakpoint()
```

## Part II

The Twitter API and Tweepy Package:

  + https://developer.twitter.com/en/docs
  + https://github.com/tweepy/tweepy
  + http://docs.tweepy.org/en/latest/
  + (BONUS) https://github.com/prof-rossetti/intro-to-python/blob/master/notes/python/packages/tweepy.md

## Part III

The Basilica API:

  + https://www.basilica.ai/quickstart/python/
  + https://www.basilica.ai/api-keys/
  + https://basilica-client.readthedocs.io/en/latest/basilica.html

```py
# web_app/basilica_service.py
import basilica
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("BASILICA_API_KEY")

connection = basilica.Connection(API_KEY)

if __name__ == "__main__":
    sentences = ["Hello world!", "How are you?"]
    embeddings = connection.embed_sentences(sentences)
    print(type(embeddings))
    for embedding in embeddings:
        print(len(embedding)) #> 768
        print(list(embedding)) # [[0.8556405305862427, ...], ...]
        print("-------------")
```
