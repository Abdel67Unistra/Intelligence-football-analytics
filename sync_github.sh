#!/bin/bash

cd /Users/cheriet/Documents/augment-projects/stat

echo "🔄 SYNCHRONISATION FORCÉE GITHUB"
echo "================================"

# Forcer l'ajout de tous les fichiers
git add -A
git commit -m "🚀 FINAL FIX: Removed psycopg2 completely - ready for Streamlit Cloud"
git push origin main --force

echo "✅ Synchronisation terminée!"
echo ""
echo "🎯 VALEURS STREAMLIT CLOUD:"
echo "Repository: Abdel67Unistra/Intelligence-football-analytics" 
echo "Branch: main"
echo "Main file: python_analytics/dashboards/coach_interface.py"
echo "App URL: football-analytics-$(date +%s)"
