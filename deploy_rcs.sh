#!/bin/bash
# ========================================================================
# Script de Déploiement Dashboard Racing Club de Strasbourg
# ========================================================================
# 
# Déploie l'application spécialisée RCS sur Streamlit Cloud
# 
# Auteur: Football Analytics Platform
# Équipe: Racing Club de Strasbourg
# ========================================================================

echo "🔵⚪ Déploiement Dashboard Racing Club de Strasbourg"
echo "======================================================"

# Vérification des fichiers requis
echo "📋 Vérification des fichiers..."

FICHIERS_REQUIS=(
    "python_analytics/modules/analyseur_rcs.py"
    "python_analytics/modules/moteur_scouting_rcs.py" 
    "python_analytics/modules/metriques_rcs.py"
    "python_analytics/dashboards/dashboard_rcs.py"
    "r_analytics/scripts/analyses_rcs.R"
)

for fichier in "${FICHIERS_REQUIS[@]}"; do
    if [[ -f "$fichier" ]]; then
        echo "✅ $fichier"
    else
        echo "❌ $fichier manquant"
        exit 1
    fi
done

# Test des modules Python
echo ""
echo "🧪 Test des modules RCS..."
python3 test_modules_rcs.py

if [[ $? -eq 0 ]]; then
    echo "✅ Tests réussis"
else
    echo "❌ Échec des tests - Arrêt du déploiement"
    exit 1
fi

# Création du requirements.txt spécialisé RCS
echo ""
echo "📦 Mise à jour des dépendances..."

cat > requirements_rcs.txt << EOF
# Racing Club de Strasbourg - Analytics Platform
# Dépendances spécialisées pour le RCS

# Core Data Science
pandas>=2.0.0
numpy>=1.24.0
scipy>=1.10.0
scikit-learn>=1.3.0

# Streamlit et Visualisation
streamlit>=1.28.0
plotly>=5.15.0
matplotlib>=3.7.0
seaborn>=0.12.0

# Calculs avancés
xgboost>=1.7.0

# Utilitaires
python-dotenv>=1.0.0
pyyaml>=6.0
tqdm>=4.65.0
requests>=2.31.0

# Pas de dépendances PostgreSQL pour Streamlit Cloud
# (utilisation des données simulées)
EOF

echo "✅ Requirements RCS créé"

# Création du fichier de configuration Streamlit
echo ""
echo "⚙️ Configuration Streamlit..."

mkdir -p .streamlit

cat > .streamlit/config.toml << EOF
[global]
developmentMode = false

[server]
headless = true
enableCORS = false
enableXsrfProtection = false
maxUploadSize = 200

[browser]
gatherUsageStats = false

[theme]
primaryColor = "#0066CC"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F8FF"
textColor = "#000000"
font = "sans serif"
EOF

echo "✅ Configuration Streamlit créée"

# Création d'un script de lancement RCS
echo ""
echo "🚀 Création du script de lancement..."

cat > start_dashboard_rcs.sh << 'EOF'
#!/bin/bash
echo "🔵⚪ Lancement Dashboard Racing Club de Strasbourg"
echo "=================================================="

# Vérifier que Python 3 est disponible
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 requis"
    exit 1
fi

# Installer les dépendances si nécessaire
if [[ ! -d "venv" ]]; then
    echo "📦 Installation de l'environnement virtuel..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements_rcs.txt
else
    source venv/bin/activate
fi

# Lancer le dashboard RCS
echo "🚀 Démarrage du dashboard RCS..."
echo "📍 URL: http://localhost:8501"
echo "🔵⚪ Racing Club de Strasbourg Analytics"

streamlit run python_analytics/dashboards/dashboard_rcs.py --server.port 8501
EOF

chmod +x start_dashboard_rcs.sh
echo "✅ Script de lancement créé"

# Préparation du README spécialisé RCS
echo ""
echo "📖 Création de la documentation RCS..."

cat > README_RCS.md << 'EOF'
# 🔵⚪ Racing Club de Strasbourg - Analytics Platform

Plateforme d'analyse football spécialement conçue pour le Racing Club de Strasbourg.

## 🏟️ À Propos

Cette application fournit des analyses avancées et des outils de scouting adaptés aux besoins spécifiques du RCS :

