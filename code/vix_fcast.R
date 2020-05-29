# VIX forecast
data <- read.csv("/Users/rongyebei/Desktop/MF740/project/vix.csv")
date <- as.Date(data$Date,format="%m/%d/%Y")
time <- 1:length(date)
vix <- data$VIX
# do on log of VIX
lv <- log(vix)
plot(time,lv,type="l",col=2);title("Log VIX From Year 2009 - 2018")
# one level difference
dlv <- c(NA,diff(lv))  # stationary
plot(time,dlv,type="l",col=2);title("diff(log(vix))") 
# eastablish ARMA-GARCH model
# packages needed
library(TTR)
library(quantmod)
library(rugarch) # univariate
library(rmgarch) # multi-variate
# defalut: ARMA(1,1) GARCH(1,1)
# Here, since diff(log(vix)) is stationary time series, we put dlv for forecast. And then add difference back and do exponential...
ug_spec = ugarchspec()
ugfit = ugarchfit(spec=ug_spec,data=dlv[2:2516])
ugfore <- ugarchforecast(ugfit,n.ahead=252)
ugfore



