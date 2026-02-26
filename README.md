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


Insallation
# Cloner le projet
git clone [https://github.com/votre-compte/ecf_telecom_churn.git](https://github.com/votre-compte/ecf_telecom_churn.git)
cd ecf_telecom_churn

# Créer l'environnement virtuel
python -m venv venv

# Activer l'environnement
# Sur Windows :
.\venv\Scripts\activate
# Sur Mac/Linux :
source venv/bin/activate

# Installer les dépendances
pip install --upgrade pip
pip install -r requirements.txt