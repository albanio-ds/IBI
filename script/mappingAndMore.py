#!/usr/bin/env python3

import os
import subprocess
from statistics import mean


'''
Prérequis
Unzip les fichiers .gz avant de commencer cette étape
modifier les variables ci-dessous marqué à coté "a changer" avec les noms de fichiers respectifs

genome_de_reference : par le fichiers contenant le genome de référence (.fasta ou .fsa)
path_gatk_java : par le nom du chemin vers le jar local gatk
fichierTsv : par le fichier tsv qui contient les informations liés au lien ftp,md5 et sample_alias
             (que vous avez utilisé dans l'etape précédente)

'''


genome_de_reference_fsa ="S288C_reference_sequence_R64-2-1_20150113.fsa" # a changer
path_gatk_java ="java -jar /home/jeyanthan/Documents/coursL3/S6/IBI/Gatk/gatk-4.1.9.0/gatk-package-4.1.9.0-local.jar" # a changer
fichierTsv = "filereport_read_run_PRJEB24932_tsv.txt" # a changer

#Les reads sont au format fastq qui a comme extension soit .fastq soit .fq. Ils peuvent etre utilisés compressés (pas de pb).

def getPaireEnd():
    '''

    '''
    affiche_ls = str(subprocess.check_output("ls" ,shell=True))
    affiche_ls=affiche_ls.split("\\n")
    groupe_paire=[[]]
    for i in range(len(affiche_ls)-1):
        read1=affiche_ls[i].split(".")
        read2= affiche_ls[i+1].split(".")
        if len(read1)==2 and  len(read2)==2 :
             #condition fast,fq
            if (read1[1]=="fastq" and read2[1]=="fastq")or (read1[1]=="fq" and read2[1]=="fq"):
                if read1[0]!=read2[0] and read1[0][:-1] ==read2[0][:-1]  and read1[0][-2]=='_':
                    read1_complet=read1[0]+"."+read1[1]
                    read2_complet=read2[0]+"."+read2[1]
                    groupe_paire.append([read1_complet,read2_complet])

    return groupe_paire



def checkSingleEnd(myRead):
    '''

    '''
    p=0
    double=getPaireEnd()
    for i in double:
        for j in i:
            if myRead ==j :
                p+=1
    return p

#ex : ERR43242_1.fastq
def getSingleEnd():
    '''

    '''
    affiche_ls = str(subprocess.check_output("ls" ,shell=True))
    affiche_ls=affiche_ls.split("\\n")
    singleRead=[]
    for i in range(len(affiche_ls)-1):
        reads=affiche_ls[i].split(".")
        if len(reads)==2:
            if reads[1]=="fastq" or reads[1]=="fq":
                readsComplet=reads[0]+"."+reads[1]
                if(checkSingleEnd(readsComplet) ==0):
                    singleRead.append(readsComplet)
    return singleRead



#s.fsa.amb
#s.fsa.ann
#s.fsa.bwt
#s.fsa.pac
#s.fsa.sa

#Le genome de référence doit etre au format fasta qui a comme extension soit .fasta soit .fa soit .fsa

#

def genReferenceIndexed(s):
    '''

    '''
    genomeF1= s+"."+"amb"
    genomeF2= s+"."+"ann"
    genomeF3= s+"."+"bwt"
    genomeF4= s+"."+"pac"
    genomeF5= s+"."+"sa"
    genomeF6= s+"."+"fai" # génére par samtools faidx
    genomeF7= s.split('.')[0] + ".dict"
    affiche_ls = str(subprocess.check_output("ls" ,shell=True))
    if genomeF1 in  affiche_ls and genomeF2 in  affiche_ls and genomeF3 in  affiche_ls and genomeF4 in  affiche_ls and genomeF5 in  affiche_ls and genomeF6 in affiche_ls and genomeF7 in affiche_ls:
        return True

    return False



