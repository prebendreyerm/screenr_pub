import sqlite3
import pandas as pd

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
        if any(column[1] == 'price' for column in columns):
            print(f"Table '{table_name}' has a 'price' column.")
        else:
            print(f"Table '{table_name}' does not have a 'price' column.")

    conn.close()

def get_table(table):
    conn = get_db_connection()
    cursor = conn.cursor()
    df = pd.read_sql_query(f'SELECT * FROM {table}', conn)
    return df


list_tables()
# df_prices = get_table('Prices')
# df_ratios = get_table('RatiosTTM')

# # Merge the two DataFrames on the 'symbol' column
# merged_df = pd.merge(df_prices[['symbol', 'name', 'price']], df_ratios[['symbol', 'freeCashFlowPerShareTTM']], on='symbol')

# # Calculate the free cash flow percentage
# merged_df['freeCashFlowPercentage'] = (merged_df['freeCashFlowPerShareTTM'] / merged_df['price'])

# # Filter out rows where freeCashFlowPercentage is negative or above 1
# filtered_df = merged_df[merged_df['freeCashFlowPercentage'].between(0, 1)]

# # Sort the filtered DataFrame by free cash flow percentage in descending order
# sorted_df = filtered_df.sort_values(by='freeCashFlowPercentage', ascending=False)

# # Display the sorted DataFrame with symbol, name, price, free cash flow per share, and percentage
# print(sorted_df[['symbol', 'name', 'price', 'freeCashFlowPerShareTTM', 'freeCashFlowPercentage']])




# # Filter for the row where the symbol is 'AAPL'
# aapl_row = sorted_df[sorted_df['symbol'] == 'AAPL']

# # Print the row
# print(aapl_row[['symbol', 'name', 'price', 'freeCashFlowPerShareTTM', 'freeCashFlowPercentage']])
