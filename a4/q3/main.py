import numpy as np
import pandas as pd
from sklearn.metrics import make_scorer, accuracy_score, precision_score, recall_score, average_precision_score
from sklearn.ensemble import AdaBoostClassifier
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_validate
def main():
    df = pd.read_csv("../training_data.csv")
    X = df.loc[:, 'a':'w'].values
    y = df['label'].values

    scoring = {'acurracy' : make_scorer(accuracy_score), 
               'precision' : make_scorer(precision_score),
               'rollup' : make_scorer(recall_score)}

    kfold = KFold(n_splits=10)
    scores = cross_validate(AdaBoostClassifier(), X, y, cv=kfold, scoring=scoring)
    scores = pd.DataFrame(scores)
    scores = scores.drop(['fit_time', 'score_time'], axis = 1)
    scores.index.name = 'k'
    print(scores.to_string())
    print('')
    print("average precision: ", np.mean(scores['test_precision']))
    print("average roll-up: ", np.mean(scores['test_rollup']))

if __name__ == "__main__":
    main()