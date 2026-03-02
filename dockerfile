# Utilisation de Python 3.11 sur Debian Bookworm (plus récente, inclut Java 17 facilement)
FROM python:3.11-slim-bookworm

# Installation de Java 17 (JRE) et procps
RUN apt-get update && apt-get install -y \
    openjdk-17-jre-headless \
    procps \
    && rm -rf /var/lib/apt/lists/*

# Définition du JAVA_HOME pour PySpark
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64

WORKDIR /app

# Installation des dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copie du reste du projet
COPY . .

# Commande de lancement (vérifie bien le chemin vers ton script)
CMD ["python", "scripts/analyse_spark.py"]