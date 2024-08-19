import os
import sqlite3
import pandas as pd
import numpy as np

pd.set_option('display.max_rows', 500)

conn = sqlite3.connect(r'data\financial_data.db')
ratiosTTM = pd.read_sql_query('SELECT * FROM RatiosTTM', conn)
assets = pd.read_sql_query('SELECT * FROM Assets', conn)


df = pd.merge(assets, ratiosTTM, on='symbol', how='left')
df.rename(columns={'dividendYielTTM': 'dividendYieldTTM'}, inplace=True)
df.fillna(0, inplace=True)

scoring_baseline = pd.read_csv(r'C:\Users\Preben\OneDrive\Dokumenter\GitHub\Screenr\data\Baselines\baseline.csv')
scoring_baseline['scoring_columns'] = scoring_baseline['scoring_columns'] + 'TTM'


def calculate_score(dataframe, list_of_columns, list_of_ascending_boolean):
    dataframe['score'] = 0
    for column, ascending in zip(list_of_columns, list_of_ascending_boolean):
        dataframe['score'] += dataframe[column].rank(ascending=ascending)
    dataframe['score'] = dataframe['score'] / len(list_of_columns)
    dataframe_max_scaled = dataframe.copy()
    dataframe_max_scaled['score'] = dataframe_max_scaled['score'] / dataframe_max_scaled['score'].abs().max()
    return dataframe_max_scaled


calculate_score(df, np.array(scoring_baseline['scoring_columns']), np.array(scoring_baseline['booleans']))

df = df.sort_values(by='score', ascending=False)

print(df.head(500))