def indexGenome(s):
    '''

    '''
    os.system("bwa "+"index " + s)
    os.system("samtools " + "faidx " + s)
    gatk_cmd_bis = " CreateSequenceDictionary -R "+ s
    os.system(path_gatk_java + gatk_cmd_bis)
    if genReferenceIndexed(s):
        return
    else:
        raise Exception("verifiez si il s'agit bien du génome de référence !")



def newGenomeDeReference(s):
    '''

    '''

    newName = s.strip().split('.')[0] + ".fasta"

    if checkNewFile(newName):
        return newName
    else:
        os.system("mv " + s + " " + newName)
        return newName



#read1="ERR2299966_1.fastq"
#read2="ERR2299966_2"
#nv_noms=read1+"_"+read2
#bwa index  S288C_reference_sequence_R64-2-1_20150113.fsa

#bwa mem genome_de_reference read1.fastq read2.fastq >  nv_noms
 #recup le nom de la souche

def finder_ftp(fichierTsv):
    '''

    '''
    f=open(fichierTsv)
    tsv_toListe = [ i.strip().split('\t') for i in f]
    finder=False
    i=0
    for row in tsv_toListe:
        if not finder:
            while not finder and i<len(row):
                if row[i] == "fastq_ftp":
                    finder = True
                else:
                    i+=1
        else:
            None

        if not finder:
            raise Exception('Pas de champ fastq_ftp')
    return i


def finders_alias(fichierTsv):
    '''

    '''
    f=open(fichierTsv)
    tsv_toListe = [ i.strip().split('\t') for i in f]
    finder=False
    i=0
    for row in tsv_toListe:
        if not finder:
            while not finder and  i<len(row):
                if row[i]=="sample_alias":
                    finder=True
                    #print("trouvé", i )
                    return i
                else:
                    i+=1
        else:
            None
        if not finder:
            raise Exception("pas de champs sample_alias")
    return i


def finderSampleName(fichierTsv, searchSampleN):
    '''

    '''
    fileSearching= searchSampleN.split(".")
    correctName = fileSearching[0]
    f=open(fichierTsv)
    tsv_toListe = [ i.strip().split('\t') for i in f]
    ftp_column = finder_ftp(fichierTsv)
    sample_column = finders_alias(fichierTsv)
    sample_name=""
    for i in tsv_toListe:

        lienSansGz= i[ftp_column].split(";")
        lienSansGz = lienSansGz[0].split("/")
        lienf= lienSansGz[-1].split(".")
        lienfinale = lienf[0]
      #  print(lienfinale)
        if lienfinale ==correctName:
           # print(lienf[0], "son sample name = ", i[sample_column])
            sample_name= i[sample_column]
            #print(sample_name)
            return sample_name

    if sample_name =="":
        raise Exception("Sample name introuvable")


def strainFinder(monGdeRef):
    '''

    '''
    f= open(monGdeRef)
    fsaToList =[i.strip().split('[') for i in f]
    firstLigne =fsaToList[0]
    strainRet=""
    for i in firstLigne :
        if "strain=" in i :
            strainRet = i.split("=")[1][:-2].strip()
           # print("mon strain :" ,strainRet)
            return strainRet

    if strainRet=="":
        raise Exception("No strain found")


def checkNewFile(f):
    '''

    '''
    affiche_ls = str(subprocess.check_output("ls" ,shell=True))
    if(f in affiche_ls):
        return True

    return False

