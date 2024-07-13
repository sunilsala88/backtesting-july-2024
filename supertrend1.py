import pandas_ta as ta
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
        pass



import yfinance as yf
data=yf.download('AMZN',start='2023-05-24',end='2024-06-29',interval='1D')
print(data)


print(supertrend1(data['High'], data['Low'], data['Close']))
print(supertrend2(data['High'], data['Low'], data['Close']))

bt=Backtest(data,supertrend,cash=100000)
output=bt.run()
bt.plot()