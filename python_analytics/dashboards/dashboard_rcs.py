"""
Dashboard Racing Club de Strasbourg
===================================

Interface d'analyse football spécialement conçue pour le staff technique du RCS.
Toutes les fonctionnalités sont adaptées aux besoins et au contexte du club alsacien.

Auteur: Football Analytics Platform  
Équipe: Racing Club de Strasbourg
Version: 2.0 - Spécialisée RCS
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import sys
import os

# Ajouter le chemin des modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'modules'))

# Import des modules RCS spécialisés
from analyseur_rcs import AnalyseurPerformanceRCS
from moteur_scouting_rcs import MoteurScoutingRCS

# Configuration de la page
st.set_page_config(
    page_title="Racing Club de Strasbourg - Analytics",
    page_icon="🔵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé aux couleurs du RCS
st.markdown("""
<style>
    .main > div {
        padding-top: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #0066CC 0%, #004499 100%);
        padding: 1rem;
        border-radius: 0.5rem;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    .stSelectbox > div > div {
        background-color: #f0f8ff;
    }
    h1 {
        color: #0066CC;
        text-align: center;
        padding: 1rem 0;
        border-bottom: 3px solid #0066CC;
    }
    .rcs-header {
        background: linear-gradient(90deg, #0066CC, #FFFFFF, #0066CC);
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Interface principale du dashboard RCS"""
    
    # En-tête du RCS
    st.markdown("""
    <div class="rcs-header">
        <h1>🔵⚪ Racing Club de Strasbourg - Football Analytics</h1>
        <p style="text-align: center; font-size: 1.2em; margin: 0;">
            <strong>Stade de la Meinau • Ligue 1 • Saison 2024-2025</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialisation des analyseurs
    if 'analyseur_rcs' not in st.session_state:
        st.session_state.analyseur_rcs = AnalyseurPerformanceRCS()
        st.session_state.moteur_scouting = MoteurScoutingRCS()
    
    # Menu de navigation
    st.sidebar.image("https://via.placeholder.com/300x200/0066CC/FFFFFF?text=RC+Strasbourg", width=300)
    
    pages = {
        "🏠 Tableau de Bord": afficher_tableau_de_bord,
        "👥 Effectif RCS": afficher_effectif_rcs,
        "📊 Analyse Joueur": afficher_analyse_joueur,
        "⚽ Performance Match": afficher_performance_match,
        "🎯 Scouting": afficher_scouting_rcs,
        "📈 Analyses Tactiques": afficher_analyses_tactiques,
        "📋 Rapports": afficher_rapports_rcs
    }
    
    selection = st.sidebar.selectbox("Navigation", list(pages.keys()))
    
    # Informations rapides en sidebar
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 Infos Rapides RCS")
    
    col1, col2 = st.sidebar.columns(2)
    with col1:
        st.metric("Effectif", "18", "")
        st.metric("Âge moyen", "23.2", "↓ 0.8")
    with col2:
        st.metric("Matchs joués", "12", "")
        st.metric("Points", "16", "↗️ +3")
    
    # Affichage de la page sélectionnée
    pages[selection]()

def afficher_tableau_de_bord():
    """Tableau de bord principal du RCS"""
    
    analyseur = st.session_state.analyseur_rcs
    
    st.header("🏠 Tableau de Bord Racing Club de Strasbourg")
    
    # Métriques principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>Classement</h3>
            <h2>9ème</h2>
            <small>↗️ +2 places</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>Points</h3>
            <h2>16 pts</h2>
            <small>12 matchs joués</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>Buts marqués</h3>
            <h2>18</h2>
            <small>1.5 par match</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h3>Buts encaissés</h3>
            <h2>14</h2>
            <small>1.2 par match</small>
        </div>
        """, unsafe_allow_html=True)
    
    # Graphiques de performance
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Évolution des Points")
        
        # Simulation données saison
        matchs = list(range(1, 13))
        points_cumules = [0, 1, 4, 4, 7, 8, 11, 11, 14, 14, 16, 16]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=matchs,
            y=points_cumules,
            mode='lines+markers',
            name='Points RCS',
            line=dict(color='#0066CC', width=3),
            marker=dict(size=8)
        ))
        
        fig.update_layout(
            title="Évolution des points en championnat",
            xaxis_title="Journée",
            yaxis_title="Points cumulés",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("⚽ Statistiques Offensives/Défensives")
        
        categories = ['Buts<br>marqués', 'Passes<br>décisives', 'Tirs<br>cadrés', 'Clean<br>sheets', 'Tacles<br>réussis']
        valeurs_rcs = [18, 12, 42, 4, 156]
        moyenne_ligue = [19.5, 13.2, 38.8, 3.8, 142]
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=categories,
            y=valeurs_rcs,
            name='RCS',
            marker_color='#0066CC'
        ))
        
        fig.add_trace(go.Bar(
            x=categories,
            y=moyenne_ligue,
            name='Moyenne Ligue 1',
            marker_color='#CCCCCC'
        ))
        
        fig.update_layout(
            title="Comparaison avec la moyenne Ligue 1",
            barmode='group',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Prochains matchs
    st.subheader("📅 Prochains Matchs")
    
    prochains_matchs = pd.DataFrame({
        'Date': ['23/11/2024', '30/11/2024', '07/12/2024'],
        'Adversaire': ['AS Monaco', 'Stade Rennais', 'OGC Nice'],
        'Lieu': ['Extérieur', 'Domicile', 'Extérieur'],
        'Importance': ['⭐⭐⭐', '⭐⭐', '⭐⭐⭐']
    })
    
    st.dataframe(prochains_matchs, use_container_width=True)

def afficher_effectif_rcs():
    """Affichage de l'effectif actuel du RCS"""
    
    analyseur = st.session_state.analyseur_rcs
    effectif = analyseur.obtenir_effectif_actuel()
    
    st.header("👥 Effectif Racing Club de Strasbourg 2024-2025")
    
    # Filtres
    col1, col2, col3 = st.columns(3)
    
    with col1:
        postes_filtre = st.multiselect(
            "Filtrer par poste",
            effectif['poste'].unique(),
            default=effectif['poste'].unique()
        )
    
    with col2:
        age_min, age_max = st.slider("Âge", 16, 35, (16, 35))
    
    with col3:
        nationalites_filtre = st.multiselect(
            "Filtrer par nationalité",
            effectif['nationalite'].unique(),
            default=effectif['nationalite'].unique()
        )
    
    # Application des filtres
    effectif_filtre = effectif[
        (effectif['poste'].isin(postes_filtre)) &
        (effectif['age'] >= age_min) &
        (effectif['age'] <= age_max) &
        (effectif['nationalite'].isin(nationalites_filtre))
    ]
    
    # Affichage par ligne
    st.subheader("⚽ Effectif par Ligne")
    
    gardiens = effectif_filtre[effectif_filtre['poste'] == 'GB']
    defenseurs = effectif_filtre[effectif_filtre['poste'].isin(['DC', 'DD', 'DG'])]
    milieux = effectif_filtre[effectif_filtre['poste'].isin(['MDC', 'MC', 'MOC'])]
    attaquants = effectif_filtre[effectif_filtre['poste'].isin(['BU', 'AD', 'AG'])]
    
    if not gardiens.empty:
        st.markdown("### 🥅 Gardiens")
        st.dataframe(gardiens[['nom_complet', 'age', 'nationalite', 'numero']], use_container_width=True)
    
    if not defenseurs.empty:
        st.markdown("### 🛡️ Défenseurs")
        st.dataframe(defenseurs[['nom_complet', 'poste', 'age', 'nationalite', 'numero']], use_container_width=True)
    
    if not milieux.empty:
        st.markdown("### ⚙️ Milieux")
        st.dataframe(milieux[['nom_complet', 'poste', 'age', 'nationalite', 'numero']], use_container_width=True)
    
    if not attaquants.empty:
        st.markdown("### ⚽ Attaquants")
        st.dataframe(attaquants[['nom_complet', 'poste', 'age', 'nationalite', 'numero']], use_container_width=True)
    
    # Statistiques de l'effectif
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Répartition par Âge")
        
        tranches_age = pd.cut(effectif_filtre['age'], bins=[0, 20, 23, 26, 30, 40], 
                             labels=['U20', '20-23', '23-26', '26-30', '30+'])
        repartition_age = tranches_age.value_counts()
        
        fig = px.pie(values=repartition_age.values, names=repartition_age.index,
                     title="Répartition par tranche d'âge",
                     color_discrete_sequence=['#0066CC', '#004499', '#0088FF', '#66AAFF', '#AACCFF'])
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🌍 Répartition par Nationalité")
        
        repartition_nat = effectif_filtre['nationalite'].value_counts()
        
        fig = px.bar(x=repartition_nat.index, y=repartition_nat.values,
                     title="Joueurs par nationalité",
                     color_discrete_sequence=['#0066CC'])
        
        fig.update_layout(xaxis_title="Nationalité", yaxis_title="Nombre de joueurs")
        
        st.plotly_chart(fig, use_container_width=True)

def afficher_analyse_joueur():
    """Interface d'analyse individuelle des joueurs"""
    
    analyseur = st.session_state.analyseur_rcs
    effectif = analyseur.obtenir_effectif_actuel()
    
    st.header("📊 Analyse Individuelle des Joueurs RCS")
    
    # Sélection du joueur
    joueur_selectionne = st.selectbox(
        "Choisir un joueur à analyser",
        effectif['nom_complet'].tolist()
    )
    
    if joueur_selectionne:
        # Analyse de forme
        forme = analyseur.analyser_forme_joueur_rcs(joueur_selectionne)
        
        if "erreur" not in forme:
            # Informations du joueur
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"### 👤 {forme['joueur']}")
                st.write(f"**Poste:** {forme['poste']}")
                st.write(f"**Matchs analysés:** {forme['matchs_analyses']}")
            
            with col2:
                st.metric("Tendance de forme", forme['tendance_forme'], "")
                st.metric("Score consistance", forme['score_consistance'], "")
            
            with col3:
                # Badge selon la forme
                couleur_badge = {
                    'amélioration': '🟢',
                    'stable': '🟡', 
                    'déclin': '🔴'
                }.get(forme['tendance_forme'], '⚪')
                
                st.markdown(f"### {couleur_badge} Forme Actuelle")
                st.write(forme['tendance_forme'].title())
            
            # Recommandation
            st.markdown("### 💡 Recommandation Staff")
            st.info(forme['recommandation'])
            
            # Statistiques détaillées
            st.subheader("📈 Statistiques Clés")
            
            stats = forme['statistiques_cles']
            
            # Adapter l'affichage selon le poste
            if forme['poste'] == 'GB':
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Note moyenne", f"{stats['note_moyenne']:.1f}", "")
                with col2:
                    st.metric("Arrêts/match", f"{stats['arrets_match']:.1f}", "")
                with col3:
                    st.metric("Buts encaissés", f"{stats['buts_encaisses']:.1f}", "")
                with col4:
                    st.metric("Clean sheets", stats['clean_sheets'], "")
            
            elif forme['poste'] in ['DC', 'DD', 'DG']:
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Note moyenne", f"{stats['note_moyenne']:.1f}", "")
                with col2:
                    st.metric("Tacles réussis", f"{stats['tacles_reussis']:.1f}", "")
                with col3:
                    st.metric("Interceptions", f"{stats['interceptions']:.1f}", "")
                with col4:
                    st.metric("Duels aériens %", f"{stats['duels_aeriens_pct']:.0f}%", "")
            
            elif forme['poste'] in ['MDC', 'MC', 'MOC']:
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Note moyenne", f"{stats['note_moyenne']:.1f}", "")
                with col2:
                    st.metric("Passes réussies %", f"{stats['passes_reussies_pct']:.1f}%", "")
                with col3:
                    st.metric("Passes clés", f"{stats['passes_cles']:.1f}", "")
                with col4:
                    st.metric("Km parcourus", f"{stats['kilometres_parcourus']:.1f}", "")
            
            else:  # Attaquants
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Note moyenne", f"{stats['note_moyenne']:.1f}", "")
                with col2:
                    st.metric("Buts/90min", f"{stats['buts_par_90']:.2f}", "")
                with col3:
                    st.metric("Passes D./90min", f"{stats['passes_decisives_par_90']:.2f}", "")
                with col4:
                    st.metric("Tirs/match", f"{stats['tirs_par_match']:.1f}", "")
            
            # Graphique radar de performance
            st.subheader("🎯 Profil de Performance - Radar")
            
            # Générer des données radar selon le poste
            if forme['poste'] in ['BU', 'AD', 'AG']:
                categories = ['Finition', 'Vitesse', 'Dribble', 'Passes', 'Physique', 'Mental']
                valeurs = [stats['note_moyenne']*10, 85, 75, 70, 80, 78]
            elif forme['poste'] in ['MDC', 'MC', 'MOC']:
                categories = ['Passes', 'Vision', 'Récupération', 'Physique', 'Technique', 'Mental']
                valeurs = [stats['passes_reussies_pct'], 82, 85, 80, 77, 83]
            else:  # Défenseurs et gardiens
                categories = ['Défense', 'Anticipation', 'Duel aérien', 'Passes', 'Physique', 'Mental']
                valeurs = [88, 85, stats.get('duels_aeriens_pct', 70), 75, 82, 80]
            
            # Normaliser les valeurs sur 100
            valeurs_normalisees = [min(100, max(0, v)) for v in valeurs]
            
            fig = go.Figure()
            
            fig.add_trace(go.Scatterpolar(
                r=valeurs_normalisees,
                theta=categories,
                fill='toself',
                name=joueur_selectionne,
                line_color='#0066CC'
            ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 100]
                    )),
                showlegend=True,
                title=f"Profil de performance - {joueur_selectionne}",
                height=500
            )
            
            st.plotly_chart(fig, use_container_width=True)

