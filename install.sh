#!/bin/bash

echo "🚀 Installation de la Plateforme Football Analytics"
echo "================================================="

# Vérification de Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 n'est pas installé. Veuillez l'installer d'abord."
    exit 1
fi

# Vérification de PostgreSQL
if ! command -v psql &> /dev/null; then
    echo "⚠️  PostgreSQL n'est pas détecté. Assurez-vous qu'il est installé et configuré."
fi

# Installation des dépendances Python
echo "📦 Installation des dépendances Python..."
pip install pandas numpy scikit-learn scipy psycopg2-binary sqlalchemy streamlit matplotlib seaborn plotly requests beautifulsoup4 xgboost python-dotenv pyyaml tqdm jupyter

# Création du fichier .env
if [ ! -f .env ]; then
    echo "⚙️  Création du fichier de configuration..."
    cp .env.example .env
    echo "✅ Fichier .env créé. Veuillez le configurer avec vos paramètres."
fi

# Création du dossier logs
mkdir -p logs

# Vérification de R (optionnel)
if command -v Rscript &> /dev/null; then
    echo "📊 R détecté. Installation des packages R..."
    Rscript -e "
    if (!require('randomForest')) install.packages('randomForest', repos='https://cran.rstudio.com/')
    if (!require('xgboost')) install.packages('xgboost', repos='https://cran.rstudio.com/')
    if (!require('survival')) install.packages('survival', repos='https://cran.rstudio.com/')
    if (!require('ggplot2')) install.packages('ggplot2', repos='https://cran.rstudio.com/')
    if (!require('dplyr')) install.packages('dplyr', repos='https://cran.rstudio.com/')
    if (!require('RPostgreSQL')) install.packages('RPostgreSQL', repos='https://cran.rstudio.com/')
    "
else
    echo "⚠️  R n'est pas installé. Les analyses prédictives avancées ne seront pas disponibles."
fi

echo ""
echo "✅ Installation terminée!"
echo ""
echo "📋 Prochaines étapes:"
echo "1. Configurez PostgreSQL et créez la base 'football_analytics'"
echo "2. Modifiez le fichier .env avec vos paramètres de base de données"
echo "3. Exécutez 'python database/migrations/populate_demo_data.py' pour les données de démo"
echo "4. Lancez le dashboard avec 'streamlit run python_analytics/dashboards/coach_interface.py'"
echo ""
echo "🔗 Accès:"
echo "- Dashboard: http://localhost:8501"
echo "- Jupyter: jupyter lab notebooks/"
echo ""
