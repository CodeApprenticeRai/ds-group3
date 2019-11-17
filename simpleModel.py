# import libraries
import pandas as pd
import statsmodels.api as sm
import numpy as np
import DataHelper
import os
import time
import itertools

def individual_Beta(ind_data, stand_data):
    #change to our data
    ind_stock = pd.read_csv(ind_data, parse_dates=True, index_col='date',sep = ',')
    sp_500 = pd.read_csv(stand_data, parse_dates=True, index_col='date', sep = ',')
    # joining the closing prices of the two datasets 
    #use recent 1 yrs data for training
    monthly_prices = pd.concat([ind_stock.iloc[0:216,3], sp_500.iloc[0:216,3]], axis=1)
    monthly_prices.columns = ['ind', 'SP500']


    # check the head of the dataframe
    #print(monthly_prices)

    # calculate monthly returns
    monthly_returns = monthly_prices.pct_change(1)
    clean_monthly_returns = monthly_returns.dropna(axis=0)  # drop first missing row

    # split dependent and independent variable
    X = clean_monthly_returns['SP500']
    y = clean_monthly_returns['ind']
    if(len(X) > 0):
        # Add a constant to the independent value
        X1 = sm.add_constant(X)

        # make regression model 
        model = sm.OLS(y, X1)

        # fit model and print results
        results = model.fit()
        #beta of the individual stock
        return results.params[1]
    else:
        print(ind_data)
        return 0

'''
compute beta for all individual stocks
'''
def all_beta(s_list, dPath, mPath):
    b_list = []
    for stock in s_list:
        stock_path = dPath + str(stock) + '.csv'
        stock_Beta = individual_Beta(stock_path, mPath)
        if stock_Beta >= -20 and stock_Beta <= 100:
            b_list.append((stock, stock_Beta))
        else:
            print(stock, stock_Beta)
    return b_list

'''
generate portfolios 
'''
def findPorts(s_list, num, thre):#stock list, size of portfolio, threshold
    port_list = []
    for cand_port in set(itertools.combinations(s_list, num)):
        beta_sum = sum(n for _, n in cand_port)
        if(beta_sum >= thre):
            port_list.append(cand_port)
    return port_list

#get stock list
dataPath = './AlphaData/'
marketPath = dataPath + 'SPY.csv'
stock_list = []
for filename in os.listdir(dataPath):
    #a stock file
    if filename[-3:] == 'csv':
        if filename[:4] != 'ML4T' and filename[0] != '$' :
            stock_list.append(filename[:-4])

#compute all beta
beta_list = all_beta(stock_list, dataPath, marketPath)
#print(beta_list)
'''
print(max(n for _, n in beta_list if n > 0))
print(sum(n for _, n in beta_list if n > 0)/len(beta_list))
'''

#generate portfolios brute force
print('selecting portfolios')
print(findPorts(beta_list, 4, 6))