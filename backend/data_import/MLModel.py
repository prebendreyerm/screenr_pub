import os
# import tensorflow as tf
import sqlite3
import pandas as pd
from dotenv import load_dotenv
from matplotlib import pyplot as plt
import numpy as np


load_dotenv()

api_key = os.getenv('API_KEY')


def get_db_connection():
    conn = sqlite3.connect(r'backend\data\financial_data.db')
    return conn

# Function to fetch table from database
def get_table(table):
    conn = get_db_connection()
    cursor = conn.cursor()
    df = pd.read_sql_query(f'SELECT * FROM {table}', conn)
    return df

df_ratios = get_table('RatiosAnnual')
print(df_ratios.columns)

# Drop NaN values and check for extreme values
df_free_cash_flow = df_ratios.freeCashFlowPerShare.dropna()

min_value = df_free_cash_flow.min()
shift_constant = abs(min_value) + 1  # Shift to ensure all values are positive

# Apply the transformation
transformed_data = np.log(df_free_cash_flow + shift_constant)

filtered_data = df_free_cash_flow[df_free_cash_flow > 0]  # Filter to positive values

plt.figure(figsize=(10, 6))
plt.hist(filtered_data, bins=50, edgecolor='black')
plt.xlabel('Free Cash Flow Per Share (Filtered)')
plt.ylabel('Frequency')
plt.title('Histogram of Filtered Free Cash Flow Per Share')
plt.show()


