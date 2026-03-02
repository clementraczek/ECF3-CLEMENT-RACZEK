#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, round, count, lit, when
import pyspark.sql.types as T

from pyspark.ml import Pipeline
from pyspark.ml.feature import StringIndexer, VectorAssembler, StandardScaler, SQLTransformer
from pyspark.ml.classification import LogisticRegression, RandomForestClassifier
from pyspark.ml.evaluation import MulticlassClassificationEvaluator

# Configuration Matplotlib pour Docker (évite les erreurs d'interface graphique)
plt.switch_backend('Agg')

# ============================================================
# 1. INITIALISATION ET CONFIGURATION DES CHEMINS
# ============================================================

# Chemins relatifs au dossier /app du conteneur
DATA_PATH = 'data/03_DONNEES.csv'
OUTPUT_DIR = 'output/spark'

# Création du dossier de sortie si inexistant
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)
    print(f"[*] Dossier créé : {OUTPUT_DIR}")

# Initialisation de la session Spark
print("[*] Démarrage de la session Spark...")
spark = SparkSession.builder \
    .appName("TelecomChurnSpark") \
    .master("local[*]") \
    .getOrCreate()

# ============================================================
# 2. CHARGEMENT ET NETTOYAGE
# ============================================================

if not os.path.exists(DATA_PATH):
    print(f"[!] ERREUR : Le fichier {DATA_PATH} est introuvable.")
    spark.stop()
    exit(1)

print(f"[*] Chargement des données depuis {DATA_PATH}...")
spark_df = spark.read.csv(DATA_PATH, header=True, inferSchema=True)

# Transtypage et nettoyage
spark_df = spark_df.withColumn("TotalCharges", col("TotalCharges").cast(T.DoubleType()))
spark_df = spark_df.dropna(subset=["TotalCharges"])

print("\n--- Aperçu du Schéma ---")
spark_df.printSchema()

# ============================================================
# 3. PIPELINE DE PRÉTRAITEMENT (SPARK ML)
# ============================================================

print("[*] Construction du pipeline de transformation...")

# Feature Engineering : Ratio de facturation
sql_transformer = SQLTransformer(
    statement="""
        SELECT *, 
            (TotalCharges / CASE WHEN tenure = 0 THEN 1 ELSE tenure END) AS charge_per_month_ratio
        FROM __THIS__
    """
)

categorical_cols = [
    'gender', 'Partner', 'Dependents', 'PhoneService', 'MultipleLines', 
    'InternetService', 'OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 
    'TechSupport', 'StreamingTV', 'StreamingMovies', 'Contract'
]
numerical_cols = ['SeniorCitizen', 'tenure', 'MonthlyCharges', 'TotalCharges', 'charge_per_month_ratio']

# CORRECTION SPARK 4.x : Utilisation de inputCol, outputCol et handleInvalid
indexers = [
    StringIndexer(inputCol=c, outputCol=f"{c}_idx", handleInvalid="keep") 
    for c in categorical_cols
]

label_indexer = StringIndexer(inputCol="Churn", outputCol="label")

# Assemblage et Mise à l'échelle
assembler = VectorAssembler(
    inputCols=numerical_cols + [f"{c}_idx" for c in categorical_cols],
    outputCol="features_raw"
)
scaler = StandardScaler(inputCol="features_raw", outputCol="features", withMean=True, withStd=True)

# Exécution du pipeline
pipeline = Pipeline(stages=[sql_transformer] + indexers + [label_indexer, assembler, scaler])
pipeline_model = pipeline.fit(spark_df)
spark_prepared_df = pipeline_model.transform(spark_df)

# ============================================================
# 4. MODÉLISATION ET ÉVALUATION
# ============================================================

# Gestion du déséquilibre (Pondération)
dataset_size = spark_prepared_df.count()
churn_count = spark_prepared_df.filter(col("label") == 1.0).count()
ratio = (dataset_size - churn_count) / churn_count

spark_weighted_df = spark_prepared_df.withColumn(
    "weight", 
    when(col("label") == 1.0, ratio).otherwise(1.0)
)

# Split Train/Test
train_data, test_data = spark_weighted_df.randomSplit([0.7, 0.3], seed=42)

# Entraînement
print("[*] Entraînement des modèles (Logistic Regression & Random Forest)...")
lr = LogisticRegression(featuresCol="features", labelCol="label", weightCol="weight", maxIter=10)
rf = RandomForestClassifier(featuresCol="features", labelCol="label", numTrees=50, seed=42)

lr_model = lr.fit(train_data)
rf_model = rf.fit(train_data)

# Prédictions
lr_preds = lr_model.transform(test_data)
rf_preds = rf_model.transform(test_data)

# Évaluation des métriques
evaluator_f1 = MulticlassClassificationEvaluator(labelCol="label", metricName="f1")
score_lr_spark = evaluator_f1.evaluate(lr_preds)
score_rf_spark = evaluator_f1.evaluate(rf_preds)

print(f"\n[RESULT] F1-Score Logistic Regression (Spark): {score_lr_spark:.4f}")
print(f"[RESULT] F1-Score Random Forest (Spark): {score_rf_spark:.4f}")

# ============================================================
# 5. EXPORT DES RÉSULTATS ET GRAPHIQUES
# ============================================================

print(f"[*] Exportation des résultats vers {OUTPUT_DIR}...")

# Données de comparaison (Valeurs Sklearn fixées pour l'exemple)
score_lr_sklearn = 0.35  
score_rf_sklearn = 0.18  

df_comp = pd.DataFrame({
    "Framework": ["Scikit-learn", "Spark MLlib", "Scikit-learn", "Spark MLlib"],
    "Modèle": ["Logistic Regression", "Logistic Regression", "Random Forest", "Random Forest"],
    "F1-Score": [score_lr_sklearn, score_lr_spark, score_rf_sklearn, score_rf_spark]
})

# Export 1 : Fichier CSV
df_comp.to_csv(os.path.join(OUTPUT_DIR, "metrics_comparison.csv"), index=False)

# Export 2 : Graphique PNG
plt.figure(figsize=(10, 6))
sns.barplot(x="Modèle", y="F1-Score", hue="Framework", data=df_comp, palette="viridis")
plt.title("Comparaison des Performances : F1-Score")
plt.ylabel("F1-Score (Équilibre Précision/Rappel)")
plt.ylim(0, 1.0)
plt.savefig(os.path.join(OUTPUT_DIR, "performance_comparison.png"))

# Clôture
spark.stop()
print("\n[SUCCESS] Analyse terminée. Consultez le dossier 'output/spark'.")