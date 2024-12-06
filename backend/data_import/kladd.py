import sqlite3
import pandas as pd
import requests
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv('API_KEY')
# pd.set_option('display.max_rows', None)

def get_db_connection():
    conn = sqlite3.connect(r'backend\data\financial_data.db')
    return conn

def list_tables():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Query to get all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    # Check each table for a 'price' column
    for table in tables:
        table_name = table[0]
        # Query to get column names for the current table
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        
        # Check if any column is named 'price'
        if any(column[1] == 'sector' for column in columns):
            print(f"Table '{table_name}' has a 'sector' column.")
        else:
            print(f"Table '{table_name}' does not have a 'sector' column.")

    conn.close()

def get_table(table):
    conn = get_db_connection()
    cursor = conn.cursor()
    df = pd.read_sql_query(f'SELECT * FROM {table}', conn)
    return df


def delete_tables(table_name):
    # Path to the database
    db_path = "backend/data/financial_data.db"

    # Connect to the database
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    # Drop the table
    cursor.execute(f"DROP TABLE IF EXISTS {table_name};")
    print(f"Table {table_name} deleted (if it existed).")

    # Commit changes and close connection
    connection.commit()
    connection.close()

    print("Finished deleting the table.")


delete_tables('ScoringStrategies')


print(get_table('ScoringStrategies'))
