import pandas as pd
import numpy as np
import spacy
import re
import joblib

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

from sklearn.svm import SVR
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier

from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import FunctionTransformer

nlp = spacy.load("en_core_web_sm")
all_stopwords = nlp.Defaults.stop_words

def score_to_label(score):
    if(score < .6):
        return 0
    else:
        return 1

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
    df = pd.read_csv('fear.txt', sep="	", names=['id', 'text', 'type', 'score'])
    df_regression = df.copy()
    
    # Filter the tweets
    df = df.drop(['id', 'type'], axis=1)
    df['text'] = df['text'].str.lower()
    df['text'] = df['text'].str.replace('#', '')
    df['text'] = df['text'].apply(filter_tweets)

    # convert scores to 0 or 1 (no fear, fear)
    df['score'] = df['score'].apply(score_to_label)

    X_train, X_test, y_train, y_test = train_test_split(df.text.values, df.score.values, test_size=0.4, shuffle=True)
    model = make_pipeline(CountVectorizer(analyzer='word', ngram_range=(1, 1)), LinearSVC())
    model.fit(X_train,y_train)

    print(model.score(X_test, y_test))
    # save
    joblib.dump(model, "model.pkl") 
    
if __name__ == "__main__":
    main()