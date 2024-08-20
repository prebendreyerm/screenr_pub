import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import random
import numpy as np
from tqdm import tqdm  # Import tqdm for progress tracking

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

        # Sort stocks by score in ascending order
        sorted_data = current_year_data.sort_values(by='score', ascending=True)

        # Select the second best stock if available
        if len(sorted_data) > 1:
            second_best_stock = sorted_data.iloc[2]  # Select the second row (index 1)
            next_year_stock_data = next_year_data[next_year_data['ticker'] == second_best_stock['ticker']]

            # Check if data exists for the second best stock in the next year
            if not next_year_stock_data.empty:
                # Process the selected stock (buying, selling, etc.)
                buy_price = second_best_stock['stock_price']
                shares_bought = total_value / buy_price
                total_value = 0  # Reset total_value to simulate selling and buying next year

                sell_price = next_year_stock_data['stock_price'].values[0]
                total_value += shares_bought * sell_price

                gain_pct = (sell_price - buy_price) / buy_price * 100  # Calculate gain as a percentage
                investment_strategy.append({
                    'year': year,
                    'ticker': second_best_stock['ticker'],
                    'buy_price': buy_price,
                    'sell_price': sell_price,
                    'total_value': total_value,
                    'gain_pct': gain_pct
                })

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

# Calculate scores and backtest for the initial strategies
for strategy_name, columns in initial_strategies.items():
    investment_results, total_value, overall_return_pct, strategy_columns = calculate_scores_and_backtest(df, columns, [True] + [False] * (len(columns) - 1))
    strategy_results[strategy_name] = (investment_results, total_value, overall_return_pct, strategy_columns)

# Generate a strategy using all scoring_columns
all_columns_strategy_name = 'Strategy All Columns'
all_columns_strategy = scoring_columns
investment_results_all, total_value_all, overall_return_pct_all, strategy_columns_all = calculate_scores_and_backtest(df, all_columns_strategy, [True] * len(scoring_columns))

# Add all columns strategy to results
strategy_results[all_columns_strategy_name] = (investment_results_all, total_value_all, overall_return_pct_all, strategy_columns_all)

# Read the baseline.csv file into a DataFrame
df_baseline = pd.read_csv('baseline.csv')

# Extract strategy details from the DataFrame
baseline_strategy_name = df_baseline['Strategy Name'].iloc[0]
baseline_strategy_columns = eval(df_baseline['Columns Used'].iloc[0])  # Convert string representation back to list
baseline_strategy_ranking_direction = eval(df_baseline['Ranking Direction'].iloc[0]) 
investment_results_baseline, total_value_baseline, overall_return_pct_baseline, strategy_columns_baseline = calculate_scores_and_backtest(df, baseline_strategy_columns, baseline_strategy_ranking_direction)

# Add baseline strategy to results
strategy_results[baseline_strategy_name] = (investment_results_baseline, total_value_baseline, overall_return_pct_baseline, strategy_columns_baseline)

# Store ranking direction for strategies
strategy_ranking_direction = {
    baseline_strategy_name: baseline_strategy_ranking_direction
}

# Function to compare strategies with baseline
# Function to compare strategies with baseline
def compare_with_baseline(strategy_results, baseline_strategy_name, overall_return_pct_baseline, baseline_std_dev):
    for strategy_name, (investment_results, total_value, overall_return_pct, strategy_columns) in strategy_results.items():
        if overall_return_pct > overall_return_pct_baseline and np.std(investment_results['gain_pct']) < baseline_std_dev:
            # Update baseline.csv
            df_baseline = pd.DataFrame({
                'Strategy Name': [strategy_name],
                'Columns Used': [strategy_columns],
                'Ranking Direction': [strategy_ranking_direction[strategy_name]]
            })
            df_baseline.to_csv('baseline.csv', index=False)
            print(f"Baseline strategy updated to {strategy_name} due to superior returns and stability.")
            return  # Exit after finding a better baseline

# Generate 1000 different strategies with tqdm for progress tracking
tested_strategies = set()

