from backtesting import Backtest, Strategy
from backtesting.lib import crossover

import pandas as pd
from ta.utils import dropna
from ta.volatility import BollingerBands
from ta.trend import sma_indicator

# Initialize Bollinger Bands Indicator


def SMA1(closing_data,l):
    sma2 = sma_indicator(data['Close'],10)
    return sma2



class SmaCross(Strategy):
    n1 = 10
    n2 = 20

    def init(self):
        close = self.data.Close
        self.sma1 = self.I(SMA1, close, self.n1)
        self.sma2 = self.I(SMA1, close, self.n2)

    def next(self):
        if crossover(self.sma1, self.sma2):
            self.buy()
        elif crossover(self.sma2, self.sma1):
            self.sell()


import yfinance as yf
data=yf.download('AMZN',start='2024-06-24',end='2024-06-29',interval='1m')
print(data)

ind1=SMA1(data['Close'],10)
print(ind1)




bt = Backtest(data, SmaCross,
              cash=10000, commission=.002,
              exclusive_orders=True)

output = bt.run()
bt.plot()