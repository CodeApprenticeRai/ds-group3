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
    #ind_stock = pd.read_csv(ind_data, parse_dates=True, index_col='date',sep = ',')
    ind_stock = pd.read_csv(ind_data, parse_dates=True, index_col=0, sep = ',')
    sp_500 = pd.read_csv(stand_data, parse_dates=True, index_col=0, sep = ',')
    # joining the closing prices of the two datasets 
    #use recent 3 yrs data for training
    temp1 = ind_stock['close']
    closes = temp1[0:216]
    temp2 = sp_500['close']
    closeSP = temp2[0:216]
    monthly_prices = pd.concat([closes, closeSP], axis=1)
    #monthly_prices = pd.concat([ind_stock[], sp_500.iloc[0:216,3]], axis=1)   #0:216
    monthly_prices.columns = ['ind', 'SP500']


    # check the head of the dataframe
    #print(monthly_prices)

    # calculate monthly returns
    monthly_returns = (monthly_prices / monthly_prices.shift(1)) - 1   #monthly_prices.pct_change(1)
    clean_monthly_returns = monthly_returns.fillna(method="ffill").fillna(method="bfill")[1:] #monthly_returns.dropna(axis=0)  # drop first missing row
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
    #print results.params[1]
    return results.params[1]

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
#def findPorts(s_list, num, thre):#stock list, size of portfolio, threshold
#    for cand_port in set(itertools.combinations(s_list, num)):
#        beta_sum = sum(n for _, n in cand_port)
#        if(beta_sum >= thre):
#            yield cand_port


dataPath = './AlphaData/'
marketPath = dataPath + 'SPY.csv'
stock_list = []
for filename in os.listdir(dataPath):
    #a stock file
    if filename[-3:] == 'csv':
        if filename[:4] != 'ML4T' and filename[0] != '$' :
            stock_list.append(filename[:-4])

beta_list = all_beta(stock_list[:10], dataPath, marketPath)
'''
print(max(n for _, n in beta_list if n > 0))
print(sum(n for _, n in beta_list if n > 0)/len(beta_list))
'''

#print(findPorts(beta_list, 4, 6))
print beta_list
a = itertools.combinations(beta_list, 4)
count = 0
t1 = int(round(time.time() * 1000)) # milliseconds
for _ in xrange(0, int(1e8)):
    cand_port = next(a)
    beta_sum = sum(n for _, n in cand_port)
    if count % 1000 == 0:
        t2 = int(round(time.time() * 1000)) # milliseconds
        delta_t = (t2 - t1)/1000.0
        print count
        print "rate (ports/sec): %f" % (count/(delta_t + 1e-6)) 
    if (beta_sum >= 4):
        #print cand_port
        pass
    count += 1
