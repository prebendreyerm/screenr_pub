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

# Strategy 1: Original scoring system
df1 = df.copy()

# Calculate scores based on enterpriseValueMultiple, returnOnAssets, and revenue_growth
df1 = df1[df1['returnOnAssets'] >= 0]  # Remove rows with negative returnOnAssets
df1 = df1[df1['revenue_growth'] >= 0]  # Remove rows with negative revenue_growth
df1['score'] = (1 - df1['enterpriseValueMultiple'].rank(pct=True, ascending=True) +
                df1['returnOnAssets'].rank(pct=True, ascending=False) +
                df1['revenue_growth'].rank(pct=True, ascending=False)) / 3

# Initialize variables for strategy 1
initial_capital = 100
total_value1 = initial_capital
investment_strategy1 = []

# Perform backtesting for strategy 1
years = df1['year'].unique()

for year in sorted(years)[:-1]:  # Loop until the last year, sorted to ensure chronological order
    current_year_data = df1[df1['year'] == year]
    next_year_data = df1[df1['year'] == year + 1]
    
    # Find the stock with the best score for the current year
    best_stock = current_year_data.nlargest(1, 'score').iloc[0]
    
    # Check if there's data available for the selected stock in the next year
    next_year_stock_data = next_year_data[next_year_data['ticker'] == best_stock['ticker']]
    if next_year_stock_data.empty:
        print(f"No data available for {best_stock['ticker']} in {year + 1} for strategy 1, skipping...")
        continue  # Skip to the next iteration if no data available
    
    # Buy the stock at the beginning of the year
    buy_price = best_stock['stock_price']
    shares_bought = total_value1 / buy_price
    total_value1 = 0  # Invest all capital in the stock
    
    # Sell the stock at the end of the year
    sell_price = next_year_stock_data['stock_price'].values[0]
    total_value1 += shares_bought * sell_price
    
    # Track investment strategy
    investment_strategy1.append({
        'year': year,
        'ticker': best_stock['ticker'],
        'buy_price': buy_price,
        'sell_price': sell_price,
        'total_value': total_value1
    })

# Convert investment strategy results to DataFrame for strategy 1
investment_results1 = pd.DataFrame(investment_strategy1)


# Strategy 2: Score based on returnOnAssets and revenue growth only
df2 = df.copy()

# Calculate scores based on returnOnAssets and revenue_growth only
df2 = df2[df2['returnOnAssets'] >= 0]  # Remove rows with negative returnOnAssets
df2 = df2[df2['revenue_growth'] >= 0]  # Remove rows with negative revenue_growth
df2['score'] = (df2['returnOnAssets'].rank(pct=True, ascending=False) +
                df2['revenue_growth'].rank(pct=True, ascending=False)) / 2

# Initialize variables for strategy 2
total_value2 = initial_capital
investment_strategy2 = []

# Perform backtesting for strategy 2
years = df2['year'].unique()

for year in sorted(years)[:-1]:  # Loop until the last year, sorted to ensure chronological order
    current_year_data = df2[df2['year'] == year]
    next_year_data = df2[df2['year'] == year + 1]
    
    # Find the stock with the best score for the current year
    best_stock = current_year_data.nlargest(1, 'score').iloc[0]
    
    # Check if there's data available for the selected stock in the next year
    next_year_stock_data = next_year_data[next_year_data['ticker'] == best_stock['ticker']]
    if next_year_stock_data.empty:
        print(f"No data available for {best_stock['ticker']} in {year + 1} for strategy 2, skipping...")
        continue  # Skip to the next iteration if no data available
    
    # Buy the stock at the beginning of the year
    buy_price = best_stock['stock_price']
    shares_bought = total_value2 / buy_price
    total_value2 = 0  # Invest all capital in the stock
    
    # Sell the stock at the end of the year
    sell_price = next_year_stock_data['stock_price'].values[0]
    total_value2 += shares_bought * sell_price
    
    # Track investment strategy
    investment_strategy2.append({
        'year': year,
        'ticker': best_stock['ticker'],
        'buy_price': buy_price,
        'sell_price': sell_price,
        'total_value': total_value2
    })

# Convert investment strategy results to DataFrame for strategy 2
investment_results2 = pd.DataFrame(investment_strategy2)


# Strategy 3: Score based on enterpriseValueMultiple and returnOnAssets only
df3 = df.copy()

# Calculate scores based on enterpriseValueMultiple and returnOnAssets only
df3 = df3[df3['returnOnAssets'] >= 0]  # Remove rows with negative returnOnAssets
df3['score'] = (1 - df3['enterpriseValueMultiple'].rank(pct=True, ascending=True) +
                df3['returnOnAssets'].rank(pct=True, ascending=False)) / 2

# Initialize variables for strategy 3
total_value3 = initial_capital
investment_strategy3 = []