def mapping_samtool(FindSampleName,newName_Sam,fichierTsv,genoRef):
    '''

    '''
    sampleName= finderSampleName(fichierTsv,FindSampleName)
    newName_Bam= sampleName + ".bam"
    newName_BamSort = sampleName + "_sort.bam"
    newName_BamDupl = sampleName + "_duplicated.bam"
    newName_BamFlag = sampleName + "_flag.txt"
    newName_BamCouv = sampleName + "_couv.txt"
    newName_Bam_Bai = newName_BamDupl + ".bai"
    newName_Gvcf_Haplot = sampleName + ".g.vcf"
    #on passe à samtools
    samtool_view=False
    samtool_sort=False
    gatk_markDupl =False
    samtool_flags=False
    bedtools_couv=False
    samtool_index=False
    gatk_haplot=False
    if checkNewFile(newName_Bam):
        print(newName_Bam, " is already there! ")
        samtool_view=True

    if not checkNewFile(newName_Bam):
        #samtools view -o aln.bam aln.sam.gz
        os.system("samtools " + "view " + "-o " + newName_Bam + " " + newName_Sam  )
        if checkNewFile(newName_Sam):
            samtool_view=True
    if samtool_view :
        #on passe à samtools sort
        if checkNewFile(newName_BamSort):
            print(newName_BamSort, " is already there! ")
            samtool_sort=True
        else:
            os.system("samtools " + "view " + "-o " + newName_BamSort + " " + newName_Bam  )
            if checkNewFile(newName_BamSort):
                samtool_sort=True
    if samtool_sort:
        #on passe a GATK

        if checkNewFile(newName_BamDupl):
            print(newName_BamDupl, " is already there! ")
            gatk_markDupl=True
        else:
            #gatk MarkDuplicatesSpark  -I input.bam -O marked_duplicated.bam

            gatk_cmd_bis=" MarkDuplicatesSpark " + "-I " + newName_BamSort + " " +"-O " + newName_BamDupl

            os.system(path_gatk_java + gatk_cmd_bis)


            if checkNewFile(newName_BamDupl):
                gatk_markDupl=True
    if gatk_markDupl:
        #samtools flagstat aln.sorted.bam
        if checkNewFile(newName_BamFlag):
            print(newName_BamFlag, " is already there! ")
            samtool_flags=True
        else:
            os.system("samtools " + "flagstat " + newName_BamDupl + " >" + newName_BamFlag )
            if checkNewFile(newName_BamFlag):
                samtool_flags=True
    if samtool_flags:
        if checkNewFile(newName_BamCouv):
            print(newName_BamCouv, " is already there! ")
            bedtools_couv=True
        else:
            os.system("bedtools " + "genomecov " + "-ibam " +  newName_BamDupl  + " -bga" + " > " + newName_BamCouv )
            if checkNewFile(newName_BamFlag):
                bedtools_couv=True
    if bedtools_couv:
        if checkNewFile(newName_Bam_Bai):
             samtool_index=True
        else:
            os.system("samtools "+ "index "+ newName_BamDupl )
            if checkNewFile(newName_Bam_Bai):
                print(newName_Bam_Bai, " is already there! ")
                samtool_index=True
    if samtool_index:
        if checkNewFile(newName_Gvcf_Haplot):
            print(newName_Gvcf_Haplot, " is already there! ")
            gatk_haplot=True
        else:
            gatk_cmd_bis2 = " HaplotypeCaller " + " -R " +  genoRef  + " -I " +  newName_BamDupl +   " -O " + newName_Gvcf_Haplot + " -ERC GVCF"
            os.system(path_gatk_java + gatk_cmd_bis2)
            if checkNewFile(newName_Gvcf_Haplot):
                gatk_haplot=True

    return
        #bedtools genomecov -ibam    fichier_duplicate.bam  -bga  >   sampleAlis_couv.txt


def  mappingCalcul(): # Calculez le % de reads mappent le génome de référence
    '''

    '''
    affiche_ls = str(subprocess.check_output("ls" ,shell=True))
    affiche_ls=affiche_ls.split("\\n")
    pourcentage=[]
    lemin =0
    lemax=0
    lamoyenne=0
    for i in range(len(affiche_ls)-1):
        fichier=affiche_ls[i].split("_")
        if len(fichier)==2:
            if fichier[1]=="flag.txt":
                file_name ="_".join(fichier)
                map_file = open(file_name)
                map_file_toList =[ i.strip().split('\t') for i in map_file]
                mapped_here= map_file_toList[4][0].split("%")
                mapped_here = mapped_here[0].split("(")
                pourcentage.append(float(mapped_here[1]))

    lemin =min(pourcentage)
    lemax=max(pourcentage)
    lamoyenne=round(mean(pourcentage))
    print("la moyenne =", lamoyenne  ,"le min = ", lemin , " le max = ", lemax )



