import pandas as pd
import statsmodels.api as sm
import numpy as np
import os

dataPath = './mergedQSTKandKaggleData/'
stock_list = []
for filename in os.listdir(dataPath):
    #a stock file
    if filename[-3:] == 'csv':
        rel_path = dataPath + filename
        df = pd.read_csv(rel_path, parse_dates=True,sep = ',')
        new_head = ['date','open','high','low','close','volume','adj close']
        df.to_csv(rel_path, sep=',', header=new_head, index=False)
