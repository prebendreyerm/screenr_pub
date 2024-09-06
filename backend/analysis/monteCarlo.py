import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import random
from tqdm import tqdm
import os

df = pd.read_csv('database.csv')
# sector = 'Technology'
# df = df[df['sector'] == sector]

# sectors = ['Industrials', 'Consumer Staples', 'Consumer Discretionary', 'Energy',
#  'Health Care', 'Real Estate', 'Technology', 'Finance', 'Basic Materials',
#  'Telecommunications', 'Miscellaneous', 'Utilities', 'Consumer Services',
#  'Consumer Goods', 'Communication Services', 'Consumer Defensive',
#  'Financials', 'Consumer Cyclical']

sectors = ['Technology', 'Energy', 'Basic Materials', 'Healthcare', 'Consumer Defensive',
 'Financial Services', 'Consumer Cyclical', 'Communication Services',
 'Real Estate', 'Utilities', 'Industrials']



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

scoring_boolean = [
    False, True, True,  # 'enterpriseValueMultiple', 'returnOnAssets', 'revenue_growth'
    False, True, True, True,  # 'debtRatio', 'freeCashFlowPerShare', 'currentRatio', 'quickRatio'
    True, False, False,  # 'cashRatio', 'daysOfSalesOutstanding', 'daysOfInventoryOutstanding'
    False, False, False,  # 'operatingCycle', 'daysOfPayablesOutstanding', 'cashConversionCycle'
    True, True, True,  # 'grossProfitMargin', 'operatingProfitMargin', 'pretaxProfitMargin'
    True, True, True,  # 'netProfitMargin', 'effectiveTaxRate', 'returnOnEquity'
    True, True, True,  # 'returnOnCapitalEmployed', 'netIncomePerEBT', 'ebtPerEbit'
    True, False, False,  # 'ebitPerRevenue', 'debtEquityRatio', 'longTermDebtToCapitalization'
    False, True, True,  # 'totalDebtToCapitalization', 'interestCoverage', 'cashFlowToDebtRatio'
    False, True, True,  # 'companyEquityMultiplier', 'receivablesTurnover', 'payablesTurnover'
    True, True, True,  # 'inventoryTurnover', 'fixedAssetTurnover', 'assetTurnover'
    True, True, False,  # 'operatingCashFlowPerShare', 'cashPerShare', 'payoutRatio'
    True, True, True,  # 'operatingCashFlowSalesRatio', 'freeCashFlowOperatingCashFlowRatio', 'cashFlowCoverageRatios'
    True, True, True,  # 'shortTermCoverageRatios', 'capitalExpenditureCoverageRatio', 'dividendPaidAndCapexCoverageRatio'
    False, False, False,  # 'dividendPayoutRatio', 'priceBookValueRatio', 'priceToBookRatio'
    False, False, False,  # 'priceToSalesRatio', 'priceEarningsRatio', 'priceToFreeCashFlowsRatio'
    False, False, False,  # 'priceToOperatingCashFlowsRatio', 'priceCashFlowRatio', 'priceEarningsToGrowthRatio'
    False, False, True,  # 'priceSalesRatio', 'dividendYield', 'priceFairValue'
]

def calculate_score(list_of_columns, list_of_ascending_boolean):
    df['score'] = df['returnOnAssets']*0
    for i in range(len(list_of_columns)):
        df['score'] += df[list_of_columns[i]].rank(ascending=list_of_ascending_boolean[i])
    df['score'] = df['score']/len(list_of_columns)
    df_max_scaled = df.copy()
    df_max_scaled['score'] = df_max_scaled['score']  / df_max_scaled['score'].abs().max()
    return df_max_scaled

def get_random_metrics_with_booleans(metrics_list):
    num_metrics = random.randint(1, len(metrics_list))
    random_metrics = random.sample(metrics_list, num_metrics)
    random_booleans = [random.choice([True, False]) for _ in range(num_metrics)]
    return random_metrics, random_booleans

