import pandas as pd
import spacy
import re
import ast
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import fpgrowth
import numpy as np

def strTolist(string):
    return ast.literal_eval(string)

def createFreqItems(data, support):
    te = TransactionEncoder()
    te_ary = te.fit(data).transform(data)
    df = pd.DataFrame(te_ary, columns=te.columns_)
    frequent_itemsets = fpgrowth(df, min_support=support, use_colnames=True, max_len=4)
    frequent_itemsets['length'] = frequent_itemsets['itemsets'].apply(lambda x: len(x))
    return frequent_itemsets

def main():
    D1 = pd.read_csv("normal.csv")
    D2 = pd.read_csv("covid.csv")

    D1_list_of_tokenized_tweets = D1['tweets'].apply(strTolist).tolist()
    D2_list_of_tokenized_tweets = D2['tweets'].apply(strTolist).tolist()

    D1_frequent_itemsets = createFreqItems(D1_list_of_tokenized_tweets, 0.005)
    D2_frequent_itemsets = createFreqItems(D2_list_of_tokenized_tweets, 0.001)

    df = D1_frequent_itemsets.merge(D2_frequent_itemsets, on='itemsets')

    df['odd'] = np.divide(df['support_y'], df['support_x'])

    df = df.nlargest(100, 'odd')

    df = df.drop(['support_x', 'support_y', 'length_x', 'length_y'], axis=1)

    df = df.reset_index(drop=True)
    
    df.to_csv('final_data.csv', index=False)

if __name__ == "__main__":
    main()