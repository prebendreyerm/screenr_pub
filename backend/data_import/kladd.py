import pandas as pd
import sqlite3


conn = sqlite3.connect(r'backend\data\financial_data.db')

cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

tables = cursor.fetchall()

for table in tables:
    print(table[0])

conn.close()

#test comment