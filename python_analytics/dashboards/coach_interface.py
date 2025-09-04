"""
Racing Club de Strasbourg - Analytics Temps Réel
===============================================

Plateforme d'analyse exclusive RCS avec données réelles et formules statistiques avancées.
Récupération automatique des actualités, stats et analyses en temps réel.

Auteur: Football Analytics Platform  
Équipe: Racing Club de Strasbourg - Données Réelles
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import sys
import os
import requests
import warnings
warnings.filterwarnings('ignore')

# Import du module de collecte de données RCS
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'modules'))

# Configuration de la page Streamlit
st.set_page_config(
    page_title="🔵⚪ Racing Club de Strasbourg - Analytics Temps Réel",
    page_icon="🔵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialisation du collecteur de données RCS
@st.cache_resource
def initialiser_collecteur():
    """Initialise le collecteur de données RCS"""
    try:
        from collecteur_donnees_rcs import CollecteurDonneesRCS, AnalyseurStatistiquesRCS
        collecteur = CollecteurDonneesRCS()
        analyseur = AnalyseurStatistiquesRCS(collecteur)
        return collecteur, analyseur
    except ImportError:
        st.error("⚠️ Module de collecte non disponible - Mode dégradé activé")
        return None, None

# CSS personnalisé RCS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #0066CC;
        text-align: center;
        background: linear-gradient(90deg, #0066CC, #FFFFFF, #0066CC);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .metric-rcs {
        background: linear-gradient(135deg, #0066CC 0%, #004499 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    .rcs-card {
        background: linear-gradient(90deg, #0066CC, #FFFFFF);
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #0066CC;
        margin: 1rem 0;
    }
    .success-card {
        background: #51cf66;
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 0.5rem 0;
    }
    .stSelectbox > div > div {
        background-color: #f0f8ff;
    }
    h1, h2, h3 {
        color: #0066CC;
    }
</style>
""", unsafe_allow_html=True)

# Fonction de génération de données simulées pour Streamlit Cloud
@st.cache_data
def generate_demo_data():
    """Génère des données de démonstration pour le dashboard"""
    return {
        'status': 'demo_mode',
        'message': 'Utilisation de données simulées pour la démonstration Streamlit Cloud'
    }

# Fonction de chargement des données équipes
@st.cache_data
def load_teams():
    """Charge la liste des équipes"""
    # Données de démonstration
    return pd.DataFrame({
        'team_id': ['team_1', 'team_2', 'team_3'],
        'name': ['Paris Saint-Germain', 'Olympique de Marseille', 'AS Monaco'],
        'league': ['Ligue 1', 'Ligue 1', 'Ligue 1']
    })

# Fonction de chargement des joueurs
@st.cache_data  
def load_players(team_id=None):
    """Charge la liste des joueurs"""
    # Données de démonstration
    players_data = {
        'team_1': [
            {'player_id': 'p1', 'name': 'Kylian Mbappé', 'position': 'ST'},
            {'player_id': 'p2', 'name': 'Marco Verratti', 'position': 'CM'},
            {'player_id': 'p3', 'name': 'Marquinhos', 'position': 'CB'}
        ],
        'team_2': [
            {'player_id': 'p4', 'name': 'Dimitri Payet', 'position': 'AM'},
            {'player_id': 'p5', 'name': 'Mattéo Guendouzi', 'position': 'CM'},
            {'player_id': 'p6', 'name': 'William Saliba', 'position': 'CB'}
        ]
    }
    
    if team_id and team_id in players_data:
        return pd.DataFrame(players_data[team_id])
    
    # Retourner tous les joueurs si pas d'équipe spécifiée
    all_players = []
    for team_players in players_data.values():
        all_players.extend(team_players)
    
    return pd.DataFrame(all_players)

