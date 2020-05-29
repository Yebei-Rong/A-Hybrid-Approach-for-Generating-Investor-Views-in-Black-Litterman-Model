
# coding: utf-8

# In[1]:

import numpy as np

import pandas as pd
from sklearn.svm import SVR


# In[2]:

from sklearn.preprocessing import StandardScaler


# In[3]:

#import matplotlib.pyplot as plt
# %matplotlib inline


# In[90]:

aapl = pd.read_csv('return_fcast.csv')


# In[79]:

y = aapl['return']


# In[80]:

X = aapl[['ADXR','ATR','SMA','Hurst','EMA','MACD','VIX','RSI']]


# In[14]:

X = X.reshape((2475,8))


# In[21]:

y = np.array(y).reshape((2475,1))


# In[22]:

sc_X = StandardScaler()
sc_y = StandardScaler()
X = sc_X.fit_transform(X)
y = sc_y.fit_transform(y)


# In[25]:

regressor = SVR(kernel='rbf')
regressor.fit(X,y)


# In[27]:

testing_df = pd.read_csv('testing.csv')


# In[28]:

X_test = testing_df[['ADXR','ATR','SMA','Hurst','EMA','MACD','VIX','RSI']]


# In[29]:

X_test.shape


# In[33]:

X_test = sc_X.fit_transform(X_test)


# In[34]:




# In[35]:

y_pred


# In[36]:

y_pred = regressor.predict(X_test)
y_pred = sc_y.inverse_transform(y_pred)


# In[37]:

y_pred


# In[38]:

for i in range(len(y_pred)):
    print(y_pred[i])


# In[3]:

# run SVR for the AXP-...DD stocks
axp = pd.DataFrame(columns=aapl.columns)


# In[3]:

#stocks = ['AAPL','AXP','BA','CAT','CSCO','CVX','DIS','DD','GS']
stocks = ['MCD']


# In[4]:

# read indicators 09-18
ADXR = pd.read_csv('data/djADXR.csv')
ATR = pd.read_csv('data/djATR.csv')
SMA = pd.read_csv('data/sma.csv')
Hurst = pd.read_csv('data/hurst.csv')
EMA = pd.read_csv('data/ema.csv')
MACD = pd.read_csv('data/macd.csv')
VIX = pd.read_csv('data/vix.csv')
RSI = pd.read_csv('data/rsi.csv')


# In[5]:

VIX.iloc[40:2476]


# In[121]:

# read stock prices 09-18


# In[3]:

dj_df = pd.read_csv('data/djindex.csv')


# In[7]:

dj_df = pd.read_csv('data/djindex.csv')
#dj_df = dj_df[['Date','AAPL','AXP','BA','CAT','CSCO','CVX','DIS','DD','GS']].iloc[39:2516]
#dj_df = dj_df[['Date','MCD']].iloc[39:2516]

return_df = pd.DataFrame(columns=dj_df.columns[1:],index=dj_df['Date'])

for i in dj_df.columns[1:]:
    return_df[i] = list(np.log(dj_df[i]/dj_df[i].shift(1)))


# In[9]:

return_df = return_df.dropna()


# In[10]:

cov = return_df.cov()
cov.to_csv('cov0918.csv')


# In[41]:

list(dj_df.columns[1:])


# In[39]:

dj_df.index = dj_df


# In[65]:

stock18 = dj_df[dj_df.columns[1:]].iloc[-252:]


# In[67]:

stock18


# In[44]:

dj_df


# In[68]:

dj_df = pd.read_csv('data/djindex.csv')
dj_df.index = dj_df['Date']

return_df = pd.DataFrame(columns=list(dj_df.columns[1:]))

for i in dj_df.columns[1:]:
    return_df[i] = list(np.log(stock18[i]/stock18[i].shift(1)))


# In[69]:

return_df = return_df.dropna()


# In[70]:

return_df


# In[71]:

cov = return_df.cov()


# In[72]:

cov


# In[73]:

cov.to_csv('cov.csv')


# In[10]:

# store return prediction
result = pd.DataFrame(columns=stocks)


# In[21]:

# indicators forecast
ADXR_f = pd.read_csv('data/tesingadxr740.csv')
ATR_f = pd.read_csv('data/tesingatr740.csv')
SMA_f = pd.read_csv('data/sma_forecast.csv')
Hurst_f = pd.read_csv('data/hurst_forecast.csv')
EMA_f = pd.read_csv('data/ema_fcast.csv')
MACD_f = pd.read_csv('data/macd_fcast.csv')
VIX_f = pd.read_csv('data/vix_fcast.csv')
RSI_f = pd.read_csv('data/rsi_fcast.csv')


# In[22]:

# Initialized scaler in order to transform variables into (-1,1)
sc_X = StandardScaler()
sc_y = StandardScaler()
regressor = SVR(kernel='rbf')

temp = pd.DataFrame(columns=['ADXR','ATR','SMA','Hurst','EMA','MACD','VIX','RSI'])
temp['VIX'] = list(VIX['VIX'].iloc[40:2516]) # all stocks share the same vix

temp_f = pd.DataFrame(columns=['ADXR','ATR','SMA','Hurst','EMA','MACD','VIX','RSI'])
temp_f['VIX'] = list(VIX_f['VIX Forecast'].iloc[0:250])

for i in ['MCD']: # iterate each stock
    
    # First, extract training data set, including indicators(X) and return(y)   
    temp['ADXR'] = list(ADXR[i].iloc[40:2516])
    temp['ATR'] = list(ATR[i].iloc[40:2516])
    temp['SMA'] = list(SMA['SMA_'+i].iloc[40:2516])
    temp['Hurst'] = list(Hurst['Hurst'+i].iloc[40:2516])
    temp['EMA'] = list(EMA[i].iloc[40:2516])
    temp['MACD'] = list(MACD[i].iloc[40:2516])
    temp['RSI'] = list(RSI[i].iloc[40:2516])
    # transformation
    X = sc_X.fit_transform(temp[['ADXR','ATR','SMA','Hurst','EMA','MACD','VIX','RSI']])
    #print(X.shape)
    y = sc_y.fit_transform(np.array(return_df[i].dropna()).reshape(2476,1))
    #print(y.shape)
    # training 
    regressor.fit(X,y)
    # predicting
    temp_f['ADXR'] = list(ADXR_f[i+'.1976.10.11.20.00.00'].iloc[0:250])
    temp_f['ATR'] = list(ATR_f[i+'.1976.11.07.19.00.00'].iloc[0:250])
    temp_f['SMA'] = list(SMA_f[i].iloc[0:250])
    temp_f['Hurst'] = list(Hurst_f[i].iloc[0:250])
    temp_f['EMA'] = list(EMA_f[i].iloc[0:250])
    temp_f['MACD'] = list(MACD_f[i].iloc[0:250])
    temp_f['RSI'] = list(RSI_f[i].iloc[0:250])
    X_test = temp_f[['ADXR','ATR','SMA','Hurst','EMA','MACD','VIX','RSI']]
    X_test = sc_X.fit_transform(X_test)
    y_pred = regressor.predict(X_test)
    y_pred = sc_y.inverse_transform(y_pred)
    # write predicted returns into result
    result[i] = y_pred
    print(i)


# In[23]:

result.to_csv('mac_fcast.csv')


# In[161]:

ADXR['AAPL'].iloc[40:2516]


# In[ ]:



