import pandas as pd
import sqlite3
import re
import spacy
import joblib

nlp = spacy.load("en_core_web_sm")
all_stopwords = nlp.Defaults.stop_words

def filter_tweets(tweet):
    tweet = re.sub("@[A-Za-z0-9]+","", tweet)
    tweet = re.sub(r"[^a-zA-Z ]+", '', tweet)
    doc = nlp(tweet)
    final_token = []
    for token in doc:
        text = token.text;
        if (text not in all_stopwords) and (len(text) > 1) and (text != " "):
            final_token.append(text)
    return " ".join(final_token)

def main():
    conn = sqlite3.connect('./tweets/covid.db')
    c = conn.cursor()

    df = pd.read_sql_query("select * from tweets where country = 'Canada' and location_name like '%British Columbia%'" , conn,  parse_dates=['date_time'])
    
    df['tweet_text'] = df['tweet_text'].str.lower()
    df['tweet_text'] = df['tweet_text'].str.replace('#', '')
    df['tweet_text'] = df['tweet_text'].apply(filter_tweets)

    model = joblib.load("./training/model.pkl")
    df['model_score'] = model.predict(df['tweet_text'])
    df_groupby = df.groupby(df['date_time'].dt.strftime('%W'))['model_score'].mean()
    print(df_groupby)

if __name__ == "__main__":
    main()