"""
🔵⚪ Racing Club de Strasbourg - Interface Web Moderne
====================================================

Interface Streamlit complète et moderne pour la plateforme d'analytics RCS
avec graphiques interactifs, analyses en temps réel et rapports automatisés.

Auteur: GitHub Copilot
Date: Septembre 2025
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.figure_factory as ff
from datetime import datetime, timedelta
import json
import time

# Import des modules RCS
try:
    from assets_rcs import AssetsRCS, assets_rcs
    from config_rcs import ConfigRCS, config_rcs
    from analytics_avances_rcs import AnalyticsAvancesRCS
except ImportError as e:
    st.error(f"Erreur d'import des modules RCS: {e}")
    st.stop()

# Configuration de la page
st.set_page_config(
    page_title="🔵⚪ Racing Club de Strasbourg - Analytics Platform",
    page_icon="🔵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import des modules
try:
    from config_rcs import config_rcs, metriques, ui_config
    from analytics_avances_rcs import AnalyticsAvancesRCS
    from python_analytics.modules.collecteur_donnees_rcs import CollecteurDonneesRCS
    from python_analytics.modules.analyseur_rcs import AnalyseurPerformanceRCS
except ImportError:
    st.error("❌ Erreur d'import des modules. Vérifiez l'installation.")
    st.stop()

# CSS personnalisé avec logos RCS intégrés
st.markdown(assets_rcs.STREAMLIT_CSS, unsafe_allow_html=True)

# Header principal avec logos RCS
st.markdown(
    assets_rcs.get_header_rcs(
        "Racing Club de Strasbourg", 
        "Analytics Platform - Saison 2024-2025"
    ), 
    unsafe_allow_html=True
)

# CSS complémentaire pour l'interface
st.markdown("""
<style>
    /* Boutons */
    .stButton > button {
        background-color: #0066CC;
        color: white;
        border-radius: 20px;
        border: none;
        padding: 0.5rem 2rem;
        font-weight: bold;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        background-color: #004499;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 102, 204, 0.3);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: #f0f8ff;
        border-radius: 4px;
        color: #0066CC;
        font-weight: bold;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #0066CC;
        color: white;
    }
    
    /* Alertes */
    .alert-success {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    
    .alert-warning {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        color: #856404;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    
    .alert-danger {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialisation des données en cache
@st.cache_data(ttl=300)  # Cache de 5 minutes
def charger_donnees_rcs():
    """Charge les données RCS avec mise en cache"""
    try:
        collecteur = CollecteurDonneesRCS()
        analytics = AnalyticsAvancesRCS()
        
        # Chargement des données
        effectif = collecteur.recuperer_stats_joueurs_rcs()
        classement = collecteur.recuperer_classement_ligue1()
        
        # Chargement des analytics avancés
        analytics.charger_donnees_completes()
        
        return {
            'effectif': effectif,
            'classement': classement,
            'analytics': analytics,
            'derniere_maj': datetime.now()
        }
    except Exception as e:
        st.error(f"❌ Erreur lors du chargement des données: {str(e)}")
        return None

def afficher_header():
    """Affiche le header principal de l'application"""
    st.markdown("""
    <div class="main-header">
        <h1>🔵⚪ Racing Club de Strasbourg</h1>
        <h2>Plateforme d'Analytics Football Professionnelle</h2>
        <p>Saison 2024-2025 • Stade de la Meinau • Ligue 1</p>
    </div>
    """, unsafe_allow_html=True)

def afficher_sidebar(donnees):
    """Affiche la sidebar avec les contrôles"""
    st.sidebar.markdown("## 🎛️ Contrôles")
    
    # Sélection de la vue
    vue_selectionnee = st.sidebar.selectbox(
        "🎯 Sélectionnez la vue",
        ["🏠 Vue d'ensemble", "👥 Effectif détaillé", "📊 Analytics avancés", 
         "🤖 Prédictions IA", "🏥 Santé & Performance", "📈 Rapports"]
    )
    
    # Filtres
    st.sidebar.markdown("### 🔍 Filtres")
    
    postes_disponibles = ["Tous"] + list(donnees['effectif']['poste'].unique())
    postes_selectionnes = st.sidebar.multiselect(
        "Postes", postes_disponibles, default=["Tous"]
    )
    
    age_min, age_max = st.sidebar.slider(
        "Tranche d'âge", 
        min_value=int(donnees['effectif']['age'].min()),
        max_value=int(donnees['effectif']['age'].max()),
        value=(int(donnees['effectif']['age'].min()), int(donnees['effectif']['age'].max()))
    )
    
    # Mise à jour des données
    if st.sidebar.button("🔄 Actualiser les données"):
        st.cache_data.clear()
        st.experimental_rerun()
    
    # Informations système
    st.sidebar.markdown("### ℹ️ Informations")
    st.sidebar.info(f"**Dernière MAJ:** {donnees['derniere_maj'].strftime('%H:%M:%S')}")
    st.sidebar.info(f"**Joueurs:** {len(donnees['effectif'])}")
    st.sidebar.info(f"**Position Ligue 1:** {obtenir_position_rcs(donnees['classement'])}ème")
    
    return vue_selectionnee, postes_selectionnes, (age_min, age_max)

def obtenir_position_rcs(classement_df):
    """Récupère la position actuelle du RCS"""
    try:
        rcs_row = classement_df[classement_df['equipe'] == 'Racing Club de Strasbourg']
        if not rcs_row.empty:
            return rcs_row.iloc[0]['position']
        return "N/A"
    except:
        return "N/A"

def afficher_vue_ensemble(donnees):
    """Affiche la vue d'ensemble du RCS"""
    st.markdown("## 🏠 Vue d'ensemble Racing Club de Strasbourg")
    
    # Métriques principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        position = obtenir_position_rcs(donnees['classement'])
        st.metric(
            label="🏆 Position Ligue 1",
            value=f"{position}ème",
            delta="Maintien confortable" if position != "N/A" and int(position) <= 15 else "Vigilance"
        )
    
    with col2:
        effectif_size = len(donnees['effectif'])
        valeur_totale = donnees['effectif']['valeur_marche'].sum()
        st.metric(
            label="💰 Valeur effectif",
            value=f"{valeur_totale:.1f}M€",
            delta=f"{effectif_size} joueurs"
        )
    
    with col3:
        note_moyenne = donnees['effectif']['note_moyenne'].mean()
        st.metric(
            label="⭐ Note moyenne",
            value=f"{note_moyenne:.2f}/10",
            delta="Équipe" if note_moyenne >= 6.5 else "À améliorer"
        )
    
    with col4:
        age_moyen = donnees['effectif']['age'].mean()
        st.metric(
            label="👥 Âge moyen",
            value=f"{age_moyen:.1f} ans",
            delta="Expérience" if age_moyen >= 25 else "Jeunesse"
        )
    
    # Graphiques principaux
    col1, col2 = st.columns(2)
    
    with col1:
        # Répartition par poste
        fig_postes = px.pie(
            donnees['effectif'].groupby('poste').size().reset_index(),
            values=0, names='poste',
            title="🎯 Répartition de l'effectif par poste",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig_postes.update_layout(height=400)
        st.plotly_chart(fig_postes, use_container_width=True)
    
    with col2:
        # Valeur vs Performance
        fig_valeur = px.scatter(
            donnees['effectif'], 
            x='note_moyenne', y='valeur_marche',
            size='age', color='poste',
            hover_name='nom',
            title="💎 Valeur marchande vs Performance",
            labels={'note_moyenne': 'Note moyenne', 'valeur_marche': 'Valeur (M€)'}
        )
        fig_valeur.update_layout(height=400)
        st.plotly_chart(fig_valeur, use_container_width=True)
    
    # Tableau des dernières performances
    st.markdown("### 📈 Top 10 des performances actuelles")
    top_performers = donnees['effectif'].nlargest(10, 'note_moyenne')[
        ['nom', 'poste', 'age', 'note_moyenne', 'valeur_marche', 'matchs_joues']
    ]
    
    # Formatage du tableau
    top_performers_display = top_performers.copy()
    top_performers_display['note_moyenne'] = top_performers_display['note_moyenne'].round(2)
    top_performers_display['valeur_marche'] = top_performers_display['valeur_marche'].apply(lambda x: f"{x:.1f}M€")
    
    st.dataframe(
        top_performers_display,
        column_config={
            "nom": "Joueur",
            "poste": "Poste", 
            "age": "Âge",
            "note_moyenne": "Note",
            "valeur_marche": "Valeur",
            "matchs_joues": "Matchs"
        },
        use_container_width=True
    )

def afficher_effectif_detaille(donnees, filtres):
    """Affiche l'effectif détaillé avec filtres"""
    st.markdown("## 👥 Effectif détaillé - Saison 2024-2025")
    
    postes_filtres, (age_min, age_max) = filtres
    
    # Application des filtres
    effectif_filtre = donnees['effectif'].copy()
    
    if "Tous" not in postes_filtres:
        effectif_filtre = effectif_filtre[effectif_filtre['poste'].isin(postes_filtres)]
    
    effectif_filtre = effectif_filtre[
        (effectif_filtre['age'] >= age_min) & 
        (effectif_filtre['age'] <= age_max)
    ]
    
    # Statistiques filtrées
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Joueurs sélectionnés", len(effectif_filtre))
    with col2:
        st.metric("Valeur totale", f"{effectif_filtre['valeur_marche'].sum():.1f}M€")
    with col3:
        st.metric("Note moyenne", f"{effectif_filtre['note_moyenne'].mean():.2f}")
    
    # Graphiques de l'effectif
    col1, col2 = st.columns(2)
    
    with col1:
        # Distribution des âges
        fig_age = px.histogram(
            effectif_filtre, x='age', 
            title="📅 Distribution des âges",
            color_discrete_sequence=[config_rcs.couleur_primaire]
        )
        st.plotly_chart(fig_age, use_container_width=True)
    
    with col2:
        # Boxplot notes par poste
        fig_notes = px.box(
            effectif_filtre, x='poste', y='note_moyenne',
            title="📊 Distribution des notes par poste"
        )
        st.plotly_chart(fig_notes, use_container_width=True)
    
    # Tableau détaillé
    st.markdown("### 📋 Tableau détaillé de l'effectif")
    
    # Ajout de colonnes calculées
    effectif_display = effectif_filtre.copy()
    effectif_display['efficacite'] = (effectif_display['note_moyenne'] / 10 * 100).round(1)
    effectif_display['rapport_qualite_prix'] = (
        effectif_display['note_moyenne'] / effectif_display['valeur_marche']
    ).round(2)
    
    st.dataframe(
        effectif_display,
        column_config={
            "nom": "Joueur",
            "poste": "Poste",
            "age": "Âge", 
            "note_moyenne": st.column_config.NumberColumn("Note", format="%.2f"),
            "valeur_marche": st.column_config.NumberColumn("Valeur (M€)", format="%.1f"),
            "matchs_joues": "Matchs",
            "efficacite": st.column_config.ProgressColumn("Efficacité (%)", min_value=0, max_value=100),
            "rapport_qualite_prix": "Qualité/Prix"
        },
        use_container_width=True
    )

def afficher_analytics_avances(donnees):
    """Affiche les analytics avancés"""
    st.markdown("## 📊 Analytics Avancés - Intelligence Football")
    
    try:
        # Génération du dashboard de performance
        dashboard = donnees['analytics'].creer_dashboard_performance()
        st.plotly_chart(dashboard, use_container_width=True)
        
        # Métriques avancées RCS
        st.markdown("### 🎯 Métriques Exclusives RCS")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # xG moyen équipe (simulé)
            xg_moyen = 1.47
            st.metric(
                "⚽ xG moyen par match",
                f"{xg_moyen:.2f}",
                delta="Style contre-attaque"
            )
        
        with col2:
            # PPDA (simulé) 
            ppda = 12.8
            st.metric(
                "🔥 PPDA (Pressing)",
                f"{ppda:.1f}",
                delta="Intensité moyenne-haute"
            )
        
        with col3:
            # Probabilité maintien (simulé)
            prob_maintien = 87.3
            st.metric(
                "📈 Probabilité maintien",
                f"{prob_maintien:.1f}%",
                delta="Objectif en bonne voie"
            )
        
        # Analyse de forme par joueur
        st.markdown("### 📈 Analyse de forme individuelle")
        
        # Sélection de joueur pour analyse détaillée
        joueur_selectionne = st.selectbox(
            "Sélectionnez un joueur pour analyse détaillée",
            donnees['effectif']['nom'].tolist()
        )
        
        if joueur_selectionne:
            # Simulation d'analyse de forme
            analyse_forme = donnees['analytics'].analyseur.analyser_forme_joueur_rcs(
                joueur_selectionne, 10
            )
            
            if 'erreur' not in analyse_forme:
                col1, col2 = st.columns(2)
                
                with col1:
                    # Métriques du joueur
                    st.markdown(f"**Analyse de {joueur_selectionne}**")
                    
                    joueur_info = donnees['effectif'][
                        donnees['effectif']['nom'] == joueur_selectionne
                    ].iloc[0]
                    
                    st.metric("Note moyenne saison", f"{joueur_info['note_moyenne']:.2f}")
                    st.metric("Matchs joués", joueur_info['matchs_joues'])
                    st.metric("Valeur marchande", f"{joueur_info['valeur_marche']:.1f}M€")
                
                with col2:
                    # Graphique de forme (simulé)
                    dates = pd.date_range(
                        start=datetime.now() - timedelta(days=100),
                        periods=10, freq='10D'
                    )
                    notes_simulees = np.random.normal(
                        joueur_info['note_moyenne'], 0.5, 10
                    )
                    notes_simulees = np.clip(notes_simulees, 4, 9)
                    
                    fig_forme = go.Figure()
                    fig_forme.add_trace(
                        go.Scatter(
                            x=dates, y=notes_simulees,
                            mode='lines+markers',
                            name=joueur_selectionne,
                            line=dict(color=config_rcs.couleur_primaire, width=3)
                        )
                    )
                    fig_forme.update_layout(
                        title=f"Évolution de forme - {joueur_selectionne}",
                        xaxis_title="Date",
                        yaxis_title="Note",
                        height=300
                    )
                    st.plotly_chart(fig_forme, use_container_width=True)
        
    except Exception as e:
        st.error(f"❌ Erreur lors de la génération des analytics: {str(e)}")
        st.info("📝 Certaines fonctionnalités nécessitent des données complètes.")

def afficher_predictions_ia(donnees):
    """Affiche les prédictions IA"""
    st.markdown("## 🤖 Prédictions Intelligence Artificielle")
    
    # Analyse des risques de blessures
    try:
        risques = donnees['analytics'].analyser_risques_blessures()
        
        st.markdown("### 🏥 Analyse des risques de blessures")
        
        # Résumé des risques
        col1, col2, col3 = st.columns(3)
        
        risque_faible = len(risques[risques['niveau_risque'] == '🟢 Faible'])
        risque_moyen = len(risques[risques['niveau_risque'] == '🟡 Moyen'])
        risque_eleve = len(risques[risques['niveau_risque'] == '🔴 Élevé'])
        
        with col1:
            st.metric("🟢 Risque faible", risque_faible)
        with col2:
            st.metric("🟡 Risque moyen", risque_moyen)
        with col3:
            st.metric("🔴 Risque élevé", risque_eleve)
        
        # Tableau des risques
        st.dataframe(
            risques[['joueur', 'poste', 'age', 'niveau_risque', 'risque_blessure']],
            column_config={
                "joueur": "Joueur",
                "poste": "Poste",
                "age": "Âge",
                "niveau_risque": "Niveau de risque",
                "risque_blessure": st.column_config.ProgressColumn(
                    "Score de risque", min_value=0, max_value=1
                )
            },
            use_container_width=True
        )
        
        # Recommandations IA
        st.markdown("### 🎯 Recommandations IA")
        
        if risque_eleve > 0:
            st.markdown('<div class="alert-danger">⚠️ <strong>Attention:</strong> Joueurs à risque élevé détectés. Repos préventif recommandé.</div>', unsafe_allow_html=True)
        
        if risque_moyen > 3:
            st.markdown('<div class="alert-warning">⚠️ <strong>Vigilance:</strong> Plusieurs joueurs nécessitent une surveillance renforcée.</div>', unsafe_allow_html=True)
        
        if risque_faible >= len(donnees['effectif']) * 0.7:
            st.markdown('<div class="alert-success">✅ <strong>Excellent:</strong> La majorité de l\'effectif présente un faible risque de blessure.</div>', unsafe_allow_html=True)
    
    except Exception as e:
        st.error(f"❌ Erreur lors de l'analyse des risques: {str(e)}")
    
    # Composition optimale IA
    st.markdown("### 🎯 Composition optimale IA")
    
    try:
        composition = donnees['analytics'].optimiser_composition_ia()
        
        # Affichage de la composition
        formation_col1, formation_col2 = st.columns(2)
        
        with formation_col1:
            st.markdown("**Formation: 4-2-3-1**")
            
            for poste, joueurs in composition.items():
                if joueurs:  # Si des joueurs sont sélectionnés pour ce poste
                    st.markdown(f"**{poste}:**")
                    for joueur in joueurs:
                        score = joueur['score_selection']
                        st.write(f"  • {joueur['nom']} (Score: {score:.2f})")
        
        with formation_col2:
            # Visualisation tactique simplifiée
            fig_tactique = go.Figure()
            
            # Terrain
            fig_tactique.add_shape(
                type="rect", x0=0, y0=0, x1=10, y1=7,
                line=dict(color="green", width=2), fillcolor="lightgreen", opacity=0.3
            )
            
            # Positions approximatives en 4-2-3-1
            positions = {
                'GB': [(5, 0.5)],
                'DC': [(3, 2), (7, 2)],
                'DD': [(9, 2)], 'DG': [(1, 2)],
                'MDC': [(3.5, 4), (6.5, 4)],
                'MOC': [(5, 5.5)],
                'AD': [(8.5, 5.5)], 'AG': [(1.5, 5.5)],
                'BU': [(5, 6.5)]
            }
            
            for poste, coords in positions.items():
                for x, y in coords:
                    fig_tactique.add_trace(
                        go.Scatter(
                            x=[x], y=[y], mode='markers+text',
                            marker=dict(size=20, color=config_rcs.couleur_primaire),
                            text=[poste], textposition="middle center",
                            textfont=dict(color="white", size=10),
                            showlegend=False
                        )
                    )
            
            fig_tactique.update_layout(
                title="Formation 4-2-3-1 RCS",
                xaxis=dict(showgrid=False, showticklabels=False, range=[0, 10]),
                yaxis=dict(showgrid=False, showticklabels=False, range=[0, 7]),
                height=400
            )
            
            st.plotly_chart(fig_tactique, use_container_width=True)
    
    except Exception as e:
        st.error(f"❌ Erreur lors de l'optimisation de composition: {str(e)}")

def afficher_sante_performance(donnees):
    """Affiche les métriques de santé et performance"""
    st.markdown("## 🏥 Santé & Performance de l'effectif")
    
    # Métriques de charge de travail
    st.markdown("### 📊 Charge de travail")
    
    # Simulation de données de fatigue
    effectif_avec_fatigue = donnees['effectif'].copy()
    effectif_avec_fatigue['fatigue_estimee'] = np.random.uniform(0.2, 0.8, len(effectif_avec_fatigue))
    effectif_avec_fatigue['minutes_totales'] = effectif_avec_fatigue['matchs_joues'] * 75  # Estimation
    
    # Graphiques de charge
    col1, col2 = st.columns(2)
    
    with col1:
        fig_fatigue = px.bar(
            effectif_avec_fatigue.nlargest(10, 'fatigue_estimee'),
            x='fatigue_estimee', y='nom',
            orientation='h',
            title="🔋 Niveau de fatigue estimé (Top 10)",
            color='fatigue_estimee',
            color_continuous_scale=['green', 'yellow', 'red']
        )
        st.plotly_chart(fig_fatigue, use_container_width=True)
    
    with col2:
        fig_minutes = px.scatter(
            effectif_avec_fatigue,
            x='minutes_totales', y='fatigue_estimee',
            size='age', color='poste',
            hover_name='nom',
            title="⏱️ Minutes jouées vs Fatigue"
        )
        st.plotly_chart(fig_minutes, use_container_width=True)
    
    # Alertes de santé
    st.markdown("### ⚠️ Alertes de santé")
    
    # Détection automatique d'alertes
    alertes = []
    
    for _, joueur in effectif_avec_fatigue.iterrows():
        if joueur['fatigue_estimee'] > 0.7:
            alertes.append({
                'type': 'danger',
                'joueur': joueur['nom'],
                'message': f"Fatigue élevée ({joueur['fatigue_estimee']:.1%}) - Repos recommandé"
            })
        elif joueur['matchs_joues'] > 15 and joueur['age'] > 30:
            alertes.append({
                'type': 'warning',
                'joueur': joueur['nom'],
                'message': f"Charge importante ({joueur['matchs_joues']} matchs) pour un joueur expérimenté"
            })
        elif joueur['note_moyenne'] < 6.0:
            alertes.append({
                'type': 'warning',
                'joueur': joueur['nom'],
                'message': f"Performance en baisse (note: {joueur['note_moyenne']:.2f})"
            })
    
    if alertes:
        for alerte in alertes:
            if alerte['type'] == 'danger':
                st.markdown(f'<div class="alert-danger">🚨 <strong>{alerte["joueur"]}:</strong> {alerte["message"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="alert-warning">⚠️ <strong>{alerte["joueur"]}:</strong> {alerte["message"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="alert-success">✅ Aucune alerte critique détectée. L\'effectif est en bonne condition.</div>', unsafe_allow_html=True)

def afficher_rapports(donnees):
    """Affiche les rapports automatisés"""
    st.markdown("## 📈 Rapports & Analyses Automatisées")
    
    # Génération du rapport hebdomadaire
    try:
        rapport = donnees['analytics'].generer_rapport_weekly()
        
        st.markdown("### 📋 Rapport Hebdomadaire Automatisé")
        
        # Informations générales
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"**Date de génération:** {rapport['date_generation']}")
            st.markdown(f"**Saison:** {rapport['saison']}")
            st.markdown(f"**Position Ligue 1:** {rapport['position_ligue1']}ème")
            st.markdown(f"**Meilleur joueur:** {rapport['meilleur_joueur']} ({rapport['meilleure_note']:.2f})")
        
        with col2:
            st.markdown(f"**Note moyenne équipe:** {rapport['note_moyenne_equipe']:.2f}")
            st.markdown(f"**Âge moyen:** {rapport['age_moyen']:.1f} ans")
            st.markdown(f"**Valeur totale effectif:** {rapport['valeur_totale']:.1f}M€")
        
        # Alertes automatiques
        if rapport['joueurs_fatigue']:
            st.markdown("#### ⚠️ Joueurs en situation de fatigue")
            for joueur in rapport['joueurs_fatigue']:
                st.warning(f"🔋 **{joueur['nom']}** - {joueur['matchs_joues']} matchs joués (fatigue: {joueur['fatigue_moyenne']:.1%})")
        
        if rapport['joueurs_forme_descendante']:
            st.markdown("#### 📉 Joueurs en baisse de forme")
            for joueur in rapport['joueurs_forme_descendante']:
                st.warning(f"📈 **{joueur['nom']}** - Baisse de {joueur['baisse']:.2f} pts (forme actuelle: {joueur['forme_actuelle']:.2f})")
        
        # Axes d'amélioration
        if rapport['axes_amelioration']:
            st.markdown("#### 🎯 Axes d'amélioration prioritaires")
            for axe in rapport['axes_amelioration']:
                priorite_color = "🔴" if axe['priorite'] == 'Haute' else "🟡"
                st.info(f"{priorite_color} **{axe['domaine']}** (Note: {axe['note_actuelle']:.2f}) - {axe['recommandation']}")
        
    except Exception as e:
        st.error(f"❌ Erreur lors de la génération du rapport: {str(e)}")
    
    # Boutons d'export
    st.markdown("### 📤 Export des données")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Exporter effectif (CSV)"):
            csv = donnees['effectif'].to_csv(index=False)
            st.download_button(
                label="💾 Télécharger CSV",
                data=csv,
                file_name=f"effectif_rcs_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
    
    with col2:
        if st.button("📈 Exporter graphiques"):
            st.info("🚧 Fonctionnalité en développement")
    
    with col3:
        if st.button("📋 Rapport PDF"):
            st.info("🚧 Génération PDF à venir")

def main():
    """Fonction principale de l'application"""
    
    # Affichage du header
    afficher_header()
    
    # Chargement des données
    with st.spinner("⏳ Chargement des données RCS..."):
        donnees = charger_donnees_rcs()
    
    if donnees is None:
        st.error("❌ Impossible de charger les données. Vérifiez la connexion.")
        st.stop()
    
    # Sidebar et filtres
    vue_selectionnee, postes_filtres, filtres_age = afficher_sidebar(donnees)
    filtres = (postes_filtres, filtres_age)
    
    # Affichage selon la vue sélectionnée
    if vue_selectionnee == "🏠 Vue d'ensemble":
        afficher_vue_ensemble(donnees)
    
    elif vue_selectionnee == "👥 Effectif détaillé":
        afficher_effectif_detaille(donnees, filtres)
    
    elif vue_selectionnee == "📊 Analytics avancés":
        afficher_analytics_avances(donnees)
    
    elif vue_selectionnee == "🤖 Prédictions IA":
        afficher_predictions_ia(donnees)
    
    elif vue_selectionnee == "🏥 Santé & Performance":
        afficher_sante_performance(donnees)
    
    elif vue_selectionnee == "📈 Rapports":
        afficher_rapports(donnees)
    
    # Footer
    st.markdown("---")
    st.markdown(
        f"🔵⚪ **Racing Club de Strasbourg Analytics Platform** | "
        f"Saison {config_rcs.saison} | "
        f"Généré le {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}"
    )

if __name__ == "__main__":
    main()
