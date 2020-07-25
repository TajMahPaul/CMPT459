import numpy as np
import pandas as pd
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_validate, train_test_split

def main():
    df = pd.read_csv("../training_data.csv")
    dtest = pd.read_csv("../test_data.csv")
    X = df.loc[:, 'a':'w'].values
    y = df['label'].values
    
    test_date = dtest.values
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=0)


    clf = DecisionTreeClassifier(max_depth=3)
    model = AdaBoostClassifier(base_estimator=clf,learning_rate=1)

    clf.fit(X_train, y_train)
    prediction = clf.predict(test_date)

    with open("output4.txt", 'w') as f:
        f.write("\n".join(map(str, prediction)))

if __name__ == "__main__":
    main()