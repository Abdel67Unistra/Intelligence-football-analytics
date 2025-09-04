#!/bin/zsh

# Script d'urgence pour synchroniser GitHub
cd /Users/cheriet/Documents/augment-projects/stat

# Vérifier que nous sommes dans le bon répertoire
echo "📍 Répertoire actuel: $(pwd)"

# Vérifier le statut Git
echo "📋 Status Git:"
git status --short

# Ajouter tous les fichiers
echo "📦 Ajout des fichiers..."
git add .

# Commit avec message clair
echo "💾 Commit..."
git commit -m "🚀 EMERGENCY: Remove psycopg2 import from coach_interface.py"

# Push forcé
echo "📤 Push forcé vers GitHub..."
git push origin main --force

echo ""
echo "✅ SYNCHRONISATION TERMINÉE!"
echo "🔄 REDÉPLOYEZ SUR STREAMLIT CLOUD MAINTENANT!"
echo ""
echo "Repository: Abdel67Unistra/Intelligence-football-analytics"
echo "Branch: main"  
echo "Main file: python_analytics/dashboards/coach_interface.py"
echo "App URL suggestion: football-emergency-deploy-2025"
