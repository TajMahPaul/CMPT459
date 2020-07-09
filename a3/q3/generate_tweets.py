import tweepy
import os
from dotenv import load_dotenv
from pathlib import Path  # python3 only
import spacy
import csv
import re
import pandas as pd

def tokenize(tweet):
    tokens = []
    nlp = spacy.load("en_core_web_sm")
    all_stopwords = nlp.Defaults.stop_words
    all_stopwords.add(' ')
    all_stopwords.add('\n')
    all_stopwords.add('')
    all_stopwords.add('-')
    
    doc = nlp(tweet)
    for token in doc:
        text = token.text.lower().strip()
        if (text not in all_stopwords and re.match("^[A-Za-z_-]*$", text) and len(text) != 1):
            if text not in tokens:
                tokens.append(text)
    return tokens

def generate_tweets(keyword,api):
    N = 1000
    tweets = []
    count = 1
    for tweet_info in tweepy.Cursor(api.search, q=keyword, lang = 'en',  tweet_mode='extended').items(N):
        print(count)
        count = count + 1
        if "retweeted_status" in dir(tweet_info):
            tweet=tweet_info.retweeted_status.full_text
        else:
            tweet=tweet_info.full_text

        tokens = tokenize(tweet)
        tweets.append(str(tokens))

    return tweets


# logins to twitter api and returns tweetpy.API object
def twitter_login():

    # get crendentials
    consumer_key = os.getenv("consumer_key")
    consumer_secret = os.getenv("consumer_secret")
    access_token_key = os.getenv("access_token_key")
    access_token_secret = os.getenv("access_token_secret")

    # login and get api object
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token_key, access_token_secret)
    api = tweepy.API(auth)

    return api

# Loads credentials from .env file. Look at .env.example for expected format
def load_crendentials():
    env_path = Path('.') / '.env'
    load_dotenv(dotenv_path=env_path)


def main():
    load_crendentials()
    api = twitter_login()

    # generate covid-19 tweets
    tweets = generate_tweets("#covid19",api)
    df = pd.DataFrame(tweets)
    df.columns =['tweets']
    df.to_csv('covid.csv', index=False)
    
    # generate normal tweets
    tweets = generate_tweets("*",api)
    df = pd.DataFrame(tweets)
    df.columns =['tweets']
    df.to_csv('normal.csv', index=False)
    
if __name__ == "__main__":
    main()