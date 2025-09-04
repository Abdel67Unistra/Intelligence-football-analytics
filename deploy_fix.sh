#!/bin/bash

echo "🔧 CORRECTION DÉPLOIEMENT STREAMLIT CLOUD"
echo "========================================"

cd /Users/cheriet/Documents/augment-projects/stat

# Nettoyage et push forcé
echo "📤 Push final vers GitHub..."
git add . 
git commit -m "🚀 DEPLOY: Ready for Streamlit Cloud deployment" || echo "Rien à commiter"
git push origin main --force

echo ""
echo "✅ VALEURS POUR STREAMLIT CLOUD :"
echo "Repository: Abdel67Unistra/Intelligence-football-analytics"
echo "Branch: main"
echo "Main file: python_analytics/dashboards/coach_interface.py"
echo "App URL: football-analytics-intelligence"
echo ""
echo "🌐 Allez sur : https://share.streamlit.io"
