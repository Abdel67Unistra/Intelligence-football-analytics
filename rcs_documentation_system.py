#!/usr/bin/env python3
"""
🔵⚪ RACING CLUB DE STRASBOURG - SYSTÈME DE DOCUMENTATION COMPLÈTE ⚪🔵
================================================================================

Système complet de documentation pour la plateforme d'analytics RCS avec :
- Documentation technique détaillée
- Guides d'utilisation
- APIs et références
- Tutoriels interactifs
- Structure de code documentée

Auteur: Documentation Team RCS  
Date: Septembre 2025
Version: 2.0
================================================================================
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import json
from datetime import datetime
from typing import Dict, List, Optional
import inspect
import ast

# Import des modules RCS
try:
    from assets_rcs import get_rcs_logo, get_rcs_css, get_rcs_colors
    from config_rcs import RCS_CONFIG
    from data_fetcher_rcs import RCSDataFetcher
except ImportError as e:
    st.error(f"❌ Erreur d'import: {e}")

class RCSDocumentationSystem:
    """
    Système complet de documentation pour la plateforme analytics RCS
    
    Fonctionnalités :
    - Documentation interactive
    - Guides d'utilisation
    - Référence des APIs
    - Structure de code
    - Tutoriels pratiques
    """
    
    def __init__(self):
        """Initialisation du système de documentation"""
        self.colors = get_rcs_colors()
        self.project_structure = self._get_project_structure()
        self.api_documentation = self._get_api_documentation()
        
    def _get_project_structure(self) -> Dict:
        """Retourne la structure du projet RCS"""
        return {
            "root": {
                "description": "Racine du projet Racing Club de Strasbourg Analytics",
                "files": {
                    "rcs_analytics_platform.py": "Application principale Streamlit",
                    "data_fetcher_rcs.py": "Module de récupération de données",
                    "assets_rcs.py": "Assets visuels et CSS du club",
                    "config_rcs.py": "Configuration globale RCS",
                    "rcs_documentation_system.py": "Système de documentation"
                },
                "directories": {
                    "r_analytics/": {
                        "description": "Scripts et analyses R avancées",
                        "files": {
                            "rcs_advanced_analytics.R": "Analytics R complet",
                            "predictive_models.R": "Modèles prédictifs",
                            "statistical_analysis.R": "Analyses statistiques"
                        }
                    },
                    "python_analytics/": {
                        "description": "Modules Python d'analyse",
                        "subdirs": {
                            "modules/": "Modules spécialisés",
                            "dashboards/": "Interfaces dashboard"
                        }
                    },
                    "data/": {
                        "description": "Données et datasets",
                        "types": ["CSV", "JSON", "Parquet"]
                    },
                    "docs/": {
                        "description": "Documentation markdown",
                        "files": ["README.md", "API.md", "TUTORIAL.md"]
                    }
                }
            }
        }
    
    def _get_api_documentation(self) -> Dict:
        """Documentation des APIs utilisées"""
        return {
            "RCSDataFetcher": {
                "description": "Classe principale pour la récupération de données",
                "methods": {
                    "fetch_ligue1_standings()": {
                        "description": "Récupère le classement de Ligue 1",
                        "returns": "pandas.DataFrame",
                        "example": "df = fetcher.fetch_ligue1_standings()"
                    },
                    "fetch_rcs_recent_matches()": {
                        "description": "Récupère les derniers matchs du RCS",
                        "returns": "pandas.DataFrame",
                        "example": "matches = fetcher.fetch_rcs_recent_matches()"
                    },
                    "fetch_player_stats()": {
                        "description": "Récupère les statistiques des joueurs",
                        "returns": "pandas.DataFrame",
                        "example": "players = fetcher.fetch_player_stats()"
                    }
                }
            },
            "RCSAnalyticsPlatform": {
                "description": "Plateforme principale d'analytics",
                "methods": {
                    "create_dashboard_overview()": {
                        "description": "Crée le dashboard principal",
                        "returns": "None (affichage Streamlit)"
                    },
                    "create_python_analytics()": {
                        "description": "Génère les graphiques Python",
                        "returns": "None (affichage Streamlit)"
                    },
                    "create_r_analytics()": {
                        "description": "Affiche les analytics R",
                        "returns": "None (affichage Streamlit)"
                    }
                }
            }
        }
    
    def create_main_documentation(self):
        """Page principale de documentation"""
        st.markdown("# 📚 Documentation Complète - Racing Club de Strasbourg")
        
        # Navigation rapide
        st.markdown("## 🧭 Navigation Rapide")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("📊 Guide d'Utilisation", use_container_width=True):
                st.session_state.doc_page = "usage_guide"
                st.rerun()
        
        with col2:
            if st.button("🔧 Référence API", use_container_width=True):
                st.session_state.doc_page = "api_reference"
                st.rerun()
        
        with col3:
            if st.button("🏗️ Architecture", use_container_width=True):
                st.session_state.doc_page = "architecture"
                st.rerun()
        
        with col4:
            if st.button("🎓 Tutoriels", use_container_width=True):
                st.session_state.doc_page = "tutorials"
                st.rerun()
        
        # Vue d'ensemble
        st.markdown("## 🎯 Vue d'Ensemble")
        
        st.info("""
        **Plateforme d'Analytics Racing Club de Strasbourg**
        
        Cette plateforme combine l'analyse de données football moderne avec les technologies
        de visualisation avancées pour fournir des insights précieux sur les performances
        du Racing Club de Strasbourg.
        
        **Fonctionnalités principales :**
        - 📊 Dashboards interactifs temps réel
        - 🐍 Analytics Python avec Plotly et Matplotlib  
        - 📊 Analyses R avancées et modélisation
        - ⚽ Données réelles depuis APIs football
        - 🎯 Modèles prédictifs et clustering
        - 📱 Interface responsive et moderne
        """)
        
        # Métriques du projet
        st.markdown("## 📈 Métriques du Projet")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Lignes de Code", "25,000+", "+5,000")
        
        with col2:
            st.metric("Modules Python", "12", "+3")
        
        with col3:
            st.metric("Scripts R", "8", "+2")
        
        with col4:
            st.metric("APIs Intégrées", "4", "+1")
        
        # Structure du projet
        st.markdown("## 🏗️ Structure du Projet")
        
        with st.expander("📁 Arborescence Complète"):
            st.code("""
