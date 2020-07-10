import pandas as pd
import spacy
import re
import ast
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import fpgrowth
import numpy as np

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