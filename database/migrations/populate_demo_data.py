"""
Insertion de Données de Démonstration
====================================

Script pour peupler la base de données avec des données réalistes
de démonstration pour tester la plateforme football analytics.

Author: Football Analytics Platform
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'configs'))

import pandas as pd
import numpy as np
from datetime import datetime, timedelta, date
import uuid
from database import DatabaseManager
import random
from faker import Faker

# Configuration
fake = Faker('fr_FR')  # Données en français
np.random.seed(42)
random.seed(42)

class FootballDataGenerator:
    """Générateur de données football réalistes"""
    
    def __init__(self):
        self.db = DatabaseManager()
        self.leagues = []
        self.teams = []
        self.players = []
        self.positions = []
        
    def generate_leagues(self) -> pd.DataFrame:
        """Génère des données de championnats"""
        leagues_data = [
            {
                'league_id': str(uuid.uuid4()),
                'name': 'Ligue 1',
                'country': 'France',
                'level': 1,
                'season': '2024-2025'
            },
            {
                'league_id': str(uuid.uuid4()),
                'name': 'Premier League',
                'country': 'Angleterre',
                'level': 1,
                'season': '2024-2025'
            },
            {
                'league_id': str(uuid.uuid4()),
                'name': 'La Liga',
                'country': 'Espagne',
                'level': 1,
                'season': '2024-2025'
            }
        ]
        
        self.leagues = pd.DataFrame(leagues_data)
        return self.leagues
    
    def generate_teams(self) -> pd.DataFrame:
        """Génère des données d'équipes"""
        ligue1_teams = [
            {'name': 'Paris Saint-Germain', 'short_name': 'PSG', 'city': 'Paris', 'stadium': 'Parc des Princes', 'capacity': 47929, 'budget': 600},
            {'name': 'Olympique de Marseille', 'short_name': 'OM', 'city': 'Marseille', 'stadium': 'Stade Vélodrome', 'capacity': 67394, 'budget': 150},
            {'name': 'Olympique Lyonnais', 'short_name': 'OL', 'city': 'Lyon', 'stadium': 'Groupama Stadium', 'capacity': 59186, 'budget': 180},
            {'name': 'AS Monaco', 'short_name': 'ASM', 'city': 'Monaco', 'stadium': 'Stade Louis II', 'capacity': 18523, 'budget': 200},
            {'name': 'LOSC Lille', 'short_name': 'LOSC', 'city': 'Lille', 'stadium': 'Stade Pierre-Mauroy', 'capacity': 50186, 'budget': 120},
            {'name': 'Stade Rennais', 'short_name': 'SRFC', 'city': 'Rennes', 'stadium': 'Roazhon Park', 'capacity': 29778, 'budget': 100},
            {'name': 'OGC Nice', 'short_name': 'OGCN', 'city': 'Nice', 'stadium': 'Allianz Riviera', 'capacity': 35624, 'budget': 90},
            {'name': 'RC Strasbourg', 'short_name': 'RCSA', 'city': 'Strasbourg', 'stadium': 'Stade de la Meinau', 'capacity': 26109, 'budget': 70}
        ]
        
        teams_data = []
        ligue1_id = self.leagues[self.leagues['name'] == 'Ligue 1']['league_id'].iloc[0]
        
        for team in ligue1_teams:
            teams_data.append({
                'team_id': str(uuid.uuid4()),
                'name': team['name'],
                'short_name': team['short_name'],
                'league_id': ligue1_id,
                'city': team['city'],
                'stadium_name': team['stadium'],
                'stadium_capacity': team['capacity'],
                'founded_year': random.randint(1900, 1950),
                'budget_millions': team['budget'],
                'color_home': random.choice(['#FF0000', '#0000FF', '#000000', '#FFFFFF']),
                'color_away': random.choice(['#FFFF00', '#00FF00', '#FF00FF'])
            })
        
        self.teams = pd.DataFrame(teams_data)
        return self.teams
    
    def generate_positions(self) -> pd.DataFrame:
        """Génère les positions de football"""
        positions_data = [
            {'position_id': str(uuid.uuid4()), 'code': 'GK', 'name': 'Gardien de but', 'line': 'Goalkeeper', 'zone': 'Center'},
            {'position_id': str(uuid.uuid4()), 'code': 'CB', 'name': 'Défenseur central', 'line': 'Defence', 'zone': 'Center'},
            {'position_id': str(uuid.uuid4()), 'code': 'LB', 'name': 'Arrière gauche', 'line': 'Defence', 'zone': 'Left'},
            {'position_id': str(uuid.uuid4()), 'code': 'RB', 'name': 'Arrière droit', 'line': 'Defence', 'zone': 'Right'},
            {'position_id': str(uuid.uuid4()), 'code': 'DM', 'name': 'Milieu défensif', 'line': 'Midfield', 'zone': 'Center'},
            {'position_id': str(uuid.uuid4()), 'code': 'CM', 'name': 'Milieu central', 'line': 'Midfield', 'zone': 'Center'},
            {'position_id': str(uuid.uuid4()), 'code': 'AM', 'name': 'Milieu offensif', 'line': 'Midfield', 'zone': 'Center'},
            {'position_id': str(uuid.uuid4()), 'code': 'LW', 'name': 'Ailier gauche', 'line': 'Attack', 'zone': 'Left'},
            {'position_id': str(uuid.uuid4()), 'code': 'RW', 'name': 'Ailier droit', 'line': 'Attack', 'zone': 'Right'},
            {'position_id': str(uuid.uuid4()), 'code': 'ST', 'name': 'Attaquant', 'line': 'Attack', 'zone': 'Center'}
        ]
        
        self.positions = pd.DataFrame(positions_data)
        return self.positions
    
    def generate_players(self, n_players_per_team: int = 25) -> pd.DataFrame:
        """Génère des joueurs réalistes"""
        players_data = []
        
        # Noms de joueurs français réalistes
        french_first_names = [
            'Kylian', 'Antoine', 'Paul', 'N\'Golo', 'Olivier', 'Hugo', 'Raphaël',
            'Kingsley', 'Ousmane', 'Wissam', 'Florian', 'Alexandre', 'Thomas',
            'Karim', 'Adrien', 'Moussa', 'Presnel', 'Lucas', 'Benjamin', 'Jordan'
        ]
        
        french_last_names = [
            'Mbappé', 'Griezmann', 'Pogba', 'Kanté', 'Giroud', 'Lloris', 'Varane',
            'Coman', 'Dembélé', 'Ben Yedder', 'Thauvin', 'Lacazette', 'Lemar',
            'Benzema', 'Rabiot', 'Sissoko', 'Kimpembe', 'Hernandez', 'Mendy', 'Veretout'
        ]
        
        for team in self.teams.itertuples():
            for i in range(n_players_per_team):
                # Répartition réaliste des positions
                position_weights = {
                    'GK': 0.08,  # 2 gardiens
                    'CB': 0.16,  # 4 défenseurs centraux
                    'LB': 0.08,  # 2 arrières gauches
                    'RB': 0.08,  # 2 arrières droits
                    'DM': 0.12,  # 3 milieux défensifs
                    'CM': 0.16,  # 4 milieux centraux
                    'AM': 0.08,  # 2 milieux offensifs
                    'LW': 0.08,  # 2 ailiers gauches
                    'RW': 0.08,  # 2 ailiers droits
                    'ST': 0.08   # 2 attaquants
                }
                
                position_code = np.random.choice(
                    list(position_weights.keys()),
                    p=list(position_weights.values())
                )
                
                # Générer des caractéristiques réalistes selon la position
                if position_code == 'GK':
                    height = np.random.normal(188, 5)
                    weight = np.random.normal(82, 6)
                elif position_code in ['CB']:
                    height = np.random.normal(185, 4)
                    weight = np.random.normal(80, 5)
                elif position_code in ['LB', 'RB', 'LW', 'RW']:
                    height = np.random.normal(175, 4)
                    weight = np.random.normal(72, 4)
                else:  # Milieux et attaquants
                    height = np.random.normal(178, 5)
                    weight = np.random.normal(75, 5)
                
                # Âge avec distribution réaliste
                age = int(np.clip(np.random.normal(26, 4), 18, 38))
                birth_date = date.today() - timedelta(days=age*365 + random.randint(0, 365))
                
                # Valeur marchande selon l'âge et la position
                base_value = np.random.exponential(15)  # Moyenne 15M€
                
                # Facteur d'âge (pic vers 26-28 ans)
                age_factor = 1 - abs(age - 27) * 0.03
                age_factor = max(0.3, age_factor)
                
                # Bonus selon la position
                position_multiplier = {
                    'ST': 1.5, 'AM': 1.3, 'LW': 1.4, 'RW': 1.4,
                    'CM': 1.2, 'DM': 1.0, 'CB': 1.1, 'LB': 1.0, 'RB': 1.0, 'GK': 0.8
                }.get(position_code, 1.0)
                
                market_value = base_value * age_factor * position_multiplier
                market_value = max(0.5, min(200, market_value))  # Entre 0.5M et 200M€
                
                players_data.append({
                    'player_id': str(uuid.uuid4()),
                    'first_name': random.choice(french_first_names),
                    'last_name': random.choice(french_last_names),
                    'birth_date': birth_date,
                    'nationality': random.choice(['France', 'Senegal', 'Algeria', 'Morocco', 'Ivory Coast']),
                    'height_cm': int(np.clip(height, 160, 210)),
                    'weight_kg': int(np.clip(weight, 60, 100)),
                    'foot': random.choice(['Right', 'Left', 'Both']),
                    'market_value_millions': round(market_value, 1),
                    'salary_annual_millions': round(market_value * 0.2, 2),
                    'contract_end_date': date(random.randint(2025, 2028), random.randint(1, 12), random.randint(1, 28)),
                    'jersey_number': random.randint(1, 99),
                    'team_id': team.team_id,
                    'position_code': position_code
                })
        
        self.players = pd.DataFrame(players_data)
        return self.players
    
    def generate_matches(self, n_matchdays: int = 15) -> pd.DataFrame:
        """Génère des matchs de championnat"""
        matches_data = []
        
        # Calendrier de Ligue 1
        start_date = datetime(2024, 8, 15)
        
        teams_list = self.teams['team_id'].tolist()
        n_teams = len(teams_list)
        
        for matchday in range(1, n_matchdays + 1):
            match_date = start_date + timedelta(weeks=matchday-1)
            
            # Créer des matchs pour cette journée
            teams_copy = teams_list.copy()
            random.shuffle(teams_copy)
            
            for i in range(0, n_teams - 1, 2):
                if i + 1 < len(teams_copy):
                    home_team = teams_copy[i]
                    away_team = teams_copy[i + 1]
                    
                    # Simuler le score
                    home_goals = np.random.poisson(1.4)
                    away_goals = np.random.poisson(1.1)
                    
                    matches_data.append({
                        'match_id': str(uuid.uuid4()),
                        'league_id': self.leagues[self.leagues['name'] == 'Ligue 1']['league_id'].iloc[0],
                        'home_team_id': home_team,
                        'away_team_id': away_team,
                        'match_date': match_date,
                        'matchday': matchday,
                        'home_score': home_goals,
                        'away_score': away_goals,
                        'home_score_halftime': max(0, home_goals - np.random.poisson(0.3)),
                        'away_score_halftime': max(0, away_goals - np.random.poisson(0.3)),
                        'attendance': random.randint(20000, 60000),
                        'referee': fake.name(),
                        'weather': random.choice(['Sunny', 'Cloudy', 'Rainy']),
                        'temperature': random.randint(5, 25),
                        'status': 'Finished'
                    })
        
        return pd.DataFrame(matches_data)
    
    def insert_all_data(self):
        """Insère toutes les données dans la base de données"""
        if not self.db.connect():
            print("❌ Impossible de se connecter à la base de données")
            return False
        
        try:
            print("🏆 Génération des championnats...")
            leagues_df = self.generate_leagues()
            self.db.to_sql(leagues_df, 'leagues', if_exists='replace')
            
            print("⚽ Génération des équipes...")
            teams_df = self.generate_teams()
            self.db.to_sql(teams_df, 'teams', if_exists='replace')
            
            print("🎯 Génération des positions...")
            positions_df = self.generate_positions()
            self.db.to_sql(positions_df, 'positions', if_exists='replace')
            
            print("👥 Génération des joueurs...")
            players_df = self.generate_players()
            self.db.to_sql(players_df, 'players', if_exists='replace')
            
            print("📅 Génération des matchs...")
            matches_df = self.generate_matches()
            self.db.to_sql(matches_df, 'matches', if_exists='replace')
            
            print("✅ Toutes les données ont été insérées avec succès!")
            
            # Afficher un résumé
            print("\n📊 RÉSUMÉ DES DONNÉES GÉNÉRÉES:")
            print(f"  • Championnats: {len(leagues_df)}")
            print(f"  • Équipes: {len(teams_df)}")
            print(f"  • Positions: {len(positions_df)}")
            print(f"  • Joueurs: {len(players_df)}")
            print(f"  • Matchs: {len(matches_df)}")
            
            return True
            
        except Exception as e:
            print(f"❌ Erreur lors de l'insertion des données: {e}")
            return False
        finally:
            self.db.disconnect()

if __name__ == "__main__":
    print("🚀 GÉNÉRATION DES DONNÉES DE DÉMONSTRATION")
    print("=" * 50)
    
    generator = FootballDataGenerator()
    
    if generator.insert_all_data():
        print("\n🎉 Base de données football prête à l'utilisation!")
    else:
        print("\n💥 Échec de la génération des données")
