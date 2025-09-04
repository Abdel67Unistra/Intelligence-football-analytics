#!/bin/zsh

echo "🚨 CORRECTION URGENTE ERREUR PSYCOPG2"
echo "====================================="

cd /Users/cheriet/Documents/augment-projects/stat

echo "📍 Répertoire: $(pwd)"

echo "📦 Ajout des fichiers modifiés..."
git add python_analytics/dashboards/coach_interface.py

echo "💾 Commit de la correction..."
git commit -m "🚀 URGENT: Remove psycopg2 import from coach_interface.py for Streamlit Cloud"

echo "📤 Push vers GitHub..."
git push origin main

echo ""
echo "✅ CORRECTION APPLIQUÉE!"
echo "🔄 Redéployez maintenant sur Streamlit Cloud"
echo ""
echo "🎯 VALEURS POUR STREAMLIT:"
echo "Repository: Abdel67Unistra/Intelligence-football-analytics"
echo "Branch: main"
echo "Main file: python_analytics/dashboards/coach_interface.py"
echo "App URL: football-fixed-$(date +%s)"
echo ""
echo "🌐 https://share.streamlit.io"
