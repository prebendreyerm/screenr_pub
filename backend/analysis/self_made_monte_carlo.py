import pandas as pd
import numpy as np

df = pd.read_csv('database.csv')


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


df = calculate_score(scoring_columns, scoring_boolean)
df.sort_values(by='score')
print(df[df['year']==1984])

    ###### SIMULATION ######

iterations = 200
returns = []
years = np.arange(1984,2023,1)
for year in years:
    current_year_temp_df = df[df['year']==year]
    current_year_temp_df_sorted = current_year_temp_df.sort_values(by='score', ascending=False)
    next_year_temp_df = df[df['year']==year+1]
    if len(next_year_temp_df[next_year_temp_df['ticker']==current_year_temp_df_sorted.iloc[0,1]].stock_price.values) > 0:
        returns.append(next_year_temp_df[next_year_temp_df['ticker']==current_year_temp_df_sorted.iloc[0,1]].stock_price.values[0] - current_year_temp_df_sorted.iloc[0,63])
        print(returns)
    
        returns.append(next_year_temp_df[next_year_temp_df['ticker']==current_year_temp_df_sorted.iloc[1,1]].stock_price.values[0] - current_year_temp_df_sorted.iloc[1,63])
    


