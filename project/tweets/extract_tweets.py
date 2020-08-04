import tweepy
import os
from dotenv import load_dotenv
import sqlite3
import pandas
from pathlib import Path  # python3 only
import itertools

# https://stackoverflow.com/questions/44581647/retrieving-a-list-of-tweets-using-tweet-id-in-tweepy
def lookup_tweets(tweet_IDs, api):
    full_tweets = []
    tweet_count = len(tweet_IDs)
    try:
        for i in range((tweet_count // 100) + 1):
            # Catch the last group if it is less than 100 tweets
            end_loc = min((i + 1) * 100, tweet_count)
            full_tweets.extend(
                
                api.statuses_lookup(tweet_IDs[i * 100:end_loc], tweet_mode='extended')
            )
        return full_tweets
    except tweepy.TweepError as e:
        print(e)
        if(len(full_tweets) > 0):
            return full_tweets

def twitter_login():

    # get crendentials
    consumer_key = os.getenv("consumer_key")
    consumer_secret = os.getenv("consumer_secret")
    access_token_key = os.getenv("access_token_key")
    access_token_secret = os.getenv("access_token_secret")

    # login and get api object
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token_key, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    return api

# Loads credentials from .env file. Look at .env.example for expected format
def load_crendentials():
    env_path = Path('.') / '../.env'
    load_dotenv(dotenv_path=env_path)

def main():
    conn = sqlite3.connect('covid.db')
    c = conn.cursor()
    load_crendentials()
    api = twitter_login()
    try:
        c.execute('''SELECT tweet_id from tweet_ids WHERE is_processed=? LIMIT 50000;''', (False,))
        tweet_ids = c.fetchall()
        tweet_ids = list(itertools.chain(*tweet_ids))
        results = lookup_tweets(tweet_ids, api)
        count = 1
        for result in results:
            try:
                tweet_data = result._json
                print(count)
                tweet_id = tweet_data['id_str']
                date_time = tweet_data['created_at']
                tweet_text = tweet_data['full_text']
                location_name = tweet_data['place']['full_name']
                country = tweet_data['place']['country']
                c.execute('''INSERT into tweets  VALUES (?,?,?,?)''', (date_time, location_name, country, tweet_text) )
                c.execute('''UPDATE tweet_ids set is_processed=? WHERE tweet_id=?''', (True,tweet_id))
                conn.commit()
                count = count + 1
            except Exception as e:
                print(str(e))
                continue
    except Exception as e:
        print(str(e))
        raise(e)
    finally:
        # close connection and cursor
        c.close()
        conn.close()  

if __name__ == "__main__":
    main()