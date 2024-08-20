import os
import sqlite3
import pandas as pd

pd.set_option('display.max_rows', 500)

# Connect to the SQLite database
conn = sqlite3.connect('data/financial_data.db')

# Read the data into a DataFrame
assets = pd.read_sql_query('SELECT * FROM Assets', conn)

# Print the DataFrame
print(assets)
