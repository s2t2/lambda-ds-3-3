


import os
from dotenv import load_dotenv
import tweepy

load_dotenv()

consumer_key = os.getenv("TWITTER_API_KEY", default="OOPS")
consumer_secret = os.getenv("TWITTER_API_SECRET", default="OOPS")
access_token = os.getenv("TWITTER_ACCESS_TOKEN", default="OOPS")
access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET", default="OOPS")

# AUTHENTICATE

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# INITIALIZE API CLIENT

client = tweepy.API(auth)
print(client)

# ISSUE REQUESTS

user = client.me() # get information about the currently authenticated user
print(user)

tweets = client.user_timeline() # get a list of tweets posted by the currently authenticated user

# PARSE RESPONSES

print("---------------------------------------------------------------")
print(f"RECENT TWEETS BY @{user.screen_name} ({user.followers_count} FOLLOWERS / {user.friends_count} FOLLOWING):")
print("---------------------------------------------------------------")

for tweet in tweets:
    created_on = tweet.created_at.strftime("%Y-%m-%d")
    print(" + ", tweet.id_str, created_on, tweet.text)






elon = client.get_user("elonmusk")

print("---------------------------------------------------------------")
print(f"RECENT TWEETS BY @{elon.screen_name} ({elon.followers_count} FOLLOWERS / {elon.friends_count} FOLLOWING):")
print("---------------------------------------------------------------")

elon_tweets = elon.timeline(
    count=200,
    exclude_replies=True,
    include_rts=False,
    tweet_mode='extended'
)

for tweet in elon_tweets:
    created_on = tweet.created_at.strftime("%Y-%m-%d")
    print(" + ", tweet.id_str, created_on, tweet.full_text)
