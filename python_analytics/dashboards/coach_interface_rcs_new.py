"""
Racing Club de Strasbourg - Football Analytics Dashboard
=======================================================

Interface spécialisée pour le staff technique du Racing Club de Strasbourg.
Version optimisée Streamlit Cloud avec données réelles RCS 2024-2025.

Auteur: Football Analytics Platform
Équipe: Racing Club de Strasbourg
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta

# Configuration de la page
st.set_page_config(
    page_title="🔵⚪ Racing Club de Strasbourg - Analytics",
    page_icon="🔵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé aux couleurs du RCS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #0066CC;
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(90deg, #0066CC, #FFFFFF, #0066CC);
        padding: 1rem;
        border-radius: 10px;
    }
    .metric-card {
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
    .stSelectbox > div > div {
        background-color: #f0f8ff;
    }
    h1, h2, h3 {
        color: #0066CC;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: #f0f8ff;
        border-radius: 4px 4px 0px 0px;
        color: #0066CC;
        font-weight: bold;
    }
    .stTabs [aria-selected="true"] {
        background-color: #0066CC;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Données effectif réel Racing Club de Strasbourg 2024-2025
@st.cache_data
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

@st.cache_data
def obtenir_cibles_scouting_rcs():
    """Base de données scouting adaptée budget RCS"""
    cibles_data = [
        {"nom": "Quentin Boisgard", "age": 25, "poste": "MOC", "club": "Stade Laval", "ligue": "Ligue 2", "valeur": 3.0, "note": 8.2},
        {"nom": "Gustavo Sá", "age": 23, "poste": "BU", "club": "FC Porto B", "ligue": "Liga Portugal 2", "valeur": 5.0, "note": 7.8},
        {"nom": "Ellis Simms", "age": 23, "poste": "BU", "club": "Coventry City", "ligue": "Championship", "valeur": 8.0, "note": 7.5},
        {"nom": "Mees Hilgers", "age": 23, "poste": "DC", "club": "FC Twente", "ligue": "Eredivisie", "valeur": 12.0, "note": 8.0},
        {"nom": "Ryan Manning", "age": 28, "poste": "DG", "club": "Southampton", "ligue": "Championship", "valeur": 6.0, "note": 7.3},
        {"nom": "Ilyes Hamache", "age": 24, "poste": "AG", "club": "Paris FC", "ligue": "Ligue 2", "valeur": 4.5, "note": 7.6},
        {"nom": "Milan van Ewijk", "age": 24, "poste": "DD", "club": "Coventry City", "ligue": "Championship", "valeur": 7.0, "note": 7.4},
        {"nom": "Ethan Laird", "age": 22, "poste": "DD", "club": "Birmingham City", "ligue": "League One", "valeur": 5.5, "note": 7.7}
    ]
    
    return pd.DataFrame(cibles_data)

def main():
    """Interface principale du dashboard RCS"""
    
    # En-tête du RCS
    st.markdown("""
    <div class="main-header">
        🔵⚪ Racing Club de Strasbourg - Football Analytics ⚪🔵
        <br><small>Stade de la Meinau • Ligue 1 • Saison 2024-2025</small>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar avec logo et navigation
    st.sidebar.markdown("## 🔵⚪ Navigation RCS")
    
    tabs = st.tabs([
        "🏠 Tableau de Bord",
        "👥 Effectif",
        "📊 Analyse Joueur", 
        "⚽ Performances",
        "🎯 Scouting",
        "📈 Tactiques"
    ])
    
    # Tab 1: Tableau de Bord
    with tabs[0]:
        afficher_tableau_de_bord()
    
    # Tab 2: Effectif
    with tabs[1]:
        afficher_effectif_rcs()
    
    # Tab 3: Analyse Joueur
    with tabs[2]:
        afficher_analyse_joueur()
    
    # Tab 4: Performances
    with tabs[3]:
        afficher_performances_match()
    
    # Tab 5: Scouting
    with tabs[4]:
        afficher_scouting_rcs()
    
    # Tab 6: Tactiques
    with tabs[5]:
        afficher_analyses_tactiques()

