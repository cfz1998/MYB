rm(list=ls())
library(ggplot2)
library(ggtreeExtra)
library(ggtree)
library(treeio)
library(tidytree)
library(ggstar)
library(ggnewscale)
library(MetBrewer)
library(reshape2)

Fig2_tree <- read.newick("new_final.tree")
Fig2_da1 <- read.csv("data1.txt", sep="\t")
Fig2_da1["Size"] = 1

Fig2_da2 <- read.csv("data2.txt")
Fig2_da3 <- read.csv("data3.txt")


Fig2_da2 <- melt(Fig2_da2, id.vars="ID", variable.name="Sites")
Fig2_da2$Sites <- factor(Fig2_da2$Sites, levels = c("MYB_1R","MYB_2R","MYB_3R","MYB_4R"))
Fig2_da3$Sites <- factor(Fig2_da3$Sites, levels = c("MYB_1R","MYB_2R","MYB_3R","MYB_4R"))
# nodeids <- c(820, 429, 804+428+430, 402, 401, 802, 394, 799, 796, 390, 
             # 794,792+386, 787, 721, 713+714+715, 286, 697, 614, 610, 607,
             # 555, 458)
color_value <- c("#ed1299", "#09f9f5", "#246b93", "#cc8e12",
                 "#d561dd", "#c93f00", "#ddd53e","#4aef7b",
                 "#e86502", "#9ed84e", "#39ba30", "#00EE00",
                 "#8249aa", "#00BFFF", "#e07233", "#ff523f",
                 "#ce2523", "#f7aa5d", "#cebb10", "#03827f",
                 "#931635", "#373bbf")

Fig2_nodeids <- c(820, 429,428,804,
                  430, 402, 401, 802, 
                  394, 799, 796, 390, 
                  794, 792,386, 787, 721, 
                  713, 714, 715, 
                  286, 697, 614, 
                  610, 607,555, 458)

Fig2_nodelab <- c("Rhodophyta", "Prasinodermophyta",  "Chlorophyta","Chlorophyta",
                  "Chlorophyta","Klebsormidiophyceae", "Charophyceae", "Zygnematophyceae",
             "Marchantiophyta", "Bryophyta", "Anthocerotales", "Lycopodiophyta",
             "Gymnospermae", "basal Angiosperms", "basal Angiosperms", "Magnoliidae","Monocotyledoneae", 
             "Early-diverging eudicotyledons", "Early-diverging eudicotyledons","Early-diverging eudicotyledons",
             "Santalales", 'Caryophyllales', "Asterids",
             "Saxifragales", "Vitales", "Malvids", "Fabids")

Fig2_poslist <- c(0.2, 1.0, 0.2,1.6, 
                  0.9, 0.1, 0.25, 1.6, 
                  1.6, 1.2, 0.4, 1.2, 
                  2.0, 1.8,0.1, 0.8,0.4,
                  0.3,0.9, 1.8,
                  0.8, 0.4, 0.4, 
                  0.6, 0.3, 0.4, 0.3)



Fig2_labdf <- data.frame(node=Fig2_nodeids, label=Fig2_nodelab, pos=Fig2_poslist)

F2 <- ggtree(Fig2_tree, layout="fan", size=0.15, open.angle=5) +
  geom_hilight(data=Fig2_labdf, mapping=aes(node=node,fill=label),
               extendto=6.8, alpha=0.6,size=0.05) +
  scale_fill_manual(values = color_value)+
  geom_cladelab(data=Fig2_labdf, 
                mapping=aes(node=node, 
                            label=label,
                            offset.text=pos),
                hjust=0.5,
                angle="auto",
                barsize=NA,
                horizontal=FALSE, 
                fontsize=1.4,
                fontface="italic"
) 

F2 <- F2 %<+% Fig2_da1 + geom_star(
  mapping=aes(fill=Phylum, size=Size, starshape=Type),
  position="identity",starstroke=0.1) + 
  scale_fill_manual(values = color_value,
                    guide=guide_legend(keywidth = 0.5,
                                       keyheight = 0.5, order=1,
                                       override.aes=list(starshape=15)),
                    na.translate=FALSE)+
  scale_starshape_manual(values=c(15, 1),
                         guide=guide_legend(keywidth = 0.5,
                                            keyheight = 0.5, order=2),
                         na.translate=FALSE)+
  scale_size_continuous(range = c(0.5, 1.5),
                        guide = guide_legend(keywidth = 0.5,
                                             keyheight = 0.5, order=3,
                                             override.aes=list(starshape=15)))


F2 <- F2 + new_scale_fill() +
  geom_fruit(data=Fig2_da2, geom=geom_tile,
             mapping=aes(y=ID, x=Sites, alpha=value, fill=Sites),
             color = "grey50", offset = 0.08,size = 0.02)+
  scale_alpha_continuous(range=c(0, 1),
                         guide=guide_legend(keywidth = 0.2, 
                                            keyheight = 0.2, order=5)) +
  geom_fruit(data=Fig2_da3, geom=geom_bar,
             mapping=aes(y=ID, x=value, fill=Sites),
             pwidth=0.38, 
             orientation="y", 
             stat="identity",
  ) +
  scale_fill_manual(values=c("#0000FF","#FFA500","#FF0000",
                             "#800000"),
                    guide=guide_legend(keywidth = 0.2, 
                                       keyheight = 0.2, order=4))+
  geom_treescale(fontsize=2, linesize=0.3, x=4.9, y=0.1) +
  theme(legend.position=c(0.93, 0.5),
        legend.background=element_rect(fill=NA),
        legend.title=element_text(size=6.5),
        legend.text=element_text(size=4.5),
        legend.spacing.y = unit(0.02, "cm"),
  )

pdf("Fig2.pdf", 15, 15)
F2
dev.off()

