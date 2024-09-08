import os
import requests
import fmp
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()

api_key = os.getenv('API_KEY')


def update_keyMetricsAnnual():
    tickers = fmp.get_all_tickers()
    table = 'KeyMetricsAnnual'
    fmp.clear_table(table)
    for ticker in tqdm(tickers):
        url = f'https://financialmodelingprep.com/api/v3/key-metrics/{ticker}?period=annual&apikey={api_key}'
        fmp.fetch_and_update_data(url, table, ticker)


def update_keyMetricsQuarter():
    tickers = fmp.get_all_tickers()
    table = 'KeyMetricsQuarter'
    fmp.clear_table(table)
    for ticker in tqdm(tickers):
        url = f'https://financialmodelingprep.com/api/v3/key-metrics/{ticker}?period=Quarter&apikey={api_key}'
        fmp.fetch_and_update_data(url, table, ticker)

def update_ratiosAnnual():
    tickers = fmp.get_all_tickers()
    table = 'RatiosAnnual'
    fmp.clear_table(table)
    for ticker in tqdm(tickers):
        url = f'https://financialmodelingprep.com/api/v3/ratios/{ticker}?period=annual&apikey={api_key}'
        fmp.fetch_and_update_data(url, table, ticker)


def update_ratiosQuarter():
    tickers = fmp.get_all_tickers()
    table = 'RatiosQuarter'
    fmp.clear_table(table)
    for ticker in tqdm(tickers):
        url = f'https://financialmodelingprep.com/api/v3/ratios/{ticker}?period=Quarter&apikey={api_key}'
        fmp.fetch_and_update_data(url, table, ticker)

def update_keyMetricsTTM():
    tickers = fmp.get_all_tickers()
    table = 'KeyMetricsTTM'
    fmp.clear_table(table)
    for ticker in tqdm(tickers):
        url = f'https://financialmodelingprep.com/api/v3/key-metrics-TTM/{ticker}?period=Quarter&apikey={api_key}'
        fmp.fetch_and_update_data(url, table, ticker)

def update_ratiosTTM():
    tickers = fmp.get_all_tickers()
    table = 'RatiosTTM'
    fmp.clear_table(table)
    for ticker in tqdm(tickers):
        url = f'https://financialmodelingprep.com/api/v3/ratios-TTM/{ticker}?period=annual&apikey={api_key}'
        fmp.fetch_and_update_data(url, table, ticker)


def update_FinancialGrowthAnnual():
    tickers = fmp.get_all_tickers()
    table = 'FinancialGrowthAnnual'
    fmp.clear_table(table)
    for ticker in tqdm(tickers):
        url = f'https://financialmodelingprep.com/api/v3/ratios/{ticker}?period=annual&apikey={api_key}'
        fmp.fetch_and_update_data(url, table, ticker)


def update_FinancialGrowthQuarter():
    tickers = fmp.get_all_tickers()
    table = 'FinancialGrowthQuarter'
    fmp.clear_table(table)
    for ticker in tqdm(tickers):
        url = f'https://financialmodelingprep.com/api/v3/FinancialGrowth/{ticker}?period=Quarter&apikey={api_key}'
        fmp.fetch_and_update_data(url, table, ticker)