# Perform backtesting for strategy 3
years = df3['year'].unique()

for year in sorted(years)[:-1]:  # Loop until the last year, sorted to ensure chronological order
    current_year_data = df3[df3['year'] == year]
    next_year_data = df3[df3['year'] == year + 1]
    
    # Find the stock with the best score for the current year
    best_stock = current_year_data.nlargest(1, 'score').iloc[0]
    
    # Check if there's data available for the selected stock in the next year
    next_year_stock_data = next_year_data[next_year_data['ticker'] == best_stock['ticker']]
    if next_year_stock_data.empty:
        print(f"No data available for {best_stock['ticker']} in {year + 1} for strategy 3, skipping...")
        continue  # Skip to the next iteration if no data available
    
    # Buy the stock at the beginning of the year
    buy_price = best_stock['stock_price']
    shares_bought = total_value3 / buy_price
    total_value3 = 0  # Invest all capital in the stock
    
    # Sell the stock at the end of the year
    sell_price = next_year_stock_data['stock_price'].values[0]
    total_value3 += shares_bought * sell_price
    
    # Track investment strategy
    investment_strategy3.append({
        'year': year,
        'ticker': best_stock['ticker'],
        'buy_price': buy_price,
        'sell_price': sell_price,
        'total_value': total_value3
    })

# Convert investment strategy results to DataFrame for strategy 3
investment_results3 = pd.DataFrame(investment_strategy3)


# Strategy 4: Score based on enterpriseValueMultiple, returnOnAssets, revenue_growth, debtRatio, and freeCashFlowPerShare
df4 = df.copy()

# Calculate scores based on all five parameters
df4 = df4[df4['returnOnAssets'] >= 0]  # Remove rows with negative returnOnAssets
df4 = df4[df4['revenue_growth'] >= 0]  # Remove rows with negative revenue_growth
df4['score'] = (1 - df4['enterpriseValueMultiple'].rank(pct=True, ascending=True) +
                df4['returnOnAssets'].rank(pct=True, ascending=False) +
                df4['revenue_growth'].rank(pct=True, ascending=False) +
                (1 - df4['debtRatio'].rank(pct=True, ascending=True)) +
                df4['freeCashFlowPerShare'].rank(pct=True, ascending=False)) / 5

# Initialize variables for strategy 4
total_value4 = initial_capital
investment_strategy4 = []

# Perform backtesting for strategy 4
years = df4['year'].unique()

for year in sorted(years)[:-1]:  # Loop until the last year, sorted to ensure chronological order
    current_year_data = df4[df4['year'] == year]
    next_year_data = df4[df4['year'] == year + 1]
    
    # Find the stock with the best score for the current year
    best_stock = current_year_data.nlargest(1, 'score').iloc[0]
    
    # Check if there's data available for the selected stock in the next year
    next_year_stock_data = next_year_data[next_year_data['ticker'] == best_stock['ticker']]
    if next_year_stock_data.empty:
        print(f"No data available for {best_stock['ticker']} in {year + 1} for strategy 4, skipping...")
        continue  # Skip to the next iteration if no data available
    
    # Buy the stock at the beginning of the year
    buy_price = best_stock['stock_price']
    shares_bought = total_value4 / buy_price
    total_value4 = 0  # Invest all capital in the stock
    
    # Sell the stock at the end of the year
    sell_price = next_year_stock_data['stock_price'].values[0]
    total_value4 += shares_bought * sell_price
    
    # Track investment strategy
    investment_strategy4.append({
        'year': year,
        'ticker': best_stock['ticker'],
        'buy_price': buy_price,
        'sell_price': sell_price,
        'total_value': total_value4
    })

# Convert investment strategy results to DataFrame for strategy 4
investment_results4 = pd.DataFrame(investment_strategy4)


# Print the investment results for each strategy
print("Investment Results for Strategy 1:")
print(investment_results1)
print()

print("Investment Results for Strategy 2:")
print(investment_results2)
print()

print("Investment Results for Strategy 3:")
print(investment_results3)
print()

print("Investment Results for Strategy 4:")
print(investment_results4)
print()

# Plot cumulative returns for each strategy
plt.figure(figsize=(12, 8))
plt.plot(investment_results1['year'], investment_results1['total_value'], marker='o', label='Strategy 1')
plt.plot(investment_results2['year'], investment_results2['total_value'], marker='o', label='Strategy 2')
plt.plot(investment_results3['year'], investment_results3['total_value'], marker='o', label='Strategy 3')
plt.plot(investment_results4['year'], investment_results4['total_value'], marker='o', label='Strategy 4')
plt.title('Cumulative Returns of Investment Strategies')
plt.xlabel('Year')
plt.ylabel('Total Value')
plt.legend()
plt.grid(True)
plt.show()
