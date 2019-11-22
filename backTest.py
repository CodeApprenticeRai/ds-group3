import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da
import QSTK.qstkfeat.features as ft
import numpy as np
import math
import itertools as it

import copy
import datetime as dt
import finance
import matplotlib.pyplot as plt
import pandas as pd

def simulate(start_date, end_date, symbols_list_with_beta, allocation_list):
    symbols_list = [sym for sym,_ in symbols_list_with_beta]
    betas_list = [beta for _, beta in symbols_list_with_beta]

    dt_timeofday = dt.timedelta(hours=16)
    ldt_timestamps = du.getNYSEdays(start_date, end_date, dt_timeofday)

    c_dataobj = da.DataAccess('Yahoo')
    keys_list = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
    ldf_data = c_dataobj.get_data(ldt_timestamps, symbols_list, keys_list)
    d_data = dict(zip(keys_list, ldf_data))

    dataframe_returns = d_data['close'].copy()
    dataframe_returns = dataframe_returns.fillna(method='ffill')
    dataframe_returns = dataframe_returns.fillna(method='bfill')

    na_returns = dataframe_returns.values
    tsu.returnize0(na_returns)

    array_dimensions = na_returns.shape
    num_rows = array_dimensions[0]
    num_cols = array_dimensions[1]

    for index in range(len(allocation_list)):
        allocation_list[index] = allocation_list[index] * 100;
    daily_portfolio_return = [100]
    for index in range(1,num_rows):
        row = na_returns[index,:]+1
        allocations = np.array(allocation_list)
        allocations = allocations.reshape((len(allocation_list),1))
        temp = np.dot(row, allocations)
        daily_portfolio_return.append(temp[0])
        for index2 in range(num_cols):
            allocation_list[index2]=row[index2]*allocation_list[index2]

    daily_portfolio_return = np.array(daily_portfolio_return)
    daily_portfolio_return = daily_portfolio_return.reshape(len(daily_portfolio_return), 1)
    tsu.returnize0(daily_portfolio_return)

    average_daily_return = np.average(daily_portfolio_return)

    #calc new percentage of portfolio for each stock
    sum_alloc = sum(allocation_list)
    percent_alloc = np.array([x/sum_alloc for x in allocation_list])

    #create a np array of just beta values originally (ticker, beta)
    beta_arr = np.array(betas_list)

    #calculate portfolio beta
    pBeta = beta_arr.dot(percent_alloc)

    #calculate standard deviation of daily return
    stdDev = np.std(daily_portfolio_return)

    #calculate Sharpe ratio for 250 day period
    sharpe_ratio = math.sqrt(252)*average_daily_return/stdDev

    #calculate cumulative return
    #cumulative_return = np.cumprod(daily_portfolio_return+1)
    #cumulative_return = cumulative_return[len(cumulative_return)-1]

    return symbols_list, pBeta, sharpe_ratio

#Case 1
#symbols = ["AAPL", "GLD", "GOOG", "XOM"]
#start = dt.datetime(2011,1,1)
#end = dt.datetime(2011,12,31)
#allocate = [0.4, 0.4, 0, 0.2]
#volatility, average_daily_return, sharpe, cumulative_return = simulate(start, end, symbols, allocate)
    
#Case 2
#symbols = ["AXP", "HPQ", "IBM", "HNZ"]
#start = dt.datetime(2010,1,1)
#end = dt.datetime(2010,12,31)
#allocate = [0.0, 0.0, 0.0, 1.0]
#volatility, average_daily_return, sharpe, cumulative_return = simulate(start, end, symbols, allocate)

#Case 3
#symbols = ["AXP", "HPQ", "IBM", "HNZ"]
#start = dt.datetime(2010,1,1)
#end = dt.datetime(2010,12,31)
#volatility, average_daily_return, sharpe, cumulative_return, allocation = best_allocation(start, end, symbols)

#print "Start date: " + str(start)
#print "End date: " + str(end)
#print "Symbols: " + str(symbols)
#print "Optimal Allocation: " + str(allocation)
#print "Sharpe Ratio: " + str(sharpe)
#print "Volatility (stdev of daily returns): " + str(volatility)
#print "Average daily return: " + str(average_daily_return)
#print "Cumulative Return: " + str(cumulative_return)

#Case 4
#symbols = ["AAPL", "GLD", "GOOG", "XOM"]
#start = dt.datetime(2011,1,1)
#end = dt.datetime(2011,12,31)
#volatility, average_daily_return, sharpe, cumulative_return, allocation = best_allocation(start, end, symbols)

#print "Start date: " + str(start)
#print "End date: " + str(end)
#print "Symbols: " + str(symbols)
#print "Optimal Allocation: " + str(allocation)
#print "Sharpe Ratio: " + str(sharpe)
#print "Volatility (stdev of daily returns): " + str(volatility)
#print "Average daily return: " + str(average_daily_return)
#print "Cumulative Return: " + str(cumulative_return)

#Case 5
#symbols = ['BRCM', 'TXN', 'IBM', 'HNZ'] 
#start = dt.datetime(2010,1,1)
#end = dt.datetime(2010,12,31)
#volatility, average_daily_return, sharpe, cumulative_return, allocation = best_allocation(start, end, symbols)

#print "Start date: " + str(start)
#print "End date: " + str(end)
#print "Symbols: " + str(symbols)
#print "Optimal Allocation: " + str(allocation)
#print "Sharpe Ratio: " + str(sharpe)
#print "Volatility (stdev of daily returns): " + str(volatility)
#print "Average daily return: " + str(average_daily_return)
#print "Cumulative Return: " + str(cumulative_return)

#Case 5:
#symbols = ['BRCM', 'TXN', 'IBM', 'HNZ'] 
#symbols = ["MU", 'BA', 'ALGN', 'NVDA']
#start = dt.datetime(2017,1,1)
#end = dt.datetime(2017,12,31)
#allocation_orig = (1.0/len(symbols),) * len(symbols)
#allocation = list(allocation_orig)
#volatility, average_daily_return, sharpe, cumulative_return = simulate(start, end, symbols, allocation)

#print "Start date: " + str(start)
#print "End date: " + str(end)
#print "Symbols: " + str(symbols)
#print "Allocation: " + str(allocation_orig)
#print "Change: " + str(allocation) 
#print "Sharpe Ratio: " + str(sharpe)
#print "Volatility (stdev of daily returns): " + str(volatility)
#print "Average daily return: " + str(average_daily_return)
#print "Cumulative Return: " + str(cumulative_return)
