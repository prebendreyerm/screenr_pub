import sqlite3
import pandas as pd

def get_db_connection():
    conn = sqlite3.connect(r'backend\data\financial_data.db')
    return conn

def list_tables():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Query to get all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    conn.close()

    # Print out each table name
    for table in tables:
        print(table[0])

def get_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    df = pd.read_sql_query('SELECT * FROM Prices', conn)
    return df

df = get_table()
print(df)