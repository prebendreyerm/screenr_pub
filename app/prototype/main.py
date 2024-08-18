import os
import pandas as pd
import streamlit as st
import sqlite3

conn = sqlite3.connect(r'C:\Users\Preben\OneDrive\Dokumenter\GitHub\Screenr\data\financial_data.db')

df = pd.read_sql_query('SELECT * FROM KeyMetricsTTM', conn)

conn.close()

st.write(df)