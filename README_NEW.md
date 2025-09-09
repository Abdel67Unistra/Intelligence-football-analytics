# 🔵⚪ Racing Club de Strasbourg - Analytics Platform

> **Plateforme d'analyse exclusive pour le Racing Club de Strasbourg**

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-Live-brightgreen.svg)](https://coach-interface-rcs.streamlit.app)
[![RCS](https://img.shields.io/badge/RCS-2024--2025-0066CC.svg)](https://rcstrasbourg.fr)
[![Ligue 1](https://img.shields.io/badge/Ligue%201-10ème%20place-yellow.svg)](https://ligue1.fr)

## 🏆 Présentation

**Racing Club de Strasbourg Analytics Platform** est une plateforme d'intelligence footballistique **exclusivement dédiée** au Racing Club de Strasbourg, intégrant les données réelles de la saison 2024-2025.

### 🎯 Mission
Fournir au staff technique du RCS des analyses avancées pour optimiser les performances de l'équipe, le recrutement et la stratégie sportive en Ligue 1.

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

---

## ⚙️ Architecture Technique

### 🐍 Backend Python
```
python_analytics/
├── dashboards/
│   └── coach_interface.py       # Interface Streamlit RCS
└── modules/
    ├── analyseur_rcs.py         # Analyses spécialisées RCS
    ├── metriques_rcs.py         # Métriques football RCS
    └── moteur_scouting_rcs.py   # Scouting intelligent RCS
```

### 📊 Analytics R
```
r_analytics/
├── scripts/
│   ├── analyses_rcs.R           # Modèles prédictifs RCS
│   └── football_viz.R          # Visualisations
└── reports/                     # Rapports automatiques
```

### 📁 Structure Projet RCS
```
stat/
├── 🔵⚪ python_analytics/
│   ├── dashboards/
│   │   └── coach_interface.py   # Dashboard RCS exclusif
│   └── modules/
│       ├── analyseur_rcs.py     # Données RCS 2024-2025
│       ├── metriques_rcs.py     # Calculs football RCS
│       └── moteur_scouting_rcs.py
├── 📈 r_analytics/
│   └── scripts/
│       └── analyses_rcs.R       # Modèles prédictifs RCS
├── ⚙️ configs/
│   └── database.py
└── 📚 data/                     # Données RCS uniquement
```

---

## 🚀 Installation et Utilisation

### 1. Installation des Dépendances
```bash
pip install pandas numpy scikit-learn scipy streamlit matplotlib seaborn plotly requests beautifulsoup4 xgboost python-dotenv pyyaml tqdm jupyter
```

### 2. Lancement du Dashboard RCS
```bash
streamlit run python_analytics/dashboards/coach_interface.py
```

### 3. Accès à l'Interface
- **Local** : http://localhost:8501
- **En ligne** : https://coach-interface-rcs.streamlit.app

---

## 📊 Pages Disponibles

### 🏠 Vue d'ensemble RCS
- Position Ligue 1 actuelle
- Métriques principales de l'effectif
- Statistiques de maintien

### 👥 Effectif RCS Complet
- 17 joueurs avec données complètes
- Filtres par poste et statut
- Analyses par tranche d'âge

### 📊 Performances RCS
- Bilan saison 2024-2025
- Analyse des 5 derniers matchs
- Forme actuelle de l'équipe

### 🎯 Métriques RCS Avancées
- xG (Expected Goals) personnalisé RCS
- PPDA (Passes per Defensive Action)
- Analyses tactiques spécialisées

### 📈 Projections RCS
- Projection points fin de saison
- Probabilité de maintien
- Objectifs et scénarios

### ⚽ Analyse Matches RCS
- Détail des récents matchs
- Évolution des performances
- Tendances tactiques

---

## 🔵⚪ Spécificités RCS

### 🎨 Design
- **Couleurs officielles** : Bleu #0066CC et blanc
- **Branding RCS** : Logo et identité visuelle
- **Interface intuitive** : Navigation spécialisée

### 📈 Données Réelles
- **Saison 2024-2025** : Données actualisées
- **Effectif complet** : 17 joueurs avec profils détaillés
- **Résultats récents** : Matchs vs équipes de Ligue 1

### 🎯 Analyses Spécialisées
- **Formules RCS** : Calculs adaptés au style de jeu
- **Projections** : Basées sur l'historique du club
- **Objectifs** : Alignés sur la stratégie RCS

---

## 🤝 Contribution

### 📝 Améliorations Futures
- Intégration données temps réel
- Analyses vidéo automatisées
- Module de scouting avancé
- API pour staff technique

### 🔧 Développement
```bash
git clone https://github.com/your-repo/rcs-analytics-platform
cd rcs-analytics-platform
pip install -r requirements.txt
streamlit run python_analytics/dashboards/coach_interface.py
```

---

## 📞 Support

### 🆘 Support Technique
- **Issues** : Signaler bugs et suggestions
- **Documentation** : Guide utilisateur détaillé
- **Contact** : Support dédié RCS

---

## 📄 Licence

MIT License - Football Analytics Platform dédiée au Racing Club de Strasbourg

---

<div align="center">

**🔵⚪ Racing Club de Strasbourg Analytics Platform**

*Analytics exclusives pour le Racing Club de Strasbourg*

[🚀 Démo Live](https://coach-interface-rcs.streamlit.app) • [📊 Dashboard](https://coach-interface-rcs.streamlit.app) • [🔵⚪ RCS Officiel](https://rcstrasbourg.fr)

</div>
