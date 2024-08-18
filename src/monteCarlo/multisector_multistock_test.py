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
    trades = []  # List to store individual trades

    years = df['year'].unique()

    for year in sorted(years)[:-1]:
        current_year_data = df[df['year'] == year]
        if current_year_data.empty:  # Skip if no data for current year
            continue
        next_year_data = df[df['year'] == year + 1]

        # Select the top 3 stocks in the current year per sector
        top_stocks = current_year_data.groupby('sector').apply(lambda x: x.nlargest(3, 'score')).reset_index(drop=True)

        for index, top_stock in top_stocks.iterrows():
            next_year_stock_data = next_year_data[next_year_data['ticker'] == top_stock['ticker']]

            # Check if data exists for the top stock in the next year
            if next_year_stock_data.empty:
                continue

            # Process the selected stock (buying, selling, etc.)
            buy_price = top_stock['stock_price']
            shares_bought = total_value / buy_price
            total_value = 0  # Reset total_value to simulate selling and buying next year

            sell_price = next_year_stock_data['stock_price'].values[0]
            total_value += shares_bought * sell_price

            gain_pct = (sell_price - buy_price) / buy_price * 100  # Calculate gain as a percentage
            investment_strategy.append({
                'year': year,
                'ticker': top_stock['ticker'],
                'buy_price': buy_price,
                'sell_price': sell_price,
                'total_value': total_value,
                'gain_pct': gain_pct
            })

            # Record individual trades
            trades.append({
                'year': year,
                'ticker': top_stock['ticker'],
                'buy_price': buy_price,
                'sell_price': sell_price,
                'shares_bought': shares_bought
            })

    # Calculate overall return percentage
    overall_return_pct = ((total_value - initial_capital) / initial_capital) * 100

    return pd.DataFrame(investment_strategy), total_value, overall_return_pct, trades


# Initialize the results dictionary
sector_strategy_results = {}

# Perform the analysis for each sector
for sector in sectors:
    print(f"Analyzing sector: {sector}")
    sector_df = df[df['sector'] == sector]
    
    try:
        investment_results, total_value, overall_return_pct, trades = calculate_scores_and_backtest(
            sector_df, scoring_columns, [True] * len(scoring_columns))
        
        sector_strategy_results[sector] = {
            'investment_results': investment_results,
            'total_value': total_value,
            'overall_return_pct': overall_return_pct,
            'trades': trades  # Include trades in the results
        }
    except Exception as e:
        print(f"Error processing sector {sector}: {e}")
        continue

# Summarize results across all sectors
total_initial_capital = 100 * len(sectors)
total_final_value = sum(result['total_value'] for result in sector_strategy_results.values())
total_overall_return_pct = ((total_final_value - total_initial_capital) / total_initial_capital) * 100

print(f"\nTotal Initial Capital: ${total_initial_capital:.2f}")
print(f"Total Final Value: ${total_final_value:.2f}")
print(f"Total Overall Return Percentage: {total_overall_return_pct:.2f}%")

# Print trades for each year
for sector, results in sector_strategy_results.items():
    print(f"\nTrades for sector: {sector}")
    trades_df = pd.DataFrame(results['trades'])
    print(trades_df)

# Plot cumulative returns for all sectors
plt.figure(figsize=(12, 8))
for sector, results in sector_strategy_results.items():
    plt.plot(results['investment_results']['year'], results['investment_results']['total_value'], marker='o', label=f'{sector} Sector')

plt.title('Cumulative Returns for All Sectors')
plt.xlabel('Year')
plt.ylabel('Total Value')
plt.yscale('log')
plt.legend()
plt.grid(True)
plt.show()
