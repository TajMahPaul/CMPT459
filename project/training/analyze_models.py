import pandas as pd
import numpy as np
import spacy
import re
import joblib

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.model_selection import train_test_split

from sklearn.svm import SVR
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier

from sklearn.pipeline import make_pipeline

nlp = spacy.load("en_core_web_sm")
all_stopwords = nlp.Defaults.stop_words

OUTPUT_TEMPLATE = (
    'kNN classifier:         {knn:.3f}\n'
    'Rand forest classifier: {rf:.3f}\n'
    'AdaBoost Classifier:     {ada:.3f}\n'
    'LinearSVC Classifier:     {svc:.3f}\n'
)

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

    X_train, X_valid, y_train, y_valid = train_test_split(df.text.values, df.score.values, test_size=0.4, shuffle=True)

    # binary classifiers
    modelADA = make_pipeline(CountVectorizer(analyzer='word', ngram_range=(1, 1)), AdaBoostClassifier())
    modelRF = make_pipeline(CountVectorizer(analyzer='word', ngram_range=(1, 1)), RandomForestClassifier(n_estimators=50, max_depth=5, min_samples_leaf = 2))
    modelKNN = make_pipeline(CountVectorizer(analyzer='word', ngram_range=(1, 1)), KNeighborsClassifier(n_neighbors=9))
    modelSVC = make_pipeline(CountVectorizer(analyzer='word', ngram_range=(1, 1)), LinearSVC())
    
    # regression model
    modelSVR = make_pipeline(CountVectorizer(analyzer='word', ngram_range=(1, 1)), AdaBoostClassifier())

    models = [modelADA, modelRF, modelKNN, modelSVC]

    for i, m in enumerate(models):  # yes, you can leave this loop in if you want.
        m.fit( X_train ,y_train)

    print(OUTPUT_TEMPLATE.format(
        ada=modelADA.score(X_valid, y_valid),
        knn=modelKNN.score(X_valid, y_valid),
        svc=modelSVC.score(X_valid, y_valid),
        rf=modelRF.score(X_valid, y_valid)
    ))
    
if __name__ == "__main__":
    main()