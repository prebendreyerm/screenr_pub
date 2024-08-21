import os
import sqlite3
import pandas as pd
import numpy as np

pd.set_option('display.max_rows', 500)

conn = sqlite3.connect(r'C:\Users\Preben\OneDrive\Dokumenter\GitHub\screenr_pub\backend\data\financial_data.db')
ratiosTTM = pd.read_sql_query('SELECT * FROM RatiosTTM', conn)
assets = pd.read_sql_query('SELECT * FROM Assets', conn)


df = pd.merge(assets, ratiosTTM, on='symbol', how='left')
df.rename(columns={'dividendYielTTM': 'dividendYieldTTM'}, inplace=True)
df.fillna(0, inplace=True)

scoring_baseline = pd.read_csv(r'C:\Users\Preben\OneDrive\Dokumenter\GitHub\screenr_pub\backend\data\Baselines\baseline_technology.csv')
scoring_baseline['scoring_columns'] = scoring_baseline['scoring_columns'] + 'TTM'


def calculate_score(dataframe, list_of_columns, list_of_ascending_boolean):
    dataframe['score'] = 0
    for column, ascending in zip(list_of_columns, list_of_ascending_boolean):
        dataframe['score'] += dataframe[column].rank(ascending=ascending)
    dataframe['score'] = dataframe['score'] / len(list_of_columns)
    dataframe_max_scaled = dataframe.copy()
    dataframe_max_scaled['score'] = dataframe_max_scaled['score'] / dataframe_max_scaled['score'].abs().max()
    return dataframe_max_scaled

if __name__ == '__main__':
    print('yes')


# scores = calculate_score(df, scoring_baseline['scoring_columns'], scoring_baseline['booleans'])
# print(scores)

# aapl_row = scores[scores['symbol'] == 'AAPL']
# print(aapl_row)
