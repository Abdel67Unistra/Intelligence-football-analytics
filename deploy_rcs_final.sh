#!/bin/bash

# Script de Déploiement Racing Club de Strasbourg
# ================================================
# Déploie la plateforme analytics spécialisée RCS

echo "🔵⚪ DÉPLOIEMENT RACING CLUB DE STRASBOURG"
echo "=========================================="

# Variables
PROJECT_DIR="/Users/cheriet/Documents/augment-projects/stat"
MODULES_DIR="$PROJECT_DIR/python_analytics/modules"
DASHBOARD_DIR="$PROJECT_DIR/python_analytics/dashboards"

echo ""
echo "📋 Vérification des fichiers RCS..."

# Vérifier les modules RCS
if [ -f "$MODULES_DIR/analyseur_rcs.py" ]; then
    echo "✅ Module analyseur_rcs.py présent"
else
    echo "❌ Module analyseur_rcs.py manquant"
    exit 1
fi

if [ -f "$MODULES_DIR/moteur_scouting_rcs.py" ]; then
    echo "✅ Module moteur_scouting_rcs.py présent"
else
    echo "❌ Module moteur_scouting_rcs.py manquant"
    exit 1
fi

if [ -f "$MODULES_DIR/metriques_rcs.py" ]; then
    echo "✅ Module metriques_rcs.py présent"
else
    echo "❌ Module metriques_rcs.py manquant"
    exit 1
fi

# Vérifier le dashboard
if [ -f "$DASHBOARD_DIR/dashboard_rcs.py" ]; then
    echo "✅ Dashboard dashboard_rcs.py présent"
else
    echo "❌ Dashboard dashboard_rcs.py manquant"
    exit 1
fi

# Vérifier les scripts utilitaires
if [ -f "$PROJECT_DIR/dashboard_rcs_simple.py" ]; then
    echo "✅ Dashboard simplifié présent"
else
    echo "❌ Dashboard simplifié manquant"
fi

if [ -f "$PROJECT_DIR/lancer_rcs.py" ]; then
    echo "✅ Script de lancement présent"
else
    echo "❌ Script de lancement manquant"
fi

if [ -f "$PROJECT_DIR/MANUEL_RCS.md" ]; then
    echo "✅ Manuel d'utilisation présent"
else
    echo "❌ Manuel d'utilisation manquant"
fi

echo ""
echo "📊 Statistiques du projet RCS:"
echo "------------------------------"

# Compter les lignes de code
total_lines=0
for file in "$MODULES_DIR"/*rcs.py "$DASHBOARD_DIR/dashboard_rcs.py"; do
    if [ -f "$file" ]; then
        lines=$(wc -l < "$file")
        total_lines=$((total_lines + lines))
        echo "$(basename "$file"): $lines lignes"
    fi
done

echo "📈 Total lignes de code RCS: $total_lines"

# Vérifier les dépendances Python
echo ""
echo "🔧 Vérification des dépendances..."

python3 -c "
import sys
modules = ['pandas', 'numpy', 'streamlit', 'plotly']
missing = []
for module in modules:
    try:
        __import__(module)
        print(f'✅ {module}')
    except ImportError:
        print(f'❌ {module} manquant')
        missing.append(module)

if missing:
    print(f'\\n🔴 Modules manquants: {missing}')
    print('💡 Installation: pip install ' + ' '.join(missing))
    sys.exit(1)
else:
    print('\\n✅ Toutes les dépendances sont installées')
"

echo ""
echo "🚀 Options de lancement:"
echo "-------------------------"
echo "1. Dashboard complet:     python lancer_rcs.py"
echo "2. Dashboard simplifié:   python dashboard_rcs_simple.py"
echo "3. Tests modules:         python test_simple_rcs.py"
echo "4. Manuel d'utilisation:  cat MANUEL_RCS.md"

echo ""
echo "🌐 URLs d'accès:"
echo "-----------------"
echo "• Local: http://localhost:8502"
echo "• En ligne: https://football-analytics-platform-2025.streamlit.app"

echo ""
echo "🎯 Effectif RCS intégré:"
echo "-------------------------"
echo "• 19 joueurs saison 2024-2025"
echo "• Valeurs marchandes réalistes"
echo "• Postes et âges exacts"
echo "• Statuts titulaire/remplaçant"

echo ""
echo "📈 Fonctionnalités spécialisées:"
echo "---------------------------------"
echo "• Métriques xG/xA style RCS (contre-attaque)"
echo "• Scouting budget adapté (max 15M€)"
echo "• Analyses en français complet"
echo "• Interface aux couleurs du club"

echo ""
echo "🔵⚪ Déploiement Racing Club de Strasbourg terminé !"
echo "======================================================"
