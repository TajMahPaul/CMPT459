import pandas as pd
import sqlite3
import re
import spacy
import joblib
import matplotlib.pyplot as plt

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
    df_bc = pd.read_csv("bc_data.csv", parse_dates=['Reported_Date'])
    df_bc = df_bc.groupby(df_bc['Reported_Date'].dt.strftime('%W'))['Classification_Reported'].count().reset_index(name='count')
    df_bc = df_bc.rename(columns={"Reported_Date": "Week"})
    df_bc['Week'] =  df_bc['Week'].astype(int)

    df['tweet_text'] = df['tweet_text'].str.lower()
    df['tweet_text'] = df['tweet_text'].str.replace('#', '')
    df['tweet_text'] = df['tweet_text'].apply(filter_tweets)

    model = joblib.load("./training/model.pkl")
    df['model_score'] = model.predict(df['tweet_text'])
    df_groupby = df.groupby(df['date_time'].dt.strftime('%W'))['model_score'].mean().reset_index(name='score')
    df_groupby = df_groupby.rename(columns={"date_time": "Week"})
    df_groupby['Week'] =  df_groupby['Week'].astype(int)
    df_groupby['Week'] =  df_groupby['Week'] + 2
    df_join = df_groupby.join(df_bc,on=['Week'], how='inner', lsuffix='_left', rsuffix='_right')
    df_join.drop(['Week_left', 'Week_right'], axis=1)
    df_join = df_join[df_join['Week'] != 28]

    fig, ax1 = plt.subplots()
    color = 'tab:blue'
    ax1.set_xlabel('Week Number')
    ax1.set_ylabel('Covid-19 Case Count', color=color)
    ax1.bar(df_join['Week'], df_join['count'], color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color = 'tab:red'
    ax2.set_ylabel('Fear Score', color=color)
    ax2.plot(df_join['Week'], df_join['score'], color=color)

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.show()
if __name__ == "__main__":
    main()