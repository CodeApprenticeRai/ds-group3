import json, requests, pandas as pd
import os

class DataHelper:
    def __init__(self):
        self.alpha_vantage_api_key = None

        with open("config.json") as config:
            self.alpha_vantage_api_key = json.load(config)["alpha_vantage_api_key"]

        self.default_request_params = {
            # "symbol": None, # required
            "function": "TIME_SERIES_DAILY",
            "outputsize": "compact",
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

        for ticker_symbol in list_of_ticker_symbols:
            data = self._get_data(ticker_symbol)
            data_as_df = pd.DataFrame.from_dict(data["Time Series (Daily)"],
                                                orient='index')  # !! flagged for unoptimized

            # extract closing price
            master_df[ticker_symbol] = data_as_df["4. close"].apply( lambda price : float(price) )

        return master_df