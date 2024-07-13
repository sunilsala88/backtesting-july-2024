import pandas_ta as ta
import pandas as pd
from backtesting import Strategy, Backtest

def supertrend1(high_data,low_data,close_data):
    o=ta.supertrend(high_data,low_data,close_data,length=10)
    print(o)
    return o['SUPERTd_10_3.0']
def supertrend2(high_data,low_data,close_data):
    o=ta.supertrend(high_data,low_data,close_data,length=10)
    return o['SUPERT_10_3.0']


class supertrend(Strategy):
    

    def init(self):
        self.super1=self.I(supertrend1,self.data.High.s,self.data.Low.s,self.data.Close.s)
        self.super2=self.I(supertrend2,self.data.High.s,self.data.Low.s,self.data.Close.s)

    def next(self):
        if self.super1[-1]>0 and self.super1[-2]<0:
            if self.position.is_short:
                self.position.close()
            else:
                pass
            self.buy()
        elif self.super1[-1]<0 and self.super1[-2]>0:
            if self.position.is_long:
                self.position.close()
            else:
                pass
            self.sell()



# import yfinance as yf
# data=yf.download('AMZN',start='2020-05-24',end='2024-06-29',interval='1D')
# print(data)

data=pd.read_csv('TSLA_1hour.csv')
data['Date']=pd.to_datetime(data['Date'])
data['Date']=data['Date'].dt.tz_localize(None)
data.set_index('Date',inplace=True)
print(data)

print(supertrend1(data['High'], data['Low'], data['Close']))
print(supertrend2(data['High'], data['Low'], data['Close']))

bt=Backtest(data,supertrend,cash=100000)
output=bt.run()
bt.plot()