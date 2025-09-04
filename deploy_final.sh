#!/bin/zsh

echo "🚀 DÉPLOIEMENT FINAL STREAMLIT CLOUD"
echo "===================================="

# Se positionner dans le bon répertoire
cd /Users/cheriet/Documents/augment-projects/stat

# Commit des dernières modifications
echo "📝 Commit des corrections psycopg2..."
git add .
git commit -m "🚀 FIXED: Removed psycopg2 dependency for Streamlit Cloud deployment" || echo "Rien à commiter"

# Push vers GitHub
echo "📤 Push vers GitHub..."
git push origin main

echo ""
echo "✅ CORRECTIONS APPLIQUÉES :"
echo "  - Supprimé import psycopg2"
echo "  - Supprimé paramètre db_conn des fonctions"
echo "  - Mode démonstration activé"
echo ""
echo "🌐 VALEURS POUR STREAMLIT CLOUD :"
echo "Repository: Abdel67Unistra/Intelligence-football-analytics"
echo "Branch: main"
echo "Main file: python_analytics/dashboards/coach_interface.py"
echo "App URL: football-analytics-intelligence"
echo ""
echo "🎯 ÉTAPES FINALES :"
echo "1. Allez sur https://share.streamlit.io"
echo "2. Connectez votre compte GitHub"
echo "3. Cliquez 'New app'"
echo "4. Utilisez les valeurs ci-dessus"
echo "5. Cliquez 'Deploy!'"
echo ""
echo "🎉 Votre application sera accessible à :"
echo "   https://football-analytics-intelligence.streamlit.app"
