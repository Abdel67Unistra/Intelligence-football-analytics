#!/usr/bin/env python3
"""
🏆 DÉMONSTRATION SPECTACULAIRE - Football Analytics Platform
============================================================
Présentation complète des capacités de la plateforme en conditions réelles
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sys
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Configuration matplotlib pour de beaux graphiques
plt.style.use('default')
sns.set_palette("husl")

# Ajouter le chemin du projet
sys.path.insert(0, str(Path(__file__).parent))

class FootballDemoShowcase:
    """Classe principale pour la démonstration"""
    
    def __init__(self):
        self.players_data = None
        self.matches_data = None
        self.setup_demo_data()
    
    def setup_demo_data(self):
        """Configuration des données de démonstration réalistes"""
        print("📊 Configuration des données de démonstration...")
        
        # Données joueurs réalistes
        self.players_data = pd.DataFrame({
            'name': [
                'Kylian Mbappé', 'Erling Haaland', 'Vinicius Jr', 'Pedri González',
                'Jude Bellingham', 'Bukayo Saka', 'Phil Foden', 'Jamal Musiala',
                'Gavi', 'Eduardo Camavinga', 'Florian Wirtz', 'Rafael Leão',
                'Victor Osimhen', 'Khvicha Kvaratskhelia', 'Aurélien Tchouaméni',
                'Enzo Fernández', 'Mason Mount', 'Declan Rice', 'Virgil van Dijk', 'Rúben Dias'
            ],
            'age': [26, 24, 24, 22, 21, 23, 24, 21, 20, 22, 21, 25, 25, 23, 24, 23, 25, 25, 32, 27],
            'position': [
                'RW', 'ST', 'LW', 'CM', 'CM', 'RW', 'CAM', 'CAM', 'CM', 'CDM',
                'CAM', 'LW', 'ST', 'LW', 'CDM', 'CM', 'CM', 'CDM', 'CB', 'CB'
            ],
            'club': [
                'Real Madrid', 'Manchester City', 'Real Madrid', 'Barcelona',
                'Real Madrid', 'Arsenal', 'Manchester City', 'Bayern Munich',
                'Barcelona', 'Real Madrid', 'Bayer Leverkusen', 'AC Milan',
                'Napoli', 'Napoli', 'Real Madrid', 'Chelsea', 'Chelsea', 'Arsenal', 'Liverpool', 'Manchester City'
            ],
            'market_value': [180, 170, 120, 90, 120, 80, 90, 85, 60, 70, 75, 75, 100, 85, 80, 75, 55, 105, 40, 80],
            'goals': [28, 35, 21, 4, 14, 16, 12, 10, 2, 3, 8, 15, 26, 12, 1, 5, 7, 3, 2, 1],
            'assists': [8, 6, 15, 12, 8, 9, 8, 6, 8, 4, 12, 8, 4, 9, 3, 6, 5, 4, 2, 1],
            'minutes': [2800, 3100, 2900, 2400, 2700, 2600, 2500, 2200, 2000, 2300, 2100, 2400, 2900, 2200, 2400, 2300, 2000, 2800, 2600, 2900],
            'rating': [8.2, 8.5, 8.0, 7.8, 7.9, 7.7, 7.8, 7.6, 7.4, 7.2, 7.9, 7.8, 8.1, 7.9, 7.3, 7.1, 6.9, 7.5, 8.0, 7.8]
        })
        
        # Calculs de métriques avancées
        self.players_data['goals_per_90'] = (self.players_data['goals'] / self.players_data['minutes']) * 90
        self.players_data['assists_per_90'] = (self.players_data['assists'] / self.players_data['minutes']) * 90
        self.players_data['g+a_per_90'] = self.players_data['goals_per_90'] + self.players_data['assists_per_90']
        
        print(f"✅ {len(self.players_data)} joueurs élite configurés")
    
    def demo_football_metrics(self):
        """Démonstration des métriques football avancées"""
        print("\n⚽ === MÉTRIQUES FOOTBALL AVANCÉES ===")
        print("-" * 50)
        
        try:
            from python_analytics.modules.performance_analyzer import FootballMetrics
            
            metrics = FootballMetrics()
            
            # Simulation de tirs réalistes
            shots_data = pd.DataFrame({
                'x': np.random.uniform(10, 25, 50),
                'y': np.random.uniform(-15, 15, 50),
                'situation': np.random.choice(['open_play', 'corner', 'free_kick', 'counter', 'penalty'], 50),
                'body_part': np.random.choice(['foot', 'head'], 50, p=[0.8, 0.2]),
                'distance': np.random.uniform(5, 35, 50),
                'angle': np.random.uniform(0, 90, 50)
            })
            
            # Calcul xG
            result = metrics.calculate_xg(shots_data)
            
            print(f"📊 Analyse de {len(result)} tirs:")
            print(f"   🎯 Total xG: {result['xg'].sum():.2f}")
            print(f"   📈 xG moyen: {result['xg'].mean():.3f}")
            print(f"   🌟 Meilleure chance: {result['xg'].max():.3f}")
            
            # Analyse par situation
            xg_by_situation = result.groupby('situation')['xg'].agg(['count', 'sum', 'mean'])
            print(f"\n📋 xG par situation:")
            for situation, data in xg_by_situation.iterrows():
                print(f"   {situation:12}: {data['count']:2d} tirs → {data['sum']:.2f} xG (moy: {data['mean']:.3f})")
            
            return True
            
        except Exception as e:
            print(f"❌ Erreur métriques: {e}")
            return False
    
    def demo_performance_analysis(self):
        """Analyse de performance des joueurs"""
        print("\n👥 === ANALYSE DE PERFORMANCE JOUEURS ===")
        print("-" * 50)
        
        try:
            # Top performers par position
            positions = ['ST', 'RW', 'LW', 'CM', 'CAM', 'CDM', 'CB']
            
            for pos in positions:
                pos_players = self.players_data[self.players_data['position'] == pos]
                if len(pos_players) > 0:
                    if pos in ['ST', 'RW', 'LW']:
                        top_player = pos_players.loc[pos_players['g+a_per_90'].idxmax()]
                        print(f"🏆 Meilleur {pos}: {top_player['name']}")
                        print(f"   Stats: {top_player['goals']}G {top_player['assists']}A ({top_player['g+a_per_90']:.2f}/90min)")
                    else:
                        top_player = pos_players.loc[pos_players['rating'].idxmax()]
                        print(f"🏆 Meilleur {pos}: {top_player['name']}")
                        print(f"   Note: {top_player['rating']:.1f} | Valeur: {top_player['market_value']}M€")
            
            # Analyse marché
            print(f"\n💰 ANALYSE MARCHÉ:")
            most_valuable = self.players_data.loc[self.players_data['market_value'].idxmax()]
            best_value = self.players_data.loc[(self.players_data['g+a_per_90'] / self.players_data['market_value']).idxmax()]
            
            print(f"   💎 Plus cher: {most_valuable['name']} ({most_valuable['market_value']}M€)")
            print(f"   🎯 Meilleur rapport qualité/prix: {best_value['name']}")
            print(f"      {best_value['g+a_per_90']:.2f} G+A/90min pour {best_value['market_value']}M€")
            
            return True
            
        except Exception as e:
            print(f"❌ Erreur analyse: {e}")
            return False
    
    def demo_tactical_insights(self):
        """Insights tactiques"""
        print("\n🎯 === INSIGHTS TACTIQUES ===")
        print("-" * 50)
        
        try:
            # Analyse par club
            club_stats = self.players_data.groupby('club').agg({
                'goals': 'sum',
                'assists': 'sum', 
                'market_value': 'sum',
                'rating': 'mean',
                'age': 'mean'
            }).round(2)
            
            # Top 5 clubs
            top_clubs = club_stats.sort_values('market_value', ascending=False).head(5)
            
            print("🏟️  TOP 5 CLUBS (par valeur d'équipe):")
            for club, stats in top_clubs.iterrows():
                print(f"   {club:15}: {stats['market_value']:4.0f}M€ | Note moy: {stats['rating']:.1f}")
                print(f"   {'':17} {stats['goals']:2.0f}G {stats['assists']:2.0f}A | Âge moy: {stats['age']:.1f} ans")
            
            # Style de jeu par âge
            young_players = self.players_data[self.players_data['age'] <= 22]
            experienced = self.players_data[self.players_data['age'] >= 28]
            
            print(f"\n⚡ ANALYSE GÉNÉRATIONNELLE:")
            print(f"   Jeunes talents (≤22 ans): {len(young_players)} joueurs")
            print(f"      Créativité moy: {young_players['assists_per_90'].mean():.3f} assists/90min")
            print(f"   Expérimentés (≥28 ans): {len(experienced)} joueurs") 
            print(f"      Efficacité moy: {experienced['goals_per_90'].mean():.3f} buts/90min")
            
            return True
            
        except Exception as e:
            print(f"❌ Erreur tactique: {e}")
            return False
    
    def demo_scouting_intelligence(self):
        """Intelligence de scouting"""
        print("\n🔍 === INTELLIGENCE DE SCOUTING ===")
        print("-" * 50)
        
        try:
            # Profils de recherche
            search_profiles = {
                'Jeune Crack': {'age_max': 21, 'rating_min': 7.5, 'value_max': 80},
                'Star Confirmée': {'age_max': 26, 'rating_min': 8.0, 'value_max': 200},
                'Opportunité': {'age_max': 30, 'rating_min': 7.0, 'value_max': 50},
                'Potentiel': {'age_max': 23, 'g+a_per_90_min': 0.5, 'value_max': 100}
            }
            
            for profile_name, criteria in search_profiles.items():
                candidates = self.players_data.copy()
                
                # Appliquer les filtres
                if 'age_max' in criteria:
                    candidates = candidates[candidates['age'] <= criteria['age_max']]
                if 'rating_min' in criteria:
                    candidates = candidates[candidates['rating'] >= criteria['rating_min']]
                if 'value_max' in criteria:
                    candidates = candidates[candidates['market_value'] <= criteria['value_max']]
                if 'g+a_per_90_min' in criteria:
                    candidates = candidates[candidates['g+a_per_90'] >= criteria['g+a_per_90_min']]
                
                print(f"🎯 Profil '{profile_name}': {len(candidates)} candidats")
                
                if len(candidates) > 0:
                    # Meilleur candidat
                    if profile_name == 'Jeune Crack':
                        best = candidates.loc[candidates['rating'].idxmax()]
                    elif profile_name == 'Potentiel':
                        best = candidates.loc[candidates['g+a_per_90'].idxmax()]
                    else:
                        best = candidates.loc[(candidates['rating'] * candidates['g+a_per_90']).idxmax()]
                    
                    print(f"   🌟 Recommandation: {best['name']} ({best['club']})")
                    print(f"      {best['age']} ans | {best['market_value']}M€ | Note: {best['rating']:.1f}")
            
            return True
            
        except Exception as e:
            print(f"❌ Erreur scouting: {e}")
            return False
    
    def demo_predictions(self):
        """Démonstration de prédictions"""
        print("\n🔮 === PRÉDICTIONS & TENDANCES ===")
        print("-" * 50)
        
        try:
            # Évolution des valeurs
            young_talents = self.players_data[
                (self.players_data['age'] <= 22) & 
                (self.players_data['rating'] >= 7.5)
            ].copy()
            
            # Simulation évolution sur 3 ans
            young_talents['predicted_value_3y'] = young_talents['market_value'] * (
                1 + (young_talents['rating'] - 7.0) * 0.5 + 
                young_talents['g+a_per_90'] * 10
            )
            
            print("📈 PRÉDICTIONS VALEURS MARCHANDES (3 ans):")
            top_growth = young_talents.nlargest(5, 'predicted_value_3y')[
                ['name', 'age', 'market_value', 'predicted_value_3y']
            ]
            
            for _, player in top_growth.iterrows():
                growth = ((player['predicted_value_3y'] / player['market_value']) - 1) * 100
                print(f"   {player['name']:18}: {player['market_value']:3.0f}M€ → {player['predicted_value_3y']:3.0f}M€ (+{growth:4.0f}%)")
            
            # Prédiction de forme
            print(f"\n⚡ PRÉDICTIONS DE FORME:")
            form_players = self.players_data[self.players_data['minutes'] >= 2000].copy()
            form_players['form_score'] = (
                form_players['rating'] * 0.4 +
                form_players['g+a_per_90'] * 20 * 0.3 +
                (3000 - form_players['minutes']) / 100 * 0.3  # Fraîcheur
            )
            
            top_form = form_players.nlargest(5, 'form_score')[['name', 'club', 'form_score']]
            for _, player in top_form.iterrows():
                print(f"   {player['name']:18}: Score forme {player['form_score']:.1f}")
            
            return True
            
        except Exception as e:
            print(f"❌ Erreur prédictions: {e}")
            return False
    
    def generate_summary_report(self):
        """Génération du rapport de synthèse"""
        print("\n📋 === RAPPORT DE SYNTHÈSE ===")
        print("-" * 50)
        
        total_market_value = self.players_data['market_value'].sum()
        avg_age = self.players_data['age'].mean()
        total_goals = self.players_data['goals'].sum()
        total_assists = self.players_data['assists'].sum()
        
        print(f"📊 STATISTIQUES GLOBALES:")
        print(f"   👥 Joueurs analysés: {len(self.players_data)}")
        print(f"   💰 Valeur totale: {total_market_value:,.0f}M€")
        print(f"   🎂 Âge moyen: {avg_age:.1f} ans")
        print(f"   ⚽ Total buts: {total_goals}")
        print(f"   🎯 Total assists: {total_assists}")
        
        # Top performers globaux
        best_scorer = self.players_data.loc[self.players_data['goals'].idxmax()]
        best_assister = self.players_data.loc[self.players_data['assists'].idxmax()]
        most_valuable = self.players_data.loc[self.players_data['market_value'].idxmax()]
        
        print(f"\n🏆 RECORDS:")
        print(f"   👑 Meilleur buteur: {best_scorer['name']} ({best_scorer['goals']} buts)")
        print(f"   🎨 Meilleur passeur: {best_assister['name']} ({best_assister['assists']} assists)")
        print(f"   💎 Plus gros transfert: {most_valuable['name']} ({most_valuable['market_value']}M€)")
        
        print(f"\n🎯 RECOMMANDATIONS STRATÉGIQUES:")
        print(f"   • Focus sur les jeunes talents (âge ≤ 22) pour ROI long terme")
        print(f"   • Surveiller les joueurs sous-évalués avec bonnes stats/90min")
        print(f"   • Équilibrer expérience (28+) et potentiel (≤23) dans l'effectif")
        print(f"   • Prioriser polyvalence et adaptabilité tactique")

def main():
    """Fonction principale de la démonstration spectaculaire"""
    print("🚀 FOOTBALL ANALYTICS PLATFORM - DÉMONSTRATION SPECTACULAIRE")
    print("=" * 70)
    print("Présentation complète des capacités d'intelligence football moderne")
    print("=" * 70)
    
    demo = FootballDemoShowcase()
    
    demos = [
        ("Métriques Football Avancées", demo.demo_football_metrics),
        ("Analyse de Performance", demo.demo_performance_analysis),
        ("Insights Tactiques", demo.demo_tactical_insights),
        ("Intelligence de Scouting", demo.demo_scouting_intelligence),
        ("Prédictions & Tendances", demo.demo_predictions)
    ]
    
    results = []
    
    for name, demo_func in demos:
        try:
            success = demo_func()
            results.append(success)
        except Exception as e:
            print(f"❌ Erreur dans {name}: {e}")
            results.append(False)
    
    # Rapport final
    demo.generate_summary_report()
    
    # Résultats
    passed = sum(results)
    total = len(results)
    
    print("\n" + "=" * 70)
    print(f"📊 RÉSULTATS: {passed}/{total} démonstrations réussies")
    
    if passed == total:
        print("🎉 DÉMONSTRATION SPECTACULAIRE RÉUSSIE !")
        print("\n🚀 PLATEFORME PRÊTE POUR UTILISATION PROFESSIONNELLE:")
        print("   🌐 Dashboard: http://localhost:8501")
        print("   📓 Jupyter: http://localhost:8888")
        print("   🔗 GitHub: https://github.com/Abdel67Unistra/Intelligence-football-analytics")
        print("\n🏆 Cette plateforme représente l'état de l'art en analytics football !")
        
    print("\n" + "=" * 70)
    print("🎯 DÉMONSTRATION TERMINÉE - FOOTBALL ANALYTICS PLATFORM OPÉRATIONNELLE")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