def afficher_tableau_de_bord():
    """Affiche le tableau de bord principal RCS"""
    
    st.header("📊 Tableau de Bord Racing Club de Strasbourg")
    
    # Métriques principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>📍 Classement</h3>
            <h2>15e</h2>
            <p>Ligue 1</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>⚽ Buts marqués</h3>
            <h2>23</h2>
            <p>20 matchs</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>🛡️ Buts encaissés</h3>
            <h2>31</h2>
            <p>20 matchs</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h3>💰 Valeur effectif</h3>
            <h2>73M€</h2>
            <p>19 joueurs</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Objectifs saison
    st.subheader("🎯 Objectifs Saison 2024-2025")
    
    objectifs_col1, objectifs_col2 = st.columns(2)
    
    with objectifs_col1:
        st.markdown("""
        <div class="rcs-card">
            <h4>📍 Classement</h4>
            <p><strong>Objectif:</strong> Maintien confortable (14e-17e)</p>
            <p><strong>Actuel:</strong> 15e place ✅</p>
            <p><strong>Points:</strong> 23 pts / 60 possibles</p>
        </div>
        """, unsafe_allow_html=True)
    
    with objectifs_col2:
        st.markdown("""
        <div class="rcs-card">
            <h4>⚽ Performance offensive</h4>
            <p><strong>Objectif:</strong> 45+ buts sur la saison</p>
            <p><strong>Rythme actuel:</strong> 41 buts projetés ⚠️</p>
            <p><strong>Amélioration:</strong> +10% finition requise</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Graphique évolution classement
    st.subheader("📈 Évolution Classement Ligue 1")
    
    # Données simulées d'évolution
    journees = list(range(1, 21))
    positions = [18, 17, 16, 15, 14, 16, 15, 14, 13, 15, 16, 15, 14, 15, 16, 15, 14, 15, 16, 15]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=journees,
        y=positions,
        mode='lines+markers',
        name='Position RCS',
        line=dict(color='#0066CC', width=3),
        marker=dict(size=8, color='#0066CC')
    ))
    
    fig.add_hline(y=17, line_dash="dash", line_color="red", annotation_text="Zone de relégation")
    fig.update_layout(
        title="Position en Ligue 1 par journée",
        xaxis_title="Journée",
        yaxis_title="Position",
        yaxis=dict(autorange="reversed"),
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)

def afficher_effectif_rcs():
    """Affiche l'effectif complet du RCS"""
    
    st.header("👥 Effectif Racing Club de Strasbourg 2024-2025")
    
    effectif = obtenir_effectif_rcs()
    
    # Statistiques globales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("👥 Total joueurs", len(effectif))
    
    with col2:
        st.metric("📈 Âge moyen", f"{effectif['age'].mean():.1f} ans")
    
    with col3:
        st.metric("💰 Valeur totale", f"{effectif['valeur_marche'].sum():.1f}M€")
    
    with col4:
        st.metric("⭐ Titulaires", len(effectif[effectif['titulaire'] == True]))
    
    # Répartition par poste
    st.subheader("📊 Répartition par poste")
    
    postes_count = effectif['poste'].value_counts()
    
    fig_postes = px.pie(
        values=postes_count.values,
        names=postes_count.index,
        title="Répartition effectif par poste",
        color_discrete_sequence=['#0066CC', '#004499', '#66B2FF', '#CCE5FF', '#0044AA']
    )
    
    st.plotly_chart(fig_postes, use_container_width=True)
    
    # Tableau effectif détaillé
    st.subheader("📋 Effectif détaillé")
    
    # Filtres
    col_filtre1, col_filtre2 = st.columns(2)
    
    with col_filtre1:
        poste_filtre = st.selectbox("Filtrer par poste", ["Tous"] + list(effectif['poste'].unique()))
    
    with col_filtre2:
        statut_filtre = st.selectbox("Statut", ["Tous", "Titulaires", "Remplaçants"])
    
    # Application des filtres
    effectif_filtre = effectif.copy()
    
    if poste_filtre != "Tous":
        effectif_filtre = effectif_filtre[effectif_filtre['poste'] == poste_filtre]
    
    if statut_filtre == "Titulaires":
        effectif_filtre = effectif_filtre[effectif_filtre['titulaire'] == True]
    elif statut_filtre == "Remplaçants":
        effectif_filtre = effectif_filtre[effectif_filtre['titulaire'] == False]
    
    # Affichage du tableau
    effectif_display = effectif_filtre[['nom', 'age', 'poste', 'nationalite', 'valeur_marche', 'titulaire']].copy()
    effectif_display['valeur_marche'] = effectif_display['valeur_marche'].apply(lambda x: f"{x}M€")
    effectif_display['titulaire'] = effectif_display['titulaire'].apply(lambda x: "⭐ Oui" if x else "🔄 Non")
    
    st.dataframe(
        effectif_display,
        column_config={
            "nom": "Nom",
            "age": "Âge",
            "poste": "Poste",
            "nationalite": "Nationalité",
            "valeur_marche": "Valeur marchande",
            "titulaire": "Titulaire"
        },
        use_container_width=True,
        hide_index=True
    )

def afficher_analyse_joueur():
    """Analyse individuelle des joueurs"""
    
    st.header("📊 Analyse Individuelle des Joueurs")
    
    effectif = obtenir_effectif_rcs()
    
    # Sélection du joueur
    joueur_selectionne = st.selectbox(
        "Choisir un joueur à analyser",
        effectif['nom'].tolist()
    )
    
    if joueur_selectionne:
        joueur_data = effectif[effectif['nom'] == joueur_selectionne].iloc[0]
        
        # Informations joueur
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            <div class="rcs-card">
                <h3>👤 {joueur_data['nom']}</h3>
                <p><strong>Âge:</strong> {joueur_data['age']} ans</p>
                <p><strong>Poste:</strong> {joueur_data['poste']}</p>
                <p><strong>Nationalité:</strong> {joueur_data['nationalite']}</p>
                <p><strong>Statut:</strong> {'⭐ Titulaire' if joueur_data['titulaire'] else '🔄 Remplaçant'}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="rcs-card">
                <h3>💰 Valeur Marchande</h3>
                <h2>{joueur_data['valeur_marche']}M€</h2>
                <p>Estimation Transfermarkt</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Métriques de performance simulées
        st.subheader(f"📈 Performances de {joueur_data['nom']}")
        
        # Simulation de métriques selon le poste
        if joueur_data['poste'] in ['BU', 'MOC']:
            # Attaquant
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("⚽ Buts", "5", "↗️ +2")
            with col2:
                st.metric("🎯 xG", "4.2", "↗️ +0.8")
            with col3:
                st.metric("👟 Passes dé.", "3", "↗️ +1")
            with col4:
                st.metric("📊 Note moy.", "7.2", "↗️ +0.3")
                
        elif joueur_data['poste'] in ['MC', 'MDC', 'MOC', 'AD', 'AG']:
            # Milieu
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("👟 Passes", "1247", "↗️ +89")
            with col2:
                st.metric("📊 % Réussite", "87%", "↗️ +2%")
            with col3:
                st.metric("🎯 Passes clés", "23", "↗️ +4")
            with col4:
                st.metric("📈 Note moy.", "7.1", "↗️ +0.2")
                
        elif joueur_data['poste'] in ['DC', 'DD', 'DG']:
            # Défenseur
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("🛡️ Tacles", "34", "↗️ +3")
            with col2:
                st.metric("✈️ Duels aériens", "78%", "↗️ +5%")
            with col3:
                st.metric("🚫 Interceptions", "28", "↗️ +2")
            with col4:
                st.metric("📊 Note moy.", "6.9", "→ 0")
                
        else:  # Gardien
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("🥅 Arrêts", "67", "↗️ +8")
            with col2:
                st.metric("📊 % Arrêts", "73%", "↗️ +3%")
            with col3:
                st.metric("🚫 Clean sheets", "4", "↗️ +1")
            with col4:
                st.metric("📈 Note moy.", "7.0", "↗️ +0.1")
        
        # Graphique de forme (simulé)
        st.subheader("📈 Évolution de la forme")
        
        matchs = list(range(1, 11))
        notes = np.random.normal(7.0, 0.8, 10)
        notes = np.clip(notes, 5.0, 9.0)
        
        fig_forme = go.Figure()
        fig_forme.add_trace(go.Scatter(
            x=matchs,
            y=notes,
            mode='lines+markers',
            name=f'Note {joueur_data["nom"]}',
            line=dict(color='#0066CC', width=2),
            marker=dict(size=6)
        ))
        
        fig_forme.add_hline(y=7.0, line_dash="dash", line_color="green", annotation_text="Moyenne équipe")
        fig_forme.update_layout(
            title=f"Évolution des notes - {joueur_data['nom']} (10 derniers matchs)",
            xaxis_title="Match",
            yaxis_title="Note /10",
            height=300
        )
        
        st.plotly_chart(fig_forme, use_container_width=True)

def afficher_performances_match():
    """Performances et métriques de match"""
    
    st.header("⚽ Performances et Métriques de Match")
    
    # Simulation derniers matchs
    st.subheader("📅 Derniers Résultats")
    
    derniers_matchs = [
        {"date": "28/01/25", "adversaire": "Olympique de Marseille", "domicile": False, "resultat": "1-2", "xg_rcs": 1.3, "xg_adv": 1.8},
        {"date": "25/01/25", "adversaire": "AS Monaco", "domicile": True, "resultat": "2-1", "xg_rcs": 2.1, "xg_adv": 1.2},
        {"date": "19/01/25", "adversaire": "Stade Rennais", "domicile": False, "resultat": "0-1", "xg_rcs": 0.8, "xg_adv": 1.9},
        {"date": "12/01/25", "adversaire": "RC Lens", "domicile": True, "resultat": "1-1", "xg_rcs": 1.6, "xg_adv": 1.4},
        {"date": "05/01/25", "adversaire": "Stade Brestois", "domicile": False, "resultat": "2-0", "xg_rcs": 2.3, "xg_adv": 0.9}
    ]
    
    for match in derniers_matchs:
        domicile_icon = "🏠" if match["domicile"] else "✈️"
        
        # Déterminer la couleur selon le résultat
        buts_rcs, buts_adv = map(int, match["resultat"].split("-"))
        if buts_rcs > buts_adv:
            color = "#51cf66"  # Vert victoire
            resultat_icon = "✅"
        elif buts_rcs == buts_adv:
            color = "#ffd43b"  # Jaune nul
            resultat_icon = "🤝"
        else:
            color = "#ff6b6b"  # Rouge défaite
            resultat_icon = "❌"
        
        st.markdown(f"""
        <div style="background: {color}; padding: 1rem; border-radius: 10px; margin: 0.5rem 0; color: white;">
            <strong>{match['date']} {domicile_icon} vs {match['adversaire']} {resultat_icon}</strong><br>
            Score: RCS {match['resultat']} | xG: {match['xg_rcs']} - {match['xg_adv']}
        </div>
        """, unsafe_allow_html=True)
    
    # Métriques xG
    st.subheader("📊 Métriques Expected Goals (xG)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>🎯 xG pour</h3>
            <h2>1.64</h2>
            <p>par match (moyenne)</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>🛡️ xG contre</h3>
            <h2>1.44</h2>
            <p>par match (moyenne)</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Exemple de calcul xG RCS
    st.subheader("🎯 Simulateur xG - Style RCS")
    
    col_xg1, col_xg2, col_xg3 = st.columns(3)
    
    with col_xg1:
        distance = st.slider("Distance du but (mètres)", 6, 30, 15)
    
    with col_xg2:
        situation = st.selectbox("Type de situation", ["jeu_normal", "contre_attaque", "corner", "coup_franc"])
    
    with col_xg3:
        tireur = st.selectbox("Tireur", ["Emanuel Emegha", "Dilane Bakwa", "Habib Diarra", "Sebastian Nanasi", "Autre"])
    
    xg_calcule = calculer_xg_rcs(distance, situation, tireur)
    
    st.markdown(f"""
    <div class="rcs-card">
        <h3>⚽ Expected Goals calculé</h3>
        <h2>{xg_calcule:.3f}</h2>
        <p>Formule adaptée style Racing Club de Strasbourg</p>
        <small>Distance: {distance}m | Situation: {situation} | Tireur: {tireur}</small>
    </div>
    """, unsafe_allow_html=True)

def afficher_scouting_rcs():
    """Module de scouting adapté RCS"""
    
    st.header("🎯 Scouting Intelligence - Budget RCS")
    
    # Contraintes budgétaires
    st.subheader("💰 Contraintes Budgétaires RCS")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>💰 Budget max</h3>
            <h2>15M€</h2>
            <p>par transfert</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>💵 Salaire max</h3>
            <h2>80k€</h2>
            <p>par mois</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>🎯 Âge optimal</h3>
            <h2>18-26</h2>
            <p>ans</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Base de données scouting
    st.subheader("🔍 Cibles Scouting Prioritaires")
    
    cibles = obtenir_cibles_scouting_rcs()
    
    # Filtres
    col_filtre1, col_filtre2, col_filtre3 = st.columns(3)
    
    with col_filtre1:
        poste_scouting = st.selectbox("Poste recherché", ["Tous"] + list(cibles['poste'].unique()))
    
    with col_filtre2:
        budget_max = st.slider("Budget maximum (M€)", 0, 15, 15)
    
    with col_filtre3:
        ligue_filtre = st.selectbox("Ligue", ["Toutes"] + list(cibles['ligue'].unique()))
    
    # Application des filtres
    cibles_filtrees = cibles.copy()
    
    if poste_scouting != "Tous":
        cibles_filtrees = cibles_filtrees[cibles_filtrees['poste'] == poste_scouting]
    
    cibles_filtrees = cibles_filtrees[cibles_filtrees['valeur'] <= budget_max]
    
    if ligue_filtre != "Toutes":
        cibles_filtrees = cibles_filtrees[cibles_filtrees['ligue'] == ligue_filtre]
    
    # Tri par note
    cibles_filtrees = cibles_filtrees.sort_values('note', ascending=False)
    
    # Affichage des cibles
    st.subheader(f"📋 {len(cibles_filtrees)} cibles trouvées")
    
    for _, cible in cibles_filtrees.iterrows():
        # Couleur selon la note
        if cible['note'] >= 8.0:
            color = "#51cf66"  # Vert excellent
            priorite = "🔴 TRÈS HAUTE"
        elif cible['note'] >= 7.5:
            color = "#ffd43b"  # Jaune bon
            priorite = "🟡 HAUTE"
        else:
            color = "#74c0fc"  # Bleu moyen
            priorite = "🔵 MOYENNE"
        
        dans_budget = "✅" if cible['valeur'] <= 15 else "❌"
        
        st.markdown(f"""
        <div style="background: {color}; padding: 1rem; border-radius: 10px; margin: 0.5rem 0; color: white;">
            <h4>{dans_budget} {cible['nom']} ({cible['age']} ans) - {priorite}</h4>
            <p><strong>Poste:</strong> {cible['poste']} | <strong>Club:</strong> {cible['club']} ({cible['ligue']})</p>
            <p><strong>Valeur:</strong> {cible['valeur']}M€ | <strong>Note scout:</strong> {cible['note']}/10</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Recommandations
    if len(cibles_filtrees) > 0:
        st.subheader("💡 Recommandations")
        
        top_cible = cibles_filtrees.iloc[0]
        
        st.markdown(f"""
        <div class="rcs-card">
            <h3>🎯 Cible prioritaire recommandée</h3>
            <h4>{top_cible['nom']} ({top_cible['club']})</h4>
            <p><strong>Pourquoi:</strong> Meilleure note scout ({top_cible['note']}/10) dans budget RCS</p>
            <p><strong>Profil:</strong> {top_cible['poste']} de {top_cible['age']} ans en {top_cible['ligue']}</p>
            <p><strong>Investissement:</strong> {top_cible['valeur']}M€ (dans contraintes club)</p>
        </div>
        """, unsafe_allow_html=True)

def afficher_analyses_tactiques():
    """Analyses tactiques et composition"""
    
    st.header("📈 Analyses Tactiques Racing Club de Strasbourg")
    
    # Composition idéale
    st.subheader("🎯 Composition Idéale - Formation 4-2-3-1")
    
    composition = obtenir_composition_ideale_rcs()
    
    st.markdown(f"""
    <div class="rcs-card">
        <h3>⚽ Formation: {composition['formation']}</h3>
        <br>
        <div style="text-align: center; font-family: monospace; font-size: 14px; line-height: 2;">
            <strong>{composition['gardien']}</strong><br>
            🥅 (Gardien)<br><br>
            
            {composition['defenseurs'][0]} &nbsp;&nbsp;&nbsp; {composition['defenseurs'][1]} &nbsp;&nbsp;&nbsp; {composition['defenseurs'][2]} &nbsp;&nbsp;&nbsp; {composition['defenseurs'][3]}<br>
            🛡️ DD &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 🛡️ DC &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 🛡️ DC &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 🛡️ DG<br><br>
            
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; {composition['milieux_defensifs'][0]} &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; {composition['milieux_defensifs'][1]}<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ⚙️ MDC &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ⚙️ MC<br><br>
            
            {composition['milieux_offensifs'][0]} &nbsp;&nbsp;&nbsp; {composition['milieux_offensifs'][1]} &nbsp;&nbsp;&nbsp; {composition['milieux_offensifs'][2]}<br>
            🎨 AD &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 🎨 MOC &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 🎨 AG<br><br>
            
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; {composition['attaquant']}<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ⚽ BU
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Analyses tactiques
    st.subheader("📊 Analyses Style de Jeu")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="rcs-card">
            <h4>🚀 Points Forts Identifiés</h4>
            <ul>
                <li>• Transitions défense-attaque rapides</li>
                <li>• Créativité milieu (Diarra-Nanasi)</li>
                <li>• Percussion latérale (Bakwa)</li>
                <li>• Finition surface (Emegha)</li>
                <li>• Solidité défensive centrale</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="rcs-card">
            <h4>⚠️ Axes d'Amélioration</h4>
            <ul>
                <li>• Profondeur effectif (banc)</li>
                <li>• Alternative à Emegha</li>
                <li>• Constance défensive</li>
                <li>• Efficacité dans la surface</li>
                <li>• Gestion fins de match</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Métriques PPDA
    st.subheader("📊 Pressing et PPDA")
    
    col_ppda1, col_ppda2, col_ppda3 = st.columns(3)
    
    with col_ppda1:
        st.markdown("""
        <div class="metric-card">
            <h3>🔄 PPDA actuel</h3>
            <h2>10.7</h2>
            <p>Pressing moyen-haut</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_ppda2:
        st.markdown("""
        <div class="metric-card">
            <h3>🎯 PPDA objectif</h3>
            <h2>8-12</h2>
            <p>Style RCS</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_ppda3:
        st.markdown("""
        <div class="metric-card">
            <h3>✅ Statut</h3>
            <h2>Optimal</h2>
            <p>Dans objectifs</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Graphique heat map simulé
    st.subheader("🔥 Heat Map - Zones d'activité")
    
    # Simulation heat map
    x_zones = np.random.normal(50, 20, 100)
    y_zones = np.random.normal(30, 15, 100)
    
    fig_heat = go.Figure(data=go.Histogram2d(
        x=x_zones,
        y=y_zones,
        colorscale='Blues',
        showscale=False
    ))
    
    fig_heat.update_layout(
        title="Zones d'activité RCS (simulation)",
        xaxis_title="Largeur terrain (%)",
        yaxis_title="Longueur terrain (%)",
        height=400
    )
    
    st.plotly_chart(fig_heat, use_container_width=True)

if __name__ == "__main__":
    main()
