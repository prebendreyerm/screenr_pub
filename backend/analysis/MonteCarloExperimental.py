import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import random
import numpy as np
from tqdm import tqdm
import multiprocessing

# Connect to the SQLite database
conn = sqlite3.connect(r'backend\data\financial_data.db')

# Function to fetch data as DataFrame
def fetch_data_as_dataframe(query):
    try:
        with sqlite3.connect(r'backend\data\financial_data.db') as conn:
            df = pd.read_sql_query(query, conn)
            return df
    except sqlite3.Error as e:
        print(f"An error occurred while fetching data: {e}")
        return None

# Drop rows with NaN values
def clean_data(df):
    df = df.dropna()
    return df

# Ensure the DataFrame is sorted by ticker and year
def sort_data(df):
    df['calendarYear'] = df['calendarYear'].astype(int)  # Convert calendarYear to integers
    df = df.sort_values(by=['calendarYear', 'symbol'])
    return df


# Combine multiple database tables into a single DataFrame
def combined_df():
    df_assets = pd.read_sql_query('SELECT * FROM Assets', conn)
    df_ratios = pd.read_sql_query('SELECT * FROM RatiosAnnual', conn)
    df_keyMetrics = pd.read_sql_query('SELECT * FROM KeyMetricsAnnual', conn)
    df_financial = pd.read_sql_query('SELECT * FROM FinancialGrowthAnnual', conn)
    df_prices = pd.read_sql_query('SELECT * FROM HistoricalPricesAnnual', conn)

    df = pd.merge(df_ratios, df_keyMetrics, on=['symbol', 'date'], how='inner')
    df = pd.merge(df, df_financial, on=['symbol', 'date'], how='inner')
    df = pd.merge(df, df_prices, on=['symbol', 'date'], how='inner')
    df = pd.merge(df, df_assets[['symbol', 'name', 'industry', 'sector']], on='symbol', how='left')

    df = df.loc[:, ~df.columns.str.contains('_')]
    return df

# Fetch and clean data
df = combined_df()
df = clean_data(df)
df = sort_data(df)

# Select numerical columns for scoring
scoring_columns = df.select_dtypes(include=['number']).columns.tolist()

# Function to calculate scores and perform backtesting
def calculate_scores_and_backtest(df, scoring_columns, ascending_flags):
    df = df.copy()
    ranks = [df[col].rank(pct=True, ascending=asc) for col, asc in zip(scoring_columns, ascending_flags)]
    df['score'] = sum(ranks) / len(scoring_columns)

    initial_capital = 100
    total_value = initial_capital
    investment_strategy = []
    years = df['calendarYear'].unique()

    for year in sorted(years)[:-1]:
        current_year_data = df[df['calendarYear'] == year]
        if current_year_data.empty:
            continue
        next_year_data = df[df['calendarYear'] == year + 1]

        for _, best_stock in current_year_data.sort_values(by='score').iterrows():
            next_year_stock_data = next_year_data[next_year_data['symbol'] == best_stock['symbol']]
            if next_year_stock_data.empty:
                continue

            buy_price = best_stock['stockPrice']
            shares_bought = total_value / buy_price
            total_value = 0
            
            sell_price = next_year_stock_data['stockPrice'].values[0]
            total_value += shares_bought * sell_price

            gain_pct = (sell_price - buy_price) / buy_price * 100
            investment_strategy.append({
                'year': year,
                'symbol': best_stock['symbol'],
                'buy_price': buy_price,
                'sell_price': sell_price,
                'total_value': total_value,
                'gain_pct': gain_pct
            })
            break

    overall_return_pct = ((total_value - initial_capital) / initial_capital) * 100
    return pd.DataFrame(investment_strategy), total_value, overall_return_pct

