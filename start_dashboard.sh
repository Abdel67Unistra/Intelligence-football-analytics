#!/bin/bash

echo "🚀 LANCEMENT FOOTBALL ANALYTICS PLATFORM"
echo "========================================"

# Arrêter tous les processus Streamlit existants
echo "🔄 Nettoyage des processus existants..."
pkill -f streamlit 2>/dev/null || true
sleep 2

# Vérifier que le répertoire existe
if [ ! -d "python_analytics/dashboards" ]; then
    echo "❌ Erreur: Répertoire dashboard non trouvé"
    echo "Assurez-vous d'être dans le répertoire racine du projet"
    exit 1
fi

# Lancer le dashboard principal
echo "🌐 Lancement du dashboard Football Analytics..."
echo "📍 URL: http://localhost:8501"
echo ""

# Lancer Streamlit en mode headless (sans interaction)
streamlit run python_analytics/dashboards/coach_interface.py \
    --server.port 8501 \
    --server.headless true \
    --server.runOnSave true \
    --browser.serverAddress localhost \
    --browser.gatherUsageStats false &

STREAMLIT_PID=$!

# Attendre que le service démarre
echo "⏳ Démarrage en cours..."
sleep 8

# Tester la connexion
if curl -s -f http://localhost:8501 > /dev/null 2>&1; then
    echo "✅ Dashboard opérationnel!"
    echo ""
    echo "🎯 ACCÈS:"
    echo "   • Dashboard: http://localhost:8501"
    echo "   • PID du processus: $STREAMLIT_PID"
    echo ""
    echo "🔧 COMMANDES UTILES:"
    echo "   • Arrêter: pkill -f streamlit"
    echo "   • Logs: tail -f ~/.streamlit/logs/*"
    echo ""
    echo "🏆 La plateforme Football Analytics est prête!"
    
    # Ouvrir automatiquement le navigateur (optionnel)
    if command -v open > /dev/null 2>&1; then
        echo "🌐 Ouverture automatique du navigateur..."
        sleep 2
        open http://localhost:8501
    fi
    
else
    echo "❌ Erreur: Dashboard non accessible"
    echo "Vérifiez les logs: tail ~/.streamlit/logs/*"
    kill $STREAMLIT_PID 2>/dev/null || true
    exit 1
fi

# Garder le script actif pour afficher le PID
echo "✋ Dashboard en cours d'exécution (PID: $STREAMLIT_PID)"
echo "   Pressez Ctrl+C pour arrêter"
echo ""

# Attendre l'interruption
trap "echo '🛑 Arrêt du dashboard...'; kill $STREAMLIT_PID 2>/dev/null || true; exit 0" INT

# Monitoring simple
while kill -0 $STREAMLIT_PID 2>/dev/null; do
    sleep 10
done

echo "⚠️  Le processus Streamlit s'est arrêté de manière inattendue"
