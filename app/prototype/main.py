import os
import pandas as pd
import streamlit as st
import sqlite3

conn = sqlite3.connect(r'data\financial_data.db')

df = pd.read_sql_query('SELECT * FROM RatiosTTM', conn)

conn.close()

st.write(df)