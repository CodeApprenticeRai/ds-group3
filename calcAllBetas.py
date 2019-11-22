import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da
import numpy as np
import math
import itertools as it

import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import QSTK.qstkfeat.features as ft
from random import sample 

start = dt.datetime(2008,1,1)
end = dt.datetime(2008,12,31)

dt_timeofday = dt.timedelta(hours=16)
ldt_timestamps = du.getNYSEdays(start, end, dt_timeofday)
c_dataobj = da.DataAccess('Yahoo')
symbols_list = sample(c_dataobj.get_symbols_from_list('sp5002008'), 10) + ['SPY']
#symbols_list.sort() 

keys_list = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
ldf_data = c_dataobj.get_data(ldt_timestamps, symbols_list, keys_list)
#ldf_data = ldf_data.fillna(method='ffill')
#ldf_data = ldf_data.fillna(method='bfill')
d_data = dict(zip(keys_list, ldf_data))

#second parameter is number of days back
betas = ft.featBeta(d_data, 200, 'SPY')

list_betas = zip(betas.columns, betas.ix[betas.shape[0] - 1, :])
print list_betas




