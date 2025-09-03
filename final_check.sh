#!/bin/sh

echo "🏆 FOOTBALL ANALYTICS PLATFORM - VALIDATION FINALE"
echo "=================================================="
echo "Date: $(date)"
echo "Utilisateur: $(whoami)"
echo "Répertoire: $(pwd)"
echo ""

# Couleurs pour l'affichage
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

success_count=0
total_checks=8

# Function pour afficher les résultats
check_result() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✅ $2${NC}"
        ((success_count++))
    else
        echo -e "${RED}❌ $2${NC}"
    fi
}

echo "🔍 VÉRIFICATIONS SYSTÈME"
echo "------------------------"

# 1. Vérification Python
python3 --version > /dev/null 2>&1
check_result $? "Python 3 installé"

# 2. Vérification packages Python essentiels
python3 -c "import pandas, numpy, streamlit, matplotlib" > /dev/null 2>&1
check_result $? "Packages Python essentiels disponibles"

# 3. Vérification structure du projet
if [ -f "python_analytics/dashboards/coach_interface.py" ] && [ -f "database/sql/create_schema.sql" ]; then
    check_result 0 "Structure du projet complète"
else
    check_result 1 "Structure du projet complète"
fi

# 4. Vérification fichiers de configuration
if [ -f ".env.example" ] && [ -f "requirements.txt" ]; then
    check_result 0 "Fichiers de configuration présents"
else
    check_result 1 "Fichiers de configuration présents"
fi

# 5. Vérification Git repository
if [ -d ".git" ] && git remote get-url origin > /dev/null 2>&1; then
    check_result 0 "Repository Git configuré"
else
    check_result 1 "Repository Git configuré"
fi

# 6. Vérification modules Python
python3 -c "
import sys
sys.path.insert(0, '.')
from python_analytics.modules.performance_analyzer import FootballMetrics
print('Import réussi')
" > /dev/null 2>&1
check_result $? "Modules Football Analytics importables"

# 7. Vérification R (optionnel)
if command -v Rscript > /dev/null 2>&1; then
    if [ -f "r_analytics/scripts/predictive_models.R" ]; then
        check_result 0 "Scripts R Analytics disponibles"
    else
        check_result 1 "Scripts R Analytics disponibles"
    fi
else
    echo -e "${YELLOW}⚠️  R non installé (optionnel)${NC}"
    ((success_count++)) # On compte comme succès car R est optionnel
fi

# 8. Test de syntaxe Streamlit
streamlit --help > /dev/null 2>&1
if [ $? -eq 0 ]; then
    check_result 0 "Streamlit accessible"
else
    check_result 1 "Streamlit accessible"
fi

echo ""
echo "📊 RÉSULTATS"
echo "------------"
echo -e "Score: ${BLUE}$success_count/$total_checks${NC}"

if [ $success_count -eq $total_checks ]; then
    echo -e "${GREEN}🎉 PLATEFORME ENTIÈREMENT OPÉRATIONNELLE !${NC}"
    echo ""
    echo "🚀 COMMANDES DE DÉMARRAGE:"
    echo "  Dashboard: streamlit run python_analytics/dashboards/coach_interface.py"
    echo "  Jupyter:   jupyter lab notebooks/"
    echo "  Tests:     python simple_test.py"
    echo ""
    echo "🌐 ACCÈS:"
    echo "  Dashboard: http://localhost:8501"
    echo "  Jupyter:   http://localhost:8888"
    echo "  GitHub:    https://github.com/Abdel67Unistra/Intelligence-football-analytics"
    
elif [ $success_count -ge 6 ]; then
    echo -e "${YELLOW}⚠️  PLATEFORME FONCTIONNELLE AVEC LIMITATIONS${NC}"
    echo "La plupart des fonctionnalités sont disponibles."
    echo "Consultez les erreurs ci-dessus pour les améliorations."
    
else
    echo -e "${RED}❌ PROBLÈMES DÉTECTÉS${NC}"
    echo "Veuillez résoudre les erreurs avant d'utiliser la plateforme."
    echo ""
    echo "💡 SOLUTIONS:"
    echo "  1. Installer les dépendances: pip install -r requirements.txt"
    echo "  2. Configurer l'environnement: cp .env.example .env"
    echo "  3. Exécuter les tests: python simple_test.py"
fi

echo ""
echo "📚 DOCUMENTATION:"
echo "  README.md - Guide complet"
echo "  QUICK_START.md - Démarrage rapide"
echo "  ACCOMPLISHMENTS.md - État des fonctionnalités"

exit $((total_checks - success_count))
