# Stratégie de Rétention Client (Churn) - TeleCom+

## Description du Projet
Ce projet vise à prédire le **Churn** (résiliation) des clients de l'opérateur TeleCom+. L'enjeu est double : 
1. **Technique** : Traiter et explorer les données via un environnement Big Data (**Spark**).
2. **Métier** : Développer un modèle prédictif (**Scikit-Learn**) capable d'identifier les clients à risque pour déclencher des actions de rétention ciblées et maximiser le ROI.

---

## Stack Technique
- **Traitement Big Data :** **PySpark** (Spark SQL, Spark MLlib)
- **Machine Learning :** **Scikit-Learn** (Logistic Regression, Random Forest, GBT)
- **Analyse de données :** **Pandas**, **Numpy**
- **Visualisation :** **Matplotlib**, **Seaborn**
- **Format de données :** CSV / Pandas DataFrames / Spark DataFrames

---

## Structure du Projet et installation 
```text
ECF_3_Clement_Raczek/
├── README.md                        
├── data/                              
│   └── 03_DONNEES.csv                 
├── notebooks/                        
│   ├── sickit-learn.ipynb             
│   ├── spark.ipynb                     
│   ├── 03_modelisation_sklearn.ipynb  
│   ├── 04_comparaison_frameworks.ipynb 
│   └── 05_recommandations_metier.ipynb 
├── output/                          
│   ├── scikit-learn/                  
│   ├── figures/                      
│   └── predictions_test.csv          
└── requirements.txt                 
--- 


## Installation et Configuration de l'Environnement

### 1. Récupération du projet
# Clonage du dépôt distant vers la machine locale
git clone https://github.com/clementraczek/ECF3-CLEMENT-RACZEK.git

# Déplacement dans le répertoire racine du projet
# Note : veillez à ce que le nom du dossier corresponde au dépôt cloné
cd ECF3-CLEMENT-RACZEK

### 2. Gestion de l'environnement virtuel
# Création d'un environnement isolé pour éviter les conflits de dépendances
python -m venv venv

# Activation de l'environnement virtuel
# Procédure pour Windows (PowerShell / CMD) :
.\venv\Scripts\activate

# Procédure pour systèmes Unix (Linux / macOS) :
# source venv/bin/activate

### 3. Installation des dépendances
# Mise à jour du gestionnaire de paquets pip pour garantir la compatibilité
pip install --upgrade pip

# Installation groupée des bibliothèques nécessaires (Pandas, Scikit-Learn, PySpark, etc.)
pip install -r requirements.txt