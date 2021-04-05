#R script pour faire des distributions
#!/usr/bin/env Rscript
library(lattice) # pour faire les densités
library(VennDiagram) # pour les diagrammes de venn

# LECTURE DU FICHIER
annot.file = "forFiltration.vcf"
annotations = read.table(annot.file, h=TRUE,na.strings=".")

# dim(annotations)
# head(annotations)

# INITIALISATION DES SEUILS
lim.QD = 21.459095080692492
lim.FS = 2.15642723558344
lim.SOR = 0.927618426437828
lim.MQRankSum = -0.13173060023865243
lim.ReadPosRankSum =  0.12945328565870648
lim.MQ = 58.38629456079415

# CREATION DES FIGURES
pdf(paste(annot.file,"Filtres.pdf",sep="_"), height = 8, width = 12)
par(mfrow=c(2,3))

# FIGURE DE QD
  prop.QD=length( which(annotations$QD < lim.QD)) / nrow(annotations)
  plot(density(annotations$QD,na.rm=T),main="QD", sub = paste("Filtre: QD >",lim.QD,"( = ", signif(prop.QD*100,3),"% des SNP) " ,sep="") )
  abline(v=lim.QD, col="red")

# FIGURE DE FS
  prop.FS=length( which(annotations$FS >lim.FS)) / nrow(annotations)
  plot(density(annotations$FS,na.rm=T),main="FS", sub = paste("Filtre: FS >",lim.FS,"( = ", signif(prop.FS*100,3),"% des SNP) " ,sep="") )
  abline(v=lim.FS, col="red")

# FIGURE DE SOR
  prop.SOR=length( which(annotations$SOR >lim.SOR)) / nrow(annotations)
  plot(density(annotations$ReadPosRankSum,na.rm=T),main="SOR", sub = paste("Filtre: SOR >",lim.SOR,"( = ", signif(prop.SOR*100,3),"% des SNP) " ,sep="") )
  abline(v=lim.SOR, col="red")

# FIGURE DE MQ
  prop.MQ=length( which(annotations$MQ < lim.MQ)) / nrow(annotations)
  plot(density(annotations$MQ,na.rm=T),main="MQ", sub = paste("Filtre: MQ <",lim.MQ,"( = ", signif(prop.MQ*100,3),"% des SNP) " ,sep="") )
  abline(v=lim.MQ, col="red")

# FIGURE DE MQRankSum
  prop.MQRankSum=length( which(annotations$MQRankSum <lim.MQRankSum)) / nrow(annotations)
  plot(density(annotations$MQRankSum,na.rm=T),main="MQRankSum", sub = paste("Filtre: MQRankSum <",lim.MQRankSum,"( = ", signif(prop.MQRankSum*100,3),"% des SNP) " ,sep="") )
  abline(v=lim.MQRankSum, col="red")

# FIGURE DE ReadPosRankSum
  prop.ReadPosRankSum=length( which(annotations$ReadPosRankSum <lim.ReadPosRankSum)) / nrow(annotations)
  plot(density(annotations$ReadPosRankSum,na.rm=T),main="ReadPosRankSum", sub = paste("Filtre: ReadPosRankSum <",lim.ReadPosRankSum,"( = ", signif(prop.ReadPosRankSum*100,3),"% des SNP) " ,sep="") )
  abline(v=lim.ReadPosRankSum, col="red")

dev.off()


# DIAGRAMME DE VENN
qd.pass = which(annotations$QD>lim.QD)
fs.pass = which(annotations$FS>lim.FS)
sor.pass = which(annotations$SOR > lim.SOR)
mq.pass = which(annotations$MQ < lim.MQ & annotations$MQRankSum < lim.MQRankSum)
rprs.pass= which(annotations$ReadPosRankSum <= lim.ReadPosRankSum)

venn.diagram(
  x=list(qd.pass, fs.pass, mq.pass, sor.pass, rprs.pass),
  category.names = c("QD" , "FS" , "MQ and MQRankSum", "SOR", "ReadPosRankSum"),
  fill = c("blue","darkgreen","orange","yellow","red"),
  output=TRUE,
  filename = "MondiagrammedeVenn"
)