# Données effectif réel Racing Club de Strasbourg 2024-2025
def obtenir_effectif_rcs():
    """Retourne l'effectif actuel du RCS avec données réelles"""
    effectif_data = [
        # Gardiens
        {"nom": "Matz Sels", "age": 32, "poste": "GB", "valeur_marche": 4.0, "titulaire": True, "nationalite": "Belgique"},
        {"nom": "Alaa Bellaarouch", "age": 20, "poste": "GB", "valeur_marche": 0.5, "titulaire": False, "nationalite": "France"},
        
        # Défenseurs
        {"nom": "Guela Doué", "age": 22, "poste": "DD", "valeur_marche": 8.0, "titulaire": True, "nationalite": "Côte d'Ivoire"},
        {"nom": "Abakar Sylla", "age": 25, "poste": "DC", "valeur_marche": 3.5, "titulaire": True, "nationalite": "France"},
        {"nom": "Saïdou Sow", "age": 22, "poste": "DC", "valeur_marche": 4.0, "titulaire": True, "nationalite": "Guinée"},
        {"nom": "Mamadou Sarr", "age": 26, "poste": "DG", "valeur_marche": 3.0, "titulaire": True, "nationalite": "Sénégal"},
        {"nom": "Marvin Senaya", "age": 22, "poste": "DD", "valeur_marche": 2.5, "titulaire": False, "nationalite": "France"},
        {"nom": "Ismaël Doukouré", "age": 23, "poste": "DC", "valeur_marche": 2.0, "titulaire": False, "nationalite": "France"},
        
        # Milieux
        {"nom": "Habib Diarra", "age": 20, "poste": "MC", "valeur_marche": 12.0, "titulaire": True, "nationalite": "Sénégal"},
        {"nom": "Andrey Santos", "age": 20, "poste": "MDC", "valeur_marche": 8.0, "titulaire": True, "nationalite": "Brésil"},
        {"nom": "Dilane Bakwa", "age": 21, "poste": "AD", "valeur_marche": 10.0, "titulaire": True, "nationalite": "France"},
        {"nom": "Sebastian Nanasi", "age": 22, "poste": "AG", "valeur_marche": 6.0, "titulaire": True, "nationalite": "Suède"},
        {"nom": "Caleb Wiley", "age": 19, "poste": "DG", "valeur_marche": 4.0, "titulaire": False, "nationalite": "USA"},
        {"nom": "Pape Diong", "age": 20, "poste": "MC", "valeur_marche": 1.5, "titulaire": False, "nationalite": "Sénégal"},
        
        # Attaquants
        {"nom": "Emanuel Emegha", "age": 21, "poste": "BU", "valeur_marche": 8.0, "titulaire": True, "nationalite": "Pays-Bas"},
        {"nom": "Félix Lemaréchal", "age": 19, "poste": "MOC", "valeur_marche": 4.0, "titulaire": False, "nationalite": "France"},
        {"nom": "Abdoul Ouattara", "age": 18, "poste": "AD", "valeur_marche": 2.0, "titulaire": False, "nationalite": "France"},
        {"nom": "Moïse Sahi", "age": 18, "poste": "BU", "valeur_marche": 1.0, "titulaire": False, "nationalite": "France"},
        {"nom": "Jeremy Sebas", "age": 19, "poste": "BU", "valeur_marche": 0.8, "titulaire": False, "nationalite": "France"}
    ]
    
    return pd.DataFrame(effectif_data)

def calculer_xg_rcs(distance, situation, joueur):
    """Calcule l'xG adapté au style RCS"""
    # xG de base selon distance
    xg_base = max(0.05, 1.0 - (distance / 40))
    
    # Bonus situation (style contre-attaque RCS)
    if situation == "contre_attaque":
        xg_base *= 1.35
    elif situation == "corner":
        xg_base *= 0.9
    elif situation == "coup_franc":
        xg_base *= 0.8
    
    # Bonus finisseurs RCS
    bonus_finisseurs = {
        "Emanuel Emegha": 1.15,
        "Dilane Bakwa": 1.10,
        "Habib Diarra": 1.08,
        "Sebastian Nanasi": 1.05
    }
    
    if joueur in bonus_finisseurs:
        xg_base *= bonus_finisseurs[joueur]
    
    return min(0.95, xg_base)

def obtenir_composition_ideale_rcs():
    """Composition idéale 4-2-3-1 RCS"""
    return {
        "formation": "4-2-3-1",
        "gardien": "Matz Sels",
        "defenseurs": ["Guela Doué", "Abakar Sylla", "Saïdou Sow", "Mamadou Sarr"],
        "milieux_defensifs": ["Andrey Santos", "Habib Diarra"],
        "milieux_offensifs": ["Dilane Bakwa", "Sebastian Nanasi", "Caleb Wiley"],
        "attaquant": "Emanuel Emegha"
    }

