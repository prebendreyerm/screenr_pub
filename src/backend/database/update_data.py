import os
import requests
import backend
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()

api_key = os.getenv('API_KEY')

tickers = backend.get_all_tickers()
table = 'KeyMetricsTTM'

backend.clear_table(table)

for ticker in tqdm(tickers):
    url = f'https://financialmodelingprep.com/api/v3/key-metrics-ttm/{ticker}?apikey={api_key}'
    backend.fetch_and_update_data(url, table, ticker)