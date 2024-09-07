import os
import requests
import fmp
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()

api_key = os.getenv('API_KEY')

tickers = fmp.get_all_tickers()
table = 'RatiosAnnually'

# fmp.clear_table(table)

# for ticker in tqdm(tickers):
#     url = f'https://financialmodelingprep.com/api/v3/key-metrics-ttm/{ticker}?apikey={api_key}'
#     fmp.fetch_and_update_data(url, table, ticker)

for ticker in tqdm(tickers):
    url = f'https://financialmodelingprep.com/api/v3/ratios/{ticker}?period=Annual&apikey={api_key}'
    fmp.fetch_and_update_data(url, table, ticker)