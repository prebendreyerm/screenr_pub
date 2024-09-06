import pandas as pd
import sqlite3


conn = sqlite3.connect(r'backend\data\financial_data.db')
df = pd.read_sql_query('SELECT * FROM Assets', conn)

print(df)