import pandas as pd
import statsmodels.api as sm
import itertools
import heapq
import json


'''
    Pipeline:
        1. Calculate Beta for Each Stock in a Given List: all_beta ->
        2. Given a List of Stocks Find Groupings That Satisfy a Beta Sum Condition:  find_ports ->
        3. Given a List of Portfolios ( List of Stock Tickers ) and a Date Range Compute the
            performance for each portfolio: generate_performance_reports
        4. Plot Performance:
'''
def individual_beta(ind_data, stand_data, start_date, end_date):
    #change to our data
    ind_stock = pd.read_csv(ind_data, parse_dates=True, index_col='date',sep = ',')
    ind_stock = ind_stock.reindex(index=ind_stock.index[::-1])

    sp_500 = pd.read_csv(stand_data, parse_dates=True, index_col='date', sep = ',')
    sp_500 = sp_500.reindex(index=sp_500.index[::-1])

    ind_stock = apply_daterange_filter( ind_stock, start_date, end_date )
    sp_500 = apply_daterange_filter( sp_500, start_date, end_date )

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
        return 0


'''
compute beta for all stocks in a given list
'''
def all_beta(s_list, dPath, mPath, start_date, end_date):
    b_list = []
    for stock in s_list:
        stock_path = dPath + str(stock) + '.csv'
        stock_Beta = individual_beta(stock_path, mPath, start_date, end_date)
        if stock_Beta >= -20 and stock_Beta <= 100:
            b_list.append((stock, stock_Beta))
#         else:
#             print(stock, stock_Beta)
    return b_list


'''
generate portfolios
'''
def findPorts(s_list, num, thre):#stock list, size of portfolio, threshold
    port_list = []
    cand_portfolios = set(itertools.combinations(s_list, num))
    for cand_port in cand_portfolios:
        beta_sum = sum(n for _ , n in cand_port)
        if (beta_sum >= thre):
            port_list.append(cand_port)
    return port_list



'''
    Return dictionary with structure:

    {
        stock_list,
        df_of_performance_of_each_stock_in_stock_list,
        portfolio_performance
    }

'''
def get_individual_porfolio_performance( stock_list, start_date, end_date ):
    data_directory = './AlphaData/'

    master_df = pd.DataFrame()

    for ticker in stock_list:
        stock_df = pd.read_csv( data_directory + ticker + ".csv", parse_dates=True, index_col='date', sep = ',')
        stock_df = stock_df.reindex(index=stock_df.index[::-1])
        stock_df = apply_daterange_filter( stock_df['close'], start_date, end_date )
        master_df[ ticker ] = stock_df

    master_df[ 'portfolio' ] =  master_df.sum( axis=1 )
    master_df[ 'performance' ] = master_df[ 'portfolio'].pct_change().fillna(0).cumsum()

    report = {
        "stock_list": stock_list,
        "data": master_df,
        "performance": master_df[ 'performance' ][-1]
    }

    return report



def apply_daterange_filter( df, start_date, end_date ):
    _filter = ( df.index.get_level_values(0) >= start_date ) & ( df.index.get_level_values(0) <= end_date )
    return df[ _filter ]

class PerformanceReportObject:
    def __init__(self, max_heap_of_performance_reports):
        self.reports = max_heap_of_performance_reports

    def get_top_n_performing_portfolios(self, n):
        n = min ( len(self.reports), n )
        top_n_performing_portfolios = [ heapq.heappop( self.reports ) for i in range( n ) ]

        for i in range(n):
            heapq.heappush( self.reports, top_n_performing_portfolios[i] )

        return [ report[-1] for report in top_n_performing_portfolios ]

    '''
        For each portfolio in the report,
        plot performance vs time
    '''
    def plot_performance(self, n=-1):
        if ( n == -1 ):
            n = len(self.reports)

        ax = None
        for i in range(n):
            report = self.reports[i][2]
            if ( ax == None ):
                ax = report["data"]["performance"].plot()
            else:
                report["data"]["performance"].plot( ax=ax )

        return ax


def generate_performance_reports( portfolios, start_date, end_date ):
    performance_report = []
    for portfolio in portfolios:
        _stock_list = []
        _beta_sum = 0
        for i in range(len(portfolio)):
            _stock_list.append( portfolio[i][0] )
            _beta_sum += portfolio[i][1]

        _report = get_individual_porfolio_performance( _stock_list, start_date, end_date )
        _report["beta_sum"] = _beta_sum

        heapq.heappush( performance_report, ( -1 * _report["performance"], id(_report), _report )  ) # push to list while maintaining max-heap constraint

    return PerformanceReportObject( performance_report )


#get stock list
def generate_stock_list(): # only needs to be called once if the value isn't already cached
    data_directory = './AlphaData/'
    marketPath = data_directory + 'SPY.csv'
    stock_list = []

    i = 0
    stock_list
    directory_contents = os.listdir(data_directory)
    while( i < len(directory_contents) ):
        filename = directory_contents[i]
        if filename[-3:] == 'csv':
            if filename[:4] != 'ML4T' and filename[0] != '$' :
                stock_list.append(filename[:-4])
        i += 1

    data = {
        "stock_list": stock_list
    }

    with open('cache.json', 'w') as out_file:
        json.dump( data, out_file )
    return None

# if name == "__main__":
#     if not os.path.exists( "cache.json" ):
#         generate_stock_list
#
#     stock_list = json.load( "cache.json" )["stock_list"]
#
#     #compute all beta
#     beta_list = all_beta(stock_list, data_directory, marketPath)
#
#     #generate portfolios brute force
#     print('selecting portfolios')
#     print(findPorts(beta_list, 4, 6))
