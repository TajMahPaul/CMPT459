import tweepy
import os
from dotenv import load_dotenv
from pathlib import Path  # python3 only
import spacy

def main():
    load_crendentials()
    api = twitter_login()
    tweets = generate_tweets(api)
    tokens = tokenize(tweets)
    print (tokens)

def top_tokens(n. tokens):

def tokenize(tweets):
    tokens = {}
    nlp = spacy.load("en_core_web_sm")
    all_stopwords = nlp.Defaults.stop_words

    for tweet in tweets:
        doc = nlp(tweet)
        for token in doc:
            text = token.text.lower()
            if text not in all_stopwords and not token.is_space and not token.is_punct:
                if text in tokens:
                    tokens[text] += 1
                else:
                    tokens[text] = 1
    return tokens

def generate_tweets(api):
    N = 1000
    tweets = []
    for tweet_info in tweepy.Cursor(api.search, q='#covid-19', lang = 'en',  tweet_mode='extended').items(N):
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