def threshold(array):
    # Count the number of elements greater than zero
    count_above_zero = sum(1 for x in array if x > 0)
    
    # Calculate the total number of elements
    total_elements = len(array)
    
    # Check if at least 75% of the elements are greater than zero
    if total_elements == 0:
        return False  # Handle the edge case where the array is empty
    return count_above_zero / total_elements >= 0.75


    ###### SIMULATION ######
for sector in sectors:
    iterations = 10000
    years = np.arange(1990,2023,1)
    if os.path.exists('returns_{}.csv'.format(sector)):
        returns = np.array(pd.read_csv('returns_{}.csv'.format(sector)).iloc[:,1])
        print(returns)
        print(np.std(returns), np.average(returns))
    else:
        returns = [-0.27868852, 0.21367521, -0.0693218, 0.22873408, 0.1969697, 0.0352,
            -0.51159196, 0.13087935, -0.08169935, 0.77906977, 0.41357027, -0.30914286,
            0.06506667, -0.40142857, -0.6836734, -0.34545455, -0.33054393, 0.05339806,
            -0.5483871, 0.28769841, 0.15562404, 0.26266667, 0.37275607, -0.23541247,
            -0.45992261, 0.49291498, 0.27566102, -0.48809524, 0.12313938, 0.23926803,
            -0.16237674, 0.08996781, 0.09806817, 0.23459707, -0.67066097, 0.03565135,
            0.09175217, -0.02465749, -0.61656839]








    for i in tqdm(range(iterations)):
        iter_returns = []
        scoring_metrics, booleans = get_random_metrics_with_booleans(scoring_columns)
        df = calculate_score(scoring_metrics, booleans)
        for year in years:
            current_year_temp_df = df[df['year'] == year]
            current_year_temp_df_sorted = current_year_temp_df.sort_values(by='score', ascending=False)
            next_year_temp_df = df[df['year'] == year + 1]

            found_valid_return = False

            for rank in range(len(current_year_temp_df_sorted)):
                current_ticker = current_year_temp_df_sorted.iloc[rank]['ticker']
                current_stock_price = current_year_temp_df_sorted.iloc[rank]['stock_price']
                
                next_year_ticker_row = next_year_temp_df[next_year_temp_df['ticker'] == current_ticker]
                
                if not next_year_ticker_row.empty:
                    next_year_stock_price = next_year_ticker_row['stock_price'].values[0]
                    iter_returns.append((next_year_stock_price - current_stock_price)/current_stock_price)
                    found_valid_return = True
                    break
            
            if not found_valid_return:
                iter_returns.append(None)  # Or any other placeholder indicating no valid return was found
        iter_returns = np.array(iter_returns)
        if (threshold(iter_returns) and np.std(iter_returns) < 0.3 and np.average(iter_returns) > np.average(returns) and np.std(iter_returns) < np.std(returns)):
        # if (threshold(iter_returns) and np.average(iter_returns) > np.average(returns) and np.std(iter_returns) < np.std(returns)):
            returns = iter_returns
            print('greater returns found with strategy {}'.format(i))
            print('Average returns', np.average(returns))
            print('Standard deviation', np.std(returns))
            baseline_df = pd.DataFrame({'scoring_columns' : scoring_metrics,
                                    'booleans': booleans})
            returns_df = pd.DataFrame({'returns': returns})
            returns_df.to_csv('returns_{}.csv'.format(sector))
            baseline_df.to_csv('baseline_{}.csv'.format(sector))
            # if np.average(iter_returns) > np.average(returns) and np.std(iter_returns) < np.std(returns):
            #     returns = iter_returns
            #     print('greater average returns found with strategy {}'.format(i))

    capital = 1000
    for i in returns:
        capital = capital*(1+i) + 1000
        print(capital)
    # Print the calculated returns
    print(returns)
    plt.figure()
    plt.bar(years, returns)
    plt.show()