# Fonction principale du dashboard
def main():
    """Interface principale du dashboard"""
    
    # Header principal
    st.markdown('<h1 class="main-header">⚽ Football Analytics Dashboard</h1>', 
                unsafe_allow_html=True)
    
    # Sidebar pour navigation
    st.sidebar.title("🎯 Navigation")
    page = st.sidebar.selectbox(
        "Choisir une vue",
        ["🏠 Vue d'ensemble", "👤 Analyse Joueur", "⚽ Analyse Équipe", 
         "📈 Performance Temps Réel", "🔍 Scouting & Recrutement", "📊 Rapports"]
    )
    
    # Initialisation des données de démonstration
    demo_data = generate_demo_data()
    
    # Message d'information pour Streamlit Cloud
    st.info("🎮 Mode Démonstration Streamlit Cloud - Données simulées pour présentation")
    
    # Navigation entre les pages
    if page == "🏠 Vue d'ensemble":
        show_overview()
    elif page == "👤 Analyse Joueur":
        show_player_analysis()
    elif page == "⚽ Analyse Équipe":
        show_team_analysis()
    elif page == "📈 Performance Temps Réel":
        show_realtime_performance()
    elif page == "🔍 Scouting & Recrutement":
        show_scouting_analysis()
    elif page == "📊 Rapports":
        show_reports()

