import os
import sqlite3

TWEET_ID_DIR = "./tweet_ids"


def main():
    files = os.listdir(TWEET_ID_DIR)
    list_to_insert = []
    
    for file in files:
        abs_path = os.path.dirname(os.path.abspath((TWEET_ID_DIR))) + TWEET_ID_DIR.replace(".", "") + "/" + file
        tupl_to_insert = (abs_path, False)
        list_to_insert.append(tupl_to_insert)

    conn = sqlite3.connect('covid.db')
    c = conn.cursor()
    try:
        c.executemany('INSERT INTO files VALUES (null,?,?)', list_to_insert)
        conn.commit()
    except Exception as e:
        raise(e)
    finally:
        # close connection and cursor
        c.close()
        conn.close() 

if __name__ == "__main__":
    main()