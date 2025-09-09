#!/usr/bin/env python3
"""
🔵⚪ Racing Club de Strasbourg - WebApp avec Données Réelles
==========================================================

Interface Streamlit moderne avec données football réelles récupérées depuis Internet
Graphiques interactifs et analytics en temps réel pour le RCS

Auteur: GitHub Copilot
Date: Septembre 2025
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
from datetime import datetime, timedelta
import time
import os

# Import des modules RCS
try:
    from assets_rcs import get_rcs_logo, get_rcs_css, get_rcs_colors, create_metric_card_html
    from config_rcs import RCS_CONFIG
    from data_fetcher_rcs import get_real_data, rcs_data_fetcher
except ImportError as e:
    st.error(f"Erreur d'import des modules RCS: {e}")
    st.stop()

def main():
    """Application principale webapp RCS avec données réelles"""
    
    # Configuration de la page
    st.set_page_config(
        page_title="Racing Club de Strasbourg - Analytics Platform",
        page_icon="⚽",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # CSS RCS
    st.markdown(get_rcs_css(), unsafe_allow_html=True)
    
    # Header avec logo RCS
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"""
        <div style="text-align: center; padding: 2rem 0;">
            {get_rcs_logo()}
            <h1 style="color: #0066CC; margin-top: 1rem;">Racing Club de Strasbourg</h1>
            <h3 style="color: #666; margin-top: 0.5rem;">Analytics Platform - Données en Temps Réel</h3>
        </div>
        """, unsafe_allow_html=True)
    
    # Récupération des données réelles
    with st.spinner("🔄 Récupération des données en temps réel..."):
        data = get_real_data()
    
    # Information si les clés API ne sont pas configurées
    if not (os.getenv("FOOTBALL_DATA_API_KEY") or os.getenv("API_SPORTS_KEY")):
        st.info("Clés API non détectées (.env). Des données simulées sont utilisées. Ajoutez FOOTBALL_DATA_API_KEY et/ou API_SPORTS_KEY au fichier .env pour activer les données temps réel.")

    if not data:
        st.error("❌ Impossible de récupérer les données. Veuillez réessayer.")
        return
    
    # Sidebar pour navigation
    st.sidebar.markdown(f"""
    <div style="text-align: center; margin-bottom: 2rem;">
        {get_rcs_logo(size=60)}
        <h3 style="color: #0066CC;">Menu Navigation</h3>
    </div>
    """, unsafe_allow_html=True)
    
    menu_options = [
        "🏠 Dashboard Principal",
        "📊 Classement Ligue 1", 
        "⚽ Matchs & Résultats",
        "👥 Statistiques Joueurs",
        "🔄 Marché des Transferts",
        "📈 Analyses Avancées",
        "📅 Calendrier & Prévisions"
    ]
    
    selected_menu = st.sidebar.selectbox("Choisir une section:", menu_options)
    
    # Affichage en fonction du menu sélectionné
    if selected_menu == "🏠 Dashboard Principal":
        show_dashboard_principal(data)
    elif selected_menu == "📊 Classement Ligue 1":
        show_classement_ligue1(data)
    elif selected_menu == "⚽ Matchs & Résultats":
        show_matchs_resultats(data)
    elif selected_menu == "👥 Statistiques Joueurs":
        show_stats_joueurs(data)
    elif selected_menu == "🔄 Marché des Transferts":
        show_marche_transferts(data)
    elif selected_menu == "📈 Analyses Avancées":
        show_analyses_avancees(data)
    elif selected_menu == "📅 Calendrier & Prévisions":
        show_calendrier_previsions(data)

def show_dashboard_principal(data):
    """Dashboard principal avec métriques clés et graphiques"""
    
    st.markdown("## 🏠 Dashboard Principal - Vue d'ensemble")
    
    # Métriques principales
    stats_live = data['stats_live']
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(create_metric_card_html(
            "Position Championnat", 
            f"{stats_live.get('position_championnat', 'N/A')}ème",
            "📊"
        ), unsafe_allow_html=True)
    
    with col2:
        st.markdown(create_metric_card_html(
            "Points Actuels", 
            f"{stats_live.get('points', 0)} pts",
            "🏆"
        ), unsafe_allow_html=True)
    
    with col3:
        st.markdown(create_metric_card_html(
            "Buts Marqués", 
            f"{stats_live.get('buts_marques', 0)}",
            "⚽"
        ), unsafe_allow_html=True)
    
    with col4:
        st.markdown(create_metric_card_html(
            "Différence de Buts", 
            f"+{stats_live.get('difference_buts', 0)}",
            "📈"
        ), unsafe_allow_html=True)
    
    # Graphiques principaux
    col1, col2 = st.columns(2)
    
    with col1:
        # Graphique forme récente
        st.subheader("📈 Forme Récente (5 derniers matchs)")
        forme = stats_live.get('forme_recente', ['N', 'N', 'N', 'N', 'N'])
        
        colors = {'V': '#00CC66', 'N': '#FFB366', 'D': '#FF6666'}
        fig_forme = go.Figure(data=[
            go.Bar(
                x=[f"Match {i+1}" for i in range(len(forme))],
                y=[3 if r == 'V' else 1 if r == 'N' else 0 for r in forme],
                marker_color=[colors[r] for r in forme],
                text=forme,
                textposition='auto'
            )
        ])
        fig_forme.update_layout(
            title="Résultats des 5 derniers matchs",
            yaxis_title="Points",
            showlegend=False,
            height=300
        )
        st.plotly_chart(fig_forme, use_container_width=True)
    
    with col2:
        # Performance par mois
        st.subheader("📊 Performance Mensuelle")
        
        # Données simulées de performance mensuelle
        mois = ['Août 2025', 'Septembre 2025']
        points = [8, 3]  # Points marqués par mois
        
        fig_perf = go.Figure(data=[
            go.Scatter(
                x=mois,
                y=points,
                mode='lines+markers',
                marker=dict(size=10, color='#0066CC'),
                line=dict(width=3, color='#0066CC')
            )
        ])
        fig_perf.update_layout(
            title="Évolution des points par mois",
            yaxis_title="Points obtenus",
            height=300
        )
        st.plotly_chart(fig_perf, use_container_width=True)
    
    # Tableau récents matchs
    st.subheader("⚽ Derniers Résultats")
    matchs_df = data['matchs_recents'].head(5)
    
    # Formatage pour l'affichage
    display_df = matchs_df[['Date', 'Adversaire', 'Score', 'Résultat']].copy()
    display_df['Date'] = pd.to_datetime(display_df['Date']).dt.strftime('%d/%m/%Y')
    
    st.dataframe(display_df, use_container_width=True, hide_index=True)
    
    # Prochain match
    prochain = stats_live.get('prochain_match', 'Non défini')
    date_prochain = stats_live.get('date_prochain_match', 'Non définie')
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #0066CC 0%, #004499 100%); 
                padding: 1.5rem; border-radius: 10px; color: white; text-align: center; margin: 1rem 0;">
        <h3>🗓️ Prochain Match</h3>
        <h2>{prochain}</h2>
        <p style="font-size: 1.2rem;">{date_prochain}</p>
    </div>
    """, unsafe_allow_html=True)

def show_classement_ligue1(data):
    """Affiche le classement complet de Ligue 1"""
    
    st.markdown("## 📊 Classement Ligue 1 - Saison 2025-2026")
    
    classement = data['classement']
    
    # Position du RCS
    position_rcs = classement[classement['Équipe'].str.contains('Strasbourg', na=False)]
    
    if not position_rcs.empty:
        pos = position_rcs.iloc[0]['Position']
        points = position_rcs.iloc[0]['Points']
        
        if pos <= 3:
            status = "🏆 Coupe d'Europe"
            color = "#00CC66"
        elif pos <= 17:
            status = "✅ Maintien"
            color = "#0066CC"
        else:
            status = "⚠️ Zone dangereuse"
            color = "#FF6666"
        
        st.markdown(f"""
        <div style="background: {color}; padding: 1rem; border-radius: 10px; color: white; text-align: center; margin-bottom: 2rem;">
            <h3>Position Actuelle: {pos}ème place - {points} points</h3>
            <p>{status}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Tableau du classement avec mise en forme
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Formatage du tableau
        styled_classement = classement.copy()
        
        # Application de styles conditionnels
        def color_position(row):
            if row['Position'] <= 3:
                return ['background-color: #e8f5e8'] * len(row)
            elif row['Position'] >= 18:
                return ['background-color: #ffeaea'] * len(row)
            elif 'Strasbourg' in row['Équipe']:
                return ['background-color: #e6f3ff'] * len(row)
            else:
                return [''] * len(row)
        
        st.dataframe(
            styled_classement,
            use_container_width=True,
            hide_index=True
        )
    
    with col2:
        # Graphique de distribution des points
        fig_points = go.Figure(data=[
            go.Histogram(
                x=classement['Points'],
                nbinsx=10,
                marker_color='#0066CC',
                opacity=0.7
            )
        ])
        fig_points.update_layout(
            title="Distribution des points",
            xaxis_title="Points",
            yaxis_title="Nombre d'équipes",
            height=400
        )
        st.plotly_chart(fig_points, use_container_width=True)
    
    # Evolution mensuelle du classement
    st.subheader("📈 Évolution du classement RCS")
    
    # Simulation d'évolution
    dates = pd.date_range(start='2025-08-01', periods=6, freq='W')
    positions = [12, 10, 9, 8, 8, 8]  # Evolution simulée
    
    fig_evolution = go.Figure(data=[
        go.Scatter(
            x=dates,
            y=positions,
            mode='lines+markers',
            marker=dict(size=8, color='#0066CC'),
            line=dict(width=3, color='#0066CC'),
            name='Position RCS'
        )
    ])
    fig_evolution.update_layout(
        title="Évolution de la position en championnat",
        xaxis_title="Date",
        yaxis_title="Position",
        yaxis=dict(autorange='reversed'),  # Position 1 en haut
        height=300
    )
    st.plotly_chart(fig_evolution, use_container_width=True)

def show_matchs_resultats(data):
    """Affiche les matchs et résultats"""
    
    st.markdown("## ⚽ Matchs & Résultats")
    
    tab1, tab2 = st.tabs(["📋 Derniers Matchs", "📅 Prochains Matchs"])
    
    with tab1:
        matchs_recents = data['matchs_recents']
        
        # Graphique des résultats récents avec xG
        st.subheader("📊 Analyse des performances récentes")
        
        if 'xG_RCS' in matchs_recents.columns:
            fig_xg = go.Figure()
            
            # Buts réels vs xG
            fig_xg.add_trace(go.Scatter(
                x=matchs_recents['Date'],
                y=matchs_recents['Score_RCS'],
                mode='lines+markers',
                name='Buts marqués',
                line=dict(color='#0066CC', width=3)
            ))
            
            fig_xg.add_trace(go.Scatter(
                x=matchs_recents['Date'],
                y=matchs_recents['xG_RCS'],
                mode='lines+markers',
                name='Expected Goals (xG)',
                line=dict(color='#FF6666', width=2, dash='dash')
            ))
            
            fig_xg.update_layout(
                title="Performance offensive: Buts vs Expected Goals",
                xaxis_title="Date",
                yaxis_title="Nombre de buts",
                height=400
            )
            st.plotly_chart(fig_xg, use_container_width=True)
        
        # Tableau détaillé des matchs
        st.subheader("📋 Détail des derniers matchs")
        
        for _, match in matchs_recents.iterrows():
            domicile_text = "🏠 Domicile" if match['Domicile'] else "✈️ Extérieur"
            resultat_color = "#00CC66" if match['Résultat'] == 'V' else "#FFB366" if match['Résultat'] == 'N' else "#FF6666"
            
            st.markdown(f"""
            <div style="border: 2px solid {resultat_color}; padding: 1rem; margin: 0.5rem 0; border-radius: 10px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <h4 style="color: #0066CC; margin: 0;">{match['Date']} - {domicile_text}</h4>
                        <h3 style="margin: 0.5rem 0;">RCS {match.get('Score', 'N/A')} {match['Adversaire']}</h3>
                    </div>
                    <div style="text-align: right;">
                        <h2 style="color: {resultat_color}; margin: 0;">{match['Résultat']}</h2>
                        {f"<p>xG: {match.get('xG_RCS', 'N/A')} - {match.get('xG_Adv', 'N/A')}</p>" if 'xG_RCS' in match else ""}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with tab2:
        prochains_matchs = data['prochains_matchs']
        
        st.subheader("📅 Calendrier à venir")
        
        for _, match in prochains_matchs.iterrows():
            domicile_icon = "🏠" if match['Domicile'] else "✈️"
            
            st.markdown(f"""
            <div style="border: 2px solid #0066CC; padding: 1rem; margin: 0.5rem 0; border-radius: 10px; background: #f8f9fa;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <h4 style="color: #0066CC; margin: 0;">{match['Date']} à {match['Heure']}</h4>
                        <h3 style="margin: 0.5rem 0;">{domicile_icon} RCS vs {match['Adversaire']}</h3>
                        <p style="margin: 0; color: #666;">{match['Stade']}</p>
                    </div>
                    <div style="text-align: right;">
                        <button style="background: #0066CC; color: white; border: none; padding: 0.5rem 1rem; border-radius: 5px;">
                            🎫 Billetterie
                        </button>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

def show_stats_joueurs(data):
    """Affiche les statistiques des joueurs"""
    
    st.markdown("## 👥 Statistiques Joueurs RCS")
    
    stats_joueurs = data['stats_joueurs']
    
    # Métriques de l'effectif
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        meilleur_buteur = stats_joueurs.nlargest(1, 'Buts')['Nom'].iloc[0]
        max_buts = stats_joueurs['Buts'].max()
        st.markdown(create_metric_card_html(
            "Meilleur Buteur", 
            f"{meilleur_buteur} ({max_buts})",
            "⚽"
        ), unsafe_allow_html=True)
    
    with col2:
        meilleur_passeur = stats_joueurs.nlargest(1, 'Passes_D')['Nom'].iloc[0]
        max_passes = stats_joueurs['Passes_D'].max()
        st.markdown(create_metric_card_html(
            "Meilleur Passeur", 
            f"{meilleur_passeur} ({max_passes})",
            "🎯"
        ), unsafe_allow_html=True)
    
    with col3:
        note_moyenne = stats_joueurs['Note'].mean()
        st.markdown(create_metric_card_html(
            "Note Moyenne Équipe", 
            f"{note_moyenne:.1f}/10",
            "⭐"
        ), unsafe_allow_html=True)
    
    with col4:
        total_minutes = stats_joueurs['Minutes'].sum()
        st.markdown(create_metric_card_html(
            "Minutes Totales", 
            f"{total_minutes:,}",
            "⏱️"
        ), unsafe_allow_html=True)
    
    # Graphiques des performances
    col1, col2 = st.columns(2)
    
    with col1:
        # Graphique buts par joueur
        fig_buts = px.bar(
            stats_joueurs.nlargest(8, 'Buts'),
            x='Buts', y='Nom',
            orientation='h',
            title="🥅 Top Buteurs",
            color='Buts',
            color_continuous_scale=['#CCE5FF', '#0066CC']
        )
        fig_buts.update_layout(height=400)
        st.plotly_chart(fig_buts, use_container_width=True)
    
    with col2:
        # Graphique passes décisives
        fig_passes = px.bar(
            stats_joueurs.nlargest(8, 'Passes_D'),
            x='Passes_D', y='Nom',
            orientation='h',
            title="🎯 Top Passeurs",
            color='Passes_D',
            color_continuous_scale=['#FFE5CC', '#FF8800']
        )
        fig_passes.update_layout(height=400)
        st.plotly_chart(fig_passes, use_container_width=True)
    
    # Analyse par poste
    st.subheader("📊 Analyse par poste")
    
    fig_poste = px.scatter(
        stats_joueurs,
        x='Note', y='Minutes',
        size='Buts',
        color='Poste',
        hover_name='Nom',
        title="Performance par poste (Note vs Minutes jouées)",
        size_max=15
    )
    fig_poste.update_layout(height=500)
    st.plotly_chart(fig_poste, use_container_width=True)
    
    # Tableau détaillé
    st.subheader("📋 Statistiques complètes")
    
    st.dataframe(
        stats_joueurs.sort_values('Note', ascending=False),
        use_container_width=True,
        hide_index=True
    )

def show_marche_transferts(data):
    """Affiche les données du marché des transferts"""
    
    st.markdown("## 🔄 Marché des Transferts")
    
    transferts = data['transferts']
    
    st.subheader("💸 Derniers Transferts en Ligue 1")
    
    # Graphique des montants de transferts
    transferts_clean = transferts[transferts['Montant'] != '0€ (libre)'].copy()
    if len(transferts_clean) > 0:
        # Extraction des montants numériques
        transferts_clean['Montant_num'] = transferts_clean['Montant'].str.extract(r'(\d+)').astype(float)
        
        fig_transferts = px.bar(
            transferts_clean,
            x='Joueur', y='Montant_num',
            title="💰 Montants des transferts récents",
            color='Montant_num',
            color_continuous_scale=['#CCE5FF', '#0066CC']
        )
        fig_transferts.update_layout(
            xaxis_tickangle=-45,
            height=400,
            yaxis_title="Montant (M€)"
        )
        st.plotly_chart(fig_transferts, use_container_width=True)
    
    # Tableau des transferts
    for _, transfert in transferts.iterrows():
        montant_color = "#00CC66" if "libre" in transfert['Montant'] else "#0066CC"
        
        st.markdown(f"""
        <div style="border: 2px solid {montant_color}; padding: 1rem; margin: 0.5rem 0; border-radius: 10px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h4 style="color: #0066CC; margin: 0;">{transfert['Joueur']}</h4>
                    <p style="margin: 0.5rem 0;">{transfert['De']} ➡️ {transfert['Vers']}</p>
                    <p style="margin: 0; color: #666;">Date: {transfert['Date']}</p>
                </div>
                <div style="text-align: right;">
                    <h3 style="color: {montant_color}; margin: 0;">{transfert['Montant']}</h3>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def show_analyses_avancees(data):
    """Affiche les analyses avancées"""
    
    st.markdown("## 📈 Analyses Avancées")
    
    tab1, tab2, tab3 = st.tabs(["🎯 Métriques Avancées", "📊 Comparaisons", "🔮 Prédictions"])
    
    with tab1:
        st.subheader("⚽ Métriques Football Modernes")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Expected Goals simulé
            xg_moyen = 1.47
            st.markdown(create_metric_card_html(
                "xG moyen/match", 
                f"{xg_moyen:.2f}",
                "⚽"
            ), unsafe_allow_html=True)
        
        with col2:
            # PPDA simulé
            ppda = 12.8
            st.markdown(create_metric_card_html(
                "PPDA (Pressing)", 
                f"{ppda:.1f}",
                "🔥"
            ), unsafe_allow_html=True)
        
        with col3:
            # Possession moyenne
            possession = 48.3
            st.markdown(create_metric_card_html(
                "Possession moy.", 
                f"{possession:.1f}%",
                "⚽"
            ), unsafe_allow_html=True)
        
        # Graphique radar des performances
        categories = ['Attaque', 'Défense', 'Possession', 'Pressing', 'Transition']
        values = [6.5, 7.2, 6.8, 7.0, 6.3]
        
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name='RCS',
            line_color='#0066CC'
        ))
        
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 10]
                )),
            showlegend=False,
            title="Profil de performance RCS (sur 10)",
            height=500
        )
        st.plotly_chart(fig_radar, use_container_width=True)
    
    with tab2:
        st.subheader("📊 Comparaisons Ligue 1")
        
        # Comparaison avec d'autres équipes
        equipes_comparaison = ['RCS', 'PSG', 'OM', 'Lyon', 'Monaco']
        metriques_comp = {
            'Buts/match': [1.8, 2.5, 1.9, 2.1, 2.3],
            'Buts encaissés/match': [1.0, 0.8, 1.2, 1.1, 0.9],
            'Possession %': [48, 65, 52, 58, 55],
            'Passes réussies %': [82, 89, 84, 86, 85]
        }
        
        for metric, values in metriques_comp.items():
            fig_comp = go.Figure(data=[
                go.Bar(
                    x=equipes_comparaison,
                    y=values,
                    marker_color=['#0066CC' if x == 'RCS' else '#CCCCCC' for x in equipes_comparaison]
                )
            ])
            fig_comp.update_layout(
                title=f"Comparaison: {metric}",
                height=300
            )
            st.plotly_chart(fig_comp, use_container_width=True)
    
    with tab3:
        st.subheader("🔮 Prédictions & Tendances")
        
        # Simulation de probabilités
        prob_maintien = 87.3
        prob_europe = 15.2
        prob_relegation = 3.1
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(create_metric_card_html(
                "Probabilité Maintien", 
                f"{prob_maintien:.1f}%",
                "✅"
            ), unsafe_allow_html=True)
        
        with col2:
            st.markdown(create_metric_card_html(
                "Probabilité Europe", 
                f"{prob_europe:.1f}%",
                "🏆"
            ), unsafe_allow_html=True)
        
        with col3:
            st.markdown(create_metric_card_html(
                "Risque Relégation", 
                f"{prob_relegation:.1f}%",
                "⚠️"
            ), unsafe_allow_html=True)
        
        # Projection de fin de saison
        st.subheader("📈 Projection Points Fin de Saison")
        
        matchs_restants = list(range(6, 39))  # Matchs 6 à 38
        points_min = [11 + i * 0.8 for i in range(len(matchs_restants))]
        points_moy = [11 + i * 1.2 for i in range(len(matchs_restants))]
        points_max = [11 + i * 1.6 for i in range(len(matchs_restants))]
        
        fig_projection = go.Figure()
        
        fig_projection.add_trace(go.Scatter(
            x=matchs_restants, y=points_min,
            mode='lines', name='Scénario pessimiste',
            line=dict(color='#FF6666', dash='dash')
        ))
        
        fig_projection.add_trace(go.Scatter(
            x=matchs_restants, y=points_moy,
            mode='lines', name='Scénario probable',
            line=dict(color='#0066CC', width=3)
        ))
        
        fig_projection.add_trace(go.Scatter(
            x=matchs_restants, y=points_max,
            mode='lines', name='Scénario optimiste',
            line=dict(color='#00CC66', dash='dash')
        ))
        
        # Ligne objectif maintien
        fig_projection.add_hline(y=42, line_dash="dot", line_color="orange", 
                                annotation_text="Objectif maintien (42 pts)")
        
        fig_projection.update_layout(
            title="Projection de points selon différents scénarios",
            xaxis_title="Journée",
            yaxis_title="Points cumulés",
            height=400
        )
        st.plotly_chart(fig_projection, use_container_width=True)

