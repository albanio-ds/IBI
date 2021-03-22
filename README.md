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

# Information concernant les scripts (prérequis)
* Le fichier TSV nécessaire au téléchargement et le fichier contenant le génome de référence doivent être dans le même dossier 

* Remplacer les champs marqué avec '<b>a changer </b>' c'est à dire :

Dans le <b>downloadReads.py</b> : l
* le fichier TSV.

Dans le <b>mappingAndMore.py</b> : 

* le fichier TSV 
* le fichier contenant le genome de référence 
*  'java -jar le chemin vers le jar gatk-package-4.1.9.0-local.jar'

#Concernant downloadReads.py


#Concernant  mappingAndMore.py


# Utilisation des  scripts:

* Lancer le téléchargement des échantillons :
`python3 downloadReads.py`

* Lancer le mapping et le marquage  des reads
`python3 mappingAndMore.py`

# Organisation du code

Le dossier script/ contient les scripts python à lancer dans l'ordre suivant : 
	*  downloadReads.py
	*  mappingAndMore.py


# Difficultés rencontré

* Installation de GATK
* aucun soucci concernant le code python

