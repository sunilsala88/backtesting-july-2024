from backtesting import Backtest, Strategy


import pandas as pd
from ta.utils import dropna
from ta.volatility import BollingerBands
from ta.trend import sma_indicator




def SMA1(closing_data,l):
    sma2 = sma_indicator(data['Close'],l)
    return sma2


class Sma_Strategy(Strategy):

    def init(self):
        closing_price=self.data.Close.s
        self.sma1=self.I(SMA1,closing_price,20)
        self.sma2=self.I(SMA1,closing_price,50)

    def next(self):
        pass


import yfinance as yf
data=yf.download('AMZN',start='2024-06-24',end='2024-06-29',interval='1m')
print(data)

ind1=SMA1(data['Close'],10)
print(ind1)




bt = Backtest(data, Sma_Strategy,
              cash=10000, commission=.002,
              exclusive_orders=True)

output = bt.run()
print(output)
# bt.plot()