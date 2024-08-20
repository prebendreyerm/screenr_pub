import pandas as pd
import sqlite3

# Load the CSV file into a DataFrame
df = pd.read_csv(r'C:\Users\Preben\OneDrive\Dokumenter\GitHub\Screenr\data\Stock_lists\stonks.csv')

# Drop the 'Unnamed: 0' column if it exists
if 'Unnamed: 0' in df.columns:
    df = df.drop(columns=['Unnamed: 0'])

df = df.dropna(subset=['name'])
df = df.dropna(subset=['symbol'])
df = df.dropna(subset=['sector'])
df = df.dropna(subset=['industry'])


# Connect to SQLite database
conn = sqlite3.connect(r'C:\Users\Preben\OneDrive\Dokumenter\GitHub\Screenr\data\financial_data.db')

# Insert DataFrame into SQLite table
df.to_sql('Assets', conn, if_exists='append', index=False)


# Commit changes and close the connection
conn.commit()
conn.close()
