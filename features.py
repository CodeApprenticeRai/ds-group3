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

def individual_features(ind_data, stand_data):
    print('\n', ind_data)
    
    #change to our data
    ind_stock = pd.read_csv(ind_data, parse_dates=True, index_col='date',sep = ',')
    sp_500 = pd.read_csv(stand_data, parse_dates=True, index_col='date', sep = ',')
    
    #auto fill data 
    id = sp_500.index
    ind_stock = ind_stock.reindex(id, method='ffill')
    ind_stock = ind_stock.mask(ind_stock==0)
    ind_stock.fillna(method ='bfill', inplace = True)
    

    # joining the closing prices of the two datasets 
    #use recent 1 yrs data for training
    daily_prices = pd.concat([ind_stock.iloc[0:216,3], sp_500.iloc[0:216,3]], axis=1)
    daily_prices.columns = ['ind', 'SP500']
    
    #basic values
    C_t = daily_prices.iloc[1, 0]
    C_s = daily_prices.iloc[-1, 0]
    #print(C_t, C_s)
    #highest of high and lowest of low
    HH = ind_stock['high'].max()
    LL = ind_stock['low'].min()
    MA_5 = ind_stock.iloc[:5, 2].sum()/5
    '''
    features
    '''
    #momentum
    moment = C_t/C_s
    err = 1e-12 #deal with 0
    #William
    try:
        Wil = (HH - C_t)/(HH - LL)
    except:
        Wil = (HH - C_t)/(HH - LL + err)
    ROC = (C_t - C_s)/C_s
    D5_disp = C_t/MA_5
    try:
        Stoch = (C_t - ind_stock.iloc[1, 2])/(ind_stock.iloc[1, 1] - ind_stock.iloc[1, 2])
    except:
        Stoch = (C_t - ind_stock.iloc[1, 2])/(ind_stock.iloc[1, 1] - ind_stock.iloc[1, 2] + err)
    PVT = (C_t - daily_prices.iloc[2, 0])/daily_prices.iloc[2, 0] * ind_stock.iloc[1, 4]
    return [moment, Wil, ROC, D5_disp, Stoch, PVT]


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
compute 6 features for each stock and store it back to file
'''
def all_features(s_list, dPath, mPath):
    f_list = []
    for stock in s_list:
        stock_path = dPath + str(stock) + '.csv'
        f_list.append((stock, individual_features(stock_path, mPath)))
        
        '''
        if stock_Beta >= -20 and stock_Beta <= 100:
            b_list.append((stock, stock_Beta))
        else:
            print(stock, stock_Beta)
        '''
    return f_list

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
#beta_list = all_beta(stock_list, dataPath, marketPath)
#print(beta_list)
'''
print(max(n for _, n in beta_list if n > 0))
print(sum(n for _, n in beta_list if n > 0)/len(beta_list))
'''

#compute all features
feature_list = all_features(stock_list, dataPath, marketPath)
for f in feature_list:
    print(f)
#generate portfolios
#print('selecting portfolios')
#print(findPorts(beta_list, 4, 6))