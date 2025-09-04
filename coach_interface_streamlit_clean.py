"""
Dashboard Streamlit pour Staff Technique - Version Streamlit Cloud
================================================================

Interface interactive pour les entraîneurs et staff technique.
Version optimisée pour déploiement Streamlit Cloud sans dépendances PostgreSQL.

Author: Football Analytics Platform
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

# Configuration de la page Streamlit
st.set_page_config(
    page_title="⚽ Football Analytics Dashboard",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Style CSS personnalisé
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1e3d59;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    .warning-card {
        background: #ff6b6b;
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 0.5rem 0;
    }
    .success-card {
        background: #51cf66;
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Fonction de génération de données simulées
@st.cache_data
def generate_demo_data():
    """Génère des données de démonstration pour le dashboard"""
    return {
        'status': 'demo_mode',
        'message': 'Utilisation de données simulées pour la démonstration'
    }

# Fonction de chargement des données équipes
@st.cache_data
def load_teams():
    """Charge la liste des équipes"""
    return pd.DataFrame({
        'team_id': ['team_1', 'team_2', 'team_3'],
        'name': ['Paris Saint-Germain', 'Olympique de Marseille', 'AS Monaco'],
        'league': ['Ligue 1', 'Ligue 1', 'Ligue 1'],
        'matches_played': [15, 14, 16],
        'points': [32, 28, 30]
    })

# Fonction de chargement des joueurs
@st.cache_data  
def load_players(team_id=None):
    """Charge la liste des joueurs"""
    players_data = {
        'player_id': ['p1', 'p2', 'p3', 'p4', 'p5'],
        'name': ['Kylian Mbappé', 'Neymar Jr', 'Marco Verratti', 'Presnel Kimpembe', 'Gianluigi Donnarumma'],
        'position': ['Attaquant', 'Ailier', 'Milieu', 'Défenseur', 'Gardien'],
        'team_id': ['team_1', 'team_1', 'team_1', 'team_1', 'team_1'],
        'goals': [12, 8, 2, 1, 0],
        'assists': [4, 6, 8, 2, 1],
        'minutes_played': [1200, 1100, 1300, 1250, 1350]
    }
    return pd.DataFrame(players_data)

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
    
    # Message d'information
    st.info("🎮 Mode Démonstration - Données simulées pour présentation")
    
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
            <h3>⚽ Buts marqués</h3>
            <h2>23</h2>
            <p>+15% vs saison passée</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>🎯 xG moyen</h3>
            <h2>1.8</h2>
            <p>Excellente finition</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>🛡️ Clean Sheets</h3>
            <h2>8</h2>
            <p>Défense solide</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h3>📈 Points</h3>
            <h2>32</h2>
            <p>2ème place</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Graphiques de performance
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Évolution des performances")
        
        # Simulation de données de performance
        weeks = list(range(1, 16))
        performance = np.cumsum(np.random.normal(2, 0.5, 15))
        
        fig = px.line(x=weeks, y=performance, title="Points cumulés par journée")
        fig.update_layout(xaxis_title="Journée", yaxis_title="Points")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("⚽ Répartition des buts")
        
        # Graphique en secteurs des buteurs
        players = ['Mbappé', 'Neymar', 'Messi', 'Autres']
        goals = [12, 8, 6, 7]
        
        fig = px.pie(values=goals, names=players, title="Répartition des buts par joueur")
        st.plotly_chart(fig, use_container_width=True)

def show_player_analysis():
    """Interface d'analyse des joueurs"""
    
    st.header("👤 Analyse Individuelle des Joueurs")
    
    # Sélection de joueur
    players = load_players()
    selected_player = st.selectbox(
        "Sélectionner un joueur",
        players['player_id'].tolist(),
        format_func=lambda x: players[players['player_id'] == x]['name'].iloc[0]
    )
    
    player_data = players[players['player_id'] == selected_player].iloc[0]
    
    st.subheader(f"📊 Profil de {player_data['name']}")
    
    # Métriques du joueur
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("⚽ Buts", player_data['goals'])
    with col2:
        st.metric("🎯 Passes décisives", player_data['assists'])
    with col3:
        st.metric("⏱️ Minutes jouées", player_data['minutes_played'])
    with col4:
        st.metric("📍 Position", player_data['position'])
    
    # Graphique radar des compétences
    st.subheader("🕷️ Radar des Compétences")
    
    categories = ['Vitesse', 'Technique', 'Physique', 'Mental', 'Tactique']
    values = np.random.randint(60, 95, 5)
    
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name=player_data['name']
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=True,
        title="Évaluation des compétences"
    )
    
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
        st.metric("🏆 Classement", "2ème", "↑ 1")
    with col2:
        st.metric("⚽ Buts pour", "45", "+12")
    with col3:
        st.metric("🛡️ Buts contre", "18", "-5")
    with col4:
        st.metric("📊 Possession", "62%", "+3%")
    
    # Formation tactique
    st.subheader("⚽ Formation Tactique")
    
    formation_data = {
        'Position': ['GK', 'DF', 'DF', 'DF', 'DF', 'MF', 'MF', 'MF', 'FW', 'FW', 'FW'],
        'X': [5, 20, 30, 40, 20, 35, 50, 65, 45, 70, 55],
        'Y': [50, 20, 50, 80, 50, 30, 50, 70, 20, 50, 80],
        'Joueur': ['Donnarumma', 'Kimpembe', 'Marquinhos', 'Hakimi', 'Mendes',
                  'Verratti', 'Vitinha', 'Ruiz', 'Mbappé', 'Messi', 'Neymar']
    }
    
    fig = px.scatter(formation_data, x='X', y='Y', text='Joueur',
                    title="Formation 4-3-3",
                    range_x=[0, 100], range_y=[0, 100])
    fig.update_traces(textposition="middle center", marker_size=15)
    fig.update_layout(height=400)
    
    st.plotly_chart(fig, use_container_width=True)

