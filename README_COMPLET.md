# 🔵⚪ Racing Club de Strasbourg - Analytics Platform ⚪🔵

![RCS Logo](https://img.shields.io/badge/Racing%20Club-Strasbourg-0066CC?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAiIGhlaWdodD0iNDAiIHZpZXdCb3g9IjAgMCA0MCA0MCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPGNpcmNsZSBjeD0iMjAiIGN5PSIyMCIgcj0iMjAiIGZpbGw9IiMwMDY2Q0MiLz4KPHN2ZyB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTEyIDJMMTMuMDkgOC4yNkwyMCA5TDEzLjA5IDE1Ljc0TDEyIDIyTDEwLjkxIDE1Ljc0TDQgOUwxMC45MSA4LjI2TDEyIDJaIiBmaWxsPSJ3aGl0ZSIvPgo8L3N2Zz4KPC9zdmc+)
![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![R](https://img.shields.io/badge/R-4.0+-276DC3?style=for-the-badge&logo=r&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)

## 📊 Plateforme d'Analytics Football Moderne

Plateforme complète d'analyse de données pour le Racing Club de Strasbourg, combinant l'intelligence artificielle, l'analyse statistique avancée et les technologies de visualisation modernes pour fournir des insights précieux sur les performances de l'équipe.

### 🎯 Fonctionnalités Principales

- 📈 **Dashboards Interactifs** - Visualisations temps réel avec Streamlit
- 🐍 **Analytics Python** - Graphiques Plotly, Matplotlib, Seaborn
- 📊 **Analytics R** - Modèles statistiques avancés et prédictifs  
- ⚽ **Données Réelles** - APIs Football-Data.org, API-Sports
- 🤖 **Machine Learning** - Prédictions matchs, clustering joueurs
- 📱 **Interface Responsive** - Design moderne aux couleurs RCS
- 📚 **Documentation Complète** - Guides et tutoriels intégrés

---

## 🚀 Démarrage Rapide

### Prérequis

- **Python 3.8+** 
- **R 4.0+** (optionnel pour analytics R)
- **Git**

### Installation

```bash
# 1. Cloner le repository
git clone https://github.com/Abdel67Unistra/Intelligence-football-analytics.git
cd Intelligence-football-analytics

# 2. Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# 3. Installer les dépendances Python
pip install -r requirements.txt

# 4. Installer les packages R (optionnel)
Rscript -e "install.packages(c('tidyverse', 'ggplot2', 'plotly', 'caret', 'randomForest'))"

# 5. Configuration (optionnel pour APIs réelles)
cp .env.example .env
# Éditer .env avec vos clés API
```

### Lancement

```bash
# Démarrer la plateforme principale
streamlit run rcs_analytics_platform.py

# Démarrer la documentation (port 8502)
streamlit run rcs_documentation_system.py --server.port 8502

# Exécuter les analytics R
cd r_analytics && Rscript scripts/rcs_advanced_analytics.R
```

**🌐 Applications accessibles sur :**
- **Plateforme principale:** http://localhost:8501
- **Documentation:** http://localhost:8502

---

## 🏗️ Architecture

```
🔵⚪ RCS Analytics Platform
├── 📱 Interface Layer (Streamlit)
│   ├── rcs_analytics_platform.py      # App principale
│   ├── rcs_documentation_system.py    # Documentation
│   └── webapp_rcs_avec_donnees_reelles.py # Version avec données
├── 🧠 Analytics Layer
│   ├── 🐍 Python Analytics
│   │   ├── Visualisations Plotly/Matplotlib
│   │   ├── Machine Learning (scikit-learn)
│   │   └── Analyses statistiques
│   └── 📊 R Analytics  
│       ├── Modèles prédictifs
│       ├── Clustering avancé
│       └── Tests statistiques
├── 💾 Data Layer
│   ├── data_fetcher_rcs.py           # APIs football
│   ├── 🌐 Football-Data.org API
│   ├── 🌐 API-Sports
│   └── 💾 Cache local (5min TTL)
└── ⚙️ Configuration Layer
    ├── config_rcs.py                 # Configuration RCS
    ├── assets_rcs.py                 # Assets visuels
    └── .env                          # Variables d'environnement
```

---

## 📊 Fonctionnalités Détaillées

### 🎯 Dashboard Principal
- **Métriques Clés** - Position, points, buts, forme récente
- **Vue d'Ensemble** - Performance globale de l'équipe
- **Données Temps Réel** - Mise à jour automatique depuis APIs

### 🐍 Analytics Python
- **Performance Équipe** - Radar charts, évolution des points
- **Statistiques Joueurs** - Top buteurs, notes par poste, heatmaps
- **Classement Ligue 1** - Position RCS vs autres équipes
- **Analyse Matchs** - Domicile vs extérieur, chronologie résultats

### 📊 Analytics R
- **Modèles Prédictifs** - Random Forest, SVM, régression
- **Clustering Joueurs** - K-means, analyse PCA
- **Tests Statistiques** - ANOVA, tests de normalité
- **Prédictions Matchs** - Probabilités de victoire

### 🔍 Insights & Recommandations
- **Points Forts** - Analyse des performances positives
- **Axes d'Amélioration** - Identification des faiblesses
- **Recommandations Tactiques** - Conseils basés sur les données

---

## 📚 Documentation

### 🔧 APIs Principales

#### RCSDataFetcher
```python
from data_fetcher_rcs import rcs_data_fetcher

# Classement Ligue 1
standings = rcs_data_fetcher.fetch_ligue1_standings()

# Matchs récents RCS  
matches = rcs_data_fetcher.fetch_rcs_recent_matches()

# Stats joueurs
players = rcs_data_fetcher.fetch_player_stats()
```

#### RCSAnalyticsPlatform
```python
from rcs_analytics_platform import RCSAnalyticsPlatform

platform = RCSAnalyticsPlatform()
platform.create_dashboard_overview()    # Dashboard principal
platform.create_python_analytics()      # Graphiques Python
platform.create_r_analytics()           # Analytics R
```

### 🎨 Personnalisation

#### Couleurs RCS
```python
from assets_rcs import get_rcs_colors

colors = get_rcs_colors()
# {
#   'primary': '#0066CC',    # Bleu RCS
#   'secondary': '#FFFFFF',  # Blanc  
#   'accent': '#FFD700',     # Or
#   'success': '#28a745',
#   'warning': '#ffc107', 
#   'danger': '#dc3545'
# }
```

#### Configuration Club
```python
from config_rcs import RCS_CONFIG

club_info = RCS_CONFIG['club_info']
# {
#   'nom': 'Racing Club de Strasbourg',
#   'stade': 'Stade de la Meinau',
#   'capacite': 26109,
#   'ville': 'Strasbourg'
# }
```

---

## 🔧 Configuration Avancée

### Variables d'Environnement

Créer un fichier `.env` pour les APIs réelles :

```bash
# APIs Football (optionnel)
FOOTBALL_DATA_API_KEY=your_football_data_api_key
API_SPORTS_KEY=your_api_sports_key

# Configuration Cache
CACHE_TIMEOUT=300  # 5 minutes
CACHE_ENABLED=true

# Configuration Debug
DEBUG_MODE=false
LOG_LEVEL=INFO
```

### Paramètres Streamlit

Personnaliser `.streamlit/config.toml` :

```toml
[theme]
primaryColor = "#0066CC"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"

[server]
port = 8501
headless = false
```

---

## 📈 Sources de Données

### APIs Intégrées

| API | Description | Données |
|-----|-------------|---------|
| **Football-Data.org** | Données officielles | Classements, résultats, calendrier |
| **API-Sports** | Stats détaillées | Joueurs, transferts, métriques avancées |
| **Fallback Simulé** | Données de secours | Données réalistes si APIs indisponibles |

### Types de Données

- **⚽ Matchs** - Résultats, scores, adversaires, domicile/extérieur
- **👥 Joueurs** - Buts, passes, notes, minutes, postes
- **🏆 Classements** - Position, points, différence de buts
- **📊 Métriques Avancées** - xG, possession, passes réussies

---

## 🤖 Machine Learning

### Modèles Disponibles

#### Prédiction Notes Joueurs
```python
from sklearn.ensemble import RandomForestRegressor

# Features: buts, passes, minutes, âge
# Target: note moyenne joueur
model = RandomForestRegressor(n_estimators=100)
model.fit(X_train, y_train)
predictions = model.predict(X_test)
```

#### Clustering Joueurs  
```python
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Clustering basé sur performances
scaler = StandardScaler()
features_scaled = scaler.fit_transform(player_stats)
kmeans = KMeans(n_clusters=3)
clusters = kmeans.fit_predict(features_scaled)
```

#### Prédiction Résultats Matchs
```python
# Probabilités victoire/nul/défaite
match_predictions = predict_match_outcomes(match_data)
# Retourne: probabilités pour chaque résultat possible
```

---

## 📱 Interface Utilisateur

### Navigation

La plateforme utilise une **sidebar** pour la navigation principale :

1. **📊 Dashboard Principal** - Vue d'ensemble RCS
2. **🐍 Analytics Python** - Graphiques interactifs  
3. **📊 Analytics R** - Analyses statistiques avancées
4. **🔍 Insights & Recommandations** - Conclusions
5. **📚 Documentation** - Guide complet

### Fonctionnalités Interactives

- **🔍 Zoom/Pan** sur tous les graphiques
- **🎯 Hover** pour détails au survol  
- **📊 Filtres** dynamiques par période/joueur
- **💾 Export** des graphiques et données
- **📱 Responsive** - Compatible mobile/tablette

---

## 🔄 Mise à Jour des Données

### Cache Intelligent

- **⏱️ TTL 5 minutes** - Données fraîches sans surcharger APIs
- **🔄 Fallback** automatique si APIs indisponibles  
- **📊 Indicateurs** de fraîcheur des données
- **🔃 Refresh** manuel disponible

### Gestion d'Erreurs

```python
try:
    # Tentative API réelle
    data = fetch_from_api()
except APIError:
    # Fallback données simulées
    data = get_fallback_data()
    st.warning("Utilisation des données simulées")
```

---

## 🚀 Déploiement

### Déploiement Local

```bash
# Production locale
streamlit run rcs_analytics_platform.py --server.port 80

# Avec SSL (optionnel)
streamlit run app.py --server.enableCORS=false --server.enableXsrfProtection=false
```

### Déploiement Cloud

#### Streamlit Cloud
1. Fork le repository
2. Connecter à Streamlit Cloud
3. Déployer automatiquement

#### Heroku
```bash
# Procfile déjà configuré
git push heroku main
```

#### Docker
```dockerfile
# Dockerfile inclus
docker build -t rcs-analytics .
docker run -p 8501:8501 rcs-analytics
```

---

## 🧪 Tests et Développement

### Tests

```bash
# Tests unitaires
python -m pytest tests/

# Tests d'intégration  
python -m pytest tests/integration/

# Tests de performance
python -m pytest tests/performance/ --benchmark-only
```

### Développement

```bash
# Mode développement avec auto-reload
streamlit run rcs_analytics_platform.py --server.runOnSave=true

# Debug mode
export DEBUG_MODE=true
streamlit run rcs_analytics_platform.py
```

### Structure de Tests

```
tests/
├── unit/
│   ├── test_data_fetcher.py
│   ├── test_analytics.py
│   └── test_config.py
├── integration/
│   ├── test_apis.py
│   └── test_workflows.py
└── performance/
    └── test_benchmarks.py
```

---

## 📋 Roadmap

### Version 2.1 (Q4 2025)
- [ ] 🔄 Intégration API Transfermarkt
- [ ] 📊 Analytics tactiques avancées  
- [ ] 🎯 Prédictions blessures joueurs
- [ ] 📱 Application mobile native

### Version 2.2 (Q1 2026)
- [ ] 🤖 IA conversationnelle pour analyses
- [ ] 📺 Streaming données matchs en direct
- [ ] 🎮 Simulateur tactique interactif
- [ ] 🌍 Comparaisons européennes

### Version 3.0 (Q2 2026)
- [ ] 🧠 Deep Learning pour analyses vidéo
- [ ] ⚡ Architecture microservices
- [ ] 🔐 Authentification multi-utilisateurs
- [ ] 📈 Marketplace d'analytics

---

## 🤝 Contribution

### Comment Contribuer

1. **Fork** le repository
2. **Créer** une branche feature (`git checkout -b feature/amazing-feature`)
3. **Commit** les changements (`git commit -m 'Add amazing feature'`)
4. **Push** vers la branche (`git push origin feature/amazing-feature`)
5. **Ouvrir** une Pull Request

### Standards de Code

- **Python:** PEP 8, type hints, docstrings
- **R:** Style tidyverse, documentation roxygen2
- **Commits:** Messages conventionnels (feat/fix/docs/refactor)
- **Tests:** Couverture minimum 80%

### Issues et Bugs

Utiliser les [GitHub Issues](https://github.com/Abdel67Unistra/Intelligence-football-analytics/issues) avec les labels :
- 🐛 `bug` - Problèmes et erreurs
- ✨ `enhancement` - Nouvelles fonctionnalités
- 📚 `documentation` - Améliorations docs
- 🚀 `performance` - Optimisations

---

## 📄 License

Ce projet est sous licence **MIT License** - voir le fichier [LICENSE](LICENSE) pour plus de détails.

### Crédits

- **APIs Données:** Football-Data.org, API-Sports
- **Technologies:** Streamlit, Plotly, R, Python
- **Design:** Inspiré de l'identité visuelle RCS
- **Développement:** Équipe Analytics RCS

---

## 📞 Support et Contact

### Support Technique

- 📧 **Email:** support@rcs-analytics.fr
- 💬 **Discord:** [RCS Analytics Community](https://discord.gg/rcs-analytics)
- 📱 **Twitter:** [@RCS_Analytics](https://twitter.com/rcs_analytics)

### Documentation

- 📚 **Wiki:** [GitHub Wiki](https://github.com/Abdel67Unistra/Intelligence-football-analytics/wiki)
- 🎥 **Tutoriels:** [YouTube Channel](https://youtube.com/rcs-analytics)
- 📖 **Blog:** [Medium @RCS-Analytics](https://medium.com/@rcs-analytics)

### Communauté

- 🏟️ **Forum:** [RCS Analytics Community](https://community.rcs-analytics.fr)
- 👥 **LinkedIn:** [Groupe Professionnel](https://linkedin.com/groups/rcs-analytics)
- 📊 **Kaggle:** [Équipe RCS](https://kaggle.com/teams/rcs-analytics)

---

## 🏆 Remerciements

Un grand merci à :

- **🔵⚪ Racing Club de Strasbourg** - Pour l'inspiration et les couleurs
- **⚽ Communauté Football Analytics** - Pour les méthodes et best practices  
- **🐍 Communauté Python** - Pour les outils fantastiques
- **📊 Communauté R** - Pour les analyses statistiques avancées
- **🙏 Contributeurs** - Pour leurs améliorations et feedback

---

<div align="center">

## 🔵⚪ ALLEZ RACING ! ⚪🔵

*Développé avec ❤️ pour l'analyse de données football*

[![GitHub stars](https://img.shields.io/github/stars/Abdel67Unistra/Intelligence-football-analytics?style=social)](https://github.com/Abdel67Unistra/Intelligence-football-analytics/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/Abdel67Unistra/Intelligence-football-analytics?style=social)](https://github.com/Abdel67Unistra/Intelligence-football-analytics/network/members)

**[⬆ Retour au début](#-racing-club-de-strasbourg---analytics-platform-)**

</div>
