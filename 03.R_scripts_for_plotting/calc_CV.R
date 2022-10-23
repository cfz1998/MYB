rm(list=ls())
library(ggplot2)
library(tidyr)
library(ggpubr)
library(stringr)
library(grid)
library(xlsx)

data <- read.xlsx("new_draw_data.xlsx", sheetIndex = 1)
names(data) <- c("class", 'R1', 'R2')

class_name <- unique(data$class)

sd1 <- c()
mean1 <- c()
cout1 <- c()

for (i in class_name){
  temp_data <- data[data$class == i, ]
  temp_sd <- sd(temp_data$R1)
  temp_mean <- mean(temp_data$R1)
  temp_cout <- nrow(temp_data)
  sd1 <- c(sd1, temp_sd)
  mean1 <- c(mean1, temp_mean)
  cout1 <- c(cout1, temp_cout)
}

cv1 <- sd1/mean1

sd2 <- c()
mean2 <- c()
cout2 <- c()

for (i in class_name){
  temp_data <- data[data$class == i, ]
  temp_sd <- sd(temp_data$R2)
  temp_mean <- mean(temp_data$R2)
  temp_cout <- nrow(temp_data)
  sd2 <- c(sd2, temp_sd)
  mean2 <- c(mean2, temp_mean)
  cout2 <- c(cout2, temp_cout)
}

cv2 <- sd2/mean2

final_tab <- data.frame(class_name, cout1, sd1, mean1, cv1, sd2, mean2, cv2)
write.csv(file = "static.csv", final_tab)

# ¿ªÊ¼»­Í¼ cv1
# cv1[is.na(cv1)] <- 0
data_v1 <- data.frame(class_name,cv1)
quanluty = c(1:22)
data_v1$cv1 = as.numeric(data_v1$cv1)
data_v1$class_name <- factor(data_v1$class_name, levels = class_name)
data_v1$cv2 <- cv2
names(data_v1) <- c("class_name", "R1", "R2")
gdata=gather(data_v1,key = "Key",  value = "value", R1, R2)


pdf("CV.pdf", 10,10)
ggplot(gdata, aes(x=class_name, y = value, 
                  type=Key, group=Key, 
                  shape=Key,color=Key)) + 
  geom_point(size = 3) +
  geom_line() +
  theme_bw() +
  xlab("") +
  ylab("") +
  ylim(0,2) +
  theme(panel.background = element_blank(),
        panel.grid.major = element_blank(),
        panel.grid.major.y = element_line(colour = "grey",linetype = 2),
        axis.line = element_line(colour = "black",size = rel(2),arrow = arrow(angle = 30,length = unit(0.1,"inches"))),
        axis.title = element_text(size = rel(1.2)),
        axis.text.x = element_text(angle = 90,face="bold",hjust = 1,vjust=0.5,
                                   size = 12),
        axis.text.y = element_text(hjust = 1,size = rel(1.5)),
        axis.ticks = element_line(size = rel(1.5)),
        panel.border = element_blank())

dev.off()
  
  