- **Effectif 2024-2025** complet avec analyses individuelles
- **Métriques xG/xA** optimisées pour le style de jeu RCS
- **Scouting intelligent** focalisé sur le budget et les cibles réalistes
- **Analyses tactiques** adaptées à la formation 4-2-3-1
- **Code entièrement en français** pour le staff technique

## 🚀 Démarrage Rapide

### Installation

```bash
# Cloner le projet
git clone [repository-url]
cd stat

# Installer les dépendances
pip install -r requirements_rcs.txt

# Lancer le dashboard
./start_dashboard_rcs.sh
```

### Utilisation

1. **Tableau de Bord** : Vue d'ensemble des performances RCS
2. **Effectif RCS** : Analyse complète des 19 joueurs
3. **Analyse Joueur** : Statistiques individuelles détaillées
4. **Performance Match** : Rapports post-match
5. **Scouting** : Cibles de recrutement adaptées au budget
6. **Analyses Tactiques** : Insights sur le style de jeu
7. **Rapports** : Documentation automatisée

## 🎯 Fonctionnalités Spécialisées

### Effectif Réel 2024-2025
- Matz Sels, Emanuel Emegha, Dilane Bakwa, Abakar Sylla...
- Statistiques adaptées par poste et âge
- Évaluation du potentiel et de la forme

### Scouting Adapté RCS
- Budget réaliste (max 15M€ par joueur)
- Focus sur jeunes talents français et européens
- Ligues prioritaires : Ligue 2, Championship, Eredivisie...

### Analyses Prédictives
- Modèles de résultats adaptés au niveau RCS
- Prédiction de performance des joueurs
- Projections de fin de saison

## 🔧 Modules Techniques

- `analyseur_rcs.py` : Analyses de performance
- `moteur_scouting_rcs.py` : Intelligence de recrutement
- `metriques_rcs.py` : Calculs xG/xA/PPDA
- `dashboard_rcs.py` : Interface utilisateur
- `analyses_rcs.R` : Modèles prédictifs R

## 📊 Données

L'application utilise :
- **Effectif réel** du RCS 2024-2025
- **Données simulées** réalistes pour les performances
- **Base scouting** avec vrais joueurs de Ligue 2/Championship
- **Métriques FIFA** standards (xG, xA, PPDA)

## 🎨 Interface

- **Couleurs RCS** : Bleu (#0066CC) et Blanc
- **Français intégral** : Variables, fonctions, commentaires
- **UX optimisée** : Navigation intuitive pour staff technique

## 📈 Analytics Avancées

- Expected Goals (xG) avec bonus contre-attaque
- Expected Assists (xA) pour créateurs
- PPDA et métriques de pressing
- Heat maps et analyses spatiales
- Projections statistiques

## 🏆 Objectifs

Aider le Racing Club de Strasbourg à :
- **Optimiser les performances** individuelles et collectives
- **Identifier des cibles** de recrutement réalistes
- **Analyser les tendances** tactiques et physiques
- **Prendre des décisions** data-driven

---

**🔵⚪ Allez Strasbourg ! 🔵⚪**
EOF

echo "✅ Documentation RCS créée"

# Test final du dashboard
echo ""
echo "🧪 Test final du dashboard RCS..."

# Vérifier que le dashboard peut être importé
python3 -c "
import sys
sys.path.append('python_analytics/modules')
sys.path.append('python_analytics/dashboards')

try:
    import dashboard_rcs
    print('✅ Dashboard RCS importé avec succès')
except Exception as e:
    print(f'❌ Erreur import dashboard: {e}')
    exit(1)
"

if [[ $? -eq 0 ]]; then
    echo "✅ Dashboard RCS prêt au déploiement"
else
    echo "❌ Problème avec le dashboard"
    exit 1
fi

echo ""
echo "🎉 Déploiement RCS préparé avec succès !"
echo ""
echo "📋 Prochaines étapes :"
echo "1. Tester localement : ./start_dashboard_rcs.sh"
echo "2. Déployer sur Streamlit Cloud avec requirements_rcs.txt"
echo "3. Configurer l'URL : dashboard_rcs.py comme point d'entrée"
echo ""
echo "🔵⚪ Racing Club de Strasbourg Analytics - Prêt ! 🔵⚪"
