 #!/usr/bin/env python3

import os
import subprocess
import signal
 



genome_de_reference ="S288C_reference_sequence_R64-2-1_20150113.fsa" # a changer 
path_gatk_java ="java -jar /home/jeyanthan/Documents/coursL3/S6/IBI/Gatk/gatk-4.1.9.0/gatk-package-4.1.9.0-local.jar" # achanger 
fichierTsv = "filereport_read_run_PRJEB24932_tsv.txt" # a changer 


#Les reads sont au format fastq qui a comme extension soit .fastq soit .fq. Ils peuvent etre utilisés compressés (pas de pb).

def getPaireEnd():
    affiche_ls = str(subprocess.check_output("ls" ,shell=True))
    affiche_ls=affiche_ls.split("\\n")
    
  
    groupe_paire=[[]]
    for i in range(len(affiche_ls)-1):
        read1=affiche_ls[i].split(".")
        read2= affiche_ls[i+1].split(".")
        if len(read1)==2 and  len(read2)==2 :
            if (read1[1]=="fastq" and read2[1]=="fastq")or (read1[1]=="fq" and read2[1]=="fq"):
                if read1[0]!=read2[0] and read1[0][:-1] ==read2[0][:-1]  and read1[0][-2]=='_':
                    read1_complet=read1[0]+"."+read1[1]
                    read2_complet=read2[0]+"."+read2[1]
                    groupe_paire.append([read1_complet,read2_complet])

    return groupe_paire


def checkSingleEnd(myRead):
    p=0
    double=getPaireEnd()
    for i in double:
        for j in i:
            if myRead ==j :
                p+=1
    return p
               
                

def getSingleEnd():
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
def genReferenceIndexed(s):
    genomeF1= s+"."+"amb" 
    genomeF2= s+"."+"ann" 
    genomeF3= s+"."+"bwt" 
    genomeF4= s+"."+"pac" 
    genomeF5= s+"."+"sa" 

    affiche_ls = str(subprocess.check_output("ls" ,shell=True))
    affiche_ls=affiche_ls.split("\\n")
    #for i in range(len(affiche_ls)):
    if genomeF1 in  affiche_ls and genomeF2 in  affiche_ls and genomeF3 in  affiche_ls and genomeF4 in  affiche_ls and genomeF5 in  affiche_ls:
        return True
    
    return False



def indexGenome(s):
    os.system("bwa "+"index " + s)
    if genReferenceIndexed(s):
        return
    else:
        raise Exception("verifiez si il s'agit bien du génome de référence !")



#read1="ERR2299966_1.fastq"
#read2="ERR2299966_2"
#nv_noms=read1+"_"+read2
#bwa index  S288C_reference_sequence_R64-2-1_20150113.fsa

#bwa mem genome_de_reference read1.fastq read2.fastq >  nv_noms
 #recup le nom de la souche

def finder_ftp(fichierTsv):
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
            return sample_name

    if sample_name =="":
        raise Exception("Sample name introuvable")
    

def strainFinder(monGdeRef):
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
    affiche_ls = str(subprocess.check_output("ls" ,shell=True))
    affiche_ls=affiche_ls.split("\\n")
    if(f in affiche_ls):
        return True
    
    return False

def mapping_samtool(FindSampleName,newName_Sam,fichierTsv):
    sampleName= finderSampleName(fichierTsv,FindSampleName)
    newName_Bam= sampleName + ".bam"
    newName_BamSort = sampleName + "_sort.bam"
    newName_BamDupl = sampleName + "_duplicated.bam"
    newName_BamFlag = sampleName + "_flag.txt"
    #on passe à samtools
    samtool_view=False
    samtool_sort=False
    gatk_markDupl =False
    samtool_flags=False
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
        return

    

        





def mappingPaired(fichierTsv,genoRef,f1,f2):
    sampleName= finderSampleName(fichierTsv,f1)
    newName_Sam= sampleName + ".sam"
    strainName = strainFinder(genoRef)
    #print("bwa "+ "mem " +genoRef + " " + f1 + " " + f2 + " >" + newName)
    rg_id = strainName+"-"+sampleName
    rg_sm = sampleName
    rg_flag = repr("@RG\tID:"+ rg_id +"\tSM:" + rg_sm + "\tPL:Illumina\tPU:0\tLB:1")
    bwa_map =False
    samtool_map=False
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
        mapping_samtool(f1,newName_Sam,fichierTsv)

    
 

def mappingSingle(fichierTsv,genoRef,f):
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
        mapping_samtool(f,newName_Sam,fichierTsv)
        
    

def pipeline(fichierTsv, monGdeRef):
    readPairEnd=getPaireEnd()
    readSinglEnd=getSingleEnd()
    compteur=0
    if genReferenceIndexed(monGdeRef):
        print("le genome de réference à bien étais indexé !")
    else:
        indexGenome(monGdeRef)
    print("Debut du mapping !")
    for i in readPairEnd:
        if i!=[]:
            compteur+=2
          #  print(i," :",compteur)
            read1_pair=i[0]
            read2_pair=i[1]
            #print("paire1 :",read1_pair, " paire2 :", read2_pair)
            mappingPaired(fichierTsv,monGdeRef,read1_pair,read2_pair)
            #for j in i :
             #   print(" read ",j )
    
    for k in readSinglEnd:
        compteur+=1
        mappingSingle(fichierTsv,monGdeRef,k)
      #  print(k,":", compteur)



 

pipeline(fichierTsv,genome_de_reference)
