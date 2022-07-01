#!/usr/local/bin/Rscript
rm(list=ls())
library(edgeR)
Args <- commandArgs(T)
inf <- Args[1]
ouf_file <- Args[2]

data <- read.delim(inf, row.names = 1, stringsAsFactors=FALSE,
                   check.names=FALSE)

col_name <- names(data)

targets <- data.frame(Lane = c(1:length(col_name)), 
                      Treatment = substr(col_name,1,nchar(col_name)-1), 
                      Label = col_name)

y <- DGEList(counts=data[,1:length(col_name)], 
             group=targets$Treatment)

colnames(y) <- targets$Label
y <- y[rowSums(cpm(y) > 1) >= 1,]
y$samples$lib.size <- colSums(y$counts)
y <- calcNormFactors(y)

bcv <- 0.4
et <- exactTest(y, dispersion = bcv ^ 2)
# 
summary(de <- decideTestsDGE(et))
detags <- rownames(y)[as.logical(de)]
ordered_tags <- topTags(et, n=Inf)
diff <- ordered_tags$table
write.table(diff, file=ouf_file, row.names = T, col.names = T, quote=F,sep="\t")


