from backtesting import Backtest, Strategy


import pandas as pd
from ta.utils import dropna
from ta.volatility import BollingerBands
from ta.trend import sma_indicator,ema_indicator

def EMA1(closing_data,l1):
    return ema_indicator(closing_data,l1)



def SMA1(closing_data,l):
    sma2 = sma_indicator(closing_data,l)
    return sma2

def SMA2(closing_data,l):
    sma2 = sma_indicator(closing_data,l)
    return sma2


class Sma_Strategy(Strategy):

    def init(self):
        closing_price=self.data.Close.s
        self.sma1=self.I(SMA1,closing_price,20)
        self.sma2=self.I(SMA2,closing_price,50)



    def next(self):
        if self.sma1[-1]<self.sma2[-1] and self.sma1[-2]>self.sma2[-2]:
            self.buy()
        if self.sma1[-1]>self.sma2[-1] and self.sma1[-2]<self.sma2[-2]:
            self.position.close()
        


import yfinance as yf
data=yf.download('GOOG',start='2020-06-24',end='2024-06-29',interval='1d')
print(data)


# data=pd.read_csv('GOOG_5min.csv')
# print(data)
# data['Date']=pd.to_datetime(data['Date'])
# data.set_index('Date',inplace=True)
# print(data)

# data=data['2023-01-03 14:30:00':'2023-06-03 14:30:00']
# print(data)
bt = Backtest(data, Sma_Strategy,
              cash=10000, commission=.002,
              exclusive_orders=True)

output = bt.run()
print(output)
# print(output['_trades'])
bt.plot()