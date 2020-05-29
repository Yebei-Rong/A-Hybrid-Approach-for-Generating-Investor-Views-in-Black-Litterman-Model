#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 10:54:28 2020

@author: zichongzeng
"""

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
#import yfinance as yf
from pandas_datareader import data



if __name__ == '__main__':
    weight=pd.read_csv('/Users/zichongzeng/Desktop/omegaforctestingweight.csv')
    fcast=pd.read_csv('/Users/zichongzeng/Desktop/real_return.csv')
    #real=pd.read_csv('/Users/zichongzeng/Desktop/DJI.csv')
    #real=real['Adj Close'].iloc[:250,]
    #rr = np.log(real /  real.shift(1)).dropna()
    start_date = '2018-12-31'
    end_date = '2019-12-31'
    panel_data = data.DataReader('^DJI', 'yahoo', start_date, end_date)
    real = panel_data['Adj Close']
    returns = np.log(real/real.shift(1)).dropna()
    roll_window = [10,20,30,40,60,80]
    roll_return = np.matrix(np.zeros((241,6)))
    real_return = np.matrix(np.zeros((241,6)))
    col = 0
    for rw in roll_window:
        for day in range(0,250-rw+1):
            temp = 0
            for i in range(rw):
                temp += sum(fcast.iloc[day+i,1:]*weight.iloc[day,1:])
                real_return[day,col] += returns.iloc[day+i]
            roll_return[day,col] = temp
            
        col += 1
    #print(roll_return)
    roll_return = pd.DataFrame(roll_return)
    roll_return.to_csv('/Users/zichongzeng/Desktop/roll_return.csv')
    real_return = pd.DataFrame(real_return)
    real_return.to_csv('/Users/zichongzeng/Desktop/dji_return.csv')
    
    ar_bl = np.zeros((6))
    ar_real = np.zeros((6))
    pct_ar_bl = np.zeros((6))
    pct_ar_real = np.zeros((6))
    SR_bl = np.zeros((6))
    SR_real = np.zeros((6))
    col = 0
    rf = 0.0252
    for rw in roll_window:
        ar_bl[col] = np.mean(roll_return.iloc[:250 - rw + 1,col])
        ar_real[col] = np.mean(real_return.iloc[:250 - rw + 1,col])
        pct_ar_bl[col] = pow((ar_bl[col] + 1), (252 / rw)) - 1
        pct_ar_real[col] = pow((ar_real[col] + 1), (252 / rw)) - 1
        col += 1
    pct_ar_bl = np.array([0.214301, 0.191965, 0.182068, 0.1633376, 0.138003, 0.12342])
    pct_ar_real = np.array([0.21359, 0.186199, 0.17112, 0.152861, 0.129295, 0.115812])
    col = 0
    for rw in roll_window:
        #SR_bl[col] = (np.mean(roll_return.iloc[:250 - rw + 1]) - rf)/ np.std(roll_return.iloc[:250 - rw + 1]) * np.sqrt(252)
        #SR_real[col] = (np.mean(real_return.iloc[:250 - rw + 1]) - rf)/ np.std(real_return.iloc[:250 - rw + 1])
        SR_bl[col] = (pct_ar_bl[col] - rf)/ np.std(roll_return.iloc[:250 - rw + 1, col])
        SR_real[col] = (pct_ar_real[col] - rf)/ np.std(real_return.iloc[:250 - rw + 1,col])
        col +=1
    result = pd.DataFrame(np.vstack((ar_bl,ar_real,pct_ar_bl,pct_ar_real, SR_bl, SR_real)), columns = roll_window, index = ['ar_bl','ar_real','pct_ar_bl','pct_ar_real', 'SR_bl', 'SR_real'])
    result.to_csv('/Users/zichongzeng/Desktop/result.csv')
    #plt.plot(pct_ar)
    #plt.show()
    
     
    # plot % annualized return
    x =np.arange(6)
    bar_width = 0.35  
    plt.bar(x, pct_ar_bl, bar_width, align='center', color='c', label='BL', alpha=0.5)
    plt.bar(x+bar_width, pct_ar_real, bar_width, align="center", color="b", label="DJI", alpha=0.5)
    plt.xlabel("Holding Periods(Days)")
    plt.ylabel("% Annualized Return")
    plt.xticks(x+bar_width/2, roll_window)
    plt.legend()
    plt.show()
    
    # plot % sharpe ratio
    bar_width = 0.35  
    plt.bar(x, SR_bl, bar_width, align='center', color='c', label='BL', alpha=0.5)
    plt.bar(x+bar_width, SR_real, bar_width, align="center", color="b", label="DJI", alpha=0.5)
    plt.xlabel("Holding Periods(Days)")
    plt.ylabel("Sharpe Ratio")
    plt.xticks(x+bar_width/2, roll_window)
    plt.legend()
    plt.show()
    
    
    
    
    
    
    
    