#!/usr/bin/env python3
"""
Script de démonstration rapide de la Plateforme Football Analytics
================================================================

Ce script génère des données de démonstration et lance les principales fonctionnalités
sans nécessiter une base de données PostgreSQL complète.
"""

import pandas as pd
import numpy as np
import sys
from pathlib import Path

# Ajouter le répertoire racine au path
sys.path.insert(0, str(Path(__file__).parent))

def generate_demo_data():
    """Génère des données de démonstration réalistes"""
    print("📊 Génération des données de démonstration...")
    
    # Données joueurs
    players_data = {
        'player_id': range(1, 23),
        'name': [
            'Kylian Mbappé', 'Erling Haaland', 'Vinicius Jr', 'Pedri', 'Jude Bellingham',
            'Bukayo Saka', 'Phil Foden', 'Jamal Musiala', 'Luka Modrić', 'Kevin De Bruyne',
            'Robert Lewandowski', 'Harry Kane', 'Victor Osimhen', 'Rafael Leão', 'Khvicha Kvaratskhelia',
            'Gavi', 'Aurelien Tchouameni', 'Enzo Fernández', 'Martin Ødegaard', 'Bruno Fernandes',
            'Virgil van Dijk', 'Ruben Dias'
        ],
        'position': [
            'RW', 'ST', 'LW', 'CM', 'CM', 'RW', 'CAM', 'CAM', 'CM', 'CAM',
            'ST', 'ST', 'ST', 'LW', 'LW', 'CM', 'CDM', 'CM', 'CAM', 'CAM',
            'CB', 'CB'
        ],
        'age': np.random.randint(19, 35, 22),
        'market_value': np.random.uniform(20, 180, 22),  # en millions €
        'goals': np.random.poisson(12, 22),
        'assists': np.random.poisson(8, 22),
        'minutes_played': np.random.randint(1500, 3000, 22),
        'xg': np.random.uniform(0.3, 1.2, 22),
        'xa': np.random.uniform(0.2, 0.9, 22)
    }
    
    players_df = pd.DataFrame(players_data)
    
    # Données de tirs pour xG
    shots_data = {
        'player_id': np.random.choice(range(1, 23), 100),
        'x': np.random.uniform(10, 22, 100),  # Position X sur le terrain
        'y': np.random.uniform(-10, 10, 100),  # Position Y sur le terrain
        'situation': np.random.choice(['open_play', 'corner', 'free_kick', 'penalty'], 100),
        'body_part': np.random.choice(['foot', 'head'], 100),
        'distance': np.random.uniform(5, 35, 100),
        'angle': np.random.uniform(0, 90, 100),
        'goal': np.random.choice([0, 1], 100, p=[0.8, 0.2])
    }
    
    shots_df = pd.DataFrame(shots_data)
    
    print("✅ Données générées avec succès")
    return players_df, shots_df