for i in tqdm(range(1, 101)):
    num_columns = random.randint(2, len(scoring_columns))
    selected_columns = random.sample(scoring_columns, num_columns)
    ascending_flags = [random.choice([True, False]) for _ in selected_columns]

    # Create a unique identifier for the strategy to avoid duplicates
    strategy_identifier = (tuple(selected_columns), tuple(ascending_flags))

    if strategy_identifier in tested_strategies:
        continue  # Skip if this strategy has already been tested

    tested_strategies.add(strategy_identifier)
    strategy_name = f'Strategy {i + 4}'
    investment_results, total_value, overall_return_pct, strategy_columns = calculate_scores_and_backtest(df, selected_columns, ascending_flags)
    strategy_results[strategy_name] = (investment_results, total_value, overall_return_pct, strategy_columns)
    strategy_ranking_direction[strategy_name] = ascending_flags

    # Early exit after finding a better and more stable strategy
    if compare_with_baseline(strategy_results, baseline_strategy_name, overall_return_pct_baseline, np.std(investment_results_baseline['gain_pct'])):
        break

# Sort strategies by total value in descending order and select top 10
sorted_strategies = sorted(strategy_results.items(), key=lambda x: x[1][1], reverse=True)[:10]

# Calculate stability (standard deviation of gains per trade) for top 10 strategies
stable_strategies = []
for strategy_name, (investment_results, total_value, overall_return_pct, columns_used) in sorted_strategies:
    gains_pct = investment_results['gain_pct']
    std_dev = np.std(gains_pct)
    stable_strategies.append((strategy_name, investment_results, total_value, overall_return_pct, std_dev, columns_used))

# Find the best performing and most stable strategies
best_strategy_name, best_investment_results, best_total_value, best_return_pct, best_columns = sorted_strategies[0][0], sorted_strategies[0][1][0], sorted_strategies[0][1][1], sorted_strategies[0][1][2], sorted_strategies[0][1][3]

most_stable_strategy_name, most_stable_investment_results, most_stable_total_value, most_stable_return_pct, most_stable_std_dev, most_stable_columns = sorted(stable_strategies, key=lambda x: x[4])[0][:6]
most_stable_strategy_ranking_direction = strategy_ranking_direction[most_stable_strategy_name]

# Sort strategies by total value in descending order and select top 10
sorted_strategies = sorted(strategy_results.items(), key=lambda x: x[1][1], reverse=True)[:10]

# Calculate stability (standard deviation of gains per trade) for top 10 strategies
stable_strategies = []
for strategy_name, (investment_results, total_value, overall_return_pct, columns_used) in sorted_strategies:
    gains_pct = investment_results['gain_pct']
    std_dev = np.std(gains_pct)
    stable_strategies.append((strategy_name, investment_results, total_value, overall_return_pct, std_dev, columns_used))

# Find the best performing strategy
best_strategy_name, best_investment_results, best_total_value, best_return_pct, best_columns = sorted_strategies[0][0], sorted_strategies[0][1][0], sorted_strategies[0][1][1], sorted_strategies[0][1][2], sorted_strategies[0][1][3]

# Find the most stable strategy overall
most_stable_strategy_name, most_stable_investment_results, most_stable_total_value, most_stable_return_pct, most_stable_std_dev, most_stable_columns = sorted(stable_strategies, key=lambda x: x[4])[0][:6]
most_stable_strategy_ranking_direction = strategy_ranking_direction[most_stable_strategy_name]

# Print the best performing strategy and its details
print(f"The best performing strategy is {best_strategy_name}")
print(f"Total Value: {best_total_value}")
print(f"Overall Return Percentage: {best_return_pct:.2f}%")
print(f"Columns included in the scoring: {best_columns}")
print()

# Print the most stable strategy overall and its details
print(f"The most stable strategy overall is {most_stable_strategy_name}")
print(f"Total Value: {most_stable_total_value}")
print(f"Overall Return Percentage: {most_stable_return_pct:.2f}%")
print(f"Standard Deviation of Gains: {most_stable_std_dev:.2f}")
print(f"Columns included in the scoring: {most_stable_columns}")
print(f"Ranking Direction for Most Stable Strategy: {most_stable_strategy_ranking_direction}")
print()

