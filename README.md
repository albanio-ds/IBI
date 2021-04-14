
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

* Remplacer les champs marqués avec '<b>a changer </b>' c'est à dire :

Dans le <b>downloadReads.py</b> : 
* le fichier TSV. (fichier obligatoire)

Dans le <b>mappingAndMore.py</b> : 

* le fichier TSV (fichier obligatoire)
* le fichier contenant le genome de référence (fichier obligatoire)
*  'java -jar le chemin vers le jar gatk-package-4.1.9.0-local.jar' (obligatoires)
*  liste des positions de chromosomes (fichier obligatoire)
*  exception : 2 fichiers R arbre.R et filtration.R contenant des valeurs brutes (obligatoire pour avoir les mêmes figures que nous)

# Concernant downloadReads.py
 ```sh
python3 downloadReads.py
```  
En fonction de votre connexion, le téléchargement sera plus ou moins long.
* Fichier nécessaire :
	- `tsv`
* Vous pouvez annuler le téléchargement à tout moment en faisant ctrl+c, 2 fois.
* Les fonctions sont directement commentées

# Concernant mappingAndMore.py

 ```sh
python3 mappingAndMore.py
```  
Ce script nécessite une dizaine d'heures pour s'exécuter.

* Fichiers nécessaires : 
    - `tsv`
   - `fichier contenant le génome de référence (généralement .fsa, .fasta)`
   -  `les .fastq (que vous avez obtenu en lançant downloadReads.py) `
    - `liste intervalle genomique `
    - `2 fichiers R :   `
    - ` un qui va servir pour visualiser les données à filtrer (QD,FS..) `
	-  `un qui servira à faire notre arbre PCA` 

* Tous ces fichiers doivent être dans le même répertoire (voir le répertoire <b>ready</b>)
 
* Les fonctions sont directement commentées

# Difficultés rencontrées

* mappingAndMore.py demande énormément de temps et pas mal de ressources, concernant notre groupe on ne pouvait pas se permettre de lancer un tel script en semaine
* aucun souci concernant le code python

# Ce qu'on aurait aimé améliorer

* Ajouter une interface interactive pour que le pipeline soit plus user-friendly.

# Remarque : 

* Pour avoir nos résultats vous pouvez lancer les commandes présentées au-dessus dans le répertoire <b>ready</b> directement.
