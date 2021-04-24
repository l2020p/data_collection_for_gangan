import quandl
import pandas as pd
import numpy as np

quandl.ApiConfig.api_key="_Hi22UWDBu6vwiBhsLpS"

# This function is supposed to create a list of quandl tickers
# quandl futures tickers has the following pattern
# [exchange]/[future_root]+[month_code]+[yyyy]
# example: get_quandl_futures_ticker('CFFEX/IF',2018,2020)
# more tickers name please check on https://www.quandl.com/data/
def get_quandl_futures_ticker(root,start_year,end_year):
	month_code = ['F','G','H','J','K','M','N','Q','U','V','X','Z']
	futures_ticker_list = []
	for year in range(start_year,end_year):
		for month in month_code:
			futures_ticker_list.append(root+month+str(year))
	return(futures_ticker_list)

# This function returned all columns of given tickers
def get_data_quandl(tickers):
	data_list = []
	for ticker in tickers:
		data = quandl.get(ticker)
		data['ticker'] = ticker
		data_list.append(data)
	all_data = pd.concat(data_list)
	return(all_data)