# Compare returns of the most stable strategy and baseline strategy
if most_stable_return_pct > overall_return_pct_baseline:
    print(f"The most stable strategy ({most_stable_strategy_name}) has a higher overall return percentage ({most_stable_return_pct:.2f}%) than the baseline strategy ({overall_return_pct_baseline:.2f}%).")
else:
    print(f"The baseline strategy ({baseline_strategy_name}) has a higher overall return percentage ({overall_return_pct_baseline:.2f}%) than the most stable strategy ({most_stable_return_pct:.2f}%).")

# Compare stability (standard deviation of gains)
if most_stable_std_dev < np.std(investment_results_baseline['gain_pct']):
    print(f"The most stable strategy ({most_stable_strategy_name}) is more stable (std dev: {most_stable_std_dev:.2f}) than the baseline strategy (std dev: {np.std(investment_results_baseline['gain_pct']):.2f}).")
else:
    print(f"The baseline strategy ({baseline_strategy_name}) is more stable (std dev: {np.std(investment_results_baseline['gain_pct']):.2f}) than the most stable strategy (std dev: {most_stable_std_dev:.2f}).")

# Check if the most stable strategy outperforms in both returns and stability to update baseline.csv
if most_stable_return_pct > overall_return_pct_baseline and most_stable_std_dev < np.std(investment_results_baseline['gain_pct']):
    # Update baseline.csv
    df_baseline = pd.DataFrame({
        'Strategy Name': [most_stable_strategy_name],
        'Columns Used': [most_stable_columns],
        'Ranking Direction': [most_stable_strategy_ranking_direction]
    })
    
    df_baseline.to_csv('baseline.csv', index=False)
    print(f"Baseline strategy updated to {most_stable_strategy_name} due to superior returns and stability.")
else:
    print("No update needed for baseline strategy.")

def print_positions(strategy_name, investment_results):
    print(f"Positions for {strategy_name}:")
    for year, data in investment_results.groupby('year'):
        total_portfolio_value = 0
        cash_at_year_end = data['buy_price'].iloc[0]  # Assuming initial capital is cash

        print(f"Year {year}:")
        for index, row in data.iterrows():
            print(f"  Ticker: {row['ticker']}, Buy Price: {row['buy_price']}, Sell Price: {row['sell_price']}, Gain: {row['gain_pct']:.2f}%")
            total_portfolio_value = row['total_value']  # Update after each sell

        cash_at_year_end = total_portfolio_value  # Portfolio value at year-end becomes cash

        print(f"  Total Portfolio Value: {total_portfolio_value:.2f}")
        print(f"  Cash at Year End: {cash_at_year_end:.2f}")
        print()



# # Print positions for the best performing strategy
# print_positions(best_strategy_name, best_investment_results)

# # Print positions for the most stable strategy
# print_positions(most_stable_strategy_name, most_stable_investment_results)

# # Print positions for the baseline strategy
# print_positions(baseline_strategy_name, investment_results_baseline)

# Plot cumulative returns for the best performing strategy, the most stable strategy, and the baseline strategy
plt.figure(figsize=(12, 8))
plt.plot(best_investment_results['year'], best_investment_results['total_value'], marker='o', label=f'Best Strategy: {best_strategy_name}')
plt.plot(most_stable_investment_results['year'], most_stable_investment_results['total_value'], marker='o', label=f'Most Stable Strategy: {most_stable_strategy_name}')
plt.plot(investment_results_baseline['year'], investment_results_baseline['total_value'], marker='o', label=f'Baseline Strategy: {baseline_strategy_name}', linestyle='--')
plt.title('Comparison of Best Performing, Most Stable, and Baseline Strategies')
plt.xlabel('Year')
plt.ylabel('Total Value')
plt.yscale('log')
plt.legend()
plt.grid(True)
plt.show()

