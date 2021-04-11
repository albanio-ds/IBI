
# Introduction
Projet intégré de bioinformatique : construction d'un pipeline de préparation de
données génomiques.

# L'équipe des étudiants

* Dealann Srikumar
* De Souza Albanio
* Jeyanthan Markandu

Université Paris-Saclay

Année Universitaire 2021

# Responsable du cours

Fanny POUYET et Marine DJAFFARDJY

Option: Projet intégré de bioinformatique 
# Pré-requis: 

* python3
* samtools
* bwa 
* gatk
* bedtools
* bcftools
* R
# packages R :
* install.packages("BiocManager")
* BiocManager::install("SNPRelate")
* install.packages("ape")
* install.packages("RColorBrewer")
* install.packages("VennDiagram")

# Information concernant les scripts:

* Remplacer les champs marqué avec '<b>a changer </b>' c'est à dire :

Dans le <b>downloadReads.py</b> : 
* le fichier TSV.

Dans le <b>mappingAndMore.py</b> : 

* le fichier TSV 
* le fichier contenant le genome de référence 
*  'java -jar le chemin vers le jar gatk-package-4.1.9.0-local.jar'

# Concernant downloadReads.py
 ```sh
python3 downloadReads.py
```  
En fonction de votre connexion, le téléchargement sera plus où moins long.
* Pour lancer ce script le seul fichier nécessaire est le fichier .tsv
* Vous pouvez annulez le téléchargement à tout moment en faisant ctrl+c, 2 fois.
* Les fonctions sont directement commentées

# Concernant  mappingAndMore.py

 ```sh
python3 mappingAndMore.py
```  
Ce script nécessite  une dizaine d'heure pour s'éxecuter.

* Fichier nécessaire : 
    `-tsv`
    `-fichier contenant le genome de réference (généralement .fsa, .fasta)`
     `-les .fastq (reads) `
     `-liste intervalle genomique `
     `-2 fichiers R :   `
    - ` un qui va servir pour visualiser les données à filtrées (QD,FS..) `
	-  `un qui servira à faire notre arbre PCA` 

* Tous ces fichiers doivent être dans le même répertoire (voir le répertoire <b>exemple</b>)
 
* Les fonctions sont directement commentées



# Difficultés rencontré

* mappingAndMore.py demande énormément de temps et pas mal ressource, concernant notre groupe on ne pouvait pas se permettre de lancer un tel script en semaine
* aucun soucci concernant le code python

# Ce qu'on aurait aimé améliorer

* Ajouter une interface interractive pour que la pipeline soit plus user-friendly.
