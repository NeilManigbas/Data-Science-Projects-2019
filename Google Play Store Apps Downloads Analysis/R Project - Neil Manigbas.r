### IMPORT DATASET
rm(list=ls())
getwd()
setwd('C:\\Users\\Neil\\Desktop\\Neil DATA SCIENTIST\\R')
df = read.csv("googleplaystore.csv",stringsAsFactors=FALSE)

### UNDERSTANDING DATA

dim(df)
head(df,n=3)
typeof(df)
class(df)
summary(df)

### DATA CLEANING

ncol(df)
colnames(df)
colnames(df)=gsub('.','_',colnames(df),fixed=TRUE)

head(df)

unique(df$Size)
df$Size=gsub('k','000',df$Size,fixed=TRUE)
df$Size=gsub('M','000000',df$Size,fixed=TRUE)
df$Size=gsub('+','',df$Size,fixed=TRUE)
df$Size=gsub('Varies','',df$Size,fixed=TRUE)
length(df$Size[grepl('Varies', df$Size)])
df$Size[grepl('Varies', df$Size)]=NA
df$Size=suppressWarnings(as.numeric(df$Size))

unique(df$Installs)
df$Installs=gsub('+','',df$Installs,fixed=TRUE)
df$Installs=gsub(',','',df$Installs,fixed=TRUE)
df$Installs=gsub('Free',NA,df$Installs,fixed=TRUE)
df$Installs=suppressWarnings(as.numeric(df$Installs))

is.numeric(df$Reviews)
is.character(df$Reviews)
suppressWarnings(df[is.na(as.numeric(df$Reviews)),'Reviews'])
df$Reviews=gsub('.0M','000000',df$Reviews,fixed=TRUE)
df$Reviews=as.numeric(df$Reviews)

is.numeric(df$Rating)
df[is.na(df$Rating),'Rating']=NA
nrow(df[is.na(df$Rating),])
df$Rating=as.numeric(Rating)

typeof(df$Price)
unique(df$Price)
df$Price=gsub('$','',df$Price,fixed=TRUE)
df$Price=suppressWarnings(as.numeric(df$Price))

unique(df$Category)
df=df[!(df$Category=='1.9'),]

head(df$Last_Updated,n=3)
typeof(df$Last_Updated)
df$Last_Updated=as.Date(df$Last_Updated, "%B %d,%Y")

df=na.omit(df)

### DATA VISUALIZATION, TABLES AND GRAPHS

sapply(df,class)

col_num=c()
for (loop in colnames(df)){
  if (is.numeric(df[,loop])==TRUE){
    col_num=c(col_num,loop)
  }
}

cormat=round(cor(df[,col_num]),2)

library(reshape2)
melted_cormat <- melt(cormat)
head(melted_cormat)

library(ggplot2)
ggplot(data = melted_cormat, aes(x=Var1, y=Var2, fill=value)) + geom_tile() + xlab('') + ylab('')

### 

x=barplot(table(df$Category), xaxt="n", main='Barplot by App Category', ylab='No. of Installs (in hundred thousand)')
cat=names(table(df$Category))
text(cex=1/2, x=x, y=-10, cat, xpd=TRUE, srt=90, adj=1)

tapply(df$Category,df$Genres,length)

###

library(scales)
library(ggplot2)
ggplot(df, aes(x=df$Reviews, y=df$Rating)) +
  scale_x_continuous(trans='log10', labels=comma) +
  geom_point(aes(col=Type)) +
  labs(title="Android App Ratings vs Number of Reviews", subtitle="Google Playstore Dataset", y="Rating from 1 to 5 stars", x="Number of Reviews") +
  theme_linedraw()

library(scales)
library(ggplot2)
ggplot(df, aes(y=df$Reviews, x=df$Installs)) +
  scale_x_continuous(trans='log10', labels=comma) +
  geom_point(aes(col=Type)) +
  labs(title="Android App Reviews vs Number of Installs", subtitle="Google Playstore Dataset", y="Number of Reviews", x="Number of Installs") +
  theme_linedraw()

library(scales)
library(ggplot2)
ggplot(df, aes(y=df$Rating, x=df$Installs)) +
  scale_x_continuous(trans='log10', labels=comma) +
  geom_point(aes(col=Type)) +
  labs(title="Android App Reviews vs Number of Installs", subtitle="Google Playstore Dataset", y="Number of Ratings", x="Number of Installs") +
  theme_linedraw()

###

# 3D Exploded Pie Chart
install.packages('plotrix')
library(plotrix)
lbl=unique(df$Type)
slices=c()
perc=c()
for (loop in lbl){
  slices=c(slices,nrow(df[df$Type==loop,]))
  perc=c(perc,(format(nrow(df[df$Type==loop,])/nrow(df)*100,digits=3)))
}

pie3D(slices,labels=paste(lbl,'\n',perc,'%'),explode=0.1,
      main="Pie Chart of Apps by Purchase Type ",labelcex=1)

