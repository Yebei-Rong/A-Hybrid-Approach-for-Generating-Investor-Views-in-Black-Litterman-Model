# A Hybrid Approach for Generating Investor Views in Black Litterman Model

## 1 Introduction
This is a replication of an academic paper -- *A Hybrid Approach for Generating Investor Views in Black Litterman (BL) Model*. This paper takes a hybrid approach to generate investor views. Specifically, it applies the ARMA-GARCH model to predict indicators for stocks and then establish a Support Vector Regression (SVR) model to generate return forecasts. Finally, feeding the forecast returns into Black-Litterman (BL) model, it obtains the optimal portfolio weights for each day. Then this proposed approach is tested in a developed market, Dow Jones Index (DJI) of the US stock market.

Different from the paper we refer to, we implement this approach by using all the stocks of DJI in a time period from year 2009 to 2018 and validate our results of forecasts of year 2019. For the methodology, we follow the three well known models in the original paper -- ARMA-GARCH, SVR and Black-Litterman. However, before applying the ARMA-GARCH model to stock indicators, we examined carefully of the stationary of each indicator time series. Moreover, although the paper takes the SVR and it shows that the results outperformed the DJI returns. We further analyzed other machine learning methods which are Bayesian, Random Forest, Adaptive Boosting, Decision Tree, KNN, Logistic Regression, GradientBoosting. In conclusion, the BL results reveal better portfolio returns than the DJI return for different holding periods. Meanwhile, we also have some new findings. First, the BL results didn’t show better performance compared with randomly generated and 1/N rule portfolios. Second, we observe that it appears a positive relationship between portfolio returns and holding periods, which means it is better to hold a portfolio for a long time and not to change positions frequently.

## 2 Implementation
### 2.1 Stage 1: Forecasting Indicators with ARMA-GARCH(1,1)
ARMA-GARCH(1,1) model is used to obtain the daily forecast of 8 common technical indicators of stock for 250 days in (starting from Jan 2019) using the available data from 2009 to 2018 of DJI. Before modelling, we plotted the ACF and PACF figures to choose the proper parameters for ARMA models which is important but not given in the original paper.

#### 2.1.1 Indicators
Eight indicators we use are ATR(average true range), ADXR(average directional movement index rating), EMA (exponential Moving Average), MACD (moving average convergence divergence), SMA(simple moving average), Hurst (hurst exponent), RSI (relative strength index), VIX (CBOE volatility index). Note, the first seven are widespread used technical indicators. We calculated them for DJI stocks by using their adjusted close prices. The last one VIX is an indicator that reflects investor perceptions. It is often referred to as the fear index of fear gauge. The VIX index is a volatility index derived from S&P 500 options, with the price of each option representing the market's expectation of 30-day forward-looking volatility.

### 2.2 Stage 2: Forecasting Stock Returns from Indicators with SVR
In this stage, we translated the indicators into return values via SVR model. The implementation can be considered as two parts, model training and model testing.

Firstly, we use the 10-year data {X,Y} to train the prediction model for stock returns. Here X is a 8-dimension data which consists of 8 indicators data from 2009 to 2018, and Y is the stock return in the same time period. Also we need to note that we train a SVR model for each stock of DJI. After we obtain the model from the training data, we can make stock return forecasts by feeding the model with what we got in stage 1. Besides, before the model construction step, we should standardize the 8 indicators and returns in order to put them in a (-1, 1) range. On the other hand, we should inverse the predicted values back to the original return data in the end.

### 2.3 Stage 3: Black-Litterman Model Using Predicted Returns
Finally, stock return forecasts are investor views for generating portfolio weights in the BL model. During the BL model, 
* Risk aversion coefficient is taken as 2.5 which is given by He and Litterman(1999) as world average risk tolerance.
* Different from the original paper, we set the coefficient of uncertainty as the volatility of the predicted returns to reflect our confidence in investors ' views becasue the volatility represents the prediction imprecision. And we found that if we follow the same setting of this paper which takes 100% confidence on investors’ views, the optimal weights will be very unstable. 
* In addition, τ is taken as 0.01 because the market environment is bullish in 2019, which means investors are confident in the market.