def couvertureMapp(): #Calculez la couverture moyenne
    '''

    '''
    affiche_ls = str(subprocess.check_output("ls" ,shell=True))
    affiche_ls=affiche_ls.split("\\n")
    moyTab=[]
    lamoyenneToTal=0
    leMin=0
    leMax=0
    for i in range(len(affiche_ls)-1):
        fichier=affiche_ls[i].split("_")
        if len(fichier)==2:
            if fichier[1]=="couv.txt":
                #print(fichier)
                file_name ="_".join(fichier)
                map_file = open(file_name)
                fileToList = [ i.strip().split('\t') for i in map_file]
                res=0
                taille=0
                for i in range(len(fileToList)):
                    res+=int(fileToList[i][3])
                    taille+=1
                moy=res/taille
                moyTab.append(moy)


    leMin =min(moyTab)
    leMax=max(moyTab)
    lamoyenneToTal=round(mean(moyTab))
    print("la moyenne =", lamoyenneToTal  ,"le min = ", leMin , " le max = ", leMax )




def mappingPaired(fichierTsv,genoRef,f1,f2):
    '''

    '''
    sampleName= finderSampleName(fichierTsv,f1)
    newName_Sam= sampleName + ".sam"
    strainName = strainFinder(genoRef)
    #print("bwa "+ "mem " +genoRef + " " + f1 + " " + f2 + " >" + newName)
    rg_id = strainName+"-"+sampleName
    rg_sm = sampleName
    rg_flag = repr("@RG\tID:"+ rg_id +"\tSM:" + rg_sm + "\tPL:Illumina\tPU:0\tLB:1")
    bwa_map =False
    samtool_map=False
    #print(newName_Sam)
    if checkNewFile(newName_Sam) :

        print(newName_Sam, " is already there! ")
        bwa_map = True
    if not checkNewFile(newName_Sam) :
        #print("bwa "+ "mem " +"-R " + rg_flag+ " " +genoRef +" " +  f1 + " " + f2 + " >" + newName)
        os.system("bwa "+ "mem " +"-R " + rg_flag+ " " +genoRef +" " +  f1 + " " + f2 + " >" + newName_Sam)
        if checkNewFile(newName_Sam) :
            print("new file : ", newName_Sam)
            bwa_map = True

    if bwa_map :
        mapping_samtool(f1,newName_Sam,fichierTsv,genoRef)




def mappingSingle(fichierTsv,genoRef,f):
    '''

    '''
    sampleName= finderSampleName(fichierTsv,f)
    newName_Sam= sampleName + ".sam"
    strainName = strainFinder(genoRef)
    rg_id = strainName+"-"+sampleName
    rg_sm = sampleName
    rg_flag = repr("@RG\tID:"+ rg_id +"\tSM:" + rg_sm + "\tPL:Illumina\tPU:0\tLB:1")
    bwa_map = False
    samtool_map=False
    if checkNewFile(newName_Sam) :
        print(newName_Sam, " is already there! ")
        bwa_map= True
    if not checkNewFile(newName_Sam) :
        #print("bwa "+ "mem " +"-R " + rg_flag+ " " +genoRef +" " +  f + " >" + newName)
        os.system("bwa "+ "mem " +"-R " + rg_flag+ " " +genoRef +" " +  f + " >" + newName_Sam)
        if checkNewFile(newName_Sam):
            print("new file : ", newName_Sam)
            bwa_map=True
    if bwa_map :
        mapping_samtool(f,newName_Sam,fichierTsv,genoRef)

def finders_md5(fichierTsv):
    '''

    '''
    f=open(fichierTsv)
    tsv_toListe = [ i.strip().split('\t') for i in f]
    finder=False
    i=0
    for row in tsv_toListe:
        if not finder:
            while not finder and  i<len(row):
                if row[i]=="fastq_md5":
                    finder=True
                   # print("trouvé", i )
                    return i
                else:
                    i+=1
        else:
            None
        if not finder:
            raise Exception("pas de champs fastq_md5")
    return i


