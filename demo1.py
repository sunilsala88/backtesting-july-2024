

import yfinance as yf
data=yf.download('AMZN',start='2024-06-24',end='2024-06-29',interval='1m')
print(data)


import pandas as pd
from ta.utils import dropna
from ta.volatility import BollingerBands
from ta.trend import sma_indicator

# Initialize Bollinger Bands Indicator
sma2 = sma_indicator(data['Close'],10)
print(sma2)