### 2.4 Computations
We implemented the ARMA-GARCH model in R. Python platform is employed for SVR and Black-Litterman models.

## 3 Findings on Black-Litterman Portfolio Returns
### 3.1 Rolling Data Scheme
Although we calculated the optimal weights for each day, it is unrealistic to trade and change positions every single day. Thus, we take different holding periods 10,20,30,40,60,80 days into consideration.

Our rolling data scheme is explained below:
* We begin with optimal daily portfolio weight for each of 250 days, which is obtained in stage 3.
* We will hold the portfolio unchanged from the first day until the end of the holding period. For example, if we invest in the first day’s portfolio and hold it for 10 days, and then invest in the second holding period for 10 days (correspond to 2nd, 3rd,...11th of the test periods). And we calculate the return value for each day. We can get these holding period returns by adding up these daily returns.
* Taking 10-days rolling window as example, we execute 241 runs and obtain 241 returns for DJI. Then we took the average of these returns values. Last, the average of these returns are compounded and converted into annualized returns for doing comparison between rolling periods and indexes.
* Based on the 10-days rolling scheme mentioned above, annualized return for 20,30,40,60 and 80 days holding periods are calculated in the same manner. For 20-days holding period, we can get 231 returns.
* Getting the annualized index return for different rolling window for both markets and our portfolio of the optimal weights given by the BL model.

### 3.2 Portfolio Returns in DJI
The table below shows the percentage of the hybrid BL returns beats the DJI returns for different rolling windows. It is pretty clear that this percentage is all greater than 50%, which shows that the hybrid BL returns outperforming the DJI returns.

| Holding periods | # of runs | % our model return > index return  |
| ---------------:| ---------:| ----------------------------------:|
| 10              | 241       | 58.92%                             |
| 20              | 231       | 58.01%                             |
| 30              | 221       | 55.66%                             |
| 40              | 211       | 62.46%                             |
| 60              | 191       | 69.63%                             |
| 80              | 171       | 74.27%                             |
| Overall         | 1266      | 63.18%                             |

And the figure below reveals the return comparison for DJI. And the highest return level for the BL model is achieved at 10-days(21.43%) and 20-days(19.2%) holding periods. The DJ Index returns are 21.36%, 18.62% under the same assumption.

