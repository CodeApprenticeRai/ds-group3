# import libraries
import pandas as pd
import statsmodels.api as sm
import numpy as np
import DataHelper
import os
import time
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


#stock list(all file names)
stock_list = ['ACAS', 'ANDV', 'APC', 'APOL', 'ARG', 'BCR', 'BDK', 'BEAM', 'BF.B', 'BJS', 'BMS', 'BRCM', 'BRLI', 'CAM', 'CBG', 'CCMO', 'CFC+A', 'CFN', 'COH', 'CPWR', 'CVC', 'DPS', 'DV', 'DWDP', 'EDS', 'EK', 'ERTS', 'ESV', 'FDO', 'FMCC', 'FNMA', 'FRX', 'GENZ', 'GGP', 'HCBK', 'HCN', 'HRS', 'HSP', 'IACI', 'JAVA', 'JDSU', 'JNS', 'JOY', 'KFT', 'KG', 'KORS', 'LEHMQ', 'LIZ', 'LLL', 'LLTC', 'LO', 'LTD', 'LUK', 'LXK', 'MHP', 'MHS', 'MI', 'MIL', 'MJN', 'MON', 'MWV', 'MWW', 'MYL', 'NAVI', 'NBL', 'NBR', 'NCC', 'NCLH', 'NDAQ', 'NE', 'NEE', 'NEM', 'NFLX', 'NFX', 'NI', 'NKE', 'NLSN', 'NOC', 'NOV', 'NOVL', 'NRG', 'NSC', 'NSM', 'NTAP', 'NTRS', 'NU', 'NUE', 'NVDA', 'NVLS', 'NWL', 'NWS', 'NWSA', 'NYT', 'NYX', 'O', 'ODP', 'OI', 'OKE', 'OMC', 'OMX', 'ORCL', 'ORLY', 'OXY', 'PAYX', 'PBCT', 'PBG', 'PBI', 'PCAR', 'PCG', 'PCL', 'PCLN', 'PCP', 'PCS', 'PDCO', 'PEG', 'PEP', 'PFE', 'PFG', 'PG', 'PGN', 'PGR', 'PH', 'PHM', 'PKG', 'PKI', 'PLD', 'PLL', 'PM', 'PNC', 'PNR', 'PNW', 'POM', 'PPG', 'PPL', 'PRGO', 'PRU', 'PSA', 'PSX', 'PTV', 'PVH', 'PWR', 'PX', 'PXD', 'PYPL', 'Q', 'QCOM', 'QEP', 'QLGC', 'QRVO', 'R', 'RAI', 'RCL', 'RDC', 'RE', 'REG', 'REGN', 'RF', 'RHI', 'RHT', 'RIG', 'RJF', 'RL', 'RMD', 'ROH', 'ROK', 'ROP', 'ROST', 'RRC', 'RRD', 'RSG', 'RSH', 'RTN', 'S', 'SAF', 'SAI', 'SBAC', 'SBUX', 'SCG', 'SCHW', 'SDS', 'SE', 'SEE', 'SGP', 'SH', 'SHLD', 'SHW', 'SIAL', 'SIG', 'SII', 'SINE_FAST', 'SINE_FAST_NOISE', 'SINE_SLOW', 'SINE_SLOW_NOISE', 'SJM', 'SLB', 'SLE', 'SLG', 'SLM', 'SNDK', 'SNI', 'SPLS', 'STJ', 'SVU', 'SWY', 'T', 'TE', 'TIE', 'TMK', 'TSO', 'TWC', 'TYC', 'VIA.B', 'WAG', 'WAMUQ', 'WFM', 'WFR', 'WFT', 'WIN', 'WLP', 'WPI', 'WPO', 'WWY', 'WYE', 'WYN', 'XTO', 'YHOO', 'ZMH']
print(len(stock_list))
'''
for filename in os.listdir('./mergedQSTKandKaggleData/'):
    #a stock file
    if filename[-3:] == 'csv':
        if filename[:4] != 'ML4T' and filename[0] != '$' :
            stock_list.append(filename[:-4])
'''
#use DataHelper to get data
dh = DataHelper.DataHelper()
nonExist = dh.get_data(stock_list)
#stocks_df = dh.get_data(stock_list)
print(nonExist)
#individual_Beta('./mergedQSTKandKaggleData/AA.csv', './mergedQSTKandKaggleData/SPY.csv')