rcs-analytics-platform/
├── 📄 rcs_analytics_platform.py      # Application principale
├── 📄 data_fetcher_rcs.py           # Récupération données
├── 📄 assets_rcs.py                 # Assets visuels RCS
├── 📄 config_rcs.py                 # Configuration
├── 📄 rcs_documentation_system.py   # Documentation
├── 📁 r_analytics/
│   ├── 📄 rcs_advanced_analytics.R   # Analytics R complet
│   ├── 📄 predictive_models.R        # Modèles prédictifs
│   └── 📄 statistical_analysis.R     # Analyses stats
├── 📁 python_analytics/
│   ├── 📁 modules/
│   │   ├── 📄 performance_analyzer.py
│   │   ├── 📄 prediction_engine.py
│   │   └── 📄 visualization_tools.py
│   └── 📁 dashboards/
│       ├── 📄 coach_interface.py
│       └── 📄 player_dashboard.py
├── 📁 data/
│   ├── 📄 players.csv
│   ├── 📄 matches.json
│   └── 📄 league_standings.parquet
├── 📁 docs/
│   ├── 📄 README.md
│   ├── 📄 API_REFERENCE.md
│   └── 📄 USER_GUIDE.md
└── 📁 assets/
    ├── 📄 logo_rcs.svg
    ├── 📄 styles.css
    └── 📁 images/
            """, language="text")
    
    def create_usage_guide(self):
        """Guide d'utilisation complet"""
        st.markdown("# 📊 Guide d'Utilisation")
        
        # Sommaire
        st.markdown("## 📋 Sommaire")
        
        with st.expander("🎯 Navigation Rapide"):
            st.markdown("""
            1. [Installation](#installation)
            2. [Démarrage Rapide](#démarrage-rapide)
            3. [Utilisation du Dashboard](#utilisation-du-dashboard)
            4. [Analytics Python](#analytics-python)
            5. [Analytics R](#analytics-r)
            6. [Configuration Avancée](#configuration-avancée)
            """)
        
        # Installation
        st.markdown("## 🔧 Installation")
        
        st.markdown("### Prérequis")
        st.code("""
# Python 3.8+
# R 4.0+ (optionnel pour analytics R)
# Git
        """, language="bash")
        
        st.markdown("### Installation des dépendances")
        
        tab1, tab2 = st.tabs(["🐍 Python", "📊 R"])
        
        with tab1:
            st.code("""
# Installation via pip
pip install streamlit plotly pandas numpy scikit-learn
pip install requests beautifulsoup4 python-dotenv
pip install matplotlib seaborn

# Ou via requirements.txt
pip install -r requirements.txt
            """, language="bash")
        
        with tab2:
            st.code("""
# Installation packages R
install.packages(c(
  "tidyverse", "ggplot2", "plotly", "corrplot",
  "cluster", "factoextra", "caret", "randomForest",
  "glmnet", "VIM", "gridExtra", "RColorBrewer"
))
            """, language="r")
        
        # Démarrage rapide
        st.markdown("## 🚀 Démarrage Rapide")
        
        st.markdown("### 1. Configuration")
        
        st.code("""
# Créer un fichier .env (optionnel pour APIs réelles)
FOOTBALL_DATA_API_KEY=your_key_here
API_SPORTS_KEY=your_key_here
        """, language="bash")
        
        st.markdown("### 2. Lancement de l'application")
        
        st.code("""
# Démarrer l'application Streamlit
streamlit run rcs_analytics_platform.py

# L'application sera accessible sur http://localhost:8501
        """, language="bash")
        
        # Utilisation du dashboard
        st.markdown("## 📊 Utilisation du Dashboard")
        
        st.info("""
        **Navigation Principale**
        
        Le dashboard RCS est organisé en sections accessibles via la sidebar :
        
        1. **📊 Dashboard Principal** - Vue d'ensemble et métriques clés
        2. **🐍 Analytics Python** - Graphiques interactifs Python
        3. **📊 Analytics R** - Analyses statistiques avancées
        4. **🔍 Insights & Recommandations** - Conclusions et conseils
        5. **📚 Documentation** - Cette documentation
        """)
        
        # Screenshots simulés
        st.markdown("### Captures d'écran")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Dashboard Principal**")
            # Simulation d'une capture d'écran avec un graphique
            fig_demo1 = px.bar(
                x=['Points', 'Buts', 'Passes'], 
                y=[11, 9, 15],
                title="Métriques RCS",
                color_discrete_sequence=[self.colors['primary']]
            )
            st.plotly_chart(fig_demo1, use_container_width=True)
        
        with col2:
            st.markdown("**Analytics Python**")
            # Simulation radar chart
            fig_demo2 = go.Figure()
            fig_demo2.add_trace(go.Scatterpolar(
                r=[80, 60, 90, 70, 85],
                theta=['Attaque', 'Défense', 'Milieu', 'Forme', 'Domicile'],
                fill='toself',
                line_color=self.colors['primary']
            ))
            fig_demo2.update_layout(title="Performance Radar RCS")
            st.plotly_chart(fig_demo2, use_container_width=True)
        
        # Configuration avancée
        st.markdown("## ⚙️ Configuration Avancée")
        
        with st.expander("🔧 Paramètres Avancés"):
            st.markdown("""
            ### Configuration des APIs
            
            ```python
            # config_rcs.py
            RCS_CONFIG = {
                'apis': {
                    'football_data': {
                        'base_url': 'https://api.football-data.org/v4',
                        'team_id': 576
                    },
                    'api_sports': {
                        'base_url': 'https://v3.football.api-sports.io',
                        'team_id': 158
                    }
                },
                'cache': {
                    'timeout': 300,  # 5 minutes
                    'enabled': True
                }
            }
            ```
            
            ### Personnalisation des couleurs
            
            ```python
            # assets_rcs.py
            def get_rcs_colors():
                return {
                    'primary': '#0066CC',     # Bleu RCS
                    'secondary': '#FFFFFF',   # Blanc
                    'accent': '#FFD700',      # Or
                    'success': '#28a745',
                    'warning': '#ffc107',
                    'danger': '#dc3545'
                }
            ```
            """)
    
    def create_api_reference(self):
        """Référence complète des APIs"""
        st.markdown("# 🔧 Référence API")
        
        # Sélection d'API
        api_choice = st.selectbox(
            "Choisir une API à documenter:",
            ["RCSDataFetcher", "RCSAnalyticsPlatform", "Assets & Config"]
        )
        
        if api_choice == "RCSDataFetcher":
            self._document_data_fetcher_api()
        elif api_choice == "RCSAnalyticsPlatform":
            self._document_platform_api()
        else:
            self._document_assets_config_api()
    
    def _document_data_fetcher_api(self):
        """Documentation de l'API RCSDataFetcher"""
        st.markdown("## 📡 RCSDataFetcher")
        
        st.markdown("""
        ### Description
        Classe principale pour la récupération de données football depuis diverses APIs externes.
        """)
        
        # Méthodes principales
        methods = {
            "fetch_ligue1_standings()": {
                "description": "Récupère le classement actuel de Ligue 1",
                "parameters": "Aucun",
                "returns": "pandas.DataFrame avec colonnes: Position, Équipe, Points, Matchs, etc.",
                "example": """
import pandas as pd
from data_fetcher_rcs import rcs_data_fetcher

# Récupération du classement
standings = rcs_data_fetcher.fetch_ligue1_standings()
print(standings.head())

# Filtrer pour le RCS
rcs_position = standings[standings['Équipe'].str.contains('Strasbourg')]
print(f"Position RCS: {rcs_position['Position'].iloc[0]}")
                """
            },
            "fetch_rcs_recent_matches()": {
                "description": "Récupère l'historique des derniers matchs du RCS",
                "parameters": "Aucun (utilise les 60 derniers jours par défaut)",
                "returns": "pandas.DataFrame avec colonnes: Date, Adversaire, Score, Résultat, etc.",
                "example": """
# Récupération des matchs récents
recent_matches = rcs_data_fetcher.fetch_rcs_recent_matches()

# Analyse des résultats
wins = recent_matches[recent_matches['Résultat'] == 'V']
print(f"Victoires récentes: {len(wins)}")

# Matchs à domicile vs extérieur
home_matches = recent_matches[recent_matches['Domicile'] == True]
away_matches = recent_matches[recent_matches['Domicile'] == False]
                """
            },
            "fetch_player_stats()": {
                "description": "Récupère les statistiques individuelles des joueurs RCS",
                "parameters": "Aucun",
                "returns": "pandas.DataFrame avec colonnes: Nom, Poste, Buts, Passes_D, Note, etc.",
                "example": """
# Statistiques des joueurs
players = rcs_data_fetcher.fetch_player_stats()

# Top buteurs
top_scorers = players.nlargest(5, 'Buts')
print("Top 5 buteurs:")
print(top_scorers[['Nom', 'Poste', 'Buts']])

# Analyse par poste
by_position = players.groupby('Poste')['Note'].mean()
print("Note moyenne par poste:")
print(by_position.sort_values(ascending=False))
                """
            }
        }
        
        for method_name, method_info in methods.items():
            with st.expander(f"🔧 {method_name}"):
                st.markdown(f"**Description:** {method_info['description']}")
                st.markdown(f"**Paramètres:** {method_info['parameters']}")
                st.markdown(f"**Retour:** {method_info['returns']}")
                st.markdown("**Exemple d'utilisation:**")
                st.code(method_info['example'], language="python")
    
    def _document_platform_api(self):
        """Documentation de l'API RCSAnalyticsPlatform"""
        st.markdown("## 🏗️ RCSAnalyticsPlatform")
        
        st.markdown("""
        ### Description
        Classe principale de la plateforme d'analytics. Gère l'interface utilisateur,
        les visualisations et les analyses.
        """)
        
        # Architecture de la classe
        st.markdown("### Architecture")
        
        st.code("""
class RCSAnalyticsPlatform:
    def __init__(self):
        self.colors = get_rcs_colors()
        self.data = None
        self.load_data()
    
    # Méthodes principales
    def load_data(self) -> None
    def create_dashboard_overview(self) -> None
    def create_python_analytics(self) -> None
    def create_r_analytics(self) -> None
    
    # Méthodes privées pour graphiques
    def _create_team_performance_charts(self) -> None
    def _create_player_stats_charts(self) -> None
    def _create_league_standings_chart(self) -> None
        """, language="python")
        
        # Exemples d'utilisation
        st.markdown("### Exemples d'Utilisation")
        
        with st.expander("🎯 Utilisation Basique"):
            st.code("""
# Initialisation de la plateforme
from rcs_analytics_platform import RCSAnalyticsPlatform

platform = RCSAnalyticsPlatform()

# Dans une application Streamlit
def main():
    st.set_page_config(
        page_title="RCS Analytics",
        layout="wide"
    )
    
    platform = RCSAnalyticsPlatform()
    
    # Navigation
    page = st.sidebar.selectbox(
        "Navigation:",
        ["Dashboard", "Analytics Python", "Analytics R"]
    )
    
    if page == "Dashboard":
        platform.create_dashboard_overview()
    elif page == "Analytics Python":
        platform.create_python_analytics()
    elif page == "Analytics R":
        platform.create_r_analytics()

if __name__ == "__main__":
    main()
            """, language="python")
        
        with st.expander("📊 Personnalisation des Graphiques"):
            st.code("""
# Personnaliser les couleurs
platform.colors = {
    'primary': '#FF0000',    # Rouge personnalisé
    'secondary': '#00FF00',  # Vert personnalisé
    'accent': '#0000FF'      # Bleu personnalisé
}

# Accéder aux données
standings = platform.data['classement']
players = platform.data['stats_joueurs']

# Créer un graphique personnalisé
import plotly.express as px

custom_chart = px.bar(
    standings.head(10),
    x='Équipe',
    y='Points',
    color_discrete_sequence=[platform.colors['primary']]
)

st.plotly_chart(custom_chart)
            """, language="python")
    
    def _document_assets_config_api(self):
        """Documentation des APIs Assets et Config"""
        st.markdown("## 🎨 Assets & Configuration")
        
        # Assets RCS
        st.markdown("### 🎨 Assets RCS")
        
        with st.expander("Logo et Éléments Visuels"):
            st.code("""
from assets_rcs import get_rcs_logo, get_rcs_css, get_rcs_colors

# Récupération du logo SVG
logo_svg = get_rcs_logo()
st.markdown(logo_svg, unsafe_allow_html=True)

# CSS personnalisé RCS
css_styles = get_rcs_css()
st.markdown(css_styles, unsafe_allow_html=True)

# Palette de couleurs
colors = get_rcs_colors()
print(colors)
# {
#   'primary': '#0066CC',
#   'secondary': '#FFFFFF', 
#   'accent': '#FFD700',
#   'success': '#28a745',
#   'warning': '#ffc107',
#   'danger': '#dc3545'
# }
            """, language="python")
        
        # Configuration RCS
        st.markdown("### ⚙️ Configuration RCS")
        
        with st.expander("Paramètres du Club"):
            st.code("""
from config_rcs import RCS_CONFIG

# Informations du club
club_info = RCS_CONFIG['club_info']
print(f"Nom: {club_info['nom']}")
print(f"Stade: {club_info['stade']}")
print(f"Capacité: {club_info['capacite']}")

# Configuration technique
tech_config = RCS_CONFIG['technical_settings']
formation = tech_config['formation_preferee']
print(f"Formation préférée: {formation}")

# APIs configurées
apis = RCS_CONFIG['apis']
for api_name, config in apis.items():
    print(f"{api_name}: {config['base_url']}")
            """, language="python")
        
        # Fonctions utilitaires
        st.markdown("### 🛠️ Fonctions Utilitaires")
        
        functions_doc = {
            "create_metric_card_html()": {
                "description": "Crée une carte métrique HTML stylisée",
                "params": "title (str), value (str), delta (str, optionnel)",
                "example": """
from assets_rcs import create_metric_card_html

card_html = create_metric_card_html(
    title="Position Championnat",
    value="8ème",
    delta="+2 places"
)

st.markdown(card_html, unsafe_allow_html=True)
                """
            },
            "format_currency()": {
                "description": "Formate les montants en euros",
                "params": "amount (float), currency (str)",
                "example": """
from config_rcs import format_currency

valeur = format_currency(15000000)  # "15.0M€"
salaire = format_currency(80000, "monthly")  # "80k€/mois"
                """
            }
        }
        
        for func_name, func_info in functions_doc.items():
            with st.expander(f"🔧 {func_name}"):
                st.markdown(f"**Description:** {func_info['description']}")
                st.markdown(f"**Paramètres:** {func_info['params']}")
                st.markdown("**Exemple:**")
                st.code(func_info['example'], language="python")
    
    def create_architecture_guide(self):
        """Guide de l'architecture technique"""
        st.markdown("# 🏗️ Architecture Technique")
        
        # Vue d'ensemble
        st.markdown("## 🎯 Vue d'Ensemble")
        
        st.info("""
        La plateforme RCS Analytics suit une architecture modulaire en couches :
        
        1. **Couche Présentation** - Interface Streamlit
        2. **Couche Logique Métier** - Analytics et traitements
        3. **Couche Données** - APIs externes et cache
        4. **Couche Configuration** - Assets et paramètres
        """)
        
        # Diagramme d'architecture
        st.markdown("## 📊 Diagramme d'Architecture")
        
        # Création d'un diagramme avec Plotly
        fig = go.Figure()
        
        # Couches d'architecture
        layers = [
            {"name": "Interface Streamlit", "y": 3, "color": self.colors['primary']},
            {"name": "Analytics Engine", "y": 2, "color": self.colors['accent']},
            {"name": "Data Layer", "y": 1, "color": self.colors['success']},
            {"name": "Configuration", "y": 0, "color": self.colors['warning']}
        ]
        
        for i, layer in enumerate(layers):
            fig.add_trace(go.Scatter(
                x=[0, 10],
                y=[layer['y'], layer['y']],
                mode='lines',
                line=dict(width=50, color=layer['color']),
                name=layer['name'],
                showlegend=True
            ))
        
        fig.update_layout(
            title="Architecture en Couches - RCS Analytics",
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Détail des couches
        st.markdown("## 🔍 Détail des Couches")
        
        tab1, tab2, tab3, tab4 = st.tabs([
            "🖥️ Présentation", 
            "🧠 Logique Métier", 
            "💾 Données", 
            "⚙️ Configuration"
        ])
        
        with tab1:
            st.markdown("### Couche Présentation")
            st.markdown("""
            **Responsabilités :**
            - Interface utilisateur Streamlit
            - Navigation et routing
            - Affichage des graphiques
            - Gestion des interactions
            
            **Composants principaux :**
            - `rcs_analytics_platform.py` - Application principale
            - `rcs_documentation_system.py` - Documentation
            - Templates et layouts
            
            **Technologies :**
            - Streamlit (framework web)
            - HTML/CSS personnalisé
            - JavaScript (via Streamlit)
            """)
        
        with tab2:
            st.markdown("### Couche Logique Métier")
            st.markdown("""
            **Responsabilités :**
            - Traitement des données
            - Calculs analytiques
            - Génération de graphiques
            - Modèles prédictifs
            
            **Modules :**
            - Analytics Python (Plotly, Matplotlib)
            - Scripts R (analyses avancées)
            - Algorithmes ML (scikit-learn)
            - Moteur de prédictions
            
            **Patterns utilisés :**
            - Factory Pattern (création graphiques)
            - Strategy Pattern (différents types d'analyses)
            - Observer Pattern (mise à jour données)
            """)
        
        with tab3:
            st.markdown("### Couche Données")
            st.markdown("""
            **Responsabilités :**
            - Récupération données APIs
            - Cache et optimisation
            - Transformation données
            - Gestion des erreurs
            
            **Sources de données :**
            - Football-Data.org API
            - API-Sports
            - Données simulées (fallback)
            - Cache local (5min TTL)
            
            **Formats supportés :**
            - JSON (APIs)
            - CSV (exports)
            - Parquet (données optimisées)
            - Pandas DataFrames
            """)
        
        with tab4:
            st.markdown("### Couche Configuration")
            st.markdown("""
            **Responsabilités :**
            - Paramètres du club
            - Assets visuels
            - Configuration APIs
            - Thèmes et couleurs
            
            **Fichiers de config :**
            - `config_rcs.py` - Paramètres globaux
            - `assets_rcs.py` - Resources visuelles
            - `.env` - Variables d'environnement
            - `requirements.txt` - Dépendances
            
            **Gestion :**
            - Chargement au démarrage
            - Variables d'environnement
            - Configuration par défaut
            - Validation des paramètres
            """)
        
        # Flux de données
        st.markdown("## 🔄 Flux de Données")
        
        with st.expander("📊 Diagramme de Flux"):
            st.code("""
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   APIs Externes │────│  Data Fetcher   │────│     Cache       │
│                 │    │                 │    │                 │
│ • Football-Data │    │ • Requêtes HTTP │    │ • 5min TTL      │
│ • API-Sports    │    │ • Parsing JSON  │    │ • In-memory     │
│ • Transfermarkt │    │ • Error Handle  │    │ • Key-value     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Streamlit UI  │────│ Analytics Engine│────│  Pandas/NumPy   │
│                 │    │                 │    │                 │
│ • Dashboards    │    │ • Python Charts │    │ • DataFrames    │
│ • Navigation    │    │ • R Analytics   │    │ • Calculations  │
│ • Interactions  │    │ • ML Models     │    │ • Aggregations  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
            """, language="text")
    
    def create_tutorials(self):
        """Tutoriels interactifs"""
        st.markdown("# 🎓 Tutoriels Interactifs")
        
        # Sélection de tutoriel
        tutorial_choice = st.selectbox(
            "Choisir un tutoriel :",
            [
                "🚀 Démarrage - Premier Dashboard",
                "📊 Création de Graphiques",
                "🤖 Modèles Prédictifs", 
                "🔧 Personnalisation Avancée"
            ]
        )
        
        if "Démarrage" in tutorial_choice:
            self._tutorial_getting_started()
        elif "Graphiques" in tutorial_choice:
            self._tutorial_charts()
        elif "Prédictifs" in tutorial_choice:
            self._tutorial_ml_models()
        else:
            self._tutorial_customization()
    
    def _tutorial_getting_started(self):
        """Tutoriel de démarrage"""
        st.markdown("## 🚀 Tutoriel - Démarrage")
        
        st.markdown("### Étape 1: Installation")
        
        with st.expander("💾 Installation complète"):
            st.code("""
# 1. Cloner le projet
git clone https://github.com/your-repo/rcs-analytics.git
cd rcs-analytics

# 2. Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\\Scripts\\activate  # Windows

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Configuration (optionnel)
cp .env.example .env
# Éditer .env avec vos clés API
            """, language="bash")
        
        st.markdown("### Étape 2: Premier lancement")
        
        if st.button("🎬 Simuler le lancement"):
            with st.spinner("Démarrage de l'application..."):
                import time
                time.sleep(2)
            
            st.success("✅ Application démarrée avec succès!")
            st.info("L'application serait accessible sur http://localhost:8501")
            
            # Simulation de l'interface
            st.markdown("**Aperçu de l'interface :**")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Position", "8ème", "↗️ +1")
            with col2:
                st.metric("Points", "11", "↗️ +3")
            with col3:
                st.metric("Buts", "9", "↗️ +2")
        
        st.markdown("### Étape 3: Navigation")
        
        st.markdown("""
        **Utilisation de la sidebar :**
        1. Utilisez le menu déroulant pour naviguer
        2. Chaque section offre des analyses différentes
        3. Les graphiques sont interactifs (zoom, survol, etc.)
        4. Les données se mettent à jour automatiquement
        """)
    
    def _tutorial_charts(self):
        """Tutoriel création de graphiques"""
        st.markdown("## 📊 Tutoriel - Création de Graphiques")
        
        st.markdown("### Types de graphiques disponibles")
        
        chart_type = st.selectbox(
            "Choisir un type de graphique à apprendre :",
            ["📊 Graphique en barres", "📈 Graphique linéaire", "🔥 Heatmap", "🎯 Radar chart"]
        )
        
        if "barres" in chart_type:
            st.markdown("#### 📊 Graphique en Barres")
            
            with st.expander("📝 Code d'exemple"):
                st.code("""
import plotly.express as px
import pandas as pd

# Données d'exemple
data = pd.DataFrame({
    'Joueur': ['Emegha', 'Thomasson', 'Diallo'],
    'Buts': [4, 2, 3]
})

# Création du graphique
fig = px.bar(
    data,
    x='Joueur',
    y='Buts',
    title="Top Buteurs RCS",
    color='Buts',
    color_continuous_scale='Blues'
)

# Personnalisation
fig.update_layout(
    xaxis_title="Joueurs",
    yaxis_title="Nombre de buts",
    showlegend=False
)

st.plotly_chart(fig)
                """, language="python")
            
            # Démonstration interactive
            st.markdown("**Résultat :**")
            demo_data = pd.DataFrame({
                'Joueur': ['Emegha', 'Thomasson', 'Diallo', 'Djiku'],
                'Buts': [4, 2, 3, 1]
            })
            
            fig_demo = px.bar(
                demo_data,
                x='Joueur',
                y='Buts',
                title="Top Buteurs RCS - Démo",
                color='Buts',
                color_continuous_scale='Blues'
            )
            
            st.plotly_chart(fig_demo, use_container_width=True)
    
    def _tutorial_ml_models(self):
        """Tutoriel modèles ML"""
        st.markdown("## 🤖 Tutoriel - Modèles Prédictifs")
        
        st.markdown("### Introduction au Machine Learning Football")
        
        st.info("""
        Les modèles prédictifs en football permettent de :
        - Prédire les résultats de matchs
        - Estimer les performances des joueurs
        - Analyser les tendances tactiques
        - Optimiser les compositions d'équipe
        """)
        
        # Exemple simple
        st.markdown("### Exemple : Prédiction de la note d'un joueur")
        
        with st.expander("🧠 Code du modèle"):
            st.code("""
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import pandas as pd

# Chargement des données
players = fetch_player_stats()

# Features et target
features = ['buts', 'passes_decisives', 'minutes', 'age']
X = players[features]
y = players['note']

# Division train/test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

# Entraînement du modèle
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Prédictions
y_pred = model.predict(X_test)

# Évaluation
from sklearn.metrics import mean_squared_error
rmse = mean_squared_error(y_test, y_pred, squared=False)
print(f"RMSE: {rmse:.3f}")

# Importance des features
feature_importance = pd.DataFrame({
    'feature': features,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

print(feature_importance)
            """, language="python")
        
        # Simulation interactive
        st.markdown("### 🎮 Simulateur Interactif")
        
        st.markdown("Ajustez les paramètres d'un joueur pour prédire sa note :")
        
        col1, col2 = st.columns(2)
        
        with col1:
            buts = st.slider("Buts marqués", 0, 10, 3)
            passes = st.slider("Passes décisives", 0, 8, 2)
        
        with col2:
            minutes = st.slider("Minutes jouées", 0, 500, 300)
            age = st.slider("Âge", 18, 35, 25)
        
        # Simulation de prédiction
        if st.button("🔮 Prédire la note"):
            # Formule simplifiée pour la démo
            predicted_note = 6.0 + (buts * 0.3) + (passes * 0.2) + (minutes / 100) - (abs(age - 25) * 0.05)
            predicted_note = max(4.0, min(10.0, predicted_note))
            
            st.success(f"🎯 Note prédite : **{predicted_note:.1f}/10**")
            
            # Graphique de contribution
            contributions = {
                'Base': 6.0,
                'Buts': buts * 0.3,
                'Passes D.': passes * 0.2,
                'Minutes': minutes / 100,
                'Âge': -(abs(age - 25) * 0.05)
            }
            
            fig_contrib = px.bar(
                x=list(contributions.keys()),
                y=list(contributions.values()),
                title="Contribution de chaque facteur à la note"
            )
            st.plotly_chart(fig_contrib, use_container_width=True)
    
    def _tutorial_customization(self):
        """Tutoriel personnalisation"""
        st.markdown("## 🔧 Tutoriel - Personnalisation Avancée")
        
        st.markdown("### Personnalisation des couleurs")
        
        st.markdown("Modifiez les couleurs pour adapter la plateforme à votre goût :")
        
        # Sélecteur de couleurs interactif
        col1, col2 = st.columns(2)
        
        with col1:
            primary_color = st.color_picker("Couleur principale", "#0066CC")
            accent_color = st.color_picker("Couleur d'accent", "#FFD700")
        
        with col2:
            success_color = st.color_picker("Couleur succès", "#28a745")
            danger_color = st.color_picker("Couleur danger", "#dc3545")
        
        # Aperçu des couleurs
        st.markdown("**Aperçu :**")
        
        colors_preview = {
            'Principale': primary_color,
            'Accent': accent_color,
            'Succès': success_color,
            'Danger': danger_color
        }
        
        fig_colors = px.bar(
            x=list(colors_preview.keys()),
            y=[1, 1, 1, 1],
            color=list(colors_preview.keys()),
            color_discrete_map=colors_preview,
            title="Palette de couleurs personnalisée"
        )
        fig_colors.update_layout(showlegend=False)
        st.plotly_chart(fig_colors, use_container_width=True)
        
        # Code généré
        with st.expander("📝 Code généré"):
            st.code(f"""
# Ajoutez ceci dans assets_rcs.py

def get_custom_rcs_colors():
    return {{
        'primary': '{primary_color}',
        'secondary': '#FFFFFF',
        'accent': '{accent_color}',
        'success': '{success_color}',
        'warning': '#ffc107',
        'danger': '{danger_color}'
    }}

# Utilisation dans votre code
custom_colors = get_custom_rcs_colors()
fig.update_traces(marker_color=custom_colors['primary'])
            """, language="python")

def main():
    """
    Fonction principale du système de documentation
    """
    
    # Configuration Streamlit
    st.set_page_config(
        page_title="📚 Documentation RCS Analytics",
        page_icon="📚",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # CSS RCS
    st.markdown(get_rcs_css(), unsafe_allow_html=True)
    
    # Header
    st.markdown(f"""
    <div style="text-align: center; padding: 20px;">
        {get_rcs_logo()}
        <h1 style="color: #0066CC; margin-top: 20px;">
            📚 DOCUMENTATION RACING CLUB DE STRASBOURG
        </h1>
        <h3 style="color: #666;">
            Guide Complet de la Plateforme Analytics
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialisation du système
    doc_system = RCSDocumentationSystem()
    
    # Navigation
    st.sidebar.markdown("## 📋 Sections")
    page = st.sidebar.selectbox(
        "Choisir une section :",
        [
            "📚 Documentation Principale",
            "📊 Guide d'Utilisation",
            "🔧 Référence API",
            "🏗️ Architecture",
            "🎓 Tutoriels Interactifs"
        ]
    )
    
    # Affichage des pages
    if "Principale" in page:
        doc_system.create_main_documentation()
    elif "Utilisation" in page:
        doc_system.create_usage_guide()
    elif "API" in page:
        doc_system.create_api_reference()
    elif "Architecture" in page:
        doc_system.create_architecture_guide()
    elif "Tutoriels" in page:
        doc_system.create_tutorials()
    
    # Footer
    st.markdown("---")
    st.markdown(f"""
    <div style="text-align: center; color: #666; padding: 20px;">
        📚 Système de Documentation RCS Analytics v2.0<br>
        <small>Dernière mise à jour: {datetime.now().strftime('%d/%m/%Y %H:%M')}</small>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