![Fig 1](https://github.com/Yebei-Rong/A-Hybrid-Approach-for-Generating-Investor-Views-in-Black-Litterman-Model/blob/master/image/fig1.png?raw=true)

### 3.3 Statistical Tests on BL Portfolio Returns
We use t-tests to see whether the differences between the annalized BL return and annualized DJI returns are statistically significant for different holding days. The table below presents that there are significant differences between our annualized hybrid BL returns and annualized DJI returns.

| Holding periods | Mean difference (%) | t-stat.  | p-value.    |
| ---------------:| -------------------:| --------:|------------:|
| 10              | 0.23.               | 0.04     | 0.04        | 
| 20              | 3.90                | 0.04     | 0.23        | 
| 30              | 11.29               | 2.02     | 0.022**.    | 
| 40              | 14.75               | 1.86     | 0.032**.    | 
| 60              | 18.84               | 1.93     | 0.027**.    | 
| 80              | 22.36               | 3.94     | 5.85e-05*** | 

**  significant at 5% 
*** significant at 1%

### 3.4 Sharpe Ratios In BL Portfolio Returns
We test the Sharpe Ratios given by the hybrid BL model compared with the Sharpe Ratios of the DJI, and we can see that the hybrid BL model gets a higher level of Sharpe Ratios than DJI for all different rolling windows. We pick risk free rate to be 0.0252, which is cited from the official website of the United States Department of the treasury.

![Fig 2](https://github.com/Yebei-Rong/A-Hybrid-Approach-for-Generating-Investor-Views-in-Black-Litterman-Model/blob/master/image/fig2.png?raw=true)

We use t-tests to see whether the differences between the BL sharpe ratio and DJI sharpe ratio are significant for different holding days. However, none of the holding periods show significant sharpe ratio difference. In other words, our result will not statistically hold if we do it for another time period.

## 4 Conlusion
* The Sharpe ratio of the BL model in our testing period is higher than DJ index in all holding periods, which represents not only the annualized return of BL is higher than the DJ index but also the risk adjusted return is better than DJ index. However, when it comes to the Z-test of sharpe ratios, there is no statistical significance between the sharpe ratio of our model and the one of DJ index.
* In reality, our model performs the best in the short time horizon because of limitations of the Garch model which is not suitable to predict variance in the long term.
* For trading daily, BL models cannot beat randomly generated portfolios and equal weighted portfolios. However, BL models can beat equal weighted portfolios under our rolling data scheme.
* We observe that the annualized average return increases with rolling windows. Thus, holding a portfolio for a relative long time is more profitable than holding it for a short time period or trading daily.

## 5 New Contribution and Insights
### 5.1 Indicator Replacement
We replaced the FGI indicator with a more widely used confidence measurement, VIX. Although the paper we refer to uses the Fear and Greed Index (FGI) in analysis, we replace it by VIX with the following reasons. First, the difficulty of obtaining the FGI indicator is the main reason. Since there is no open source for it and we have no access to Bloomberg terminal which is at Questrom, we switch to find a reasonable substitute. At the same time, VIX is a popular measure of the stock’s market’s expectation of 30-day forward-looking volatility. Last but not least, FGI is constructed on the basis of the S&P 500, put and call options, market volatility, etc. In this sense, the two indicators are similar to some degree. Thus, our replacement is reasonable.

### 5.2 Stationary Analysis of Time Series
In the process of establishing an ARMA-GARCH(1,1) model for each stock indicator, we examine the stationary of indicator time series carefully in order to do analysis later. Besides, by plotting the plots of auto-correlation and partial auto-correlation functions, we finally decided the most proper parameters for the ARMA process of EMA, MACD and RSI and VIX. For instance, we forecast the difference of log value of VIX instead of using just the log value of VIX to ensure its stationary.

### 5.3 Confidence of Investor View
In the BL model, we use the volatility of predicted returns to reflect our confidence in investors ' views instead of 100% confidence. Since the variance reflects the forecast error of our generated returns, our setting here is more reasonable

### 5.4 Significance Test of Sharpe Ratio Difference
The Sharpe ratio of the Black-Litterman model in our testing period is higher than DJ index in all holding periods. Our paper gives the significance test of sharpe ratios to see if the difference of the sharpe ratio results is statistically significant so we include the volatility effect into consideration. We did a further analysis on sharpe ratio to validate the difference between Black-Litterman model and DJI.

### 5.5 Analysis of Return Using Different Machine Learning Methods to Generate Investor Views
In addition to the SVR model, we pick other seven machine learning methods to check the difference on which could present a better performance. Those other machine learning methods are: Bayesian, Random Forest, Adaptive Boosting, Decision Tree, KNN, Logistic Regression, GradientBoosting. Then we do comparison between these eight machine learning methods and obtain the graph as following:

![Fig 3](https://github.com/Yebei-Rong/A-Hybrid-Approach-for-Generating-Investor-Views-in-Black-Litterman-Model/blob/master/image/fig3.png?raw=true)

Based on the result, the optimal weight generated by SVR, Random Forest, and Decision Tree would have better performance than capitalization weight, while the others didn’t. Among those three better methods, SVR has the best outcome. SVM (Support vector machine) is suitable for small samples and feasible for high dimensional problems. It fits a non-linear surface, and avoids overfitting. But SVM is sensitive to missing data and class-outlier, and the results are dependent on the choice of kernel. Compared to the other chosen methods, since we have done data cleansing and class-outlier selection, SVR would generate the best optimal weight.

## Reference
1. Kara, Mahmut, Aydin Ulucan, and Kazim Baris Atici. "A Hybrid Approach for Generating Investor Views in Black–Litterman Model." *Expert Systems with Applications* 128 (2019): 256-70. Print.
2. He, G., & Litterman, R. (1999). The intuition behind Black-Litterman model portfo- lios. Goldman Sachs Investment Management Research. https://ssrn.com/abstract=334304.