def show_overview():
    """Affiche la vue d'ensemble du dashboard"""
    
    st.header("📊 Vue d'ensemble - Tableau de Bord")
    
    # Métriques clés en colonnes
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>Matchs Joués</h3>
            <h2>15/20</h2>
            <p>Saison 2024-25</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>Points</h3>
            <h2>32</h2>
            <p>7ème position</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>xG Pour/Contre</h3>
            <h2>24.5 / 18.2</h2>
            <p>+6.3 différentiel</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h3>PPDA Moyen</h3>
            <h2>11.4</h2>
            <p>Pressing intense</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Graphiques de performance
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Évolution des Points")
        
        # Données simulées de performance
        dates = pd.date_range('2024-08-01', periods=15, freq='W')
        points_cumules = np.cumsum(np.random.choice([0, 1, 3], 15, p=[0.2, 0.3, 0.5]))
        
        fig = px.line(x=dates, y=points_cumules, 
                     title="Points cumulés par journée")
        fig.update_layout(xaxis_title="Date", yaxis_title="Points")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("⚽ Performance xG")
        
        # Données xG simulées
        matches = [f"J{i}" for i in range(1, 16)]
        xg_for = np.random.uniform(0.5, 3.5, 15)
        xg_against = np.random.uniform(0.3, 2.8, 15)
        
        fig = go.Figure()
        fig.add_trace(go.Bar(name='xG Pour', x=matches, y=xg_for, marker_color='lightblue'))
        fig.add_trace(go.Bar(name='xG Contre', x=matches, y=-xg_against, marker_color='lightcoral'))
        fig.update_layout(title="Expected Goals par match", barmode='relative')
        st.plotly_chart(fig, use_container_width=True)
    
    # Alertes et notifications
    st.header("🚨 Alertes & Notifications")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="warning-card">
            <h4>⚠️ Risque de Blessure</h4>
            <p><strong>Kylian Mbappé</strong></p>
            <p>Charge d'entraînement élevée (95%)</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="success-card">
            <h4>✅ Forme Excellente</h4>
            <p><strong>Marco Verratti</strong></p>
            <p>Note moyenne : 8.2/10 (5 derniers matchs)</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="warning-card">
            <h4>📉 Baisse de Forme</h4>
            <p><strong>Défense Centrale</strong></p>
            <p>xGA en hausse : +0.4 par match</p>
        </div>
        """, unsafe_allow_html=True)

def show_player_analysis():
    """Interface d'analyse des joueurs"""
    
    st.header("👤 Analyse Individuelle des Joueurs")
    
    # Sélection d'équipe et joueur
    col1, col2 = st.columns(2)
    
    with col1:
        teams = load_teams()
        selected_team = st.selectbox(
            "Choisir une équipe",
            teams['team_id'].tolist(),
            format_func=lambda x: teams[teams['team_id'] == x]['name'].iloc[0]
        )
    
    with col2:
        players = load_players(selected_team)
        selected_player = st.selectbox(
            "Choisir un joueur",
            players['player_id'].tolist(),
            format_func=lambda x: players[players['player_id'] == x]['name'].iloc[0]
        )
    
    # Analyse de forme du joueur sélectionné
    if selected_player:
        player_name = players[players['player_id'] == selected_player]['name'].iloc[0]
        st.subheader(f"📊 Analyse de {player_name}")
        
        # Métriques de performance (données simulées)
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Note Moyenne", "7.8", "↗️ +0.3")
        with col2:
            st.metric("Goals/90min", "0.72", "↘️ -0.1")
        with col3:
            st.metric("xG/90min", "0.68", "↗️ +0.05")
        with col4:
            st.metric("Précision Passes", "89.2%", "↗️ +1.5%")
        
        # Graphique radar des compétences
        st.subheader("🎯 Profil de Compétences - Graphique Radar")
        
        categories = ['Finition', 'Passes', 'Défense', 'Physique', 'Vitesse', 'Technique']
        values = np.random.randint(60, 95, len(categories))
        
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name=player_name,
            line_color='blue'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )),
            showlegend=True,
            title="Profil de Compétences"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Évolution des performances
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📈 Évolution des Notes")
            dates = pd.date_range('2024-09-01', periods=10, freq='W')
            ratings = np.random.uniform(6.5, 9.0, 10)
            
            fig = px.line(x=dates, y=ratings, title="Notes des 10 derniers matchs")
            fig.add_hline(y=ratings.mean(), line_dash="dash", 
                         annotation_text=f"Moyenne: {ratings.mean():.1f}")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("⚽ Statistiques Offensives")
            stats_data = pd.DataFrame({
                'Match': [f'J{i}' for i in range(1, 11)],
                'Goals': np.random.poisson(0.5, 10),
                'xG': np.random.uniform(0.1, 1.2, 10),
                'Assists': np.random.poisson(0.3, 10)
            })
            
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            fig.add_trace(go.Bar(name='Goals', x=stats_data['Match'], y=stats_data['Goals']))
            fig.add_trace(go.Scatter(name='xG', x=stats_data['Match'], y=stats_data['xG'], 
                                   mode='lines+markers'), secondary_y=True)
            
            fig.update_xaxes(title_text="Matchs")
            fig.update_yaxes(title_text="Goals", secondary_y=False)
            fig.update_yaxes(title_text="Expected Goals", secondary_y=True)
            
            st.plotly_chart(fig, use_container_width=True)

