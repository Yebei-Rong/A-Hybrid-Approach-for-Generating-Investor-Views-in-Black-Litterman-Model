#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 21:58:15 2020

@author: samantha
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 21:13:55 2020

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

def get_weight():
    filename='weights.csv'
    da = pd.read_csv (filename) 
    df = pd.DataFrame(da)
#    ticker = df.iloc[:,1
    ticker = df['weight'].array
    return ticker
#BLcov.csv
def get_cov():
    filename='BLcov.csv'#cov0918， BLcov
    da = pd.read_csv (filename) 
    df = pd.DataFrame(da)
    ti= df.iloc[:,1:]
    ticker = ti
    return np.matrix(ticker)

def get_forcastcov():
    filename='fcast_return2019.csv'
#    filename = 'return19.csv'
    da = pd.read_csv (filename) 
    df = pd.DataFrame(da).iloc[:,1:]
#    ti= df.iloc[:,1:]
#    ticker = ti
    return np.matrix(df.cov())

def get_forcast(i):
    filename='fcast_return2019.csv'
#    filename = 'return19.csv'
    da = pd.read_csv (filename) 
    df = pd.DataFrame(da)
    ti= df.iloc[i,1:]
#    ticker = ti
    return ti.array

def get_capweight():
    tickers = ['AAPL', 'AXP', 'BA', 'CAT', 'CSCO', 'CVX', 'DIS', 'DD',
       'GS', 'HD', 'IBM', 'INTC', 'JNJ', 'JPM', 'KO', 'MCD', 'MMM', 'MRK',
       'MSFT', 'NKE', 'PFE', 'PG', 'TRV', 'UNH', 'UTX', 'V', 'VZ', 'WBA',
       'WMT', 'XOM']
    result = data.get_quote_yahoo(tickers)['marketCap']
   
    return result

def cal_optimalweight(frcastinput,cap):
    weight = cap#get_capweight()
    w = np.matrix([weight]).T
#    print('w',w)
#    w = np.matrix([[35/50, 10/50, 5/50]]).T
    c = get_forcastcov()#forecast covariance
    t =0.025# 0.01#0.025
    C = get_cov()
#    print('C',C)
    a = 1/2.5
    cov = get_cov()*t
    P = np.diag(np.ones(30))
#    P = np.matrix([[1,0,0],[-1,1,0]])
    q = np.matrix([frcastinput]).T
#    print('q',q)
    b = np.zeros((30, 30))
    np.fill_diagonal(b, np.diag(c))
    omega =0#b# np.diag(q*C*q.T)#np.diag(C)
#    print('omega=',omega)
    pi = C*w/a
    R = pi +cov*P.T*(P*cov*P.T+omega).I*(q-P*pi)
#    print(pi.shape,cov.shape,R.shape,(P*pi).shape,q.shape)
    CC = C+cov-cov*P.T*(P*cov*P.T+omega).I*(P*cov)
#    print('R',CC)
    wopt = a*CC.I*R
    return wopt


    


def opti_weight():
    opti = []
    cap = get_capweight()
    for i in range(250):
#        print(i)
        weight = np.array(cal_optimalweight(get_forcast(i),cap).T)
        opti.append(weight[0])
#    result = pd.DataFrame(opti)
    return np.array(opti)
if __name__ == '__main__':
    f = get_forcast(0)
#    a = np.zeros((30, 30))
#    t = []
#    for i in range(len(f)):
#        t.append(f[i]
#    diag = np.fill_diagonal(a, f)
#    c = get_cov()
#    C = get_forcastcov()
#    opti = cal_optimalweight(f)
    result = opti_weight()
    weight = get_capweight()
    total = np.sum(weight)
    weight = weight/total
    cap_weight
        
#    final = pd.DataFrame(result)
    
    
#    t = [0.1, 1, 10]
#    for i in range(len(t)):
#        w = cal_optimalweight(t[i])
#        print('t = ',t[i],'\n',w,'\n')