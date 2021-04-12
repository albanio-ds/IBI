#!/usr/bin/env python3

import os
import subprocess
from statistics import mean


'''
Prérequis
modifier les variables ci-dessous marqué à coté "a changer" avec les noms de fichiers respectifs

genome_de_reference : par le fichiers contenant le genome de référence (.fasta ou .fsa)
path_gatk_java : par le nom du chemin vers le jar local gatk
fichierTsv : par le fichier tsv qui contient les informations liés au lien ftp,md5 et sample_alias
             (que vous avez utilisé dans l'etape précédente)

'''


genome_de_reference_fsa ="S288C_reference_sequence_R64-2-1_20150113.fasta" # a changer
path_gatk_java ="java -jar /home/jeyanthan/Documents/coursL3/S6/IBI/Gatk/gatk-4.1.9.0/gatk-package-4.1.9.0-local.jar" # a changer
fichierTsv = "filereport_read_run_PRJEB24932_tsv.txt" # a changer

 
def getPaireEnd():
    '''
    Cette fonction verifie si deux fichiers appartiennent à un
    même échantillons et permet de récupérer les paire end du
    répertoire courant.

    @paramètre: N/A

    @sortie: (liste) contenant les pairs end

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
    Cette fonction permet de vérifier si un read est bien
    un single end
    @paramètre: (string) un read

    @sortie: (entier) valant 0 si c'est un single end sinon il s'agit d'un paire
    end

    '''
    p=0
    double=getPaireEnd()
    for i in double:
        for j in i:
            if myRead ==j :
                p+=1
    return p

 def getSingleEnd():
    '''
    cette fonction permet de récupérer l'ensemble des single end dans le répertoire courant.

    @paramètre: N/A

    @sortie: (liste) contenant les singles end

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


 

def genReferenceIndexed(s):
    '''
    cette fonction va vérifier si le
    génôme de réference est bien indéxé.

    @paramètre: (string) le nom du fichier contenant le genome de référence

    @sortie: (Boolean) true si il est bien indéxé.

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
    Cette fonction va indéxé le genome de référence et générer les
    autre fichiers que l'on doit générer avec le genome de référence
    ,ces fichiers serviront à l'étape 3.

    @paramètre:  (string) le nom du fichier contenant le genome de référence

    @sortie: N/A

    '''
    os.system("bwa "+"index " + s)
    os.system("samtools " + "faidx " + s) # utile à etape 3
    gatk_cmd_bis = " CreateSequenceDictionary -R "+ s  #gatk besoin dans etape 3
    os.system(path_gatk_java + gatk_cmd_bis)
    if genReferenceIndexed(s):
        return
    else:
        raise Exception("verifiez si il s'agit bien du génome de référence !")



def newGenomeDeReference(s):
    '''
    Cette fonction va renommer le fichier contenant
    le genome de référence en .fasta .
    A l'etape 3 , on a besoin que notre fichier contenant
    le genome de référence. se termine avec .fasta

    @parametre: (string) nom du fichier contenant le genome de référence

    @sortie: (string) le nouveau nom se terminant par .fasta

    '''

    newName = s.strip().split('.')[0] + ".fasta"

    if checkNewFile(newName):
        return newName
    else:
        os.system("mv " + s + " " + newName)
        return newName



 

def finder_ftp(fichierTsv):
    '''
    Retourne la colonne contenant les informations liés à
    la colonne fast_ftp

    @parametre: (string) fichier tsv

    @sortie: (entier)

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
    Retourne la colonne contenant les informations liés à
    la colonne sample_alias

    @parametre: (string) fichier tsv

    @sortie: (entier)

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
    Retourne le sample_alias d'un d'un read

    @parametre: (string,string) fichier tsv, nom du read

    @sortie: (string)

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
        if lienfinale ==correctName:
            sample_name= i[sample_column]
            return sample_name

    if sample_name =="":
        raise Exception("Sample name introuvable")


def strainFinder(monGdeRef):
    '''
    retourne le strain de notre genome de référence

    @parametre: (string) nom du fichier contenant le genome de référence

    @sortie: (string) strain


    '''
    f= open(monGdeRef)
    fsaToList =[i.strip().split('[') for i in f]
    firstLigne =fsaToList[0]
    strainRet=""
    for i in firstLigne :
        if "strain=" in i :
            strainRet = i.split("=")[1][:-2].strip()
            return strainRet

    if strainRet=="":
        raise Exception("No strain found")


