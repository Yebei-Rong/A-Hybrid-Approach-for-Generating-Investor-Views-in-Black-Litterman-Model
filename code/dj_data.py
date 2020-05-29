
# coding: utf-8

# In[1]:

import pandas as pd
import yfinance as yf   # yahoo finance package
from pandas_datareader import data as pdr


# In[2]:

import numpy as np


# In[3]:

def get_ticker(file_path):
    ''' return ticker symbols from local cvs file
    '''
    
    df = pd.read_csv(file_path)
    ticker_list = list(df['Symbol'])
    
    return ticker_list


# In[4]:

def download_price(tiker, start_date, end_date):
    ''' return tiker's price series from start_date to end_date
    '''
    price_series = pdr.get_data_yahoo(tiker, start = start_date, end = end_date).Close
    
    return price_series


# In[5]:

# get DJ Index components
file_path = 'dj.csv'
ticker_list = get_ticker(file_path)

ticker_list[7]='DD'

# stock price DataFrame
data_df = pd.DataFrame(columns=ticker_list)

start_date = '2008-12-31'
end_date = '2019-12-31'

# get data by Yahoo Finance
for ticker in ticker_list:
    
    price_data = download_price(ticker, start_date, end_date)
    price_data = price_data.fillna(method='pad') # fill in missing data with previous value
    data_df[ticker] = price_data
    print(ticker)


# In[10]:

data_df.to_csv('djindex.csv')


# In[8]:

data_df.head()


# In[6]:

data_df.columns


# In[14]:

return_df = pd.DataFrame(columns=list(data_df.columns),index = data_df.index)
for i in list(data_df.columns):
    return_df[i] = list((data_df[i]/data_df[i].shift(1)) -1)


# In[15]:

return_df = return_df.dropna()


# In[16]:

return_df.to_csv('return19.csv')


# In[17]:

return_df


# In[6]:

# Calculate Indicators
data_df = pd.read_csv('djindex.csv') # stock prices data

# VIX
vix = download_price('^VIX', start_date, end_date)


# In[7]:

vix.to_csv('vix.csv')


# In[2]:

# RSI
def get_rsi(t, periods=14):
    length = len(t)
    rsies = [np.nan]*length
    
    # data size <= periods, cannot calculate rsi
    if length <= periods:
        return rsies
    
    up_avg = 0
    down_avg = 0
    
    # Step1: Calculate the first RSI for getting smoothed moving average later.
    first_t = t[: periods + 1]
    for i in range(1, len(first_t)):
        # price going up
        if first_t[i] >= first_t[i-1]:
            up_avg += (first_t[i] - first_t[i-1])
        # price going down
        else:
            down_avg += (first_t[i-1] - first_t[i])  # note: this is also a positive value
            
    up_avg = up_avg/periods
    down_avg = down_avg/periods
    
    rs = up_avg/down_avg
    rsies[periods] = 100 - 100/(1+rs)
    
    # Step 2: Smooth RSI results by calculating smoothed moving average.
    for j in range(periods+1, length):
        up = 0
        down = 0
        if t[j] >= t[j-1]:
            up = t[j] - t[j-1]
            down = 0
        else:
            down = t[j-1] - t[j]
            up = 0
            
        up_avg = (up_avg * (periods - 1) + up) / periods
        down_avg = (down_avg * (periods - 1) + down ) / periods
        
        rs = up_avg/down_avg
        rsies[j] = 100 - 100/(1+rs)
        
    return rsies
            
    


# In[12]:

list(data_df.columns)


# In[14]:

rsi_df = pd.DataFrame(index=data_df.index, columns=data_df.columns)

columns = list(data_df.columns)[1:]
#periods = 14

for i in columns:
    rsi_df[i] = get_rsi(list(data_df[i]))
    


# In[15]:

rsi_df.head(30)


# In[16]:

rsi_df.to_csv('rsi.csv')


# In[36]:

# calculate rsi for 2018-2019
data = pd.read_csv("""/Users/rongyebei/Downloads/DIS.csv""")


# In[18]:

data.head()


# In[19]:

stock_price = data['Adj Close']
rsi1819 = get_rsi(stock_price)


# In[20]:

rsi1819[0:20]


# In[21]:

for i in rsi1819:
    print(i)


# In[22]:

history()


# In[23]:

history


# In[24]:

data = pd.read_csv("""/Users/rongyebei/Desktop/MF796/project/SPY1819.csv""")


# In[25]:

import matplotlib as mpl
get_ipython().magic('matplotlib inline')


# In[26]:

data['Adj Close'].plot()


# In[34]:

data['Adj Close'].iloc[251:].plot() #AAPL


# In[37]:

data['Adj Close'].iloc[251:].plot() #DSI


# In[ ]:



