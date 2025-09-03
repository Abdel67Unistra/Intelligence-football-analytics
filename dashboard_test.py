#!/usr/bin/env python3
"""
Dashboard Streamlit Simplifié - Football Analytics
================================================
Version de test pour diagnostiquer les problèmes
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Configuration de la page
st.set_page_config(
    page_title="⚽ Football Analytics - Test",
    page_icon="⚽",
    layout="wide"
)

def main():
    """Interface principale simplifiée"""
    
    # Header principal
    st.title("⚽ Football Analytics Platform")
    st.markdown("### Dashboard d'Intelligence Footballistique")
    
    # Test de base
    st.success("✅ Dashboard Streamlit opérationnel !")
    
    # Sidebar
    st.sidebar.title("🎯 Navigation")
    page = st.sidebar.selectbox(
        "Choisir une section:",
        ["🏠 Accueil", "📊 Test Métriques", "👤 Test Joueur", "🎯 Test Graphiques"]
    )
    
    if page == "🏠 Accueil":
        show_homepage()
    elif page == "📊 Test Métriques":
        show_metrics_test()
    elif page == "👤 Test Joueur":
        show_player_test()
    elif page == "🎯 Test Graphiques":
        show_charts_test()

def show_homepage():
    """Page d'accueil"""
    
    st.markdown("## 🎯 Bienvenue sur la Plateforme Football Analytics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("📊 Modules", "5", "Opérationnels")
    
    with col2:
        st.metric("⚽ Métriques", "15+", "Avancées")
        
    with col3:
        st.metric("🤖 IA", "100%", "Fonctionnelle")
    
    st.markdown("---")
    
    st.markdown("""
    ### 🚀 Fonctionnalités Principales
    
    - **📈 Analytics de Performance** : Métriques xG, xA, PPDA
    - **🎯 Analyses Tactiques** : Formations, pressing, possession
    - **🔍 Scouting IA** : Recommandations joueurs avec ML
    - **📊 Visualisations** : Graphiques interactifs et rapports
    
    ### 🎮 Navigation
    Utilisez la barre latérale pour explorer les différentes sections.
    """)

def show_metrics_test():
    """Test des métriques football"""
    
    st.markdown("## ⚽ Test des Métriques Football")
    
    # Générer données test
    np.random.seed(42)
    
    # Données de tirs
    shots_data = pd.DataFrame({
        'joueur': ['Mbappé', 'Haaland', 'Kane', 'Benzema', 'Osimhen'] * 4,
        'x': np.random.uniform(10, 25, 20),
        'y': np.random.uniform(-10, 10, 20),
        'distance': np.random.uniform(8, 25, 20),
        'angle': np.random.uniform(5, 45, 20),
        'xg': np.random.uniform(0.05, 0.8, 20)
    })
    
    st.markdown("### 📊 Données de Tirs (Sample)")
    st.dataframe(shots_data.head(10))
    
    # Calculs
    summary = shots_data.groupby('joueur').agg({
        'xg': ['sum', 'mean'],
        'distance': 'mean'
    }).round(3)
    
    st.markdown("### 🎯 Résumé par Joueur")
    st.dataframe(summary)
    
    # Graphique
    fig = px.scatter(
        shots_data, 
        x='distance', 
        y='xg',
        color='joueur',
        title="📈 xG vs Distance de Tir"
    )
    st.plotly_chart(fig, use_container_width=True)

def show_player_test():
    """Test analyse joueur"""
    
    st.markdown("## 👤 Analyse de Joueur")
    
    # Sélection joueur
    player = st.selectbox(
        "Choisir un joueur:",
        ["Kylian Mbappé", "Erling Haaland", "Harry Kane", "Vinicius Jr", "Pedri"]
    )
    
    # Données simulées
    np.random.seed(hash(player) % 100)
    
    stats = {
        'Buts': np.random.randint(15, 35),
        'Passes décisives': np.random.randint(5, 15),
        'xG': round(np.random.uniform(12, 30), 1),
        'xA': round(np.random.uniform(3, 12), 1),
        'Minutes': np.random.randint(2000, 3500),
        'Note moyenne': round(np.random.uniform(7.0, 9.0), 1)
    }
    
    st.markdown(f"### 📊 Statistiques de {player}")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("⚽ Buts", stats['Buts'])
        st.metric("🎯 xG", stats['xG'])
    
    with col2:
        st.metric("🅰️ Assists", stats['Passes décisives'])
        st.metric("📈 xA", stats['xA'])
    
    with col3:
        st.metric("⏱️ Minutes", stats['Minutes'])
        st.metric("⭐ Note", stats['Note moyenne'])
    
    # Graphique radar
    categories = ['Buts', 'Assists', 'xG', 'xA', 'Note moyenne']
    values = [stats['Buts']/35*100, stats['Passes décisives']/15*100, 
              stats['xG']/30*100, stats['xA']/12*100, stats['Note moyenne']/10*100]
    
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name=player
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        title=f"📊 Profil Radar - {player}"
    )
    
    st.plotly_chart(fig, use_container_width=True)

def show_charts_test():
    """Test des graphiques"""
    
    st.markdown("## 🎯 Test des Visualisations")
    
    # Générer données équipe
    teams = ['Real Madrid', 'Barcelona', 'Manchester City', 'Bayern Munich', 'PSG']
    
    team_stats = pd.DataFrame({
        'équipe': teams,
        'buts_pour': np.random.randint(60, 100, 5),
        'buts_contre': np.random.randint(20, 50, 5),
        'possession': np.random.uniform(55, 75, 5),
        'passes_réussies': np.random.randint(85, 95, 5)
    })
    
    st.markdown("### 📊 Comparaison d'Équipes")
    
    # Graphique en barres
    fig1 = px.bar(
        team_stats, 
        x='équipe', 
        y=['buts_pour', 'buts_contre'],
        title="⚽ Buts Pour vs Contre",
        barmode='group'
    )
    st.plotly_chart(fig1, use_container_width=True)
    
    # Scatter plot
    fig2 = px.scatter(
        team_stats,
        x='possession',
        y='passes_réussies',
        color='équipe',
        size='buts_pour',
        title="📈 Possession vs Précision des Passes"
    )
    st.plotly_chart(fig2, use_container_width=True)
    
    # Données tabulaires
    st.markdown("### 📋 Données Détaillées")
    st.dataframe(team_stats)

if __name__ == "__main__":
    main()
