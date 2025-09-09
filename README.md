# 🔵⚪ Racing Club de Strasbourg - Analytics Platform v2.0

> **Plateforme d'analyse avancée entièrement restructurée pour le Racing Club de Strasbourg**

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-2.0-brightgreen.svg)](https://streamlit.io)
[![R](https://img.shields.io/badge/R-4.0+-blue.svg)](https://r-project.org)
[![RCS](https://img.shields.io/badge/RCS-2024--2025-0066CC.svg)](https://rcstrasbourg.fr)
[![Ligue 1](https://img.shields.io/badge/Ligue%201-10ème%20place-yellow.svg)](https://ligue1.fr)
[![Analytics](https://img.shields.io/badge/Analytics-IA%20Avancés-orange.svg)](https://github.com)

## 🚀 Nouvelle Version 2.0 - Restructurée Complètement

**Racing Club de Strasbourg Analytics Platform** a été **entièrement restructurée** avec de nouvelles fonctionnalités d'intelligence artificielle, des analyses prédictives avancées et une interface moderne.

### 🎯 Mission Élargie
- **🤖 Intelligence Artificielle** : Prédictions de blessures, optimisation de compositions
- **📊 Analytics Avancés** : Modèles ML (Random Forest, XGBoost), clustering de joueurs
- **📋 Rapports Automatisés** : Génération HTML/JSON/PDF avec recommandations IA
- **🌐 Interface Moderne** : Dashboard Streamlit interactif et responsive
- **📈 Analyses R** : Modèles prédictifs, visualisations avancées, clustering

### ✨ Nouveautés Version 2.0
- **🔧 Architecture Unifiée** : Script principal `main_rcs.py` avec menu interactif
- **🤖 IA Prédictive** : Analyse des risques de blessures avec machine learning
- **📊 Graphiques Interactifs** : Plotly, heatmaps, analyses spatiales
- **📋 Système de Rapports** : Export multi-format automatisé
- **🎯 Optimisation IA** : Compositions d'équipe optimisées par algorithmes
- **🏥 Suivi Médical** : Alertes préventives et recommandations

---

## 🔵⚪ Données RCS 2024-2025

### 👥 Effectif Complet (17 joueurs)
- **Gardiens** : Matz Sels, Alaa Bellaarouch
- **Défenseurs** : Guela Doué, Abakar Sylla, Saïdou Sow, Marvin Senaya, Thomas Delaine, Frédéric Guilbert, Caleb Wiley
- **Milieux** : Habib Diarra, Andrey Santos, Ismaël Doukouré, Junior Mwanga, Sékou Mara, Dilane Bakwa
- **Attaquants** : Emanuel Emegha, Félix Lemaréchal

### 📊 Position Actuelle
- **🏆 Classement** : 10ème place Ligue 1
- **📈 Points** : 23 points en 17 matchs
- **⚽ Bilan** : 6 victoires, 5 nuls, 6 défaites
- **🥅 Buts** : 25 marqués, 28 encaissés

---

## 🚀 Fonctionnalités RCS

### 📊 Analytics Exclusives RCS
- **Vue d'ensemble** : Position, effectif, statistiques clés
- **Effectif détaillé** : 17 joueurs avec données réelles (âge, poste, valeur, nationalité)
- **Performances** : Analyse des 5 derniers matchs vs Marseille, Lille, Rennes, Reims, Nantes
- **Métriques avancées** : xG RCS personnalisé, PPDA, analyses de forme

### 🎯 Projections Saison
- **Maintien** : Probabilité calculée en temps réel
- **Projection points** : Estimation fin de saison basée sur forme actuelle
- **Objectifs RCS** : Maintien confortable, développement jeunes, équilibre financier

### 🔍 Scouting & Recrutement IA
- **Profilage automatique** : 8 types de joueurs
- **Recommandations personnalisées** selon critères
- **Prédiction valeur marchande** avec machine learning
- **Analyse d'opportunités** : coût/bénéfice transferts
- **Détection de talents** : jeunes à potentiel

### 📈 Modèles Prédictifs
- **Résultats de matchs** (Random Forest)
- **Risques de blessures** (Survival Analysis)
- **Évolution valeurs marchandes** (XGBoost)
- **Performance saisonnière** (ARIMA)

### 📱 Interface Utilisateur
- **Dashboard coach** temps réel
- **Rapports automatisés** post-match
- **Alertes intelligentes** (fatigue, forme)
- **Visualisations interactives**

---

## 🛠️ Architecture Technique

### 🗄️ Base de Données
```
PostgreSQL 13+ avec :
├── Tables partitionnées par saison
├── Index optimisés pour analytics
├── Vues matérialisées (KPI temps réel)
├── Triggers automatiques
└── Extension PostGIS (données spatiales)
```

### 🐍 Backend Python
```
python_analytics/
├── modules/
│   ├── performance_analyzer.py   # Analyses individuelles
│   ├── scouting_engine.py       # IA recrutement
│   └── tactical_analyzer.py     # Analyses d'équipe
├── dashboards/
│   └── coach_interface.py       # Interface Streamlit
└── apis/
    └── football_data_api.py     # Intégrations externes
```

### 📊 Analytics R
```
r_analytics/
├── scripts/
│   ├── predictive_models.R      # Modèles ML
│   ├── football_viz.R          # Visualisations
│   └── clustering_analysis.R   # Segmentation joueurs
└── reports/
    └── match_reports.Rmd        # Rapports automatiques
```

### 📁 Structure Projet
```
stat/
├── 📊 database/
│   ├── sql/create_schema.sql
│   └── migrations/populate_demo_data.py
├── 🐍 python_analytics/
│   ├── modules/
│   └── dashboards/
├── 📈 r_analytics/
│   ├── scripts/
│   └── reports/
├── ⚙️ configs/
│   └── database.py
├── 📚 data/
│   ├── raw/
│   └── processed/
├── 📓 notebooks/
│   └── football_analytics_demo.ipynb
└── 📋 docs/
```

---

## 📦 Installation et Configuration

### 1. Prérequis
```bash
# Python 3.9+
python --version

# PostgreSQL 13+
psql --version

# R 4.0+
R --version
```

### 2. Clone du Projet
```bash
git clone https://github.com/your-repo/football-analytics-platform
cd football-analytics-platform
```

### 3. Environnement Python
```bash
# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # macOS/Linux
# ou
venv\Scripts\activate     # Windows

# Installer les dépendances
pip install -r requirements.txt
```

### 4. Configuration Base de Données
```bash
# Créer la base de données
createdb football_analytics

# Exécuter le schéma
psql -d football_analytics -f database/sql/create_schema.sql

# Peupler avec des données de démo
python database/migrations/populate_demo_data.py
```

### 5. Variables d'Environnement
```bash
# Créer .env
echo "DB_HOST=localhost
DB_PORT=5432
DB_NAME=football_analytics
DB_USER=postgres
DB_PASSWORD=your_password" > .env
```

### 6. Packages R
```r
# Dans R/RStudio
install.packages(c(
  "tidyverse", "caret", "randomForest", "xgboost",
  "survival", "ggplot2", "plotly", "DBI", "RPostgreSQL"
))
```

---

## 🎮 Utilisation

### 🚀 Lancement du Dashboard
```bash
# Dashboard Streamlit
streamlit run python_analytics/dashboards/coach_interface.py

# Accès : http://localhost:8501
```

### 📓 Notebook de Démonstration
```bash
# Lancer Jupyter
jupyter notebook notebooks/football_analytics_demo.ipynb
```

### 📊 Scripts R
```r
# Exécuter les modèles prédictifs
source("r_analytics/scripts/predictive_models.R")

# Générer les visualisations
source("r_analytics/scripts/football_viz.R")
```

### 🐍 API Python
```python
from python_analytics.modules.performance_analyzer import PlayerPerformanceAnalyzer
from python_analytics.modules.scouting_engine import ScoutingEngine

# Analyser un joueur
analyzer = PlayerPerformanceAnalyzer(db_connection)
form = analyzer.get_player_form("player_id", last_n_matches=10)

# Recherche de talents
scout = ScoutingEngine()
recommendations = scout.scout_by_criteria({
    'position': 'ST',
    'age_max': 25,
    'max_value': 50
})
```

---

## 📊 Données et Métriques

### 🗃️ Sources de Données
- **Football-Data.org** : Statistiques matchs et joueurs
- **Transfermarkt** : Valeurs marchandes et transferts
- **Simulation GPS** : Données physiques et spatiales
- **APIs libres** : Calendriers, résultats, compositions

### 📈 Métriques Calculées

#### Offensives
- **Goals/90min** : Efficacité offensive
- **xG** : Qualité des occasions créées
- **xA** : Créativité et vision de jeu
- **Conversion Rate** : Efficacité devant le but

#### Défensives  
- **Tackles/90min** : Impact défensif
- **Interceptions** : Lecture du jeu
- **PPDA** : Intensité du pressing
- **Duels gagnés %** : Domination physique

#### Techniques
- **Pass Accuracy %** : Précision technique
- **Key Passes** : Créativité
- **Distance parcourue** : Investissement physique
- **Sprints** : Intensité

---

## 🎯 Cas d'Usage

### 👨‍💼 Pour les Entraîneurs
```
✅ Préparer les matchs avec analyses adverses
✅ Optimiser les compositions d'équipe  
✅ Suivre la forme et fatigue des joueurs
✅ Ajuster les systèmes tactiques
✅ Prendre des décisions éclairées
```

### 🔍 Pour les Recruteurs
```
✅ Identifier des cibles selon profil recherché
✅ Évaluer le rapport qualité/prix
✅ Anticiper l'adaptation au championnat
✅ Détecter les jeunes talents
✅ Optimiser les investissements
```

### 📊 Pour les Analystes
```
✅ Modéliser les performances
✅ Prédire les tendances
✅ Comprendre les patterns tactiques
✅ Quantifier l'impact des joueurs
✅ Benchmarker avec la concurrence
```

### 📈 Pour la Direction
```
✅ ROI des investissements joueurs
✅ Optimisation masse salariale
✅ Stratégie de développement
✅ Reporting performance globale
✅ Aide à la prise de décision
```

---

## 🔮 Roadmap et Évolutions

### Phase 1 : Core Analytics ✅
- [x] Base de données football
- [x] Métriques fondamentales (xG, xA, PPDA)
- [x] Dashboard de base
- [x] Analyses de performance

### Phase 2 : Intelligence Avancée 🚧
- [x] Moteur de scouting IA
- [x] Modèles prédictifs R
- [ ] Intégration APIs externes
- [ ] Alertes automatiques

### Phase 3 : Visualisations 📊
- [x] Graphiques interactifs
- [x] Heatmaps et pass networks
- [ ] Animations temporelles
- [ ] Réalité augmentée

### Phase 4 : Production 🚀
- [ ] Déploiement cloud
- [ ] APIs REST complètes
- [ ] Application mobile
- [ ] Intégration temps réel

### Phase 5 : Intelligence IA 🤖
- [ ] Computer vision (analyse vidéo)
- [ ] NLP pour scouting automatique
- [ ] Réseaux de neurones avancés
- [ ] Recommandations contextuelles

---

## 🤝 Contribution

### 🛠️ Pour Contribuer
```bash
# Fork le projet
git fork https://github.com/your-repo/football-analytics-platform

# Créer une branche feature
git checkout -b feature/nouvelle-fonctionnalite

# Commit et push
git commit -am "Ajout nouvelle fonctionnalité"
git push origin feature/nouvelle-fonctionnalite

# Créer une Pull Request
```

### 📋 Guidelines
- **Code** : Suivre PEP 8 pour Python, tidyverse pour R
- **Tests** : Ajouter des tests unitaires
- **Documentation** : Commenter le code et mettre à jour README
- **Performance** : Optimiser les requêtes et algorithmes

---

## 📚 Documentation Technique

### 🔗 APIs Principales
- **PlayerAnalyzer** : Analyses individuelles
- **TacticalAnalyzer** : Analyses d'équipe  
- **ScoutingEngine** : Recrutement intelligent
- **FootballMetrics** : Calculs métriques

### 📊 Schéma Base de Données
![Schéma DB](docs/database_schema.png)

### 🎯 Architecture Système
![Architecture](docs/system_architecture.png)

---

## 📞 Support et Contact

### 🆘 Support Technique
- **Issues GitHub** : Signaler bugs et demandes
- **Wiki** : Documentation détaillée
- **Discussions** : Questions et partage

### 👥 Équipe
- **Data Science** : Modèles et algorithmes
- **Backend** : APIs et base de données  
- **Frontend** : Interfaces utilisateur
- **Football** : Expertise métier

---

## 📄 Licence

```
MIT License

Copyright (c) 2024 Football Analytics Platform

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
```

---

## 🎉 Remerciements

- **Communauté Football Analytics** pour l'inspiration
- **Open Source Community** pour les outils
- **Clubs professionnels** pour les retours
- **Universités** pour la recherche

---

<div align="center">

**⚽ Football Analytics Platform**

*Transformez vos données en avantage compétitif*

[🌟 Star](https://github.com/your-repo/football-analytics-platform) • [🐛 Issues](https://github.com/your-repo/football-analytics-platform/issues) • [💬 Discussions](https://github.com/your-repo/football-analytics-platform/discussions)

</div>