def checkNewFile(f):
    '''
    verifie si un fichier est présent dans le répertoire courant.

    @parametre: (string) nom de fichier

    @sortie: (boolean)

    '''
    affiche_ls = str(subprocess.check_output("ls" ,shell=True))
    if(f in affiche_ls):
        return True

    return False


def mapping_and_variant_identification(FindSampleName,newName_Sam,fichierTsv,genoRef):
    '''
    Cette fonction va effectuer les appels nécessaires pour le mapping
    ainsi que ce nécessaire avant l'obtention de fichier .gvcf et .vcf

    @parametre: (string,string,string,string) read, fichier sam, fichier tsv, genome de réference


    @sortie: N/A


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
    gatk_haplot=False
    if checkNewFile(newName_Bam):
        print(newName_Bam, " is already there! ")
        samtool_view=True

    if not checkNewFile(newName_Bam):
        #samtools view -o aln.bam aln.sam.gz
        os.system("samtools " + "view " + "-o " + newName_Bam + " " + newName_Sam  )
        if checkNewFile(newName_Bam):
            samtool_view=True
    if samtool_view :
        #on passe à samtools sort
        if checkNewFile(newName_BamSort):
            print(newName_BamSort, " is already there! ")
            samtool_sort=True
        else:
            os.system("samtools " + "sort " + "-o " + newName_BamSort + " " + newName_Bam  )
            if checkNewFile(newName_BamSort):
                samtool_sort=True
    if samtool_sort:
        #on passe a GATK

        if checkNewFile(newName_BamDupl):
            print(newName_BamDupl, " is already there! ")
            gatk_markDupl=True
        else:

            gatk_cmd_bis=" MarkDuplicatesSpark " + "-I " + newName_BamSort + " " +"-O " + newName_BamDupl
            os.system(path_gatk_java + gatk_cmd_bis)
            if checkNewFile(newName_BamDupl):
                gatk_markDupl=True

    if gatk_markDupl:
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
            if checkNewFile(newName_BamCouv):
                bedtools_couv=True
    if bedtools_couv:
        if checkNewFile(newName_Gvcf_Haplot):
            print(newName_Gvcf_Haplot, " is already there! ")
            gatk_haplot=True
        else:
            gatk_cmd_bis2 = " HaplotypeCaller " + " -R " +  genoRef  + " -I " +  newName_BamDupl +   " -O " + newName_Gvcf_Haplot + " -ERC GVCF"
            os.system(path_gatk_java + gatk_cmd_bis2)
            if checkNewFile(newName_Gvcf_Haplot):
                gatk_haplot=True

    return


def  mappingCalcul():
    '''
    Cette fonction Calcule le pourcentage de reads mappent le génome de référence
    à partie du fichier généré par samtools flagstat

    @parametre: (N/A)


    @sortie: (N/A)

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



def couvertureMapp():
    '''
    Cette fonction va calculez la couverture moyenne à partir du fichier généré  par
    bedtools genomcov

    @parametre: (N/A)

    @sortie: (N/A)


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
    print("la moyenne =", lamoyenneToTal  ," le min = ", leMin , " le max = ", leMax )




def mappingPaired(fichierTsv,genoRef,f1,f2):
    '''
    fonction effectuant le mapping pour les paires end
    en obtenant le premier fichier .sam.
    Si cette étape est fonctionnelle on continue le mapping
    avec l'appel  à lafonction mapping_and_variant_identification

    @parametre:(string,string,string,string)

    @sortie:(N/A)

    '''
    sampleName= finderSampleName(fichierTsv,f1)
    newName_Sam= sampleName + ".sam"
    strainName = strainFinder(genoRef)
    rg_id = strainName+"-"+sampleName
    rg_sm = sampleName
    rg_flag = repr("@RG\tID:"+ rg_id +"\tSM:" + rg_sm + "\tPL:Illumina\tPU:0\tLB:1")
    bwa_map =False
    samtool_map=False
    if checkNewFile(newName_Sam) :

        print(newName_Sam, " is already there! ")
        bwa_map = True
    if not checkNewFile(newName_Sam) :
        os.system("bwa "+ "mem " +"-R " + rg_flag+ " " +genoRef +" " +  f1 + " " + f2 + " >" + newName_Sam)
        if checkNewFile(newName_Sam) :
            print("new file : ", newName_Sam)
            bwa_map = True

    if bwa_map :
        mapping_and_variant_identification(f1,newName_Sam,fichierTsv,genoRef)




def mappingSingle(fichierTsv,genoRef,f):
    '''
    fonction effectuant le mapping pour les single end
    en obtenant le premier fichier .sam.
    Si cette étape est fonctionnelle on continue le mapping
    avec l'appel  à lafonction mapping_and_variant_identification

    @parametre:(string,string,string,string)

    @sortie:(N/A)


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
        os.system("bwa "+ "mem " +"-R " + rg_flag+ " " +genoRef +" " +  f + " >" + newName_Sam)
        if checkNewFile(newName_Sam):
            print("new file : ", newName_Sam)
            bwa_map=True
    if bwa_map :
        mapping_and_variant_identification(f,newName_Sam,fichierTsv,genoRef)