def demo_football_metrics():
    """Démonstration des métriques football"""
    print("\n⚽ === DÉMONSTRATION MÉTRIQUES FOOTBALL ===")
    
    try:
        from python_analytics.modules.performance_analyzer import FootballMetrics
        
        players_df, shots_df = generate_demo_data()
        metrics = FootballMetrics()
        
        # Calcul xG
        print("📈 Calcul des Expected Goals (xG)...")
        shots_with_xg = metrics.calculate_xg(shots_df)
        avg_xg = shots_with_xg['xg'].mean()
        print(f"   xG moyen par tir: {avg_xg:.3f}")
        print(f"   Total xG: {shots_with_xg['xg'].sum():.1f}")
        print(f"   Buts réels: {shots_df['goal'].sum()}")
        
        # Top tireurs
        top_shooters = shots_with_xg.groupby('player_id').agg({
            'xg': 'sum',
            'goal': 'sum'
        }).sort_values('xg', ascending=False).head(5)
        
        print("\n🎯 Top 5 tireurs (xG):")
        for idx, (player_id, row) in enumerate(top_shooters.iterrows(), 1):
            print(f"   {idx}. Joueur {player_id}: {row['xg']:.2f} xG, {row['goal']} buts")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def demo_player_analysis():
    """Démonstration de l'analyse joueur"""
    print("\n👤 === ANALYSE DE PERFORMANCE JOUEUR ===")
    
    try:
        from python_analytics.modules.performance_analyzer import PlayerPerformanceAnalyzer
        
        players_df, _ = generate_demo_data()
        analyzer = PlayerPerformanceAnalyzer()
        
        # Analyse du top joueur
        top_player = players_df.loc[players_df['market_value'].idxmax()]
        print(f"🌟 Analyse de {top_player['name']} ({top_player['position']}):")
        print(f"   Âge: {top_player['age']} ans")
        print(f"   Valeur marchande: {top_player['market_value']:.1f}M€")
        print(f"   Buts: {top_player['goals']} | Passes: {top_player['assists']}")
        print(f"   Minutes: {top_player['minutes_played']}")
        
        # Calcul de forme
        form_data = pd.DataFrame({
            'match_date': pd.date_range('2024-08-01', periods=10, freq='W'),
            'goals': np.random.poisson(0.5, 10),
            'assists': np.random.poisson(0.3, 10),
            'rating': np.random.uniform(6.0, 9.0, 10)
        })
        
        current_form = analyzer.calculate_player_form(top_player['player_id'], form_data)
        print(f"   Forme actuelle: {current_form:.2f}/10")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def demo_scouting_engine():
    """Démonstration du moteur de scouting"""
    print("\n🔍 === MOTEUR DE SCOUTING IA ===")
    
    try:
        from python_analytics.modules.scouting_engine import ScoutingEngine
        
        players_df, _ = generate_demo_data()
        scout = ScoutingEngine()
        
        # Recherche de joueurs similaires
        target_player_id = 1  # Mbappé
        similar_players = scout.find_similar_players(
            target_player_id, 
            players_df,
            position_filter='RW'
        )
        
        print("🎯 Joueurs similaires à Kylian Mbappé:")
        for i, (player_id, similarity) in enumerate(similar_players.head(3).items(), 1):
            player_name = players_df[players_df['player_id'] == player_id]['name'].iloc[0]
            print(f"   {i}. {player_name} (similarité: {similarity:.3f})")
        
        # Prédiction valeur marchande
        predicted_value = scout.predict_market_value(players_df.iloc[0])
        actual_value = players_df.iloc[0]['market_value']
        print(f"\n💰 Prédiction valeur marchande:")
        print(f"   Valeur réelle: {actual_value:.1f}M€")
        print(f"   Valeur prédite: {predicted_value:.1f}M€")
        print(f"   Écart: {abs(predicted_value - actual_value):.1f}M€")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def main():
    """Fonction principale de démonstration"""
    print("🚀 DÉMONSTRATION PLATEFORME FOOTBALL ANALYTICS")
    print("=" * 60)
    print("Cette démonstration présente les capacités principales de la plateforme")
    print("sans nécessiter de base de données PostgreSQL complète.\n")
    
    demos = [
        demo_football_metrics,
        demo_player_analysis,
        demo_scouting_engine
    ]
    
    success_count = 0
    
    for demo in demos:
        try:
            if demo():
                success_count += 1
            else:
                print("❌ Démonstration échouée")
        except Exception as e:
            print(f"❌ Erreur inattendue: {e}")
        
        print()
    
    print("=" * 60)
    print(f"✅ {success_count}/{len(demos)} démonstrations réussies")
    
    if success_count == len(demos):
        print("\n🎉 La plateforme fonctionne parfaitement!")
        print("\n📋 Prochaines étapes:")
        print("1. Configurez PostgreSQL pour des données complètes")
        print("2. Lancez le dashboard: streamlit run python_analytics/dashboards/coach_interface.py")
        print("3. Explorez les notebooks Jupyter dans /notebooks/")
        print("4. Consultez la documentation complète dans README.md")
    else:
        print("\n⚠️  Certaines fonctionnalités ont des problèmes.")
        print("Vérifiez les dépendances et la configuration.")

if __name__ == "__main__":
    main()