def show_team_analysis():
    """Interface d'analyse d'équipe"""
    
    st.header("⚽ Analyse Tactique d'Équipe")
    
    # Sélection d'équipe
    teams = load_teams()
    selected_team = st.selectbox(
        "Analyser l'équipe",
        teams['team_id'].tolist(),
        format_func=lambda x: teams[teams['team_id'] == x]['name'].iloc[0]
    )
    
    team_name = teams[teams['team_id'] == selected_team]['name'].iloc[0]
    st.subheader(f"📊 Analyse de {team_name}")
    
    # Métriques d'équipe
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Possession Moyenne", "58.3%", "↗️ +2.1%")
    with col2:
        st.metric("PPDA", "11.4", "↘️ -0.8")
    with col3:
        st.metric("Passes/Match", "542", "↗️ +15")
    with col4:
        st.metric("Précision Passes", "87.1%", "↗️ +1.2%")
    
    # Analyses tactiques
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎯 Formation et Positions Moyennes")
        
        # Simulation du terrain avec positions
        fig = go.Figure()
        
        # Positions moyennes simulées (11 joueurs)
        positions_x = [10, 25, 25, 25, 25, 45, 45, 45, 70, 70, 85]
        positions_y = [50, 20, 35, 50, 65, 30, 50, 70, 35, 65, 50]
        names = ['GK', 'LB', 'CB', 'CB', 'RB', 'DM', 'CM', 'CM', 'LW', 'RW', 'ST']
        
        fig.add_trace(go.Scatter(
            x=positions_x, y=positions_y,
            mode='markers+text',
            text=names,
            textposition="middle center",
            marker=dict(size=30, color='lightblue', line=dict(width=2, color='blue')),
            name="Positions Moyennes"
        ))
        
        # Terrain de football
        fig.add_shape(type="rect", x0=0, y0=0, x1=100, y1=100, 
                     line=dict(color="green", width=3))
        fig.add_shape(type="line", x0=50, y0=0, x1=50, y1=100, 
                     line=dict(color="white", width=2))
        
        fig.update_layout(
            title="Formation 4-3-3 - Positions Moyennes",
            xaxis=dict(range=[0, 100], showgrid=False),
            yaxis=dict(range=[0, 100], showgrid=False),
            showlegend=False,
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🔗 Réseau de Passes")
        
        # Matrice de connexions de passes (simulation)
        players_network = ['Verratti', 'Marquinhos', 'Mbappé', 'Neymar', 'Hakimi']
        pass_matrix = np.random.randint(10, 50, (5, 5))
        np.fill_diagonal(pass_matrix, 0)
        
        fig = px.imshow(pass_matrix, 
                       x=players_network, y=players_network,
                       color_continuous_scale='Blues',
                       title="Intensité des Connexions de Passes")
        fig.update_layout(height=400)
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Analyse des phases de jeu
    st.subheader("⚡ Analyse des Phases de Jeu")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h4>🛡️ Phase Défensive</h4>
            <p><strong>Récupérations/Match:</strong> 52.3</p>
            <p><strong>Pressing Success:</strong> 31.2%</p>
            <p><strong>Duels Aériens:</strong> 58.7%</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h4>🔄 Transition</h4>
            <p><strong>Contre-attaques:</strong> 8.2/match</p>
            <p><strong>Vitesse Transition:</strong> 2.1s</p>
            <p><strong>Changements Jeu:</strong> 12.4</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h4>⚔️ Phase Offensive</h4>
            <p><strong>Tirs/Match:</strong> 14.7</p>
            <p><strong>Occasions Créées:</strong> 11.3</p>
            <p><strong>Centres Réussis:</strong> 23.1%</p>
        </div>
        """, unsafe_allow_html=True)

def show_realtime_performance():
    """Interface de performance en temps réel"""
    
    st.header("📈 Performance Temps Réel")
    
    st.info("🔴 LIVE - Match en cours : PSG vs OM")
    
    # Score et temps
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div style="text-align: center; font-size: 2rem; margin: 1rem 0;">
            <strong>PSG 2 - 1 OM</strong><br>
            <span style="font-size: 1rem; color: #666;">72' - Deuxième Mi-temps</span>
        </div>
        """, unsafe_allow_html=True)
    
    # Métriques live
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("xG", "PSG 1.8 - 1.2 OM", "↗️")
    with col2:
        st.metric("Possession", "PSG 62% - 38% OM", "")
    with col3:
        st.metric("Tirs", "PSG 8 - 6 OM", "")
    with col4:
        st.metric("Passes", "PSG 421 - 264 OM", "")
    
    # Évolution en temps réel
    st.subheader("📊 Évolution du Match")
    
    # Simulation de données temps réel
    minutes = list(range(0, 73))
    psg_xg = np.cumsum(np.random.exponential(0.03, 73))
    om_xg = np.cumsum(np.random.exponential(0.02, 73))
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=minutes, y=psg_xg, name='PSG xG', line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=minutes, y=om_xg, name='OM xG', line=dict(color='red')))
    
    # Ajout des buts
    goals_psg = [23, 54]  # Minutes des buts
    goals_om = [31]
    
    for goal_min in goals_psg:
        fig.add_vline(x=goal_min, line_dash="dash", line_color="blue", 
                     annotation_text=f"⚽ PSG {goal_min}'")
    
    for goal_min in goals_om:
        fig.add_vline(x=goal_min, line_dash="dash", line_color="red", 
                     annotation_text=f"⚽ OM {goal_min}'")
    
    fig.update_layout(title="Évolution xG pendant le match", 
                     xaxis_title="Minutes", yaxis_title="Expected Goals")
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Heatmap des actions
    st.subheader("🔥 Zones d'Action - Dernières 15 minutes")
    
    # Simulation heatmap
    x_coords = np.random.uniform(0, 100, 100)
    y_coords = np.random.uniform(0, 100, 100)
    
    fig = px.density_heatmap(x=x_coords, y=y_coords, 
                            title="Densité des Actions (58'-72')")
    fig.update_layout(height=300)
    
    st.plotly_chart(fig, use_container_width=True)

