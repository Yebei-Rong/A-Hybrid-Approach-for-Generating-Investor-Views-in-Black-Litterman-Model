# RSI forecast
data <- read.csv("/Users/rongyebei/Desktop/MF740/project/rsi.csv")
date <- as.Date(data$Date,format="%m/%d/%Y")
time <- 1:length(date)
# Pick one stock and check its arma model
aapl <- data$AAPL
aapl[14:15]
# [1]       NA 46.45926
aapl <- aapl[15:length(aapl)] # drop NA
# decide ARMA(p,q) by plots
Pacf(aapl)
Acf(aapl)
# Acf plot shows we need to do difference on aapl. The number of lags go beyond maximum, which means aapl time series is almost random walk, not stationary so it cannot be used to model.
# First, do log on it.
la <- log(aapl)
dla <- diff(la)
# eastablish ARMA-GARCH model
# packages needed
library(TTR)
library(quantmod)
library(rugarch) # univariate
ug_spec = ugarchspec()
ugfit = ugarchfit(spec=ug_spec,data=dla)
ugfore <- ugarchforecast(ugfit,n.ahead=252)
ugfore

# do forecast on the remaining stocks, using for loop
T <- length(date)
rsi <- data.frame(rsi[15:T],2:31)
lrsi <- apply(rsi,2,log)
dlrsi <- apply(lrsi,2,diff)
result <- matrix(0,252,N)
for (i in 1:N){
  ugfit = ugarchfit(spec=ug_spec,data=dlrsi[,i])
  ugfore = ugarchforecast(ugfit,n.ahead=252)
  result[,i] = ugfore@forecast$seriesFor
}
# get forecast results, then add difference back and do exponential..
rsi_fcast <- matrix(0,252,N)
for (i in 1:N){
	temp = result[,i]
	temp[1] = lrsi[2502,i] + result[1,i]
	for (j in 2:252){
		temp[j] = temp[j-1] + result[j,i]
	}
	rsi_fcast[,i] = temp
}
rsi_fcast <- apply(rsi_fcast,2,exp)
write.csv(x=data.frame(rsi_fcast),file='/Users/rongyebei/Desktop/rsi_fcast.csv')