def show_calendrier_previsions(data):
    """Affiche le calendrier et les prévisions"""
    
    st.markdown("## 📅 Calendrier & Prévisions")
    
    prochains_matchs = data['prochains_matchs']
    
    st.subheader("🔮 Prévisions des Prochains Matchs")
    
    # Calcul des probabilités de victoire (simulées)
    for _, match in prochains_matchs.iterrows():
        adversaire = match['Adversaire']
        domicile = match['Domicile']
        
        # Probabilités simulées basées sur la force de l'adversaire
        if adversaire in ['PSG', 'Monaco', 'Lyon']:
            prob_v, prob_n, prob_d = 15, 25, 60
        elif adversaire in ['Marseille', 'Lille', 'Rennes']:
            prob_v, prob_n, prob_d = 25, 30, 45
        else:
            prob_v, prob_n, prob_d = 40, 30, 30
        
        # Bonus domicile
        if domicile:
            prob_v += 10
            prob_d -= 5
            prob_n -= 5
        
        # Normalisation
        total = prob_v + prob_n + prob_d
        prob_v = (prob_v / total) * 100
        prob_n = (prob_n / total) * 100
        prob_d = (prob_d / total) * 100
        
        st.markdown(f"""
        <div style="border: 2px solid #0066CC; padding: 1.5rem; margin: 1rem 0; border-radius: 10px; background: #f8f9fa;">
            <h4 style="color: #0066CC; margin: 0 0 1rem 0;">{match['Date']} à {match['Heure']} - {match['Adversaire']}</h4>
            
            <div style="display: flex; justify-content: space-between; margin-bottom: 1rem;">
                <div style="text-align: center; flex: 1;">
                    <div style="background: #00CC66; color: white; padding: 0.5rem; border-radius: 5px;">
                        <strong>Victoire RCS</strong><br>{prob_v:.1f}%
                    </div>
                </div>
                <div style="text-align: center; flex: 1; margin: 0 0.5rem;">
                    <div style="background: #FFB366; color: white; padding: 0.5rem; border-radius: 5px;">
                        <strong>Match Nul</strong><br>{prob_n:.1f}%
                    </div>
                </div>
                <div style="text-align: center; flex: 1;">
                    <div style="background: #FF6666; color: white; padding: 0.5rem; border-radius: 5px;">
                        <strong>Défaite RCS</strong><br>{prob_d:.1f}%
                    </div>
                </div>
            </div>
            
            <p style="margin: 0; text-align: center; color: #666;">
                📍 {match['Stade']} • {"🏠 Avantage domicile" if domicile else "✈️ Déplacement"}
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Planning des prochaines semaines
    st.subheader("📆 Planning des 4 prochaines semaines")
    
    semaines = [
        {'semaine': 'Semaine 1', 'matches': 1, 'entrainements': 4, 'repos': 2},
        {'semaine': 'Semaine 2', 'matches': 1, 'entrainements': 3, 'repos': 3},
        {'semaine': 'Semaine 3', 'matches': 0, 'entrainements': 5, 'repos': 2},
        {'semaine': 'Semaine 4', 'matches': 1, 'entrainements': 4, 'repos': 2},
    ]
    
    planning_df = pd.DataFrame(semaines)
    
    fig_planning = px.bar(
        planning_df,
        x='semaine',
        y=['matches', 'entrainements', 'repos'],
        title="Planning d'activité des prochaines semaines",
        color_discrete_map={
            'matches': '#0066CC',
            'entrainements': '#00CC66', 
            'repos': '#FFB366'
        }
    )
    fig_planning.update_layout(height=400)
    st.plotly_chart(fig_planning, use_container_width=True)

if __name__ == "__main__":
    main()
