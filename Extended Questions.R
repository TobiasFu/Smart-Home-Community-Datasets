#Data analysis with manually derived questions
#Import packages
library(tidyverse)
library(ISLR)
library(Amelia)
library(mlbench)
library(xlsx)
library(alpaca)

##Import##
d <- read.csv(file = "C:/Users/t_fud/OneDrive/Desktop/Uni/Kurse/Seminar/Data/datasets/combined_manual.csv", header = TRUE, row.names = NULL, sep = ";")

##Data cleaning##
d$question[is.na(d$question)] <- 0
d$solved[is.na(d$solved)] <- 0
#redudant or irrelevant variables (mostly because of 100% NAs or 0s)
d2 = subset(d, select = -c(mainPid, bookmarks, postdeleted, edited, username, status, 
                           teaserPid, downvotes, deleted, pinExpiry, upvotes, postdownvotes, 
                           votes, banned, bannedExpire, group, bannedUntil, selectedGroups, 
                           profileInfo, replyshasMore, replyuser, replycount, replytext,
                           postuserID, topicname, toopicID, userpostcount))

##adding new variables##
#Adding mean and max values for reputation, topiccount, polarity and subjectivity
d2$mreputation <- with(d2, ave(reputation, topicID, FUN=mean))
d2$xreputation <- with(d2, ave(reputation, topicID, FUN=max))
d2$musertopiccount <- with(d2, ave(usertopiccount, topicID, FUN=mean))
d2$xusertopiccount <- with(d2, ave(usertopiccount, topicID, FUN=max))
d2$mpolarity <- with(d2, ave(as.numeric(polarity), topicID, FUN=mean))
d2$xpolarity <- with(d2, ave(as.numeric(polarity), topicID, FUN=max))
d2$msubjective <- with(d2, ave(subjective, topicID, FUN=mean))
d2$xsubjective <- with(d2, ave(subjective, topicID, FUN=max))
#Finding last postindex
d2$lastindex <- with(d2, ave(index, topicID, FUN=max))
#Time variables
d2$createdat <- as.Date(d2$createdat)
d2$creatednum <- as.numeric(d2$createdat)
d2$lasttime <- as.Date(d2$lasttime)
d2$lastnum <- as.numeric(d2$lasttime)
d2$lastonline <- as.Date(d2$lastonline)
d2$onlinenum <- as.numeric(d2$lastonline)
d2$posttimestamp <- as.Date(d2$posttimestamp)
d2$postnum <- as.numeric(d2$posttimestamp)
d2$runtime <- (d2$lastnum - d2$creatednum)
#chapters as variable
d2$chapterID2 <- as.character(d2$chapterID)
d2$topicID2 <- as.character(d2$topicID)

##Question dataset##
qd2 <- d2 %>% filter(question == 1)
qdf2 <- qd2 %>% filter(index == 0)
qdf2x <- qd2 %>% filter(index == lastindex)

##Models##
#m1 <- glm(solved ~ 'independent variables',data = qdf2x, family = binomial)
mbest <- glm(formula = solved ~ chapterID + mreputation + musertopiccount + 
      mpolarity + msubjective + xsubjective, family = binomial,data = qdf2x)
out <- capture.output(summary(mbest))
write.xlsx(out, "C:/Users/t_fud/OneDrive/Desktop/Uni/Kurse/Seminar/Data/mbest25_06.xlsx", col.names = TRUE, row.names = TRUE,)

