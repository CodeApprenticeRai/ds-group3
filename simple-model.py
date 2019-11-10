# import libraries
import pandas as pd
import statsmodels.api as sm
import numpy as np
import DataHelper
#import pyspark
'''
Download monthly prices of Facebook and S&P 500 index from 2014 to 2017
CSV file downloaded from Yahoo File
start period: 02/11/2014 
end period: 30/11/2014
period format: DD/MM/YEAR
'''
def individual_Beta(ind_data, stand_data):
    #change to our data
    ind_stock = pd.read_csv(ind_data, parse_dates=True, index_col='Date',sep = ',')
    sp_500 = pd.read_csv(stand_data, parse_dates=True, index_col='Date', sep = ',')
    # joining the closing prices of the two datasets 
    monthly_prices = pd.concat([ind_stock.iloc[:,3], sp_500.iloc[:,3]], axis=1)
    monthly_prices.columns = ['ind', 'SP500']


    # check the head of the dataframe
    print(monthly_prices)

    # calculate monthly returns
    monthly_returns = monthly_prices.pct_change(1)
    print(monthly_returns)
    clean_monthly_returns = monthly_returns.dropna(axis=0)  # drop first missing row
    print(clean_monthly_returns.head())

    # split dependent and independent variable
    X = clean_monthly_returns['SP500']
    y = clean_monthly_returns['ind']

    # Add a constant to the independent value
    X1 = sm.add_constant(X)

    # make regression model 
    model = sm.OLS(y, X1)

    # fit model and print results
    results = model.fit()
    #beta of the individual stock
    print(results.params[1])
    return results.params[1]

#use DataHelper to get data
dh = DataHelper.DataHelper()
example_stock_list = "CHK AMD GE UBER BAC GDX BABA KR FIT GOLD AAPL M MS SIRI MSFT".split(" ")
example_df = dh.get_data(example_stock_list[:3])
print(example_df)
#individual_Beta('./mergedQSTKandKaggleData/AA.csv', './mergedQSTKandKaggleData/SPY.csv')