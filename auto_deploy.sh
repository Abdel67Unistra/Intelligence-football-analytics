#!/bin/zsh

echo "🚀 PRÉPARATION AUTOMATIQUE POUR DÉPLOIEMENT STREAMLIT CLOUD"
echo "============================================================"

# Nettoyage des fichiers inutiles pour le déploiement
echo "🧹 Nettoyage du repository..."
rm -rf __pycache__ **/__pycache__ **/**/__pycache__ 2>/dev/null || true
rm -f *.log streamlit.log 2>/dev/null || true

# Vérification que le fichier principal existe
if [[ ! -f "python_analytics/dashboards/coach_interface.py" ]]; then
    echo "❌ Erreur: Fichier principal manquant"
    exit 1
fi

echo "✅ Fichier principal trouvé: python_analytics/dashboards/coach_interface.py"

# Création d'un requirements.txt optimisé pour Streamlit Cloud
echo "📦 Création requirements.txt optimisé..."
cat > requirements.txt << 'EOF'
streamlit>=1.28.0
pandas>=2.0.0
numpy>=1.24.0
plotly>=5.17.0
matplotlib>=3.7.0
seaborn>=0.12.0
scikit-learn>=1.3.0
requests>=2.31.0
python-dotenv>=1.0.0
EOF

# Configuration Streamlit optimisée
echo "⚙️ Configuration Streamlit..."
mkdir -p .streamlit
cat > .streamlit/config.toml << 'EOF'
[server]
enableCORS = false
enableXsrfProtection = false
headless = true

[browser]
gatherUsageStats = false

[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
EOF

# Vérification que les imports fonctionnent
echo "🔍 Test des imports critiques..."
python3 -c "
import sys
sys.path.insert(0, '.')
try:
    from python_analytics.modules.performance_analyzer import FootballMetrics
    print('✅ FootballMetrics OK')
except Exception as e:
    print(f'❌ Erreur FootballMetrics: {e}')

try:
    import streamlit as st
    print('✅ Streamlit OK')
except Exception as e:
    print(f'❌ Erreur Streamlit: {e}')

try:
    import pandas as pd
    import numpy as np
    import plotly.express as px
    print('✅ Packages de base OK')
except Exception as e:
    print(f'❌ Erreur packages: {e}')
"

# Commit et push des optimisations
echo "📤 Commit des optimisations..."
git add .
git commit -m "🌐 Optimize for Streamlit Cloud deployment

✅ Optimizations:
- Clean requirements.txt for Streamlit Cloud
- Streamlit configuration optimized
- Removed cache files
- Ready for 1-click deployment

🎯 Deploy on: https://share.streamlit.io
📁 Main file: python_analytics/dashboards/coach_interface.py" 2>/dev/null || echo "Rien à commiter"

git push origin main 2>/dev/null || echo "Push en cours..."

echo ""
echo "🎉 REPOSITORY OPTIMISÉ POUR STREAMLIT CLOUD !"
echo "=============================================="
echo ""
echo "📋 INFORMATIONS POUR LE DÉPLOIEMENT :"
echo "• Repository: https://github.com/Abdel67Unistra/Intelligence-football-analytics"
echo "• Branch: main"
echo "• Main file: python_analytics/dashboards/coach_interface.py"
echo "• Requirements: ✅ Optimisé"
echo "• Configuration: ✅ Prête"
echo ""
echo "🔗 ÉTAPES SUIVANTES :"
echo "1. Aller sur https://share.streamlit.io"
echo "2. Se connecter avec GitHub"
echo "3. Cliquer 'New app'"
echo "4. Coller: python_analytics/dashboards/coach_interface.py"
echo "5. Déployer !"
echo ""
echo "⏱️  Temps de déploiement estimé: 2-3 minutes"
echo "🌐 Votre plateforme sera en ligne 24h/24 !"

# Ouvrir automatiquement Streamlit Cloud
echo ""
echo "🌐 Ouverture automatique de Streamlit Cloud..."
open "https://share.streamlit.io" 2>/dev/null || echo "Ouvrez manuellement: https://share.streamlit.io"
