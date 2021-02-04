
#!/usr/bin/env python3

import os
import subprocess
import csv


def finder_ftp():
    tsv_file = open("filereport_read_run_PRJEB24932_tsv.txt")
    read_tsv = csv.reader(tsv_file, delimiter="\t")
    finder=False
    i=0
    for row in read_tsv:
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
    tsv_file.close()
    return i

def finders_md5():
    tsv_file = open("filereport_read_run_PRJEB24932_tsv.txt")
    read_tsv = csv.reader(tsv_file, delimiter="\t")
    finder=False
    i=0
    for row in read_tsv:
        if not finder:
            while not finder and i<len(row):
                if row[i] == "fastq_md5":
                    finder = True
                    return i
                else:
                    i+=1
        else:
            None
           # print(i)
           # print(row[i]+"\n")
        if not finder:
            raise Exception('Pas de champ fastq_md5')
    tsv_file.close()
    return



def finders_alias():
    tsv_file = open("filereport_read_run_PRJEB24932_tsv.txt")
    read_tsv = csv.reader(tsv_file, delimiter="\t")
    finder=False
    i=0
    for row in read_tsv:
        if not finder:
            while not finder and i<len(row):
                if row[i] == "sample_alias":
                    finder = True
                    return i
                else:
                    i+=1
        else:
            None
          
        if not finder:
            raise Exception('Pas de champ sample_alias')
    tsv_file.close()
    return

def count_correct(s):
    r= open(s)
    tsv_toListe = [ i.strip().split('\t') for i in r]
    compteur=0
    md5_f=finders_md5()
    for i in tsv_toListe:
       # if len(i)>6:  #première liste= premiere ligne , nous interèsse pas
        if len(i[md5_f])>=32 and (len(i[md5_f].split(";"))>=2 ):
            compteur+=2
        else:
            if len(i[md5_f])>=32:
                compteur+=1


    return compteur




def telecharge(lien,md5_value):
    """
    Cette fonction s'occupe du téléchargement des fichiers et garantie leurs source à l'aide 
    des vérifications md5.

   

    Fonctionnalité: 
        -Si l'utilisateur décide d'arrêter le téléchargement par exemple si sa connexion est insuffisante
        alors il peut faire ctrl+c 5 fois et il aura le choix entre supprimer tous les fichiers crées ou bien
        simplement le derniers



    """
    
    estDl = False
    tentative=0
    lien_targz = lien.split("/")
    print(lien_targz[-1])
    while(estDl==False):
        tentative+=1   
        full_link ="ftp://"+lien
        os.system("wget "+ full_link )
        recupMd5 = str(subprocess.check_output("md5sum  "+ lien_targz[-1]   ,shell=True)) 
        recupMd5 = recupMd5.split("'")   
        parseMd5_recup = recupMd5[1].split(' ')
        if(md5_value == parseMd5_recup[0]):
            print("TAR :" +  lien_targz[-1] + " téléchargement fini..")
            estDl=True
        if tentative ==5 :
            delete=lien_targz[-1]
            askUser = input("Voulez-vous tous supprimer ? (y/n) ")
            if askUser.lower()=="y":
                delete =  lien_targz[-1]+"*"
                os.system("rm "+  delete )
                print("\n OK tout les fichiers téléchargés sont effacé ! ")
                raise Exception('Téléchargement annulé !')
                return
            if askUser.lower()=="n":
                #delete =  lien_targz[-1]+"*"
                #os.system("rm "+  delete )
                #print("\n OK tout les fichiers téléchargés sont effacé ! ")
                raise Exception('Téléchargement annulé !')
                return
            else:
                os.system("rm "+  delete )
                print("\n OK fichier effacé ! ")
                raise Exception('Téléchargement annulé !')
                return
    
      


def pipeline_one(s):
    """
#########################
PIPELINE POUR PRJEB24932
#########################
Ouvrir prjeb_Dl.py

Donner le nom du fichier "tsv" comme une chaine de caractère ex : pipeline_one("all.txt")

Puis dans le Terminale : python3 prjeb_Dl.py

J'ai convertit le fichier tsv en une liste est je parcours seulements les éléments qui m'interessent à savoir les liens ftp et leurs  md5 !
Biblio:
*os pour faire mes appels sys comme wget ou rm.
*subprocess pour recupérer certains resultat d'appels sys , comme md5sum ou encore ls

Au bout de 5 tentatives de téléchargement  d'un même fichier, le script s'arrête => connexion trop mauvaise ou ctr+c  5 fois !
Pas d'inquiètude les fichiers sont supprimés automatiquements.

    """
    f=open(s)
    tsv_toListe = [ i.strip().split('\t') for i in f]
    compteur=0
    total = count_correct(s)
    ftp_f= finder_ftp()
    md5_f=finders_md5()
    alias_f =finders_alias()
    #autre
    for i in tsv_toListe:
        estDl=False
        tentative=0
       # if len(i)>4:  #première liste= premiere ligne , nous interèsse pas
        if len(i[md5_f])>=32 and (len(i[md5_f].split(";"))>=2 ):  #contient md5 donc contient aussi un lien / 2 liens
            compteur+=1
            estDl=False
            parseMd5=i[md5_f].split(";")  #md5
            md5_lien1=parseMd5[0]
            md5_lien2 =parseMd5[1]
            parseLink=i[ftp_f].split(";") # lien
            lien1=parseLink[0]
            lien2 = parseLink[1]
            lien1Targz = lien1.split("/")
            lien2Targz = lien2.split("/")
              
                #test si le fichier est deja present
            test_presence = str(subprocess.check_output("ls" ,shell=True))
            if lien1Targz[-1] in test_presence : 
                if lien2Targz[-1] in test_presence :
                    if compteur == total :
                        print("ATTENTION LES FICHIERS SONT DEJA PRESENT !!")
                        return
                else: 
                    compteur+=1
                    print("\nTELECHARGE  Lien2 :" + lien2 + " md5 : " + md5_lien2  +"    " +str(compteur) + "/" + str(total) )
                    telecharge(lien2,md5_lien2)

            else:
                    
                print("\nTELECHARGE  Lien1 :" + lien1 + " md5 : " + md5_lien1  +"    " +str(compteur) + "/" + str(total) )
                compteur+=1
                telecharge(lien1,md5_lien1)
                print("\nTELECHARGE  Lien2 :" + lien2 + " md5 : " + md5_lien2  +"    " +str(compteur) + "/" + str(total) )
                telecharge(lien2,md5_lien2)
                


        else:
            if len(i[md5_f])>=32 :
                compteur+=1
                estDl=False
                parseMd5=i[md5_f].split(";")
                md5_real=parseMd5[0]
                parseLink=i[ftp_f].split(";")
                lien=parseLink[0]
                lienTargz = lien.split("/")
                test_presence = str(subprocess.check_output("ls" ,shell=True))
                if lienTargz[-1] in test_presence  :
                    if compteur == total :
                        print("ATTENTION LES FICHIERS SONT DEJA PRESENT !!")
                        return
                else:
                    print("\nTELECHARGE LIEN SEUL  :" + lien + " md5 : " + md5_real  +"    " +str(compteur) + "/" + str(total) )
                    telecharge(lien,md5_real)

            else:
                None






pipeline_one("filereport_read_run_PRJEB24932_tsv.txt")
