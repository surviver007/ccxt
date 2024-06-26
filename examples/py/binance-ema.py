# -*- coding: utf-8 -*-

import os
import sys
import pandas_ta as ta
import pandas as pd

root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root + '/python')

import ccxt  # noqa: E402


print('CCXT Version:', ccxt.__version__)


def main():
    exchange = ccxt.binance(({
    'apiKey': 'eFB7692qkk1KOExLrE0PM05aEIqODSvSn7Ny5pFHHGk9t7IE8YpeHwUimQkcvjr7',
    'secret': 'S7TJ8QHTT7BsX2shd8MBQItszVRxaVQpGNhLXRsD1eLn671HBntalSvNvOsS2NSY',
}))
    markets = exchange.load_markets()
    # exchange.verbose = True  # uncomment for debugging purposes
    ohlcv = exchange.fetch_ohlcv('BTC/USDT', '1m')
    if len(ohlcv):
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms')
        ema = df.ta.ema()
        df = pd.concat([df, ema], axis=1)
        print(df)


main()
