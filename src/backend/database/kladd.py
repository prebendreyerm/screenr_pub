import sqlite3
import pandas as pd

pd.set_option('display.max_rows', 500)


conn = sqlite3.connect(r'C:\Users\Preben\OneDrive\Dokumenter\GitHub\Screenr\data\financial_data.db')

df = pd.read_sql_query('SELECT * FROM AnnualRatios', conn)
df = df[df['calendarYear']=='1995']
print(df)