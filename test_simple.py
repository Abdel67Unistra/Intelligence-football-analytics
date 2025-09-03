import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Configuration de la page
st.set_page_config(
    page_title="Football Analytics - Test",
    page_icon="⚽",
    layout="wide"
)

# Titre principal
st.title("⚽ Football Analytics Platform - Test")
st.markdown("Dashboard de test pour vérifier le fonctionnement de Streamlit")

# Sidebar
st.sidebar.title("🔧 Navigation")
st.sidebar.markdown("Test des fonctionnalités de base")

# Contenu principal
col1, col2 = st.columns(2)

with col1:
    st.header("📊 Données Test")
    
    # Générer des données factices
    players_data = {
        'Joueur': ['Mbappé', 'Haaland', 'Vinicius', 'Pedri', 'Bellingham'],
        'Buts': [25, 35, 18, 8, 12],
        'Passes': [8, 5, 12, 15, 10],
        'Note': [8.5, 9.2, 8.1, 7.8, 8.3]
    }
    
    df = pd.DataFrame(players_data)
    st.dataframe(df)

with col2:
    st.header("📈 Graphique Test")
    
    # Graphique simple
    fig = px.bar(df, x='Joueur', y='Buts', title="Buts par joueur")
    st.plotly_chart(fig, use_container_width=True)

# Métriques
st.header("🎯 Métriques Test")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Buts", df['Buts'].sum())
with col2:
    st.metric("Moyenne Buts", f"{df['Buts'].mean():.1f}")
with col3:
    st.metric("Total Passes", df['Passes'].sum())
with col4:
    st.metric("Note Moyenne", f"{df['Note'].mean():.1f}")

# Test des widgets interactifs
st.header("🎮 Widgets Test")

# Slider
seuil_buts = st.slider("Seuil minimum de buts", 0, 40, 15)

# Filtrer selon le seuil
joueurs_filtrés = df[df['Buts'] >= seuil_buts]
st.write(f"Joueurs avec au moins {seuil_buts} buts:")
st.dataframe(joueurs_filtrés)

# Statut
st.success("✅ Dashboard test fonctionnel!")
st.info("🚀 La plateforme Football Analytics est opérationnelle")

# Footer
st.markdown("---")
st.markdown("**Football Analytics Intelligence Platform** - Test Dashboard")
