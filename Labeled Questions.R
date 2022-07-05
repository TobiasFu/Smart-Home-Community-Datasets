#Data analysis without manually derived Questions
#Import packages
library(tidyverse)
library(ISLR)
library(Amelia)
library(mlbench)
library(xlsx)

data <- read.csv(file = "C:/Users/t_fud/OneDrive/Desktop/Uni/Kurse/Seminar/Data/combined.csv")

##Data cleaning##
data$question[is.na(data$question)] <- 0
data$solved[is.na(data$solved)] <- 0
#redudant or irrelevant variables (mostly because of 100% NAs or 0s)
df = subset(data, select = -c(mainPid, bookmarks, postdeleted, edited, username, status, 
                           teaserPid, downvotes, deleted, pinExpiry, upvotes, postdownvotes, 
                           votes, banned, bannedExpire, group, bannedUntil, selectedGroups, 
                           profileInfo, replyshasMore, replyuser, replycount, replytext,
                           postuserID, topicname, toopicID, userpostcount))

##adding new variables##
#Adding mean and max values for reputation, topiccount, polarity and subjectivity
df$mreputation <- with(df, ave(reputation, topicID, FUN=mean))
df$xreputation <- with(df, ave(reputation, topicID, FUN=max))
df$musertopiccount <- with(df, ave(usertopiccount, topicID, FUN=mean))
df$xusertopiccount <- with(df, ave(usertopiccount, topicID, FUN=max))
df$mpolarity <- with(df, ave(as.numeric(polarity), topicID, FUN=mean))
df$xpolarity <- with(df, ave(as.numeric(polarity), topicID, FUN=max))
df$msubjective <- with(df, ave(subjective, topicID, FUN=mean))
df$xsubjective <- with(df, ave(subjective, topicID, FUN=max))
#Finding last postindex
df$lastindex <- with(df, ave(index, topicID, FUN=max))
#Time variables
df$createdat <- as.Date(df$createdat)
df$creatednum <- as.numeric(df$createdat)
df$lasttime <- as.Date(df$lasttime)
df$lastnum <- as.numeric(df$lasttime)
df$lastonline <- as.Date(df$lastonline)
df$onlinenum <- as.numeric(df$lastonline)
df$posttimestamp <- as.Date(df$posttimestamp)
df$postnum <- as.numeric(df$posttimestamp)
df$runtime <- (df$lastnum - df$creatednum)
#chapters as variable
df$chapterID2 <- as.character(df$chapterID)

##Question dataset##
qdf <- df %>% filter(question == 1)
qdf <- qdf %>% filter(index == 0)

##Models##
#m1 <- glm(solved ~ 'independent variables',data = qdf2x, family = binomial)
mb <- glm(formula = solved ~ chapterID + mreputation + musertopiccount + 
               mpolarity + msubjective + xsubjective, family = binomial,data = qdf)
out <- capture.output(summary(mb))
write.xlsx(out, "C:/Users/t_fud/OneDrive/Desktop/Uni/Kurse/Seminar/Data/m1best25_06.xlsx", col.names = TRUE, row.names = TRUE,)

