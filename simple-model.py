# import libraries
import pandas as pd
import statsmodels.api as sm
import numpy as np

'''
Download monthly prices of Facebook and S&P 500 index from 2014 to 2017
CSV file downloaded from Yahoo File
start period: 02/11/2014 
end period: 30/11/2014
period format: DD/MM/YEAR
'''
#change to our data
gnw = pd.read_csv('./mergedQSTKandKaggleData/GNW.csv', parse_dates=True, index_col='Date',sep = ',')
sp_500 = pd.read_csv('./mergedQSTKandKaggleData/SPY.csv', parse_dates=True, index_col='Date', sep = ',')
# joining the closing prices of the two datasets 
monthly_prices = pd.concat([gnw.iloc[:,3], sp_500.iloc[:,3]], axis=1)
monthly_prices.columns = ['gnw', 'SP500']


# check the head of the dataframe
print(monthly_prices)

# calculate monthly returns
monthly_returns = monthly_prices.pct_change(1)
print(monthly_returns)
clean_monthly_returns = monthly_returns.dropna(axis=0)  # drop first missing row
print(clean_monthly_returns.head())

# split dependent and independent variable
X = clean_monthly_returns['SP500']
y = clean_monthly_returns['gnw']

# Add a constant to the independent value
X1 = sm.add_constant(X)

# make regression model 
model = sm.OLS(y, X1)

# fit model and print results
results = model.fit()
print(results.summary())