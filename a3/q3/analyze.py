import pandas as pd
import spacy
import re
import ast
import matplotlib
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori


def createFreqItems(data):
    te = TransactionEncoder()
    te_ary = te.fit(data).transform(data)
    df = pd.DataFrame(te_ary, columns=te.columns_)
    frequent_itemsets = apriori(df, min_support=0.001, use_colnames=True)
    frequent_itemsets['length'] = frequent_itemsets['itemsets'].apply(lambda x: len(x))
    return frequent_itemsets

def strTolist(string):
    return ast.literal_eval(string)

def main():
    df_normal = pd.read_csv('normal.csv')
    list_of_tokenized_normal_tweets = df_normal['tweets'].apply(strTolist).tolist()
    frequent_itemsets_normal = createFreqItems(list_of_tokenized_normal_tweets)
    
    print(frequent_itemsets_normal)


if __name__ == "__main__":
    main()

