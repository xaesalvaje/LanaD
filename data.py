import pandas as pd
import backtrader as bt
from indicators import EMA, RSI, MACD

class BotData:
    def __init__(self, symbol, timeframe):
        self.symbol = symbol
        self.timeframe = timeframe
        self.data = pd.read_csv(f'data/{self.symbol}_{self.timeframe}.csv')
        self.data['datetime'] = pd.to_datetime(self.data['datetime'])
        self.data.set_index('datetime', inplace=True)
        

    def new_method(self):
        raw_data = pd.read_csv("1min_data.csv")
        raw_data.head()

    def get_latest_candle(self):
        return self.data.iloc[-1]

    def get_candles(self, n):
        return self.data.iloc[-n:]

    def add_indicators(self, indicator_list, cerebro):
        for indicator in indicator_list:
            if indicator == 'SMA':
                self.data['sma'] = self.data['close'].rolling(20).mean()

            elif indicator == 'EMA':
                cerebro.addindicator(EMA)

            elif indicator == 'RSI':
                cerebro.addindicator(RSI)

            elif indicator == 'MACD':
                cerebro.addindicator(MACD)

            # Add your custom indicators here
            
        return self.data
