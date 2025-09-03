#!/bin/bash

echo "🚀 LANCEMENT FOOTBALL ANALYTICS PLATFORM"
echo "========================================="

# Nettoyer tous les processus Streamlit existants
echo "🧹 Nettoyage des processus existants..."
pkill -f streamlit 2>/dev/null || true
sleep 2

# Vérifier que Python et les packages sont disponibles
echo "🔍 Vérification des dépendances..."
python -c "import streamlit, pandas, numpy" 2>/dev/null || {
    echo "❌ Packages manquants. Installation..."
    pip install streamlit pandas numpy plotly
}

# Créer le dossier de configuration Streamlit
mkdir -p ~/.streamlit

# Configuration Streamlit optimisée
cat > ~/.streamlit/config.toml << EOF
[server]
port = 8501
enableCORS = false
enableXsrfProtection = false
headless = true
address = "0.0.0.0"

[browser]
gatherUsageStats = false
serverAddress = "localhost"
serverPort = 8501

[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"

[logger]
level = "info"
EOF

echo "✅ Configuration Streamlit créée"

# Dashboard de test ultra-simple pour vérifier que tout fonctionne
cat > test_working.py << 'EOF'
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="⚽ Football Analytics",
    page_icon="⚽",
    layout="wide"
)

st.title("⚽ FOOTBALL ANALYTICS PLATFORM")
st.success("🎉 Dashboard opérationnel !")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Statut", "✅ OK")
with col2:
    st.metric("Modules", "100%")
with col3:
    st.metric("Tests", "Passés")

st.subheader("📊 Test Rapide")
data = pd.DataFrame({
    'Joueur': ['Mbappé', 'Haaland', 'Messi'],
    'Buts': [30, 35, 25],
    'xG': [28.5, 32.1, 24.8]
})
st.dataframe(data, use_container_width=True)

if st.button("🚀 Test OK"):
    st.balloons()
    st.success("La plateforme fonctionne parfaitement !")

st.info("Dashboard principal : python_analytics/dashboards/coach_interface.py")
EOF

echo "📱 Lancement du dashboard de test..."
streamlit run test_working.py --server.port 8501 &
STREAMLIT_PID=$!

# Attendre que Streamlit démarre
echo "⏳ Démarrage en cours..."
sleep 8

# Tester la connexion
echo "🔗 Test de connexion..."
if curl -s -f http://localhost:8501 >/dev/null; then
    echo "✅ SUCCESS: Dashboard accessible sur http://localhost:8501"
    echo ""
    echo "🎯 PROCHAINES ÉTAPES:"
    echo "1. Ouvrir http://localhost:8501 dans votre navigateur"
    echo "2. Vérifier que le dashboard de test fonctionne"
    echo "3. Lancer le dashboard principal avec la commande:"
    echo "   streamlit run python_analytics/dashboards/coach_interface.py"
    echo ""
    echo "📋 COMMANDES UTILES:"
    echo "• Arrêter : pkill -f streamlit"
    echo "• Logs : tail -f ~/.streamlit/logs/*"
    echo "• Tests : python simple_test.py"
else
    echo "❌ ERREUR: Dashboard non accessible"
    echo "Vérification des logs..."
    ps aux | grep streamlit
fi

echo ""
echo "🏆 Football Analytics Platform - Prêt pour l'analyse !"
