import os
import sqlite3
import pandas
import itertools

def main():
    conn = sqlite3.connect('covid.db')
    c = conn.cursor()

    try:
        c.execute('''SELECT * FROM files WHERE is_processed=?''', (False,))
        files = c.fetchall()
        for file in files:
            c.execute('''SELECT tweet_id from tweet_ids''')
            current_tweet_ids = c.fetchall()
            current_tweet_ids = list(itertools.chain(*current_tweet_ids))

            try:
                file_id = file[0]
                path = file[1]
                df = pandas.read_csv(path, names=['tweet_id'], index_col=False)
                df['tweet_id'] = df['tweet_id'].astype(str)
                if(current_tweet_ids):
                    df = df[~df['tweet_id'].isin(current_tweet_ids)]

                df['is_processed'] = 0
                df.to_sql('tweet_ids', con= conn, index=False, if_exists='append')
                c.execute('''UPDATE files set is_processed=? WHERE id=?''', (True,file_id))
                conn.commit()
                
            except Exception as e:
                print("failure to insert: {} \n".format(e))
                break
    except Exception as e:
        raise(e)
    finally:
        # close connection and cursor
        c.close()
        conn.close()  

if __name__ == "__main__":
    main()