import pandas as pd
import spacy
import re
import ast
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import fpgrowth
import numpy as np

def strTolist(string):
    return ast.literal_eval(string)

def output(freqItems, name):
    freqItems[freqItems['length'] == 1].nlargest(100, 'support').to_csv(name + '-length1.csv', index=False)
    freqItems[freqItems['length'] == 2].nlargest(100, 'support').to_csv(name + '-length2.csv', index=False)
    freqItems[freqItems['length'] == 3].nlargest(100, 'support').to_csv(name + '-length3.csv', index=False)
    freqItems[freqItems['length'] == 4].nlargest(100, 'support').to_csv(name + '-length4.csv', index=False)
    freqItems[freqItems['length'] == 5].nlargest(100, 'support').to_csv(name + '-length5.csv', index=False)

def createFreqItems(data):
    te = TransactionEncoder()
    te_ary = te.fit(data).transform(data)
    df = pd.DataFrame(te_ary, columns=te.columns_)
    frequent_itemsets = fpgrowth(df, min_support=0.001, use_colnames=True, max_len=5)
    frequent_itemsets['length'] = frequent_itemsets['itemsets'].apply(lambda x: len(x))
    frequent_itemsets['support'] = frequent_itemsets['support']
    return frequent_itemsets

def process_start(name):
    df_normal = pd.read_csv(name + ".csv")
    list_of_tokenized_tweets = df_normal['tweets'].apply(strTolist).tolist()
    frequent_itemsets = createFreqItems(list_of_tokenized_tweets)
    output(frequent_itemsets, name)

def main():
    process_start('normal')
    process_start('covid')


if __name__ == "__main__":
    main()

