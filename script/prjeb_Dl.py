
#!/usr/bin/env python3

import os
import subprocess
 

fichierTsv ="filereport_read_run_PRJEB24932_tsv.txt"  # à changer

#fastq_ftp finder
def finder_ftp(fichierTsv):
    ''' 
    paramètre: fichier tsv contenant les liens des échantillons à
    télécharger

    sortie: renvoye le numéro de la colonne contenant le champs
    'fastq_ftp'. (entier)
    En cas d'erreur une exception est levée.

    remarque: 'fastq_ftp' est une colonne requise.

    '''
    f=open(fichierTsv)
    tsv_toListe = [ i.strip().split('\t') for i in f]
    finder=False
    i=0
    for row in tsv_toListe:
        if not finder:
            while not finder and  i<len(row):
                if row[i]=="fastq_ftp":
                    finder=True
                   # print("trouvé", i )
                    return i
                else:
                    i+=1
        else:
            None
        if not finder:
            raise Exception("pas de champs fast_ftp")
    return i

#fastq_md5 finder
def finders_md5(fichierTsv):
      ''' 
    paramètre: fichier tsv contenant les liens des échantillons à
    télécharger

    sortie: renvoye le numéro de la colonne contenant le champs
    'fastq_md5'. (entier)
    En cas d'erreur une exception est levée.

    remarque: 'fastq_md5' est une colonne requise.

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







def finders_alias(fichierTsv):
      ''' 
    paramètre: fichier tsv contenant les liens des échantillons à
    télécharger

    sortie: renvoye le numéro de la colonne contenant 
    le champs'sample_alias'. (entier)

    En cas d'erreur une exception est levée.

    remarque: 'sample_alias' est une colonne requise.

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
                   # print("trouvé", i )
                    return i
                else:
                    i+=1
        else:
            None
        if not finder:
            raise Exception("pas de champs sample_alias")
    return i

def count_correct(fichierTsv):
       ''' 
    paramètre: fichier tsv contenant les liens des échantillons à
    télécharger

    sortie: renvoye le nombre de lien à télécharger (entier)

   

    '''

    r= open(fichierTsv)
    tsv_toListe = [ i.strip().split('\t') for i in r]
    compteur=0
    md5_f=finders_md5(fichierTsv)
    for i in tsv_toListe:
        if len(i[md5_f])>=32 and (len(i[md5_f].split(";"))>=2 ): #deux liens 
            compteur+=2
        else:
            if len(i[md5_f])>=32: # un lien
                compteur+=1


    return compteur




def telecharge(lien,md5_value):
    """
    Cette fonction s'occupe du téléchargement des fichiers et garantie leurs origine à l'aide 
    des vérifications md5.

    paramètre:  liengz , md5 associé au lien

    sortie: télécharge le lien gz demandé et verifie le md5   

    Fonctionnalité: 
        -Si l'utilisateur décide d'arrêter le téléchargement par exemple si ça connexion est insuffisante
        alors il peut faire ctrl+c 2 fois et seul le liens en cours de téléchargement est supprimé.





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
        if tentative ==2 :
            delete =  lien_targz[-1]+"*"
            os.system("rm "+  delete )
            print("\n OK tout les fichiers téléchargés sont effacé ! ")
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


Fonctionnalité: 
On a pensé au confort utilisateur et lui permettre de télécharger les échantillons quand il le souhaite de plus 
en cas de mauvaise connexion, ce  script est très pratique en effet un compteur et une vérification permet 
d'assurer qu'on ne télécharge pas le même fichier en cas de relance de script.

Biblio:
*os pour faire mes appels sys comme wget ou rm.
*subprocess pour recupérer certains resultat d'appels sys , comme md5sum ou encore ls



    """
    f=open(s)
    tsv_toListe = [ i.strip().split('\t') for i in f]
    compteur=0
    total = count_correct(s)
    ftp_f= finder_ftp(s)
    md5_f=finders_md5(s)
    alias_f =finders_alias(s)
    #autre
    for i in tsv_toListe:
        estDl=False
        tentative=0
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






pipeline_one(fichierTsv)
