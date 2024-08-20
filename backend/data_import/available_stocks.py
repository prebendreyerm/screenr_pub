import os
import pandas as pd
import requests
from dotenv import load_dotenv
from tqdm import tqdm
import time

load_dotenv()

api_key = os.getenv('API_KEY')

url = f'https://financialmodelingprep.com/api/v3/available-traded/list?apikey={api_key}'
r = requests.get(url, timeout=10)
available_traded = r.json()

available_exchanges = ['NYSE', 'HEL', 'OSL', 'STO', 'LSE', 'CPH', 'XETRA', 'NASDAQ', 'TSX', 'AMEX']

df = pd.DataFrame(available_traded)
df = df[(df['type'] == 'stock') & (df['exchangeShortName'].isin(available_exchanges))]

def get_industry_sector(ticker):
    '''Getting the industry and sector for the different assets '''
    url = f'https://financialmodelingprep.com/api/v3/profile/{ticker}?apikey={api_key}'
    r = requests.get(url, timeout=10)
    r = r.json()[0]
    industry = r['industry']
    sector = r['sector']
    return industry, sector

# Initialize empty lists to store industries and sectors
industries = []
sectors = []

# Iterate over each symbol in the DataFrame with tqdm to track progress
for symbol in tqdm(df['symbol'], desc="Fetching industry and sector data"):
    industry, sector = get_industry_sector(symbol)
    industries.append(industry)
    sectors.append(sector)
    
    # Respect API rate limit by adding a delay
    # time.sleep(0.2)  # 0.2 seconds delay means 5 requests per second, or 300 requests per minute

# Assign the industries and sectors to the DataFrame
df['industry'] = industries
df['sector'] = sectors

df.to_csv('stonks.csv')

# Print the updated DataFrame
print(df)
