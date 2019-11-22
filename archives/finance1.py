import backTest
import DataHelper
import datetime as dt
import itertools
import matplotlib.pyplot as plt
import math
import numpy as np
import os
import pandas as pd
import pickle
import QSTK.qstkutil.DataAccess as da
import QSTK.qstkfeat.features as ft
import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import random
from random import sample 
import socket
import statsmodels.api as sm
import sys
import threading
import time

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

def calcAllBetas1():
    '''
    print(max(n for _, n in beta_list if n > 0))
    print(sum(n for _, n in beta_list if n > 0)/len(beta_list))
    '''
    dataPath = './AlphaData/'
    marketPath = dataPath + 'SPY.csv'
    stock_list = []
    for filename in os.listdir(dataPath):
        #a stock file
        if filename[-3:] == 'csv':
	    if filename[:4] != 'ML4T' and filename[0] != '$' :
	        stock_list.append(filename[:-4])

    beta_list = all_beta(stock_list[:100], dataPath, marketPath)
    return beta_list

def calcAllBetas2(start_date_arr, end_date_arr, symbols_list):
    '''
    calculates all betas using QSTK
    '''
    
    if 'SPY' not in symbols_list:
        symbols_list.append('SPY')
    c_dataobj = da.DataAccess('Yahoo')
    start_date = dt.datetime(start_date_arr[0], start_date_arr[1], start_date_arr[2])
    end_date = dt.datetime(end_date_arr[0], end_date_arr[1], end_date_arr[2])

    dt_timeofday = dt.timedelta(hours=16)

    ldt_timestamps = du.getNYSEdays(start_date, end_date, dt_timeofday)

    keys_list = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
    ldf_data = c_dataobj.get_data(ldt_timestamps, symbols_list, keys_list)
    d_data = dict(zip(keys_list, ldf_data))

    #second parameter is number of days back
    betas = ft.featBeta(d_data, 200, 'SPY')

    list_betas = zip(betas.columns, betas.ix[betas.shape[0] - 1, :])
    del list_betas[-1]
    return list_betas

def individual_Beta(ind_data, stand_data):
    #change to our data
    ind_stock = pd.read_csv(ind_data, parse_dates=True, index_col=0, sep = ',')
    sp_500 = pd.read_csv(stand_data, parse_dates=True, index_col=0, sep = ',')
    # joining the closing prices of the two datasets 
    #use recent 3 yrs data for training
    temp1 = ind_stock['close']
    closes = temp1[0:216]
    temp2 = sp_500['close']
    closeSP = temp2[0:216]
    monthly_prices = pd.concat([closes, closeSP], axis=1)
    monthly_prices.columns = ['ind', 'SP500']


    # check the head of the dataframe
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


def port_select(beta_list):
    count = 0
    portfolio_list = []
    a = itertools.combinations(beta_list, 4)
    t1 = int(round(time.time() * 1000)) # milliseconds
    for _ in xrange(0, int(210)):
        cand_port = next(a)
        beta_sum = sum(n for _, n in cand_port)
        if count % 100 == 0:
	    t2 = int(round(time.time() * 1000)) # milliseconds
	    delta_t = (t2 - t1)/1000.0
	    #print count
	    #print "rate (ports/sec): %f" % (count/(delta_t + 1e-6)) 
        if (beta_sum >= 4):
    	    #print cand_port
	        portfolio_list.append(cand_port)
        #count += 1
    return portfolio_list

def backtest_list(start_date, end_date, port_list, sharpe_threshold):
    fh = open("./portSharpe.csv", "w")
    for port in port_list:
        symbols = [sym for sym, _ in port]
        #volatility, average_daily_return, sharpe, cumulative_return = simulate(start, end, symbols, allocation)
        volatility, average_daily_return, sharpe, cumulative_return = backTest.simulate(start_date, end_date, symbols, [0.25, 0.25, 0.25, 0.25])
        line = ",".join(symbols) + "," + str(sharpe) + "\n"
        fh.writelines(line)
        print line
    fh.close()


#start = dt.datetime(2008,1,1)
#end = dt.datetime(2008,12,31)
start_arr = [2008, 1, 1]
end_arr = [2008, 12, 31]

#get symbols from list
symbols = sample(da.DataAccess('Yahoo').get_symbols_from_list('sp5002008'), 10)

#calc betas with regression
#betas = calcAllBetas1()
#port_select(betas)

#calc betas with QSTK
#betas = calcAllBetas2(start_arr, end_arr, symbols)
#port_list = port_select(betas)
#backtest_list(dt.datetime(2009,1,1), dt.datetime(2009,12,31), port_list, 1.2)
