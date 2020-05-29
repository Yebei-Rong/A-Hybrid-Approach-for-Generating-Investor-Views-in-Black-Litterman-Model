djret <- read.csv("/Users/rongyebei/Desktop/djrollingreturn.csv")
blret <- read.csv("/Users/rongyebei/Desktop/forcastrollingreturn.csv")

cnt <- 0
result <- matrix(0,6,3)

for (i in c(10,20,30,40,60,80)){
	
	cnt <- cnt+1
	size <- 250-i+1
	
	diff <- blret[1:size,cnt] - djret[1:size,cnt]
	t <- mean(diff)*sqrt(size)/sd(diff)
	print(t)
	p <- 1 - pt(t,size)
	
	result[cnt,1] <- mean(diff)*100
	result[cnt,2] <- t
	result[cnt,3] <- p
	
}

random_return <- read.csv("/Users/rongyebei/Desktop/randomweightrollingreturn.csv")

ret <- read.csv("/Users/rongyebei/Desktop/30stockreturn2019.csv",header=F)

# generate random weights, 1000 times
nsim <- 1000
for (i in 1:nsim){
	return <- matrix(0,nrow=250,ncol=1) # store daily return
	weights <- runif(30*250,0,1)
	weights <- matrix(ranwei,nrow=250,ncol=30)
	
	
}