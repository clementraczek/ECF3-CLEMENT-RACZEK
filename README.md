# 📊 Stratégie de Rétention Client (Churn) - TeleCom+

## 📝 Description du Projet
Ce projet vise à prédire le **Churn** (résiliation) des clients de l'opérateur TeleCom+. L'enjeu est double : 
1. **Technique** : Traiter et explorer les données via un environnement Big Data (**Spark**).
2. **Métier** : Développer un modèle prédictif (**Scikit-Learn**) capable d'identifier les clients à risque pour déclencher des actions de rétention ciblées et maximiser le ROI.

---

## 🛠 Stack Technique
- **Traitement Big Data :** **PySpark 4.1.1** (Spark SQL, Spark MLlib)
- **Machine Learning :** **Scikit-Learn** (Logistic Regression, Random Forest, GBT)
- **Analyse de données :** **Pandas**, **Numpy**
- **Visualisation :** **Matplotlib**, **Seaborn**
- **Conteneurisation :** **Docker** & **Docker Compose**

---

## 📂 Structure du Projet
```text
ECF_3_Clement_Raczek/
├── data/                               
│   └── 03_DONNEES.csv                  # Dataset source (7043 clients)
├── notebooks/                          
│   ├── scikit-learn.ipynb              # Analyse et modèle Sklearn
│   ├── spark.ipynb                     # Exploration Spark (Format Notebook)
│   └── spark.py                        # Script Spark optimisé pour Docker
├── output/                             
│   ├── scikit-learn/                   # Exports des modèles et prédictions
│   └── spark/                          # Résultats de l'analyse Big Data (CSV/PNG)
├── Dockerfile                          # Configuration de l'image (Python + Java 17)
├── docker-compose.yml                  # Orchestration et montage des volumes
└── requirements.txt                    # Dépendances Python     
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

### 4. Utilisation via Docker (Recommandé pour Spark)

Si vous préférez ne pas installer Java et Spark localement, vous pouvez utiliser Docker. Cette méthode garantit un environnement identique à celui du développement.



#### A. Lancement complet (Build + Up)
Cette commande télécharge les images de base, installe les dépendances (Java 17, PySpark 4.1.1) et lance le script d'analyse.
```powershell
docker-compose up --build

B. Exécution en arrière-plan (Mode détaché)
Si vous souhaitez libérer votre terminal pendant l'exécution :

PowerShell
docker-compose up -d

C. Arrêt et nettoyage des conteneurs
Pour arrêter le service et supprimer les conteneurs créés :

PowerShell
docker-compose down