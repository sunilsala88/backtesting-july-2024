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
        


# import yfinance as yf
# data=yf.download('GOOG',start='2020-06-24',end='2024-06-29',interval='1d')
# print(data)

from ib_insync import *
# util.startLoop()  # uncomment this line when in a notebook
import datetime as dt
import pandas as pd
ib = IB()
ib.connect('127.0.0.1', 7497, clientId=66)

def last_day_of_month(year, month):
    next_month = month % 12 + 1
    next_year = year + month // 12
    last_day = dt.date(next_year, next_month, 1) - dt.timedelta(days=1)
    return last_day


name='GOOG'
contract2=Stock(name,'SMART','USD')
# year=5
final_data=pd.DataFrame()
for month in range(1,6):

    end_time=last_day_of_month(2023, month)
    print(end_time)
    bars = ib.reqHistoricalData(
        contract2, endDateTime=end_time, durationStr='1 M',
        barSizeSetting='5 mins', whatToShow='TRADES', useRTH=True,formatDate=2)
    df1 = util.df(bars)
    print(df1)
    final_data=pd.concat([final_data,df1],axis=0).drop_duplicates()
    
print(final_data)

d1={'date':'Date','open':'Open','high':'High','low':'Low','close':'Close','volume':'Volume'}
final_data.rename(columns =d1, inplace = True) 
final_data.set_index('Date',inplace=True)
final_data.to_csv(f'{name}_5min.csv')
data=final_data






bt = Backtest(data, Sma_Strategy,
              cash=10000, commission=.002,
              exclusive_orders=True)

output = bt.run()
print(output)
bt.plot()