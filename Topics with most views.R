library(xlsx)
##Topics with the most views 
d <- read.csv(file = "C:/Users/t_fud/OneDrive/Desktop/Uni/Kurse/Seminar/Data/datasets/combined.csv")
df = subset(d, select = c(topicname, views, index))
dft <- df %>% filter(index == 0)
dft2 <- dft %>% filter(views > 1000)

write.xlsx(dft2, file="C:/Users/t_fud/OneDrive/Desktop/Uni/Kurse/Seminar/Data/datasets/mostviews.xlsx", sheetName = "Sheet1")
