import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import itertools
import random

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

# Fetch data into a DataFrame
query = "SELECT * FROM FinancialGrowthAnnual"
df = fetch_data_as_dataframe(query)

# Drop rows with NaN values
df = df.dropna()

print(df)

# # Define the columns that can be used for scoring
# scoring_columns = [
#     'enterpriseValueMultiple', 'returnOnAssets', 'revenue_growth', 
#     'debtRatio', 'freeCashFlowPerShare', 'currentRatio', 'quickRatio', 
#     'cashRatio', 'daysOfSalesOutstanding', 'daysOfInventoryOutstanding', 
#     'operatingCycle', 'daysOfPayablesOutstanding', 'cashConversionCycle', 
#     'grossProfitMargin', 'operatingProfitMargin', 'pretaxProfitMargin', 
#     'netProfitMargin', 'effectiveTaxRate', 'returnOnEquity', 
#     'returnOnCapitalEmployed', 'netIncomePerEBT', 'ebtPerEbit', 
#     'ebitPerRevenue', 'debtEquityRatio', 'longTermDebtToCapitalization', 
#     'totalDebtToCapitalization', 'interestCoverage', 'cashFlowToDebtRatio', 
#     'companyEquityMultiplier', 'receivablesTurnover', 'payablesTurnover', 
#     'inventoryTurnover', 'fixedAssetTurnover', 'assetTurnover', 
#     'operatingCashFlowPerShare', 'cashPerShare', 'payoutRatio', 
#     'operatingCashFlowSalesRatio', 'freeCashFlowOperatingCashFlowRatio', 
#     'cashFlowCoverageRatios', 'shortTermCoverageRatios', 
#     'capitalExpenditureCoverageRatio', 'dividendPaidAndCapexCoverageRatio', 
#     'dividendPayoutRatio', 'priceBookValueRatio', 'priceToBookRatio', 
#     'priceToSalesRatio', 'priceEarningsRatio', 'priceToFreeCashFlowsRatio', 
#     'priceToOperatingCashFlowsRatio', 'priceCashFlowRatio', 
#     'priceEarningsToGrowthRatio', 'priceSalesRatio', 'dividendYield', 
#     'priceFairValue'
# ]

# # Function to calculate scores and perform backtesting
# def calculate_scores_and_backtest(df, scoring_columns, ascending_flags):
#     df = df.copy()
#     for col, asc in zip(scoring_columns, ascending_flags):
#         if col == 'enterpriseValueMultiple' or col == 'debtRatio':
#             df = df[df[col] >= 0]  # Remove rows with negative values for these columns

#     ranks = [df[col].rank(pct=True, ascending=asc) for col, asc in zip(scoring_columns, ascending_flags)]
#     df['score'] = sum(ranks) / len(scoring_columns)

#     initial_capital = 100
#     total_value = initial_capital
#     investment_strategy = []
#     years = df['year'].unique()

#     for year in sorted(years)[:-1]:
#         current_year_data = df[df['year'] == year]
#         next_year_data = df[df['year'] == year + 1]
        
#         best_stock = current_year_data.nlargest(1, 'score').iloc[0]
#         next_year_stock_data = next_year_data[next_year_data['ticker'] == best_stock['ticker']]
#         if next_year_stock_data.empty:
#             continue

#         buy_price = best_stock['stock_price']
#         shares_bought = total_value / buy_price
#         total_value = 0
        
#         sell_price = next_year_stock_data['stock_price'].values[0]
#         total_value += shares_bought * sell_price

#         investment_strategy.append({
#             'year': year,
#             'ticker': best_stock['ticker'],
#             'buy_price': buy_price,
#             'sell_price': sell_price,
#             'total_value': total_value
#         })

#     return pd.DataFrame(investment_strategy), total_value

# # Initialize the results dictionary
# strategy_results = {}

# # Define the initial strategies
# initial_strategies = {
#     'Strategy 1': ['enterpriseValueMultiple', 'returnOnAssets', 'revenue_growth'],
#     'Strategy 2': ['returnOnAssets', 'revenue_growth'],
#     'Strategy 3': ['enterpriseValueMultiple', 'returnOnAssets'],
#     'Strategy 4': ['enterpriseValueMultiple', 'returnOnAssets', 'revenue_growth', 'debtRatio', 'freeCashFlowPerShare']
# }

# # Calculate scores and backtest for the initial strategies
# for strategy_name, columns in initial_strategies.items():
#     investment_results, total_value = calculate_scores_and_backtest(df, columns, [True] + [False] * (len(columns) - 1))
#     strategy_results[strategy_name] = (investment_results, total_value)

# # Generate 100 different strategies
# for i in range(1, 1000):
#     num_columns = random.randint(2, len(scoring_columns))
#     selected_columns = random.sample(scoring_columns, num_columns)
#     ascending_flags = [random.choice([True, False]) for _ in selected_columns]
#     strategy_name = f'Strategy {i + 4}'
#     investment_results, total_value = calculate_scores_and_backtest(df, selected_columns, ascending_flags)
#     strategy_results[strategy_name] = (investment_results, total_value, selected_columns)

# # Find the best strategy
# best_strategy = max(strategy_results.items(), key=lambda x: x[1][1])

# # Print the investment results for each strategy
# for strategy_name, (investment_results, total_value, *_) in strategy_results.items():
#     print(f"Investment Results for {strategy_name}:")
#     print(investment_results)
#     print(f"Total Value: {total_value}")
#     print()

# # Print the best strategy
# best_strategy_name, (best_investment_results, best_total_value, best_columns) = best_strategy


# # Print the investment results and total value of the best strategy
# print(f"\nInvestment Results for the Best Strategy ({best_strategy_name}):")
# print(best_investment_results)
# print(f"Total Value: {best_total_value}")
# print(f"The best strategy is {best_strategy_name}")
# print(f"Columns included in the scoring: {best_columns}")

# # Plot cumulative returns for each strategy
# plt.figure(figsize=(12, 8))
# for strategy_name, (investment_results, _, *_) in strategy_results.items():
#     plt.plot(investment_results['year'], investment_results['total_value'], marker='o', label=strategy_name)
# plt.title('Cumulative Returns of Investment Strategies')
# plt.xlabel('Year')
# plt.ylabel('Total Value')
# plt.yscale('log')
# plt.legend()
# plt.grid(True)
# plt.show()

# # Plot cumulative returns for the best strategy
# plt.figure(figsize=(12, 8))
# plt.plot(best_investment_results['year'], best_investment_results['total_value'], marker='o', label=best_strategy_name)
# plt.title(f'Cumulative Returns of the Best Strategy ({best_strategy_name})')
# plt.xlabel('Year')
# plt.ylabel('Total Value')
# plt.yscale('log')
# plt.legend()
# plt.grid(True)
# plt.show()