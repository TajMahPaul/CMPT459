import pandas as pd
import sqlite3

def main():
    conn = sqlite3.connect('./tweets/covid.db')
    c = conn.cursor()

    df = pd.read_sql_query("select * from tweets", conn)
    df = df[df["country"] == "Canada"]
    print(df.count())

if __name__ == "__main__":
    main()