def afficher_performance_match():
    """Interface de performance de match"""
    
    analyseur = st.session_state.analyseur_rcs
    
    st.header("⚽ Performance Match RCS")
    
    # Sélection du match à analyser
    adversaires_recents = [
        "AS Monaco", "Olympique Lyonnais", "Stade Rennais", 
        "OGC Nice", "RC Lens", "LOSC Lille"
    ]
    
    col1, col2 = st.columns(2)
    
    with col1:
        adversaire = st.selectbox("Adversaire", adversaires_recents)
    
    with col2:
        domicile = st.radio("Lieu", ["Domicile (Meinau)", "Extérieur"], index=0)
        est_domicile = domicile == "Domicile (Meinau)"
    
    if st.button("Générer Rapport de Match", type="primary"):
        rapport = analyseur.generer_rapport_match_rcs(adversaire, est_domicile)
        
        # Score et informations générales
        st.markdown(f"### 📊 {rapport['score_final']}")
        st.write(f"**Lieu:** {rapport['lieu']}")
        
        # Métriques principales
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Possession", 
                f"RCS {rapport['possession']['rcs']}%",
                f"{rapport['possession']['adversaire']}% {adversaire}"
            )
        
        with col2:
            st.metric(
                "Expected Goals (xG)",
                f"RCS {rapport['xg']['rcs']}",
                f"{rapport['xg']['adversaire']} {adversaire}"
            )
        
        with col3:
            efficacite_rcs = (int(rapport['score_final'].split(' ')[1]) / max(rapport['xg']['rcs'], 0.1)) * 100
            st.metric("Efficacité RCS", f"{efficacite_rcs:.0f}%", "")
        
        # Statistiques détaillées
        st.subheader("📈 Statistiques Détaillées")
        
        stats = rapport['statistiques_detaillees']
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Tirs", stats['tirs_rcs'], "")
            st.metric("Tirs cadrés", stats['tirs_cadres_rcs'], "")
        
        with col2:
            st.metric("Corners", stats['corners_rcs'], "")
            st.metric("Fautes", stats['fautes_rcs'], "")
        
        with col3:
            st.metric("Cartons jaunes", stats['cartons_jaunes_rcs'], "")
            st.metric("Cartons rouges", stats['cartons_rouges_rcs'], "")
        
        with col4:
            st.write("**Autres métriques:**")
            efficacite_tirs = (stats['tirs_cadres_rcs'] / max(stats['tirs_rcs'], 1)) * 100
            st.write(f"Efficacité tirs: {efficacite_tirs:.1f}%")
            st.write(f"Discipline: {'🟢 Bon' if stats['cartons_jaunes_rcs'] <= 2 else '🟡 Moyen' if stats['cartons_jaunes_rcs'] <= 4 else '🔴 Problème'}")
        
        # Performances individuelles
        st.subheader("⭐ Performances Individuelles")
        
        perfs = pd.DataFrame(rapport['performances_individuelles'])
        
        # Top 3 et Flop 3
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🏆 Top 3 Performances")
            top_3 = perfs.head(3)
            for _, joueur in top_3.iterrows():
                st.write(f"**{joueur['nom']}** ({joueur['poste']}) - Note: {joueur['note']}")
                st.write(f"↳ {joueur['commentaire']}")
                st.write("")
        
        with col2:
            st.markdown("#### ⚠️ Performances à améliorer")
            flop_3 = perfs.tail(3)
            for _, joueur in flop_3.iterrows():
                st.write(f"**{joueur['nom']}** ({joueur['poste']}) - Note: {joueur['note']}")
                st.write(f"↳ {joueur['commentaire']}")
                st.write("")
        
        # Graphique des notes
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=perfs['nom'],
            y=perfs['note'],
            text=perfs['note'],
            textposition='auto',
            marker_color=['#0066CC' if note >= 7 else '#FF6600' if note >= 6 else '#FF0000' 
                         for note in perfs['note']]
        ))
        
        fig.update_layout(
            title="Notes de performance individuelles",
            xaxis_title="Joueurs",
            yaxis_title="Note /10",
            height=400,
            xaxis_tickangle=45
        )
        
        st.plotly_chart(fig, use_container_width=True)

