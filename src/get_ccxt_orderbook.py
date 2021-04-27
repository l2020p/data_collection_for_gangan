# -*- coding: utf-8 -*-

import asyncio
import os
import sys

root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root + '/python')

import ccxt.async_support as ccxt  # noqa: E402

async def run_all_exchanges(exchange_ids,symbols):
    results = {}

    for exchange_id in exchange_ids:
        exchange = getattr(ccxt, exchange_id)({
            'enableRateLimit': True,  # required accoding to the Manual
            'options': {
                'useWebapiForFetchingFees': False,
            }
        })
        print('Exchange:', exchange_id)
        tickers = {}
        if len(symbols) == 0:
            markets = await load_markets(exchange)
            print("No symbols provide, fetch all available tickers from market.")
            print(list(markets.keys()))
            symbols = list(markets.keys())

        for symbol in symbols:
            ticker = await fetch_ticker(exchange, symbol)  # ←------------ STEP 2
            tickers[symbol] = ticker
        
            print(symbol, 'orderbook:')
            orderbook = await fetch_orderbook(exchange, symbol)  # ←------ STEP 3
            print(orderbook)
        await exchange.close()  # ←----------- LAST STEP GOES AFTER ALL CALLS
        results[exchange_id] = tickers
    return results


async def load_markets(exchange):
    try:
        result = await exchange.load_markets()
        return result
    except ccxt.BaseError as e:
        print(type(e).__name__, str(e), str(e.args))
        raise e


async def fetch_ticker(exchange, symbol):
    try:
        result = await exchange.fetch_ticker(symbol)
        return result
    except ccxt.BaseError as e:
        print(type(e).__name__, str(e), str(e.args))
        raise e


async def fetch_orderbook(exchange, symbol):
    try:
        result = await exchange.fetch_order_book(symbol)
        return result
    except ccxt.BaseError as e:
        print(type(e).__name__, str(e), str(e.args))
        raise e


if __name__ == '__main__':
    exchange_ids = ['bitfinex']
    symbols = ['ETH/BTC']
    results = asyncio.get_event_loop().run_until_complete(run_all_exchanges(exchange_ids,symbols))
    print("======== PRINT ALL TICKER ========")
    print([(exchange_id, ticker) for exchange_id, ticker in results.items()])