def count_correct(fichierTsv):
    '''

    '''

    r= open(fichierTsv)
    tsv_toListe = [ i.strip().split('\t') for i in r]
    compteur=0
    md5_f=finders_md5(fichierTsv)
    for i in tsv_toListe:
       # if len(i)>6:  #première liste= premiere ligne , nous interèsse pas
        if len(i[md5_f])>=32 and (len(i[md5_f].split(";"))>=2 ):
            compteur+=2
        else:
            if len(i[md5_f])>=32:
                compteur+=1


    return compteur

def find_all_gvcf():
    '''
    cette fonction sera appellé à la fin,
    on va chercher tout les fichier ayant pour extension .g.vcf
    est en faire une chaine de la forme : 
    -V fichier.g.vcf -V fichier2.g.vcf ..
    Elle nous servira notamment dans l'appel de la 
    fonction GenomicsDBImport
    '''
    affiche_ls = str(subprocess.check_output("ls" ,shell=True))
    affiche_ls=affiche_ls.strip().split("\\n")
    sequenceGvcf=""
    for i in affiche_ls:
        if ".g.vcf.idx" in i:
            None
        else:
            if ".g.vcf" in i:
                sequenceGvcf += " -V " + i 
    return sequenceGvcf

##gatk  GenomicsDBImport -V UFMG-CM-Y624.g.vcf -V UFMG-CM-Y625.g.vcf    --genomicsdb-workspace-path  my_database/ -L intervals.list
def gatkGenomic():
    affiche_ls = str(subprocess.check_output("ls" ,shell=True))
    #affiche_ls=affiche_ls.strip().split("\\n")
    if "my_database" in affiche_ls:
        print("Consolidation effectué !")
        return
    allgvcf = find_all_gvcf()
    os.system(path_gatk_java +  " GenomicsDBImport " + allgvcf + " --genomicsdb-workspace-path  my_database/ " + " -L " + " intervals.list" )


#gatk GenotypeGVCFs -R S288C_reference_sequence_R64-2-1_20150113.fasta -V gendb://my_database -O output.vcf    
def gatkGenotype(genoRef):
    affiche_ls = str(subprocess.check_output("ls" ,shell=True))
    if "sortieFinale.vcf" in affiche_ls:
        print("Appel joint effectué! ")
        return 
    os.system(path_gatk_java + " GenotypeGVCFs" + " -R " + genoRef + " -V " + "gendb://my_database " + " -O " + " sortieFinale.vcf" )

def pipeline(fichierTsv, monGdeRef):
    '''


    '''
    readPairEnd=getPaireEnd()
    readSinglEnd=getSingleEnd()
    compteur=0
    doneOrNotMapping= False
    gvcfDone=False
   # vcfDone =False
    if genReferenceIndexed(monGdeRef):
        print("Le genome de réference a bien été indexé !")
    else:
        indexGenome(monGdeRef)
    print("Début du mapping !")
    for i in readPairEnd:
        if i!=[]:
            read1_pair=i[0]
            read2_pair=i[1]
            mappingPaired(fichierTsv,monGdeRef,read1_pair,read2_pair)
            compteur+=2

    for k in readSinglEnd:
        mappingSingle(fichierTsv,monGdeRef,k)
        compteur+=1

    if count_correct(fichierTsv) == compteur :
        print("mapping fini ! ")
        doneOrNotMapping=True

    # if doneOrNot :
    #     print(" Le pourcentage de reads mappent le génome de référence : ")
    #     mappingCalcul()
    #     print("La couverture moyenne (veuillez patienter..): ")
    #     couvertureMapp()
    if doneOrNotMapping:
        gatkGenomic()
        gvcfDone=True
    if gvcfDone:
        gatkGenotype(monGdeRef)






##############
genome_de_reference_fasta = newGenomeDeReference(genome_de_reference_fsa)
pipeline(fichierTsv,genome_de_reference_fasta)

#mappingCalcul()
#################


#####
#couvertureMapp()