def afficher_scouting_rcs():
    """Interface de scouting spécialisée RCS"""
    
    moteur = st.session_state.moteur_scouting
    
    st.header("🎯 Scouting Racing Club de Strasbourg")
    
    # Filtres de recherche
    st.subheader("🔍 Critères de Recherche")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        poste_filtre = st.selectbox(
            "Poste recherché",
            ["Tous"] + ["GB", "DC", "DD", "DG", "MDC", "MC", "MOC", "AD", "AG", "BU"]
        )
    
    with col2:
        budget_max = st.slider(
            "Budget maximum (M€)",
            0.5, 20.0, 10.0, 0.5
        )
    
    with col3:
        age_max_filtre = st.slider(
            "Âge maximum",
            18, 30, 26, 1
        )
    
    # Recherche de cibles
    if st.button("🔍 Rechercher des Cibles", type="primary"):
        
        # Appliquer les filtres
        poste_recherche = None if poste_filtre == "Tous" else poste_filtre
        
        cibles = moteur.rechercher_cibles_prioritaires(
            poste_recherche=poste_recherche,
            budget_max=budget_max
        )
        
        # Filtrer par âge
        cibles_filtrees = cibles[cibles['age'] <= age_max_filtre]
        
        st.subheader(f"🎯 {len(cibles_filtrees)} Cibles Identifiées")
        
        if not cibles_filtrees.empty:
            # Top 10 cibles
            top_cibles = cibles_filtrees.head(10)
            
            # Affichage en tableau
            affichage_cibles = top_cibles[[
                'nom', 'age', 'poste', 'club', 'ligue', 'nationalite',
                'valeur_marche_millions', 'note_globale', 'potentiel', 'score_rcs'
            ]].copy()
            
            affichage_cibles.columns = [
                'Nom', 'Âge', 'Poste', 'Club', 'Ligue', 'Nationalité',
                'Valeur (M€)', 'Note', 'Potentiel', 'Score RCS'
            ]
            
            st.dataframe(affichage_cibles, use_container_width=True)
            
            # Graphiques d'analyse
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📊 Répartition par Ligue")
                repartition_ligue = top_cibles['ligue'].value_counts()
                
                fig = px.pie(
                    values=repartition_ligue.values,
                    names=repartition_ligue.index,
                    title="Origine des cibles prioritaires"
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.subheader("💰 Valeur vs Score RCS")
                
                fig = px.scatter(
                    top_cibles,
                    x='valeur_marche_millions',
                    y='score_rcs',
                    size='note_globale',
                    color='age',
                    hover_name='nom',
                    title="Opportunités de transfert",
                    labels={
                        'valeur_marche_millions': 'Valeur marchande (M€)',
                        'score_rcs': 'Score RCS'
                    }
                )
                
                st.plotly_chart(fig, use_container_width=True)
        
        else:
            st.warning("Aucune cible trouvée avec ces critères. Essayez d'élargir vos paramètres.")
    
    # Analyse détaillée d'un joueur
    st.subheader("🔍 Analyse Détaillée de Cible")
    
    # Liste des joueurs disponibles
    base_scouting = moteur.generer_base_donnees_scouting()
    joueur_analyse = st.selectbox(
        "Choisir un joueur à analyser en détail",
        base_scouting['nom'].tolist()
    )
    
    if st.button("📋 Analyser cette Cible", type="secondary"):
        analyse = moteur.analyser_opportunite_transfert(joueur_analyse)
        
        if "erreur" not in analyse:
            # Informations du joueur
            joueur_info = analyse['joueur']
            st.markdown(f"### 👤 {joueur_info['nom']}")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.write(f"**Âge:** {joueur_info['age']} ans")
                st.write(f"**Poste:** {joueur_info['poste']}")
                st.write(f"**Club:** {joueur_info['club_actuel']}")
                st.write(f"**Nationalité:** {joueur_info['nationalite']}")
            
            with col2:
                eval_sportive = analyse['evaluation_sportive']
                st.metric("Note globale", eval_sportive['note_globale'], "")
                st.write(f"**Potentiel:** {eval_sportive['potentiel']}")
                st.metric("Score RCS", eval_sportive['score_priorite'], "")
            
            with col3:
                finances = analyse['analyse_financiere']
                st.metric("Valeur marchande", finances['valeur_marche'], "")
                st.metric("Salaire annuel", finances['salaire_annuel'], "")
                st.write(f"**% Budget:** {finances['pct_budget_utilise']}")
            
            # Recommandation
            st.markdown("### 💡 Recommandation")
            st.markdown(f"**{analyse['recommandation']}**")
            
            # Avantages et risques
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### ✅ Avantages")
                for avantage in analyse['avantages']:
                    st.write(f"• {avantage}")
            
            with col2:
                st.markdown("#### ⚠️ Risques")
                for risque in analyse['risques']:
                    st.write(f"• {risque}")
            
            # Actions suivantes
            st.markdown("#### 📋 Actions Recommandées")
            for i, action in enumerate(analyse['actions_suivantes'], 1):
                st.write(f"{i}. {action}")

def afficher_analyses_tactiques():
    """Interface d'analyses tactiques"""
    
    analyseur = st.session_state.analyseur_rcs
    
    st.header("📈 Analyses Tactiques Racing Club de Strasbourg")
    
    # Analyse tactique du RCS
    analyse_tactique = analyseur.analyser_tactique_rcs()
    
    # Système de jeu
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("⚙️ Système de Jeu")
        st.metric("Formation principale", analyse_tactique['formation_principale'], "")
        
        st.write("**Formations alternatives:**")
        for formation in analyse_tactique['formations_alternatives']:
            st.write(f"• {formation}")
    
    with col2:
        st.subheader("📊 Style de Jeu")
        style = analyse_tactique['style_de_jeu']
        
        st.metric("Possession moyenne", f"{style['possession_moyenne']}%", "")
        st.metric("Passes par match", style['passes_par_match'], "")
        st.metric("Précision passes", f"{style['precision_passes']}%", "")
        
        st.write(f"**Pressing:** {style['pressing_haute']}")
        st.write(f"**Vitesse transition:** {style['vitesse_transition']}")
    
    # Forces et axes d'amélioration
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💪 Forces Tactiques")
        for force in analyse_tactique['forces']:
            st.write(f"✅ {force}")
    
    with col2:
        st.subheader("🎯 Axes d'Amélioration")
        for axe in analyse_tactique['axes_amelioration']:
            st.write(f"🔧 {axe}")
    
    # Joueurs clés
    st.subheader("⭐ Joueurs Clés par Rôle")
    
    joueurs_cles = analyse_tactique['joueurs_cles']
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("**🎯 Créateur**")
        st.write(joueurs_cles['createur'])
    
    with col2:
        st.markdown("**⚽ Finisseur**")
        st.write(joueurs_cles['finisseur'])
    
    with col3:
        st.markdown("**🛡️ Leader défensif**")
        st.write(joueurs_cles['leader_defensif'])
    
    with col4:
        st.markdown("**⚙️ Métronome**")
        st.write(joueurs_cles['metronome'])
    
    # Graphique tactique interactif
    st.subheader("🎮 Analyse Tactique Interactive")
    
    # Simulation de heatmap d'équipe
    x_pos = np.random.normal(50, 20, 100)
    y_pos = np.random.normal(50, 15, 100)
    
    fig = go.Figure()
    
    fig.add_trace(go.Histogram2d(
        x=x_pos,
        y=y_pos,
        colorscale='Blues',
        name='Zones d\'activité RCS'
    ))
    
    fig.update_layout(
        title="Heatmap d'activité d'équipe (simulation)",
        xaxis_title="Largeur du terrain",
        yaxis_title="Longueur du terrain",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)

def afficher_rapports_rcs():
    """Interface de génération de rapports"""
    
    st.header("📋 Rapports Racing Club de Strasbourg")
    
    type_rapport = st.selectbox(
        "Type de rapport",
        [
            "📊 Rapport hebdomadaire",
            "⚽ Analyse post-match",
            "📈 Bilan mensuel",
            "🎯 Rapport de scouting",
            "👥 Analyse de l'effectif"
        ]
    )
    
    if st.button("📄 Générer le Rapport", type="primary"):
        
        if "hebdomadaire" in type_rapport:
            generer_rapport_hebdomadaire()
        elif "post-match" in type_rapport:
            generer_rapport_post_match()
        elif "mensuel" in type_rapport:
            generer_rapport_mensuel()
        elif "scouting" in type_rapport:
            generer_rapport_scouting()
        else:
            generer_rapport_effectif()

def generer_rapport_hebdomadaire():
    """Génère un rapport hebdomadaire"""
    
    st.subheader("📊 Rapport Hebdomadaire RCS")
    st.write(f"**Semaine du {datetime.now().strftime('%d/%m/%Y')}**")
    
    st.markdown("""
    ### 🎯 Points Clés de la Semaine
    
    #### ⚽ Résultats Sportifs
    - Match contre Lyon: Victoire 2-1 à domicile
    - Montée de 2 places au classement (9ème position)
    - 3 points précieux dans la course au maintien
    
    #### 📈 Performances Notables
    - **Emanuel Emegha**: Doublé décisif, retour en forme
    - **Dilane Bakwa**: 2 passes décisives, créativité retrouvée
    - **Matz Sels**: 6 arrêts importants, solide dans les cages
    
    #### ⚠️ Points d'Attention
    - Concentration défensive à améliorer sur coups de pied arrêtés
    - Efficacité offensive à optimiser (18 tirs, 2 buts)
    - Gestion de l'effort sur 90 minutes
    
    #### 📋 Actions de la Semaine
    - ✅ Travail tactique spécifique défense de zone
    - ✅ Séances de finition pour les attaquants
    - ✅ Récupération active pour les cadres
    - 🔄 Analyse vidéo collective du match
    
    ### 📅 Semaine Prochaine
    - **Lundi**: Récupération + analyse vidéo
    - **Mardi**: Séance tactique pressing
    - **Mercredi**: Travail physique individuel
    - **Jeudi**: Mise en place match suivant
    - **Vendredi**: Activation + voyage
    - **Samedi**: Match vs AS Monaco (extérieur)
    """)

def generer_rapport_post_match():
    """Génère un rapport post-match"""
    
    st.subheader("⚽ Rapport Post-Match RCS")
    
    st.markdown("""
    ### 🔵⚪ RCS 2 - 1 OL
    **Stade de la Meinau - 12/11/2024 - Ligue 1**
    
    #### 📊 Statistiques du Match
    - **Possession**: RCS 47% - 53% OL
    - **Tirs**: RCS 14 - 11 OL
    - **Tirs cadrés**: RCS 6 - 4 OL
    - **xG**: RCS 1.8 - 1.2 OL
    - **Corners**: RCS 7 - 3 OL
    
    #### ⭐ Hommes du Match
    1. **Emanuel Emegha (9.5/10)** - Doublé, présence physique
    2. **Dilane Bakwa (8.8/10)** - 2 passes décisives, percussion
    3. **Abakar Sylla (8.2/10)** - Solide défensivement, leadership
    
    #### 🎯 Points Positifs
    - Efficacité offensive retrouvée (2 buts sur 1.8 xG)
    - Pressing coordonné efficace en première période
    - Solidité défensive dans les moments chauds
    - Mental d'équipe exemplaire
    
    #### 🔧 Axes d'Amélioration
    - Conservation du ballon en seconde période
    - Replacement défensif sur les transitions
    - Concentration sur toute la durée du match
    - Gestion des temps faibles
    
    #### 🏥 Bilan Médical
    - **Andrey Santos**: Coup reçu à la cheville, examens complémentaires
    - **Thomas Delaine**: Fatigue musculaire, repos préventif
    
    #### 📋 Actions Immédiates
    - Récupération active pour les titulaires
    - Travail spécifique conservation ballon
    - Préparation match Monaco (analyse adversaire)
    """)

def generer_rapport_mensuel():
    """Génère un bilan mensuel"""
    
    st.subheader("📈 Bilan Mensuel RCS - Novembre 2024")
    
    # Graphique d'évolution
    matchs = ['J8', 'J9', 'J10', 'J11', 'J12']
    points = [11, 11, 14, 14, 16]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=matchs,
        y=points,
        mode='lines+markers',
        name='Points RCS',
        line=dict(color='#0066CC', width=3)
    ))
    
    fig.update_layout(
        title="Évolution des points en novembre",
        xaxis_title="Journées",
        yaxis_title="Points cumulés"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
    ### 📊 Bilan Novembre 2024
    
    #### 🏆 Résultats
    - **4 matchs joués** | **2 victoires** | **1 nul** | **1 défaite**
    - **7 points pris** sur 12 possibles (58% de réussite)
    - **Évolution classement**: 12ème → 9ème (+3 places)
    
    #### ⚽ Statistiques Offensives
    - **8 buts marqués** (2.0 par match)
    - **xG total**: 6.8 (efficacité: +18%)
    - **Meilleur buteur**: Emanuel Emegha (4 buts)
    - **Meilleur passeur**: Dilane Bakwa (3 passes décisives)
    
    #### 🛡️ Statistiques Défensives  
    - **5 buts encaissés** (1.25 par match)
    - **2 clean sheets**
    - **Meilleur défenseur**: Abakar Sylla (note moyenne: 7.8)
    
    #### 📈 Tendances Positives
    - Amélioration nette de l'efficacité offensive
    - Solidité défensive retrouvée à domicile
    - Cohésion d'équipe en progression
    - Impact positif des jeunes (Bakwa, Emegha)
    
    #### 🎯 Objectifs Décembre
    - Confirmer la dynamique positive
    - Sécuriser le maintien mathématique
    - Développer le jeu en possession
    - Intégrer davantage les jeunes talents
    """)

def generer_rapport_scouting():
    """Génère un rapport de scouting"""
    
    st.subheader("🎯 Rapport de Scouting RCS - Cibles Prioritaires")
    
    st.markdown("""
    ### 🔍 Objectifs Mercato Hiver 2025
    
    #### 🎯 Postes Prioritaires
    1. **Milieu offensif créateur** (backup Bakwa)
    2. **Défenseur central gaucher** (concurrence Sylla)
    3. **Ailier gauche** (profondeur d'effectif)
    
    #### 💰 Budget Disponible
    - **Transferts**: 8-12 M€ maximum
    - **Salaires**: 60-80k€/mois par joueur
    - **Stratégie**: Jeunes talents + opportunités
    
    #### 🌟 Cibles Identifiées
    
    **MILIEU OFFENSIF**
    - **Quentin Boisgard** (Laval, 25 ans) - 6M€
      - ✅ Expérience Ligue 2, créativité, coups de pied arrêtés
      - ⚠️ Physicité limitée, adaptation Ligue 1 incertaine
    
    - **Gustavo Sá** (Famalicão, 22 ans) - 4M€  
      - ✅ Technique portugaise, polyvalence, potentiel
      - ⚠️ Adaptation championnat français
    
    **DÉFENSEUR CENTRAL**
    - **Maxime Do Couto** (Rodez, 23 ans) - 3M€
      - ✅ Gaucher, montées, leadership
      - ⚠️ Niveau actuel, concurrence physique L1
    
    **AILIER GAUCHE**  
    - **Enzo Bardeli** (Guingamp, 22 ans) - 5M€
      - ✅ Vitesse, percussion, potentiel de revente
      - ⚠️ Régularité, défense
    
    #### 📋 Actions Recommandées
    1. **Boisgard**: Négociation avancée, observation live
    2. **Sá**: Contact agent, analyse vidéo approfondie  
    3. **Do Couto**: Suivi continu, alternative sûre
    4. **Bardeli**: Évaluation physique, tests médicaux
    
    #### ⏰ Planning
    - **Décembre**: Finaliser évaluations et négociations
    - **Janvier**: Boucler 1-2 recrues prioritaires
    - **Été 2025**: Compléter effectif selon maintien acquis
    """)

def generer_rapport_effectif():
    """Génère un rapport d'analyse de l'effectif"""
    
    analyseur = st.session_state.analyseur_rcs
    effectif = analyseur.obtenir_effectif_actuel()
    
    st.subheader("👥 Analyse de l'Effectif RCS 2024-2025")
    
    # Statistiques générales
    age_moyen = effectif['age'].mean()
    plus_jeune = effectif['age'].min()
    plus_age = effectif['age'].max()
    
    st.markdown(f"""
    ### 📊 Vue d'Ensemble
    - **Effectif total**: {len(effectif)} joueurs
    - **Âge moyen**: {age_moyen:.1f} ans
    - **Plus jeune**: {plus_jeune} ans | **Plus âgé**: {plus_age} ans
    - **Nationalités**: {effectif['nationalite'].nunique()} différentes
    """)
    
    # Répartition par âge et graphique
    col1, col2 = st.columns(2)
    
    with col1:
        tranches_age = pd.cut(effectif['age'], bins=[0, 21, 25, 28, 35], 
                             labels=['U21', '21-25', '25-28', '28+'])
        repartition = tranches_age.value_counts()
        
        st.markdown("#### 📈 Répartition par Âge")
        for tranche, nombre in repartition.items():
            pourcentage = (nombre / len(effectif)) * 100
            st.write(f"**{tranche}**: {nombre} joueurs ({pourcentage:.1f}%)")
    
    with col2:
        # Graphique circulaire
        fig = px.pie(
            values=repartition.values,
            names=repartition.index,
            title="Pyramide des âges",
            color_discrete_sequence=['#0066CC', '#004499', '#0088FF', '#66AAFF']
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
    ### 🎯 Points Forts de l'Effectif
    - **Jeunesse**: 67% de joueurs de moins de 25 ans
    - **Polyvalence**: Plusieurs joueurs multi-postes
    - **Potentiel**: Forte marge de progression collective
    - **Cohésion**: Groupe soudé et motivé
    
    ### ⚠️ Points d'Attention
    - **Expérience**: Manque de cadres expérimentés
    - **Profondeur**: Effectif limité sur certains postes
    - **Physique**: Adaptation au rythme Ligue 1 en cours
    
    ### 🔄 Évolutions Recommandées
    1. **Recruter un cadre expérimenté** (leadership)
    2. **Densifier le milieu de terrain** (rotations)
    3. **Anticiper les départs** (clauses, renouvellements)
    4. **Valoriser les jeunes** (temps de jeu, formation)
    """)

# Point d'entrée principal
if __name__ == "__main__":
    main()