def finders_md5(fichierTsv):
    '''
    Retourne la colonne contenant les informations liés à
    la colonne fastq_md5

    @parametre: (string) fichier tsv

    @sortie: (entier)

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
    Fonction renvoyant le nombre d'échantillon total
    dans notre fichier tsv

    @parametre: (string) fichier tsv

    @sortie: (entier)

    '''

    r= open(fichierTsv)
    tsv_toListe = [ i.strip().split('\t') for i in r]
    compteur=0
    md5_f=finders_md5(fichierTsv)
    for i in tsv_toListe:
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
    -V fichier1.g.vcf -V fichier2.g.vcf ..
    Elle nous servira notamment dans l'appel de la
    fonction GenomicsDBImport nécessaire à la consolidation

    @paramètre: (N/A)

    @sortie: (string) concaténation de -V fichier .g.vcf

    '''
    affiche_ls = str(subprocess.check_output("ls" ,shell=True))
    affiche_ls=affiche_ls.strip().split("\\n")
    sequenceGvcf=""
    for i in affiche_ls:
        if ".g.vcf.idx" in i: #on skip les .g.vcf.idx
            None
        else:
            if ".g.vcf" in i:
                sequenceGvcf += " -V " + i
    return sequenceGvcf


def gatkGenomic():
    '''
    Cette fonction effectue l'appel necessaire pour la consolidation, on l'appel
    un fois qu'on a tous les .g.vcf pour chaque echantillons

    @parametre: (N/A)

    @sortie:(N/A)

    '''
    affiche_ls = str(subprocess.check_output("ls" ,shell=True))
    #affiche_ls=affiche_ls.strip().split("\\n")
    if "my_database" in affiche_ls:
        print("Consolidation effectué !")
        return True
    else:
        allgvcf = find_all_gvcf()
        os.system(path_gatk_java +  " GenomicsDBImport " + allgvcf + " --genomicsdb-workspace-path  my_database/ " + " -L " + " intervals.list" )
        if "my_database" in affiche_ls:
            print("Consolidation effectué !")
            return True
        else:
            print("Consolidation non effectué! ")
            return False

def gatkGenotype(genoRef):
    '''
    Cette fonction va effectuer l'appel joint donc
    d'obtenir notre première table vcf.
    @parametre: (string) genome de référence

    @sortie: (N/A)

    '''
    affiche_ls = str(subprocess.check_output("ls" ,shell=True))
    if "sortieFinale.vcf" in affiche_ls:
        print("Appel joint effectué! ")
        return True
    else:
        os.system(path_gatk_java + " GenotypeGVCFs" + " -R " + genoRef + " -V " + "gendb://my_database " + " -O " + " sortieFinale.vcf" )
        if "sortieFinale.vcf" in affiche_ls:
            print("Appel joint effectué! ")
            return True
        else:
            print("Appel joint non effectué! ")
            return False


def mean(lst):
    return sum(lst) / len(lst)

def filterValue():
    '''
    on effectue une moyenne sur chaque valeur de filtre
    et on renvoye le resultat dans le fichier filtreValeur.txt

    '''
    tab=os.popen('bcftools query -f "%QD %MQ %MQRankSum %FS %SOR %ReadPosRankSum\n" sortieFinale.vcf').readlines()

    for i in range(len(tab)):
        tab[i] = tab[i].replace('\n', '')

    qd = []
    mq = []
    mqrs = []
    fs = []
    sor = []
    rprs = []

    for e in tab:
        splited = e.split(' ')

        if splited[0] != '.':
            qd.append(float(splited[0]))

        if splited[1] != '.':
            mq.append(float(splited[1]))

        if splited[2] != '.':
            mqrs.append(float(splited[2]))

        if splited[3] != '.':
            fs.append(float(splited[3]))

        if splited[4] != '.':
            sor.append(float(splited[4]))

        if splited[5] != '.':
            rprs.append(float(splited[5]))


    contenu =  "La moyenne des QD est : " + str(mean(qd)) + ' \n'
    contenu += "La moyenne des MQ est : " + str(mean(mq)) + ' \n'
    contenu += "La moyenne des MQRankSum est : " + str(mean(mqrs))  + ' \n'
    contenu += "La moyenne des FS est : " + str(mean(fs))  + ' \n'
    contenu += "La moyenne des SOR est : " + str(mean(sor)) + ' \n'
    contenu += "La moyenne des ReadPosRankSum est : " + str(mean(rprs))  + ' \n'
    f = open("filtreValeur.txt", "w")
    f.write(contenu)
    f.close()


def gatkVariant_and_filter_Finding(genoRef):
    filterIsDone= False
    vcfObtain = False
    variantSelect =False
    vcfForR = False

    if(checkNewFile("sortieFinale.vcf")):
            vcfObtain = True
    if vcfObtain :
        if checkNewFile("variantSelected.vcf"):
            print("Variant selection done ! ")
            variantSelect = True
        else :
            os.system(path_gatk_java + " SelectVariants " + " -R " + genoRef + " -V "+ "sortieFinale.vcf " + " --select-type-to-include SNP " + " -O " + "variantSelected.vcf"  )
            if checkNewFile("variantSelected.vcf"):
                variantSelect = True
    if variantSelect :
        if checkNewFile("filtreValeur.txt"):
            print("filtre trouvé ! ")
            filterIsDone = True
        else:
            filterValue()
        #script pour trouver les filtres
            if checkNewFile("filtreValeur.txt") :
                filterIsDone=True
    if filterIsDone :
        if checkNewFile("forFiltration.vcf"):
            print(" vcf for R ready ! ")
            vcfForR=True
        else:

            headerVcf= "%CHROM %POS %REF %ALT %QD %FS %MQ %MQRankSum %ReadPosRankSum %SOR %DP\n"
            os.system("bcftools query"  + " -f " + " '" +  headerVcf  + "' " + " variantSelected.vcf " + " > forFiltration.vcf")
            os.system ("sed -i "  +  " '" +  "1iCHROM POS REF   ALT    QD     FS    MQ MQRankSum ReadPosRankSum SOR    DP" +  "'"  +  " forFiltration.vcf")

                #on pourra lancer le script R
            if checkNewFile("forFiltration.vcf"):
                vcfForR=True
    if vcfForR :
        #lancer le script R
        os.system("Rscript " + " filtration.R")
        return True
    else:
        print("Selection variant et filtre non trouvé !!!")
        return False



def applyFiltration(genoRef):
    if checkNewFile("filtrationIsDone.vcf"):
        print("La filtration a été effectué ! ")
        return True
    else:
        os.system(path_gatk_java + " VariantFiltration -R " + genoRef + " -V variantSelected.vcf" + " -O filtrationIsDone.vcf " + " --filter-expression  " +  "'"  + "QD > 19.9 || FS > 1.0 || SOR > 0.1   || MQ > 60.0 || MQRankSum > 1.0 || ReadPosRankSum > 0.12945328565870648"    +"'" +  " --filter-name" + " '" + "monFiltre" + "'")
        if checkNewFile("filtrationIsDone.vcf"):
            print("La filtration a été effectué ! ")
            return True
        else:
            print("Filtration RATE !!!")
            return False




def afficheArbrePcA():
    if checkNewFile("filtrationIsDone.vcf"):
        os.system("Rscript " + "arbre.R")



def pipeline(fichierTsv, monGdeRef):
    '''
    fonction qui fait tout les appels pour effectuer  l'indexation
    de genome de reference ,le mapping et
    l'identification des variants
    '''
    readPairEnd=getPaireEnd()
    readSinglEnd=getSingleEnd()
    compteur=0
    doneOrNotMapping= False
  
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

 
    if doneOrNotMapping and  gatkGenomic() and  gatkGenotype(monGdeRef) and  gatkVariant_and_filter_Finding(monGdeRef)   and applyFiltration(monGdeRef):
        afficheArbrePcA()
        return




##############
genome_de_reference_fasta = newGenomeDeReference(genome_de_reference_fsa)
pipeline(fichierTsv,genome_de_reference_fasta)

#mappingCalcul()
#couvertureMapp()
#################









  