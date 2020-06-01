import tweepy
import os
from dotenv import load_dotenv
from pathlib import Path  # python3 only
import spacy
import csv
import re

def main():
    load_crendentials()
    api = twitter_login()

    # generate covid-19 tweets
    tweets = generate_tweets("#covid19",api)
    tokens = tokenize(tweets)
    print(len(tokens))
    top_100 = top_tokens(100, tokens)
    to_csv_freq("covid-top100.csv",top_100)
    to_csv_all("covid.csv",tokens)

    # generate normal tweets
    tweets = generate_tweets("*",api)
    tokens = tokenize(tweets)
    print(len(tokens))
    top_100 = top_tokens(100, tokens)
    to_csv_freq("normal-top100.csv",top_100)
    to_csv_all("normal.csv",tokens)

def to_csv_all(filename, tokens):
    csv_columns = ['Weight','Word']
    try:
        with open(filename, 'w') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(csv_columns)
            for key, value in tokens.items():
                writer.writerow([value, key])

    except IOError:
        print("I/O error")

def to_csv_freq(filename, tokens):
    csv_columns = ['Frequency','Word']
    try:
        with open(filename, 'w') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(csv_columns)
            for key, value in tokens.items():
                writer.writerow([value/1000, key])

    except IOError:
        print("I/O error")

def top_tokens(n, tokens):
    sorted_tokens = {k: v for k, v in sorted(tokens.items(), key=lambda item: item[1], reverse=True)[:n]}
    return sorted_tokens

def tokenize(tweets):
    tokens = {}
    nlp = spacy.load("en_core_web_sm")
    all_stopwords = nlp.Defaults.stop_words

    for tweet in tweets:
        doc = nlp(tweet)
        for token in doc:
            text = token.text.lower()
            if (text not in all_stopwords and re.match("^[A-Za-z0-9_-]*$", text)):
                if text in tokens:
                    tokens[text] += 1
                else:
                    tokens[text] = 1
    return tokens

def generate_tweets(keyword,api):
    N = 1000
    tweets = []
    for tweet_info in tweepy.Cursor(api.search, q=keyword, lang = 'en',  tweet_mode='extended').items(N):
        if "retweeted_status" in dir(tweet_info):
            tweet=tweet_info.retweeted_status.full_text
        else:
            tweet=tweet_info.full_text

        tweets.append(tweet)

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

if __name__ == "__main__":
    main()