def show_scouting_analysis():
    """Interface de scouting et recrutement"""
    
    st.header("🔍 Scouting & Recrutement")
    
    # Critères de recherche
    st.subheader("🎯 Critères de Recherche")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        position = st.selectbox("Position", ["Tous", "ST", "AM", "CM", "CB", "GK"])
    with col2:
        age_range = st.slider("Âge", 16, 35, (20, 28))
    with col3:
        budget_max = st.number_input("Budget Max (M€)", 0, 200, 50)
    with col4:
        league = st.selectbox("Championnat", ["Tous", "Ligue 1", "Premier League", "La Liga"])
    
    # Résultats de recherche (simulation)
    st.subheader("📋 Résultats de Recherche")
    
    # Données simulées de joueurs
    scout_data = pd.DataFrame({
        'Joueur': ['Victor Osimhen', 'Jude Bellingham', 'Pedri González', 'Aurélien Tchouaméni'],
        'Âge': [25, 21, 22, 24],
        'Position': ['ST', 'CM', 'AM', 'DM'],
        'Équipe': ['Napoli', 'Real Madrid', 'FC Barcelona', 'Real Madrid'],
        'Valeur (M€)': [120, 150, 80, 90],
        'Note Scout': [88, 92, 85, 87],
        'Goals/90': [0.71, 0.12, 0.08, 0.04],
        'xG/90': [0.68, 0.15, 0.12, 0.06],
        'Passes/90': [25.3, 68.2, 72.4, 58.7]
    })
    
    # Filtrage interactif
    filtered_data = scout_data.copy()
    
    if position != "Tous":
        filtered_data = filtered_data[filtered_data['Position'] == position]
    
    filtered_data = filtered_data[
        (filtered_data['Âge'] >= age_range[0]) & 
        (filtered_data['Âge'] <= age_range[1]) &
        (filtered_data['Valeur (M€)'] <= budget_max)
    ]
    
    st.dataframe(filtered_data, use_container_width=True)
    
    # Analyse comparative
    if len(filtered_data) > 1:
        st.subheader("📊 Comparaison des Candidats")
        
        # Graphique radar comparatif
        selected_players = st.multiselect(
            "Sélectionner des joueurs à comparer",
            filtered_data['Joueur'].tolist(),
            default=filtered_data['Joueur'].tolist()[:3]
        )
        
        if selected_players:
            fig = go.Figure()
            
            metrics = ['Note Scout', 'Goals/90', 'xG/90', 'Passes/90']
            
            for player in selected_players:
                player_data = filtered_data[filtered_data['Joueur'] == player].iloc[0]
                values = [
                    player_data['Note Scout'],
                    player_data['Goals/90'] * 50,  # Normalisation
                    player_data['xG/90'] * 50,
                    player_data['Passes/90']
                ]
                
                fig.add_trace(go.Scatterpolar(
                    r=values,
                    theta=metrics,
                    fill='toself',
                    name=player,
                    opacity=0.7
                ))
            
            fig.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                showlegend=True,
                title="Comparaison Multi-Critères"
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    # Recommandations IA
    st.subheader("🤖 Recommandations IA")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="success-card">
            <h4>⭐ Top Recommandation</h4>
            <p><strong>Jude Bellingham</strong></p>
            <p>Compatibilité: 94%</p>
            <p>Profil: Milieu complet, jeune, grande marge de progression</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h4>💡 Opportunité Marché</h4>
            <p><strong>Pedri González</strong></p>
            <p>Valeur estimée: 20% sous-évaluée</p>
            <p>Fenêtre optimale: Été 2024</p>
        </div>
        """, unsafe_allow_html=True)

def show_reports():
    """Interface de génération de rapports"""
    
    st.header("📊 Génération de Rapports")
    
    # Types de rapports
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📋 Rapports Disponibles")
        
        report_type = st.selectbox(
            "Type de rapport",
            ["Rapport Post-Match", "Analyse Mensuelle", "Bilan de Saison", 
             "Rapport de Scouting", "Analyse Blessures"]
        )
        
        date_range = st.date_input(
            "Période d'analyse",
            value=[datetime.now() - timedelta(days=30), datetime.now()]
        )
        
        if st.button("📄 Générer le Rapport"):
            st.success("✅ Rapport généré avec succès !")
            
            # Simulation de contenu de rapport
            if report_type == "Rapport Post-Match":
                show_post_match_report()
            elif report_type == "Analyse Mensuelle":
                show_monthly_report()
    
    with col2:
        st.subheader("📈 Aperçu Rapide")
        
        # KPI de la période
        st.markdown("""
        **Période :** Dernier mois
        
        **Points clés :**
        - 🟢 Amélioration offensive (+15% xG)
        - 🟡 Stabilité défensive 
        - 🔴 Baisse de forme de 3 joueurs clés
        - ⚪ 2 nouvelles blessures à surveiller
        """)
        
        # Graphique de synthèse
        dates = pd.date_range('2024-10-01', periods=30, freq='D')
        performance_score = 70 + np.cumsum(np.random.normal(0, 2, 30))
        
        fig = px.line(x=dates, y=performance_score, 
                     title="Indice de Performance Équipe")
        fig.add_hline(y=75, line_dash="dash", annotation_text="Objectif")
        st.plotly_chart(fig, use_container_width=True)

def show_post_match_report():
    """Affiche un rapport post-match détaillé"""
    
    st.markdown("""
    ### 📊 Rapport Post-Match Détaillé
    **PSG 2 - 1 OM | 15 Novembre 2024**
    
    #### 🎯 Résumé Exécutif
    - Victoire méritée avec domination territoriale
    - Performance offensive efficace (xG: 2.1 vs 1.2)
    - Pressing haute intensité réussi (PPDA: 9.8)
    
    #### 📈 Statistiques Clés
    | Métrique | PSG | OM |
    |----------|-----|-----|
    | Possession | 64% | 36% |
    | Tirs | 16 | 9 |
    | Tirs cadrés | 7 | 4 |
    | xG | 2.14 | 1.23 |
    | Passes réussies | 521/587 (89%) | 298/376 (79%) |
    
    #### ⭐ Joueurs Performants
    1. **Mbappé (9.2/10)** - 1 but, 1 passe décisive, 0.89 xG
    2. **Verratti (8.7/10)** - 94% passes réussies, 3 passes clés
    3. **Marquinhos (8.1/10)** - 6 récupérations, 100% duels aériens
    
    #### 🔧 Points d'Amélioration
    - Efficacité défensive sur coups de pied arrêtés
    - Gestion du tempo en fin de match
    - Rotation plus fréquente du côté droit
    """)

def show_monthly_report():
    """Affiche un rapport mensuel"""
    
    st.markdown("""
    ### 📅 Analyse Mensuelle - Novembre 2024
    
    #### 📊 Bilan du Mois
    - **Matchs joués :** 6 (4V, 1N, 1D)
    - **Points récoltés :** 13/18 (72.2%)
    - **Évolution classement :** 7ème → 5ème (+2)
    
    #### 🎯 Performance Offensive
    - Goals marqués : 12 (moyenne 2.0/match)
    - xG généré : 13.4 (efficacité 89.6%)
    - Meilleur buteur : Mbappé (5 goals)
    
    #### 🛡️ Performance Défensive  
    - Goals encaissés : 7 (moyenne 1.17/match)
    - xGA concédé : 8.2 (surperformance +1.2)
    - Clean sheets : 2/6 matchs
    
    #### 👥 État de Forme Joueurs
    - **En progression :** Verratti, Hakimi, Ramos
    - **Forme stable :** Marquinhos, Donnarumma
    - **À surveiller :** Neymar (baisse régularité)
    """)

# Point d'entrée de l'application
if __name__ == "__main__":
    main()
