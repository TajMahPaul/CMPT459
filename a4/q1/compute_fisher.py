import pandas as pd
import numpy as np

# https://stackoverflow.com/questions/15481990/calculating-the-fisher-criterion-in-python
def fisher_criterion(v1, v2):
    return abs(np.mean(v1) - np.mean(v2)) / (np.var(v1) + np.var(v2))

def main():
    training_data = pd.read_csv("../training_data.csv")
    df_label_1 = training_data[training_data['label'] == 1].drop(['label'], axis=1)
    df_label_0 = training_data[training_data['label'] == 0].drop(['label'], axis=1)

    fisher_list = []

    
    for column in df_label_1.columns:
        fisher_list.append(fisher_criterion(df_label_1[column], df_label_0[column]))

    fisher_df = pd.DataFrame({'fisher_score': fisher_list}, index=df_label_1.columns)
    print(fisher_df.to_string())
if __name__ == "__main__":
    main()