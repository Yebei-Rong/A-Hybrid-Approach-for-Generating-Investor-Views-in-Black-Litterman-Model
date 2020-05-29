
# coding: utf-8

# In[1]:

import numpy as np
#import matplotlib.pyplot as plt
import pandas as pd


# In[3]:

#from sklearn.preprocessing import StandardScaler


# In[24]:

from sklearn.svm import SVR


# In[4]:

aapl = pd.read_csv('return_fcast.csv')


# In[6]:

y = aapl['return']


# In[7]:

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

y_pred = regressor.predict(X_test)


# In[35]:

y_pred


# In[36]:

y_pred = sc_y.inverse_transform(y_pred)


# In[37]:

y_pred


# In[ ]:



