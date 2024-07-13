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
    n1=28
    n2=69

    def init(self):
        closing_price=self.data.Close.s
        self.sma1=self.I(SMA1,closing_price,self.n1)
        self.sma2=self.I(SMA2,closing_price,self.n2)



    def next(self):
        if self.sma1[-1]>self.sma2[-1] and self.sma1[-2]<self.sma2[-2]:
            if self.position.is_short:
                self.position.close()
                self.buy()
            else:
                self.buy()
        if self.sma1[-1]<self.sma2[-1] and self.sma1[-2]>self.sma2[-2]:
            if self.position.is_long:
                self.position.close()
                self.sell()
            else:
                self.sell()
        


# import yfinance as yf
# data=yf.download('^NSEBANK',start='2020-06-24',end='2024-06-29',interval='1d')
# print(data)


data=pd.read_csv('GOOG_5min.csv')
print(data)
data['Date']=pd.to_datetime(data['Date'])
data.set_index('Date',inplace=True)
print(data)
data=data['2023-01-03 14:30:00':'2023-06-03 14:30:00']
print(data)




# Resample the data
ohlcv_dict = {
     'Open': 'first',
     'High': 'max',
     'Low': 'min',
     'Close': 'last',
     'Volume': 'sum'
}


data = data.resample('15T').agg(ohlcv_dict)
data.dropna(inplace=True)



bt = Backtest(data, Sma_Strategy,
              cash=1000, commission=.002,
              exclusive_orders=True)

output = bt.run()
print(output)
output['_trades'].to_csv('trades.csv')
bt.plot()

# n1_list=range(10,30,5)
# n2_list=range(50,80,1)


# stats=bt.optimize(n1=n1_list,n2=n2_list,maximize='Win Rate [%]')
# print(stats)
# print('GOOG',stats['_strategy'])
# bt.plot()

#overfitting