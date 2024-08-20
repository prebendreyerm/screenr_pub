import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import random
import numpy as np
from tqdm import tqdm

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

# Fetch data into a DataFrame for a specific sector (e.g., Technology)
def fetch_sector_data(sector):
    query = f"SELECT * FROM stock_data WHERE sector = '{sector}'"
    df = fetch_data_as_dataframe(query)
    return df

# Drop rows with NaN values
def clean_data(df):
    df = df.dropna()
    return df

# Ensure the DataFrame is sorted by ticker and year
def sort_data(df):
    df = df.sort_values(by=['year', 'ticker'])
    return df

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
    years = df['year'].unique()

    for year in sorted(years)[:-1]:
        current_year_data = df[df['year'] == year]
        if current_year_data.empty:  # Skip if no data for current year
            continue
        next_year_data = df[df['year'] == year + 1]

        # Sort and iterate over all stocks in the current year
        for rank, row in current_year_data.sort_values(by='score').iterrows():
            best_stock = row
            next_year_stock_data = next_year_data[next_year_data['ticker'] == best_stock['ticker']]

            # Check if data exists for the best stock in the next year
            if next_year_stock_data.empty:
                continue  # Skip to next stock in the current year

            # Process the selected stock (buying, selling, etc.)
            buy_price = best_stock['stock_price']
            shares_bought = total_value / buy_price
            total_value = 0
            
            sell_price = next_year_stock_data['stock_price'].values[0]
            total_value += shares_bought * sell_price

            gain_pct = (sell_price - buy_price) / buy_price * 100  # Calculate gain as a percentage
            investment_strategy.append({
                'year': year,
                'ticker': best_stock['ticker'],
                'buy_price': buy_price,
                'sell_price': sell_price,
                'total_value': total_value,
                'gain_pct': gain_pct
            })

            break

    # Calculate overall return percentage
    overall_return_pct = ((total_value - initial_capital) / initial_capital) * 100

    return pd.DataFrame(investment_strategy), total_value, overall_return_pct, scoring_columns

# Initialize the results dictionary
strategy_results = {}

# Define the initial strategies
initial_strategies = {
    'Strategy 1': ['enterpriseValueMultiple', 'returnOnAssets', 'revenue_growth'],
    'Strategy 2': ['returnOnAssets', 'revenue_growth'],
    'Strategy 3': ['enterpriseValueMultiple', 'returnOnAssets'],
    'Strategy 4': ['enterpriseValueMultiple', 'returnOnAssets', 'revenue_growth', 'debtRatio', 'freeCashFlowPerShare']
}

# Calculate scores and backtest for the initial strategies within a specific sector (e.g., 'Technology')
sector = 'Telecommunications'
df_sector = fetch_sector_data(sector)
df_sector = clean_data(df_sector)
df_sector = sort_data(df_sector)

for strategy_name, columns in initial_strategies.items():
    investment_results, total_value, overall_return_pct, strategy_columns = calculate_scores_and_backtest(df_sector, columns, [True] + [False] * (len(columns) - 1))
    strategy_results[strategy_name] = (investment_results, total_value, overall_return_pct, strategy_columns)

# Function to compare strategies with baseline and potentially update baseline
def compare_with_baseline(strategy_results, baseline_strategy_name, overall_return_pct_baseline, baseline_std_dev):
    updated = False
    for strategy_name, (investment_results, total_value, overall_return_pct, strategy_columns) in strategy_results.items():
        if overall_return_pct > overall_return_pct_baseline and np.std(investment_results['gain_pct']) < baseline_std_dev:
            # Update baseline.csv
            df_baseline = pd.DataFrame({
                'Strategy Name': [strategy_name],
                'Columns Used': [strategy_columns],
                'Ranking Direction': [[True] + [False] * (len(strategy_columns) - 1)]
            })
            df_baseline.to_csv(f'baseline_{sector}.csv', index=False)
            print(f"Baseline strategy updated to {strategy_name} due to superior returns and stability.")
            updated = True
            break  # Exit after finding a better baseline
    return updated

# Load the baseline strategy from baseline.csv if available
try:
    df_baseline = pd.read_csv(f'baseline_{sector}.csv')
    baseline_strategy_name = df_baseline['Strategy Name'].iloc[0]
    baseline_strategy_columns = eval(df_baseline['Columns Used'].iloc[0])  # Convert string representation back to list
    baseline_strategy_ranking_direction = eval(df_baseline['Ranking Direction'].iloc[0])
    
    # Perform backtesting for the baseline strategy
    investment_results_baseline, total_value_baseline, overall_return_pct_baseline, strategy_columns_baseline = calculate_scores_and_backtest(df_sector, baseline_strategy_columns, baseline_strategy_ranking_direction)
    baseline_std_dev = np.std(investment_results_baseline['gain_pct'])
except FileNotFoundError:
    print("Baseline file not found. Initializing new baseline.")
    baseline_strategy_name = None
    overall_return_pct_baseline = -np.inf
    baseline_std_dev = np.inf

# Generate multiple simulations (e.g., 1000 simulations)
num_simulations = 200
tested_strategies = set()

for i in tqdm(range(num_simulations)):
    num_columns = random.randint(2, len(scoring_columns))
    selected_columns = random.sample(scoring_columns, num_columns)
    ascending_flags = [random.choice([True, False]) for _ in selected_columns]

    # Create a unique identifier for the strategy to avoid duplicates
    strategy_identifier = (tuple(selected_columns), tuple(ascending_flags))

    if strategy_identifier in tested_strategies:
        continue  # Skip if this strategy has already been tested

    tested_strategies.add(strategy_identifier)
    strategy_name = f'Simulation_{i + 1}'

    # Calculate scores and backtest for the simulated strategy
    investment_results, total_value, overall_return_pct, strategy_columns = calculate_scores_and_backtest(df_sector, selected_columns, ascending_flags)
    strategy_results[strategy_name] = (investment_results, total_value, overall_return_pct, strategy_columns)

    # Compare with baseline and potentially update baseline.csv
    if compare_with_baseline(strategy_results, baseline_strategy_name, overall_return_pct_baseline, baseline_std_dev):
        baseline_strategy_name = strategy_name
        overall_return_pct_baseline = overall_return_pct
        baseline_std_dev = np.std(investment_results['gain_pct'])

# Close the database connection
conn.close()

# Plotting the yearly returns for the baseline strategy
if baseline_strategy_name:
    yearly_returns = investment_results_baseline.groupby('year')['gain_pct'].mean()

    plt.figure(figsize=(12, 8))
    yearly_returns.plot(kind='bar')
    plt.xlabel('Year')
    plt.ylabel('Return (%)')
    plt.title('Yearly Returns of Baseline Strategy')
    plt.show()

print("Simulation and comparison with baseline completed.")
