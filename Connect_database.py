import sqlite3






# Connect to the SQLite database

def db_connection():
    # Path to the SQLite database file
    db_file_path = '/Users/duweicheng/SQL/2017-2024_sale_record.db'
    try:
        conn = sqlite3.connect(db_file_path)
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
    return conn