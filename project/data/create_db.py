import sqlite3
conn = sqlite3.connect('covid.db')

def main():
    c = conn.cursor()
    
    try:
        # Create table
    c.execute('''CREATE TABLE files (path text, is_processed bool)''')
    # c.execute('''CREATE TABLE tweets (date_time text, location string, tweet string)''')
    except Exception as e:
        raise(e)
    finally:


if __name__ == "__main__":
    main()