import sqlite3

def main():
    conn = sqlite3.connect('covid.db')
    c = conn.cursor()
    
    try:
        # Create tables
        c.execute('''CREATE TABLE files (id integer PRIMARY KEY AUTOINCREMENT, path text, is_processed bool)''')
        c.execute('''CREATE TABLE tweet_ids (tweet_id text, is_processed bool)''')
        c.execute('''CREATE TABLE tweets (date_time text, location_name text, country text, tweet_text text)''')
    except Exception as e:
        raise(e)
    finally:
        # close connection and cursor
        c.close()
        conn.close()

if __name__ == "__main__":
    main()