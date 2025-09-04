#!/bin/zsh

echo "🚀 PRÉPARATION DÉPLOIEMENT STREAMLIT CLOUD"
echo "=========================================="

# Se positionner dans le bon répertoire
cd /Users/cheriet/Documents/augment-projects/stat

# Vérifier l'état Git
echo "📋 État du repository :"
git status --porcelain

# Commit et push des dernières modifications
echo "📝 Commit final..."
git add .
git commit -m "🚀 READY: Final deployment preparation for Streamlit Cloud" || echo "✅ Rien à commiter"

echo "📤 Push vers GitHub..."
git push origin main

# Générer un nom unique pour l'application
TIMESTAMP=$(date +%s)
UNIQUE_NAME="football-analytics-$TIMESTAMP"

echo ""
echo "✅ INFORMATIONS POUR STREAMLIT CLOUD :"
echo "======================================="
echo "Repository: Abdel67Unistra/Intelligence-football-analytics"
echo "Branch: main"
echo "Main file path: python_analytics/dashboards/coach_interface.py"
echo "App URL (unique): $UNIQUE_NAME"
echo ""
echo "🌐 URL finale sera : https://$UNIQUE_NAME.streamlit.app"
echo ""
echo "🎯 ÉTAPES :"
echo "1. Allez sur : https://share.streamlit.io"
echo "2. Connectez votre GitHub"
echo "3. Cliquez 'New app'"
echo "4. Utilisez les valeurs ci-dessus"
echo "5. Deploy!"

# Vérifier que le fichier principal existe
if [[ -f "python_analytics/dashboards/coach_interface.py" ]]; then
    echo ""
    echo "✅ Fichier principal confirmé : python_analytics/dashboards/coach_interface.py"
else
    echo ""
    echo "❌ ERREUR : Fichier principal manquant !"
    exit 1
fi

echo ""
echo "🎉 PRÊT POUR LE DÉPLOIEMENT !"
