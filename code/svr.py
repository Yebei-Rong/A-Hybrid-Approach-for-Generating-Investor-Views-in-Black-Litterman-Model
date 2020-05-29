#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 13:53:08 2020

@author: samantha
"""
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
import pandas as pd
import math
import time
from scipy import interpolate
import cmath
from scipy.optimize import minimize
from scipy.optimize import root
import pandas as pd
from sklearn.svm import SVR
from pandas_datareader import data
import yfinance as yf
from sklearn.preprocessing import StandardScaler

def ticker():
    #'PG', 'TRV', 'UNH', 'UTX', 'V', 'VZ', 'WBA', 'WMT','XOM'
    filename = 'stockprice.csv'
    da = pd.read_csv (filename) 
    df = pd.DataFrame(da)
    ticker = df.columns.tolist()
    ticker = np.array(ticker)
    return ticker.T

def ticker2():
    #'PG', 'TRV', 'UNH', 'UTX', 'V', 'VZ', 'WBA', 'WMT','XOM'
    filename = 'stockprice.csv'
    da = pd.read_csv (filename) 
    df = pd.DataFrame(da)
    ticker = df.columns.tolist()[1:9]
    ticker = np.array(ticker)
    return ticker.T
# arrange of indicator = ['adrx','atr','ema','hurst','macd','rsi','sma','vix']

def get_realindicator(tiker):
    f1 = 'djADXR.csv'
    f2 = 'djATR.csv'
    f3 = 'djema.csv'
    f4 = 'djhurst.csv'
    f5 = 'djmacd.csv'
    f6 = 'djRSI.csv'
    f7 = 'djsma.csv'
    f8 = 'djVIX.csv'
    indicator = pd.DataFrame()
    name = ['adrx','atr','ema','hurst','macd','rsi','sma','vix']
    file = [f1,f2,f3,f4,f5,f6,f7,f8]
    for i in range(7):
        a = pd.DataFrame(pd.read_csv(file[i]))
        indicator[name[i]] = a[tiker][40:]
    indicator['vix']=pd.DataFrame(pd.read_csv('djVIX.csv'))['VIX']
#    indicator = pd.DataFrame(df1)
    
#    data = [df1,df2,df3,df4,df5,df6,df7,df8]
#    for i in range(len(file)):
#        indicator[file[i]] = data[i]
    return indicator

def get_realreturn(ticker):
#    tickers = ticker()
    start_date = '2009-03-02'
    end_date = '2018-12-31'
    panel_data = data.DataReader(ticker, 'yahoo', start_date, end_date)
    adclose = panel_data['Adj Close']
    returns = np.log(adclose/adclose.shift(1))
    return returns[1:]

def get_fcastindicator(tiker):
    f1 = 'fcastadxr.csv'
    f2 = 'fcastatr.csv'
    f3 = 'fcastema.csv'
    f4 = 'fcasthurst.csv'
    f5 = 'fcastmacd.csv'
    f6 = 'fcastrsi.csv'
    f7 = 'fcastsma.csv'
    f8 = 'fcastvix.csv'
    name = ['adrx','atr','ema','hurst','macd','rsi','sma','vix']
    file = [f1,f2,f3,f4,f5,f6,f7,f8]
    findicator = pd.DataFrame()
    for i in range(7):
        a = pd.DataFrame(pd.read_csv(file[i]))
        findicator[name[i]] = a[tiker][:250]
    findicator['vix']=pd.DataFrame(pd.read_csv(f8))['VIX Forecast']
    return findicator

def predict_return(tiker):
    X = get_realindicator(tiker)[['adrx','atr','ema','hurst','macd','rsi','sma','vix']]
#    X = X.reshape((2476,8))
    y =  get_realreturn(tiker)
    y = np.array(y).reshape((2476,1))
    sc_X = StandardScaler()
    sc_y = StandardScaler()
    X = sc_X.fit_transform(X)
    y = sc_y.fit_transform(y)
    regressor = SVR(kernel='rbf')
#    regressor.fit(X,y)
    regressor.fit(X,y.ravel())
    testing_df = get_fcastindicator(tiker)
    X_test = sc_X.fit_transform(testing_df)
    y_pred = regressor.predict(X_test)
    y_pred = sc_y.inverse_transform(y_pred)
    return y_pred
    
def get_2019return(tiker):
    start_date = '2018-12-31'
    end_date = '2019-12-31'
    panel_data = data.DataReader(tiker, 'yahoo', start_date, end_date)
    adclose = panel_data['Adj Close']
    returns = np.log(adclose.shift(1)/adclose)
    return returns[1:251]

def final():
    ticker = ['AAPL', 'AXP', 'BA', 'CAT', 'CSCO', 'CVX', 'DIS', 'DD',
       'GS', 'HD', 'IBM', 'INTC', 'JNJ', 'JPM', 'KO', 'MCD', 'MMM', 'MRK',
       'MSFT', 'NKE', 'PFE', 'PG', 'TRV', 'UNH', 'UTX', 'V', 'VZ', 'WBA',
       'WMT', 'XOM']
    #['AAPL', 'AXP', 'BA', 'CAT', 'CSCO', 'CVX', 'DIS', 'DD']#['PG', 'TRV', 'UNH', 'UTX', 'V', 'VZ', 'WBA', 'WMT','XOM']
    result = pd.DataFrame()
    for i in range(len(ticker)):
        result[ticker[i]] = predict_return(ticker[i])
    return result

def finalreal():
    ticker = ['AAPL', 'AXP', 'BA', 'CAT', 'CSCO', 'CVX', 'DIS', 'DD']#['PG', 'TRV', 'UNH', 'UTX', 'V', 'VZ', 'WBA', 'WMT','XOM']
    result = pd.DataFrame()
    for i in range(len(ticker)):
        result[ticker[i]] = get_2019return(ticker[i])
    return result

#if __name__ == '__main__':
#    ticker = ticker()
#    returns = get_realreturn(ticker[0])
#    c = predict_return(ticker[0])
#    realreturn = get_2019return(ticker[0])
#    combine = pd.DataFrame([c,realreturn]).T
    
    

