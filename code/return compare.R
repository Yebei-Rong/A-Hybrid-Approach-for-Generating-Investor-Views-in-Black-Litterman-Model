weight=read.csv('/Users/jiachun/Desktop/finalweight tesing.csv',header=TRUE)
fcast=read.csv('/Users/jiachun/Desktop/real_return.csv',header=TRUE)
real=read.csv('/Users/jiachun/Desktop/^DJI.csv',header=TRUE)
real=real['Adj.Close']
real=real[c(1:250),1]

return<-matrix(NA,241,6) # 5 stands for 5 rolling window

col=0

for (roll in c(10,20,30,40,60,80)){
	col=col+1
	for (day in 1:(250-roll+1)){
		log_r=0
		#print(day)
		temp=0
		for (i in c(0:(roll-1))){
			temp=temp+sum(fcast[(day+i),c(2:31)]*weight[(day),c(2:31)])
					
		}
		return[day,col] = temp
	}
}
write.csv(return,'rolling.csv')

real_return<-matrix(NA,241,6)
col=0
for (roll in c(10,20,30,40,60,80)){
	col=col+1
	for (day in 1:(250-roll+1)){
		temp=real[(day+roll-1)]/real[(day)]
		real_return[day,col] = log(temp)
	}

}


par(mfrow=c(5,1))
for (i in c(1:5)){
    plot(real_return[,i],type='l',col='red')
    lines(return[,i],col='green')
    legend("topleft", legend = c("real_return", "our portfolio"),col=c("red","green"), lty=1,cex = 0.8)
}
sum(return[,1]>real_return[,1])/241
sum(return[c(1:231),2]>real_return[c(1:231),2])/231
sum(return[c(1:221),3]>real_return[c(1:221),3])/221
sum(return[c(1:211),4]>real_return[c(1:211),4])/211
sum(return[c(1:191),5]>real_return[c(1:191),5])/191
sum(return[c(1:171),6]>real_return[c(1:171),6])/171
temp=0
for(roll in c(10,20,30,40,60,80)){
    temp=temp+1
    print(roll)
    print(mean(return[c(1:(250-roll+1)),temp]))
    print(mean(real_return[c(1:(250-roll+1)),temp]))
}
temp=0

for(roll in c(10,20,30,40,60,80)){
    temp=temp+1
    print(roll)
    a=mean(return[c(1:(250-roll+1)),temp])
    b=mean(real_return[c(1:(250-roll+1)),temp])
    print((a+1)^(252/roll)-1)
    print((b+1)^(252/roll)-1)
}
rolling=c('10','20','30','40','60','80')
our_portfolio=c(0.2143,0.1920,0.1821,0.1634,0.1380,0.1234)
dj=c(0.2136,0.1862,0.1711,0.1529,0.1293,0.1158)
plot(x=rolling,y=our_portfolio,type='h',lable=true)
dat <- data.frame(rolling_day=c('10','20','30','40','60','80','10','20','30','40','60','80') , Annualized_return=c(0.2143,0.1920,0.1821,0.1634,0.1380,0.1234,0.2136,0.1862,0.1711,0.1529,0.1293,0.1158)*100,type=c('BL','BL','BL','BL','BL','BL','DJI','DJI','DJI','DJI','DJI','DJI'),stringsAsFactors = FALSE)

ggplot(dat,aes(x=rolling_day, y=Annualized_return,fill=type))+geom_bar(position='dodge',stat = "identity")+geom_text(aes(label=Annualized_return), position=position_dodge(width=1.2), vjust=-0.25)+xlab('Holding periods(Days)')+ylab('%Annulized Return')

dat2 <- data.frame(rolling_day=c('10','20','30','40','60','80','10','20','30','40','60','80') , Annualized_return=c(0.551,0.336,0.284,0.265,0.216,0.180,0.529,0.314,0.260,0.245,0.191,0.158),type=c('BL','BL','BL','BL','BL','BL','DJI','DJI','DJI','DJI','DJI','DJI'),stringsAsFactors = FALSE)
ggplot(dat2,aes(x=rolling_day, y=Annualized_return,fill=type))+geom_bar(position='dodge',stat = "identity")+geom_text(aes(label=Annualized_return), position=position_dodge(width=1.2), vjust=-0.25)+xlab('Holding periods(Days)')+ylab('Sharp Ratio')
