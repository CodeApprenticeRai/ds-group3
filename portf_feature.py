import features

import pandas as pd
import statsmodels.api as sm
import numpy as np
import DataHelper
import statistics 
import os
import itertools

'''
compute portfolio features based on individual stocks
'''
def port_features(pFile, dPath, mPath):
    df = pd.read_csv(pFile, header=None, names=["s1", "s2", "s3", "s4", "sharpe"])

    #initialize feature cols
    df['momentum'] = 0.0
    df['William'] = 0.0
    df['ROC'] = 0.0
    df['5D_disparity'] = 0.0
    df['Stochastic'] = 0.0
    df['PVT'] = 0.0

    #get stock list and compute individual features
    for index, row in df.iterrows():
        stock_list = [row['s1'], row['s2'], row['s3'],row['s4']]
        #print('\n',stock_list)
        f_list = features.all_features(stock_list, dPath, mPath)
        pf_list = [statistics.mean(x) for x in zip(*f_list)]    #protfolio features
        df.loc[index, 'momentum'] = pf_list[0]
        df.loc[index, 'William'] = pf_list[0]
        df.loc[index, 'ROC'] = pf_list[0]
        df.loc[index, '5D_disparity'] = pf_list[0]
        df.loc[index, 'Stochastic'] = pf_list[0]
        df.loc[index, 'PVT'] = pf_list[0]
        #print(f_list)
    #print(df.head())
    #give label to different portfolios
    df['TARGET CLASS'] = np.where(df['sharpe']>=1.5, 1, 0)
    #save to file 
    df.to_csv('./features.csv', sep=',', index=False)
    



#configuration
dataPath = './mergedQSTKandKaggleData/'
marketPath = dataPath + 'SPY.csv'
port_file = './testResults.csv'

#get labelled data with features
port_features(port_file, dataPath, marketPath)