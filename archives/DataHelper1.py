import json, requests, pandas as pd
import os
import time

class DataHelper:
    def __init__(self):
        self.alpha_vantage_api_key = None

        with open("config.json") as config:
            self.alpha_vantage_api_key = json.load(config)["alpha_vantage_api_key"]

        self.default_request_params = {
            # "symbol": None, # required
            "function": "TIME_SERIES_DAILY",
            "outputsize": "full",
            "datatype": "json",
            "apikey": self.alpha_vantage_api_key
        }

    '''
        Returns price-history for a single
        ticker as JSON
    '''
    def _get_data(self, ticker_symbol):

        request_params = dict(self.default_request_params)
        request_params["symbol"] = ticker_symbol

        response = requests.get("https://www.alphavantage.co/query?", params=request_params)

        return response.json()


    '''
        Returns price-history for given
        tickers as a datetime-indexed dataframe
    '''

    def get_data(self, list_of_ticker_symbols):
        master_df = pd.DataFrame()
        notExist = []
        i = 0
        for i in range(len(list_of_ticker_symbols)):
            ticker_symbol = list_of_ticker_symbols[i]
            ex = 0
            while True:
                try:
                    data = self._get_data(ticker_symbol)
                    print(ticker_symbol)
                    data_as_df = pd.DataFrame.from_dict(data["Time Series (Daily)"],
                                                        orient='index')  # !! flagged for unoptimized
                    #save stock data to file
                    path = './AlphaData/' + str(ticker_symbol) + '.csv'
                    head = ['date', 'open', 'high', 'low', 'close', 'volume']
                    data_as_df = data_as_df.reset_index()
                    #data_as_df.columns = head
                    data_as_df.to_csv(path, header = head, sep=',', index=False)
                    # extract closing price
                    #master_df[ticker_symbol] = data_as_df["4. close"].apply( lambda price : float(price) )
                    i += 1
                    break
                except Exception: # Try to catch something more specific
                    ex += 1
                    if ex == 2 :
                        #record this as not exist and get data for next one
                        i += 1
                        ex = 0
                        notExist.append(ticker_symbol)
                        break
                    else:
                        time.sleep(60)
                    pass

        return notExist