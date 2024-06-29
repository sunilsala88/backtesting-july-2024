import yfinance as yf
data=yf.download('AMZN',start='2024-05-24',end='2024-06-29',interval='1m')
print(data)