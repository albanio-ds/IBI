#!/usr/bin/env python3

import os
import subprocess


genome_de_reference ="S288C_reference_sequence_R64-2-1_20150113.fsa"

#read1="ERR2299966_1.fastq"
#read2="ERR2299966_2"
#nv_noms=read1+"_"+read2
#bwa index  S288C_reference_sequence_R64-2-1_20150113.fsa
#bwa mem genome_de_reference read1.fastq read2.fastq >  nv_noms


def getPaireEnd():
    affiche_ls = str(subprocess.check_output("ls" ,shell=True))
    affiche_ls=affiche_ls.split("\\n")
    
  
    groupe_paire=[[]]
    for i in range(len(affiche_ls)-1):
        read1=affiche_ls[i].split(".")
        read2= affiche_ls[i+1].split(".")
        if len(read1)>=2 and  len(read2)>=2 :
            if read1[1]=="fastq" and read2[1]=="fastq":
                if read1[0]!=read2[0] and read1[0][:-1] ==read2[0][:-1]  and read1[0][-2]=='_':
                     
                    groupe_paire.append([read1[0],read2[0]])

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
        if len(reads)>=2:
            if reads[1]=="fastq":
                if(checkSingleEnd(reads[0]) ==0):
                    singleRead.append(reads[0])
    return singleRead



                
 


def pipeline():
    readPairEnd=getPaireEnd()
    readSinglEnd=getSingleEnd()
    compteur=0
    for i in readPairEnd:
        if i!=[]:
            compteur+=2
            print(i," :",compteur)
            for j in i :
                print(" read ",j )
    
    for k in readSinglEnd:
        compteur+=1
        print(k,":", compteur)


pipeline()