# Function to compare strategies with baseline and update if superior
def compare_with_baseline(strategy_results, baseline_strategy_name, overall_return_pct_baseline, baseline_std_dev, sector):
    updated = False
    for strategy_name, (investment_results, total_value, overall_return_pct, strategy_columns) in strategy_results.items():
        if overall_return_pct > overall_return_pct_baseline and np.std(investment_results['gain_pct']) < baseline_std_dev:
            columns_used_str = ','.join(strategy_columns)
            ranking_direction_str = ','.join(map(str, [True] + [False] * (len(strategy_columns) - 1)))
            std_dev = np.std(investment_results['gain_pct'])

            with conn:
                conn.execute(""" 
                    INSERT OR REPLACE INTO ScoringStrategies (strategy_name, columns_used, ranking_direction, sector, overall_return, std_dev)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (strategy_name, columns_used_str, ranking_direction_str, sector, overall_return_pct, std_dev))

            print(f"Baseline strategy updated to {strategy_name} due to superior returns and stability.")
            updated = True
            break
    return updated

# Function for simulating and backtesting a single strategy
def run_simulation(i, df, scoring_columns):
    num_columns = random.randint(2, len(scoring_columns))
    selected_columns = random.sample(scoring_columns, num_columns)
    ascending_flags = [random.choice([True, False]) for _ in selected_columns]

    strategy_identifier = (tuple(selected_columns), tuple(ascending_flags))
    strategy_name = f'Simulation_{i + 1}'

    investment_results, total_value, overall_return_pct = calculate_scores_and_backtest(df, selected_columns, ascending_flags)

    return strategy_name, investment_results, total_value, overall_return_pct, selected_columns

# Start with a random strategy as the baseline
num_columns = random.randint(2, len(scoring_columns))
initial_columns = random.sample(scoring_columns, num_columns)
initial_ascending_flags = [random.choice([True, False]) for _ in initial_columns]

# Calculate scores for the initial random strategy
baseline_strategy_name = "Baseline"
investment_results_baseline, total_value_baseline, overall_return_pct_baseline = calculate_scores_and_backtest(
    df, initial_columns, initial_ascending_flags
)
baseline_std_dev = np.std(investment_results_baseline['gain_pct'])

print(f"Initialized with random strategy: {baseline_strategy_name}")
print(f"Initial overall return: {overall_return_pct_baseline:.2f}%")
print(f"Initial standard deviation: {baseline_std_dev:.2f}")

# Save the initial random strategy to the database
with conn:
    conn.execute(""" 
        INSERT INTO ScoringStrategies (strategy_name, columns_used, ranking_direction, sector, overall_return, std_dev)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        baseline_strategy_name,
        ','.join(initial_columns),
        ','.join(map(str, initial_ascending_flags)),
        'All',  # Sector-independent
        overall_return_pct_baseline,
        baseline_std_dev
    ))

# Parallel simulation using multiprocessing
num_simulations = 200
strategy_results = {}
tested_strategies = set()

# Use multiprocessing Pool to run simulations in parallel
with multiprocessing.Pool() as pool:
    simulation_results = pool.starmap(run_simulation, [(i, df, scoring_columns) for i in range(num_simulations)])

# Store the results and compare with the baseline
for strategy_name, investment_results, total_value, overall_return_pct, strategy_columns in simulation_results:
    strategy_results[strategy_name] = (investment_results, total_value, overall_return_pct, strategy_columns)

    # Compare with the current baseline strategy
    if compare_with_baseline(strategy_results, baseline_strategy_name, overall_return_pct_baseline, baseline_std_dev, 'All'):
        baseline_strategy_name = strategy_name
        overall_return_pct_baseline = overall_return_pct
        baseline_std_dev = np.std(investment_results['gain_pct'])

# Plot the yearly returns of the final baseline strategy
if baseline_strategy_name:
    yearly_returns = investment_results_baseline.groupby('year')['gain_pct'].mean()
    plt.figure(figsize=(12, 8))
    yearly_returns.plot(kind='bar')
    plt.xlabel('Year')
    plt.ylabel('Return (%)')
    plt.title('Yearly Returns of Baseline Strategy')
    plt.show()

print("Simulation and comparison with baseline completed.")