def show_realtime_performance():
    """Interface de performance en temps réel"""
    
    st.header("📈 Performance Temps Réel")
    
    st.info("🔴 SIMULATION - Données temps réel en mode démonstration")
    
    # Métriques live simulées
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("⚽ Tirs", "12", "+2")
    with col2:
        st.metric("🎯 Tirs cadrés", "6", "+1")
    with col3:
        st.metric("📊 Possession", "58%", "-3%")
    with col4:
        st.metric("🏃 Distance parcourue", "108.5 km", "+2.1")
    
    # Évolution temps réel
    st.subheader("📊 Évolution du Match")
    
    minutes = list(range(0, 61))
    metric_values = np.cumsum(np.random.normal(0.1, 0.3, 61))
    
    fig = px.line(x=minutes, y=metric_values, title="Indice de performance temps réel")
    fig.update_layout(xaxis_title="Minutes", yaxis_title="Performance")
    
    st.plotly_chart(fig, use_container_width=True)

def show_scouting_analysis():
    """Interface de scouting et recrutement"""
    
    st.header("🔍 Scouting & Recrutement")
    
    st.subheader("🎯 Recherche de Joueurs")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        position = st.selectbox("Position", ["Tous", "Gardien", "Défenseur", "Milieu", "Attaquant"])
    
    with col2:
        age_range = st.slider("Âge", 16, 35, (20, 28))
    
    with col3:
        budget = st.number_input("Budget max (M€)", 0, 200, 50)
    
    # Résultats de recherche simulés
    st.subheader("📋 Joueurs Recommandés")
    
    scouting_data = {
        'Joueur': ['Victor Osimhen', 'Pedri', 'Jude Bellingham', 'Rafael Leão'],
        'Âge': [24, 21, 20, 24],
        'Position': ['Attaquant', 'Milieu', 'Milieu', 'Ailier'],
        'Club': ['Naples', 'Barcelone', 'Dortmund', 'Milan'],
        'Valeur (M€)': [100, 80, 120, 90],
        'Note Scouting': [88, 85, 92, 84]
    }
    
    df_scouting = pd.DataFrame(scouting_data)
    st.dataframe(df_scouting, use_container_width=True)

def show_reports():
    """Interface de rapports"""
    
    st.header("📊 Rapports et Analyses")
    
    st.subheader("📈 Rapport de Performance Mensuel")
    
    report_data = {
        'Métrique': ['Buts marqués', 'Clean sheets', 'Possession moyenne', 'Passes réussies', 'Duels gagnés'],
        'Valeur': [15, 3, '65%', '89%', '68%'],
        'Évolution': ['+20%', '+50%', '+2%', '+3%', '+8%']
    }
    
    df_report = pd.DataFrame(report_data)
    st.table(df_report)
    
    # Graphique de tendance
    st.subheader("📊 Tendance Performance")
    
    months = ['Sep', 'Oct', 'Nov', 'Déc', 'Jan']
    performance_trend = [75, 82, 78, 88, 92]
    
    fig = px.bar(x=months, y=performance_trend, title="Évolution de la performance par mois")
    fig.update_layout(xaxis_title="Mois", yaxis_title="Score Performance (%)")
    
    st.plotly_chart(fig, use_container_width=True)

# Point d'entrée de l'application
if __name__ == "__main__":
    main()
