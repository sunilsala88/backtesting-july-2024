

# from ib_insync import *
# # util.startLoop()  # uncomment this line when in a notebook
# import datetime as dt
# import pandas as pd
# ib = IB()
# ib.connect('127.0.0.1', 7497, clientId=66)

# contract2=Stock('TSLA','NYSE','USD')
# bars = ib.reqHistoricalData(
#     contract2, endDateTime='', durationStr='1 Y',
#     barSizeSetting='1 hour', whatToShow='TRADES', useRTH=True,formatDate=2)
# df1 = util.df(bars)

# d1={'date':'Date','open':'Open','high':'High','low':'Low','close':'Close','volume':'Volume'}
# df1.rename(columns =d1, inplace = True) 
# df1.set_index('Date',inplace=True)
# data=df1
# print(data)
# data.to_csv('TSLA_1hour.csv')  





import pandas_ta as ta
import pandas as pd
from backtesting import Strategy, Backtest
import yfinance as yf
import pandas_ta as ta
from backtesting.lib import resample_apply
import time
def supertrend1(high_data,low_data,close_data):
    o=ta.supertrend(high_data,low_data,close_data,length=10)
    print(o)
    return o['SUPERTd_10_3.0']
def supertrend2(high_data,low_data,close_data):
    o=ta.supertrend(high_data,low_data,close_data,length=10)
    return o['SUPERT_10_3.0']
def ema(close_data,period=9):
    return ta.ema(close_data,length=period)


class supertrend(Strategy):
    
    n1=9

    def init(self):
        self.super1=self.I(supertrend1,self.data.High.s,self.data.Low.s,self.data.Close.s)
        self.super2=self.I(supertrend2,self.data.High.s,self.data.Low.s,self.data.Close.s)
        
        self.ema_hour=self.I(ema,self.data.Close.s,self.n1)

        self.daily_ema = resample_apply('D', ema,self.data.Close.s,self.n1)

    def next(self):

        if self.super1[-1]>0 and self.data.Close[-1]> self.daily_ema[-1]:


            if self.position.is_short:
                self.position.close()
                self.buy()



            elif not self.position:  
                self.buy()


        elif self.super1[-1]<0 and self.data.Close[-1]<self.daily_ema[-1]:
            if self.position.is_long:
                self.position.close()
                self.sell()


data=pd.read_csv('TSLA_1hour.csv')
data['Date']=pd.to_datetime(data['Date'])
data['Date']=data['Date'].dt.tz_localize(None)
data.set_index('Date',inplace=True)
#remove duplicates
data=data[~data.index.duplicated()]

print(data)

bt=Backtest(data,supertrend,cash=100000)
output=bt.run()
print(output)
# print(output['_trades'].to_csv('trades.csv'))
bt.plot()
