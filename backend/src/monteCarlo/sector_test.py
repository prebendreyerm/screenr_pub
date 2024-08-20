import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Connect to the SQLite database
conn = sqlite3.connect('stock_data_full.db')

# Function to fetch data as DataFrame
def fetch_data_as_dataframe(query):
    try:
        with sqlite3.connect('stock_data_full.db') as conn:
            df = pd.read_sql_query(query, conn)
            return df
    except sqlite3.Error as e:
        print(f"An error occurred while fetching data: {e}")
        return None

# Fetch data into a DataFrame
query = "SELECT * FROM stock_data"
df = fetch_data_as_dataframe(query)

# Drop rows with NaN values
df = df.dropna()

# Ensure the DataFrame is sorted by ticker and year
df = df.sort_values(by=['year', 'ticker'])

# Normalize sector names by removing leading/trailing spaces and converting to title case
df['sector'] = df['sector'].str.strip().str.title()

# Remove duplicates from sector list
sectors = df['sector'].unique()
sectors = [sector for sector in sectors if sector != 'Energy']

# Define the columns that can be used for scoring
scoring_columns = [
    'enterpriseValueMultiple', 'returnOnAssets', 'revenue_growth', 
    'debtRatio', 'freeCashFlowPerShare', 'currentRatio', 'quickRatio', 
    'cashRatio', 'daysOfSalesOutstanding', 'daysOfInventoryOutstanding', 
    'operatingCycle', 'daysOfPayablesOutstanding', 'cashConversionCycle', 
    'grossProfitMargin', 'operatingProfitMargin', 'pretaxProfitMargin', 
    'netProfitMargin', 'effectiveTaxRate', 'returnOnEquity', 
    'returnOnCapitalEmployed', 'netIncomePerEBT', 'ebtPerEbit', 
    'ebitPerRevenue', 'debtEquityRatio', 'longTermDebtToCapitalization', 
    'totalDebtToCapitalization', 'interestCoverage', 'cashFlowToDebtRatio', 
    'companyEquityMultiplier', 'receivablesTurnover', 'payablesTurnover', 
    'inventoryTurnover', 'fixedAssetTurnover', 'assetTurnover', 
    'operatingCashFlowPerShare', 'cashPerShare', 'payoutRatio', 
    'operatingCashFlowSalesRatio', 'freeCashFlowOperatingCashFlowRatio', 
    'cashFlowCoverageRatios', 'shortTermCoverageRatios', 
    'capitalExpenditureCoverageRatio', 'dividendPaidAndCapexCoverageRatio', 
    'dividendPayoutRatio', 'priceBookValueRatio', 'priceToBookRatio', 
    'priceToSalesRatio', 'priceEarningsRatio', 'priceToFreeCashFlowsRatio', 
    'priceToOperatingCashFlowsRatio', 'priceCashFlowRatio', 
    'priceEarningsToGrowthRatio', 'priceSalesRatio', 'dividendYield', 
    'priceFairValue'
]

# Function to calculate scores and perform backtesting
def calculate_scores_and_backtest(df, scoring_columns, ascending_flags):
    df = df.copy()

    ranks = [df[col].rank(pct=True, ascending=asc) for col, asc in zip(scoring_columns, ascending_flags)]
    df['score'] = sum(ranks) / len(scoring_columns)

    initial_capital = 100
    total_value = initial_capital
    investment_strategy = []
    trades_each_year = []

    years = df['year'].unique()

    for year in sorted(years)[:-1]:
        current_year_data = df[df['year'] == year]
        if current_year_data.empty:  # Skip if no data for current year
            continue
        next_year_data = df[df['year'] == year + 1]

        # Select the top stock in the current year
        best_stock = current_year_data.sort_values(by='score').iloc[0]
        next_year_stock_data = next_year_data[next_year_data['ticker'] == best_stock['ticker']]

        # Check if data exists for the best stock in the next year
        if next_year_stock_data.empty:
            continue

        # Process the selected stock (buying, selling, etc.)
        buy_price = best_stock['stock_price']
        shares_bought = total_value / buy_price
        sell_price = next_year_stock_data['stock_price'].values[0]
        total_value = shares_bought * sell_price

        gain_pct = (sell_price - buy_price) / buy_price * 100  # Calculate gain as a percentage
        trades_each_year.append({
            'year': year,
            'ticker': best_stock['ticker'],
            'buy_price': buy_price,
            'sell_price': sell_price,
            'shares_bought': shares_bought,
            'total_value': total_value,
            'gain_pct': gain_pct
        })

    # Calculate overall return percentage
    overall_return_pct = ((total_value - initial_capital) / initial_capital) * 100

    return pd.DataFrame(trades_each_year), total_value, overall_return_pct

# Select a sector to analyze (replace 'Technology' with your chosen sector)
sector_to_analyze = 'Consumer Services'
sector_df = df[df['sector'] == sector_to_analyze]

try:
    trades_each_year, total_value, overall_return_pct = calculate_scores_and_backtest(
        sector_df, scoring_columns, [True] * len(scoring_columns))
    
    print(f"\nTrades Each Year for {sector_to_analyze} Sector:")
    print(pd.DataFrame(trades_each_year))

    print(f"\nTotal Initial Capital: ${100:.2f}")
    print(f"Total Final Value: ${total_value:.2f}")
    print(f"Total Overall Return Percentage: {overall_return_pct:.2f}%")

    # Plot cumulative returns for the selected sector
    plt.figure(figsize=(12, 8))
    plt.plot(trades_each_year['year'], trades_each_year['total_value'], marker='o', label=f'{sector_to_analyze} Sector')

    plt.title(f'Cumulative Returns for {sector_to_analyze} Sector')
    plt.xlabel('Year')
    plt.ylabel('Total Value')
    plt.yscale('log')
    plt.legend()
    plt.grid(True)
    plt.show()

except Exception as e:
    print(f"Error processing sector {sector_to_analyze}: {e}")
