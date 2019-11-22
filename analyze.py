import pandas as pd
import numpy as np
import math
import copy
import QSTK.qstkutil.qsdateutil as du
import datetime as dt
import QSTK.qstkutil.DataAccess as da
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkstudy.EventProfiler as ep
import csv
import sys

#example command line: "python analyze.py values.csv \$SPX"

data_to_analyze = np.loadtxt(sys.argv[1], dtype='string', delimiter=',', skiprows=0)
year = (int)(data_to_analyze[0,0])

dt_start = dt.datetime(2012, 1, 1)
dt_end = dt.datetime(2012, 12, 31)
ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt.timedelta(hours=16))

dataobj = da.DataAccess('Yahoo')
ls_symbols = [sys.argv[2]]

ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
ldf_data = dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
d_data = dict(zip(ls_keys, ldf_data))

df_close = d_data['close']
#df_close['PORTFOLIO VALUE'] = data_to_analyze[:, -1].astype(np.float)

df_close = df_close.fillna(method='ffill')
df_close = df_close.fillna(method='bfill')

na_returns = df_close.values

tsu.returnize0(na_returns)
average_daily_return = np.average(na_returns)
stdev = np.std(na_returns)

cumulative_return = np.cumprod(na_returns+1)
cumulative_return = cumulative_return[len(cumulative_return)-1]

print average_daily_return
print stdev
print cumulative_return


port_values = []
for row in data_to_analyze[:, -1].astype(np.float):
    port_values.append(row)
port_values = np.array(port_values)
print port_values
na_returns = port_values

tsu.returnize0(na_returns)
average_daily_return = np.average(na_returns)
stdev = np.std(na_returns)

cumulative_return = np.cumprod(na_returns+1)
cumulative_return = cumulative_return[len(cumulative_return)-1]

sharp_ratio = (float)(average_daily_return)/(float)(stdev)*math.sqrt(252)

print "Portfolio average daily return: " + str(average_daily_return)
print "Portfolio std: " + str(stdev)
print "Portfolio cumulative return: " + str(cumulative_return)
print "sharp ratio: " + str(sharp_ratio)
