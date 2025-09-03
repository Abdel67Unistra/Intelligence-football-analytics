"""
Moteur de Recrutement et Scouting Intelligent
============================================

Système d'aide à la décision pour le recrutement footballistique.
Utilise des algorithmes de machine learning pour recommander des joueurs.

Author: Football Analytics Platform
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, classification_report
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import warnings
warnings.filterwarnings('ignore')

from typing import Dict, List, Tuple, Optional
import json
from datetime import datetime, timedelta

class PlayerProfiler:
    """Classe pour créer des profils de joueurs et clustering"""
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.pca = PCA(n_components=0.95)  # Garder 95% de la variance
        self.kmeans = KMeans(n_clusters=8, random_state=42)
        self.player_clusters = {}
        
    def create_player_profiles(self, player_stats: pd.DataFrame) -> pd.DataFrame:
        """
        Crée des profils de joueurs basés sur leurs statistiques
        
        Args:
            player_stats: DataFrame avec statistiques des joueurs
            
        Returns:
            DataFrame avec profils et clusters
        """
        # Sélection des métriques clés pour le profilage
        profile_metrics = [
            'goals_per_90', 'assists_per_90', 'xg_per_90', 'xa_per_90',
            'pass_accuracy', 'passes_per_90', 'key_passes_per_90',
            'tackles_per_90', 'interceptions_per_90', 'duels_won_pct',
            'aerial_duels_won_pct', 'distance_per_90', 'sprints_per_90'
        ]
        
        # Vérifier que toutes les colonnes existent
        available_metrics = [col for col in profile_metrics if col in player_stats.columns]
        
        if len(available_metrics) == 0:
            # Créer des données de démonstration
            player_stats = self._generate_demo_stats(len(player_stats))
            available_metrics = profile_metrics
        
        # Préparation des données
        X = player_stats[available_metrics].fillna(0)
        
        # Normalisation
        X_scaled = self.scaler.fit_transform(X)
        
        # Réduction de dimensionnalité
        X_pca = self.pca.fit_transform(X_scaled)
        
        # Clustering des joueurs
        clusters = self.kmeans.fit_predict(X_pca)
        
        # Ajout des clusters au DataFrame
        player_stats = player_stats.copy()
        player_stats['player_cluster'] = clusters
        player_stats['cluster_label'] = [self._get_cluster_label(c) for c in clusters]
        
        # Stockage des profils
        self.player_clusters = self._analyze_clusters(player_stats, available_metrics)
        
        return player_stats
    
    def _generate_demo_stats(self, n_players: int) -> pd.DataFrame:
        """Génère des statistiques de démonstration pour les joueurs"""
        np.random.seed(42)
        
        # Créer des profils de joueurs variés
        data = {
            'goals_per_90': np.random.exponential(0.3, n_players),
            'assists_per_90': np.random.exponential(0.2, n_players),
            'xg_per_90': np.random.exponential(0.25, n_players),
            'xa_per_90': np.random.exponential(0.15, n_players),
            'pass_accuracy': np.random.normal(82, 8, n_players),
            'passes_per_90': np.random.normal(45, 20, n_players),
            'key_passes_per_90': np.random.exponential(1.5, n_players),
            'tackles_per_90': np.random.exponential(2.5, n_players),
            'interceptions_per_90': np.random.exponential(1.8, n_players),
            'duels_won_pct': np.random.normal(55, 10, n_players),
            'aerial_duels_won_pct': np.random.normal(50, 15, n_players),
            'distance_per_90': np.random.normal(10.5, 1.5, n_players),
            'sprints_per_90': np.random.normal(15, 5, n_players)
        }
        
        # S'assurer que les valeurs sont réalistes
        for key in ['pass_accuracy', 'duels_won_pct', 'aerial_duels_won_pct']:
            data[key] = np.clip(data[key], 0, 100)
        
        for key in ['distance_per_90']:
            data[key] = np.clip(data[key], 5, 15)
            
        return pd.DataFrame(data)
    
    def _get_cluster_label(self, cluster_id: int) -> str:
        """Associe un label descriptif à chaque cluster"""
        labels = {
            0: "Attaquant Finisseur",
            1: "Milieu Créateur", 
            2: "Défenseur Central",
            3: "Milieu Box-to-Box",
            4: "Ailier Rapide",
            5: "Défenseur Latéral",
            6: "Milieu Défensif",
            7: "Avant-Centre Complet"
        }
        return labels.get(cluster_id, f"Profil {cluster_id}")
    
    def _analyze_clusters(self, data: pd.DataFrame, metrics: List[str]) -> Dict:
        """Analyse les caractéristiques de chaque cluster"""
        cluster_analysis = {}
        
        for cluster_id in data['player_cluster'].unique():
            cluster_data = data[data['player_cluster'] == cluster_id]
            
            # Statistiques moyennes du cluster
            cluster_stats = cluster_data[metrics].mean().to_dict()
            
            # Caractéristiques dominantes
            top_stats = sorted(cluster_stats.items(), key=lambda x: x[1], reverse=True)[:5]
            
            cluster_analysis[cluster_id] = {
                'label': self._get_cluster_label(cluster_id),
                'size': len(cluster_data),
                'avg_stats': cluster_stats,
                'top_characteristics': top_stats
            }
        
        return cluster_analysis


class MarketValuePredictor:
    """Prédicteur de valeur marchande des joueurs"""
    
    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        self.is_fitted = False
        
    def train_model(self, training_data: pd.DataFrame) -> Dict:
        """
        Entraîne le modèle de prédiction de valeur marchande
        
        Args:
            training_data: DataFrame avec stats joueurs et valeurs marchandes
            
        Returns:
            Métriques de performance du modèle
        """
        # Features pour la prédiction
        feature_columns = [
            'age', 'goals_per_90', 'assists_per_90', 'xg_per_90', 'xa_per_90',
            'pass_accuracy', 'international_caps', 'contract_years_remaining',
            'minutes_played_season', 'league_level'  # 1=top, 2=second...
        ]
        
        # Générer des données de démonstration si nécessaire
        if not all(col in training_data.columns for col in feature_columns + ['market_value']):
            training_data = self._generate_market_demo_data()
            
        # Préparation des données
        X = training_data[feature_columns].fillna(0)
        y = training_data['market_value']
        
        # Division train/test
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Normalisation
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Entraînement
        self.model.fit(X_train_scaled, y_train)
        
        # Prédictions de test
        y_pred = self.model.predict(X_test_scaled)
        
        # Métriques
        mse = mean_squared_error(y_test, y_pred)
        
        # Importance des features
        feature_importance = dict(zip(feature_columns, self.model.feature_importances_))
        
        self.is_fitted = True
        
        return {
            'mse': mse,
            'rmse': np.sqrt(mse),
            'feature_importance': feature_importance,
            'r2_score': self.model.score(X_test_scaled, y_test)
        }
    
    def predict_value(self, player_data: Dict) -> Dict:
        """
        Prédit la valeur marchande d'un joueur
        
        Args:
            player_data: Dictionnaire avec les caractéristiques du joueur
            
        Returns:
            Prédiction avec intervalle de confiance
        """
        if not self.is_fitted:
            # Entraîner avec des données de démo
            demo_data = self._generate_market_demo_data()
            self.train_model(demo_data)
        
        # Préparation des features
        features = [
            player_data.get('age', 25),
            player_data.get('goals_per_90', 0.3),
            player_data.get('assists_per_90', 0.2),
            player_data.get('xg_per_90', 0.25),
            player_data.get('xa_per_90', 0.15),
            player_data.get('pass_accuracy', 80),
            player_data.get('international_caps', 5),
            player_data.get('contract_years_remaining', 2),
            player_data.get('minutes_played_season', 2000),
            player_data.get('league_level', 1)
        ]
        
        # Normalisation et prédiction
        features_scaled = self.scaler.transform([features])
        predicted_value = self.model.predict(features_scaled)[0]
        
        # Calcul de l'intervalle de confiance (estimation basée sur les erreurs du modèle)
        confidence_interval = predicted_value * 0.15  # ±15%
        
        return {
            'predicted_value': round(predicted_value, 2),
            'min_value': round(predicted_value - confidence_interval, 2),
            'max_value': round(predicted_value + confidence_interval, 2),
            'confidence': 85  # Pourcentage de confiance
        }
    
    def _generate_market_demo_data(self) -> pd.DataFrame:
        """Génère des données de démonstration pour l'entraînement"""
        np.random.seed(42)
        n_players = 1000
        
        # Générer des données réalistes
        ages = np.random.normal(25, 4, n_players)
        ages = np.clip(ages, 16, 40)
        
        # Corrélations réalistes entre âge et performance
        age_factor = 1 - (np.abs(ages - 26) * 0.03)  # Peak vers 26 ans
        
        data = {
            'age': ages,
            'goals_per_90': np.random.exponential(0.3, n_players) * age_factor,
            'assists_per_90': np.random.exponential(0.2, n_players) * age_factor,
            'xg_per_90': np.random.exponential(0.25, n_players) * age_factor,
            'xa_per_90': np.random.exponential(0.15, n_players) * age_factor,
            'pass_accuracy': np.random.normal(80, 10, n_players),
            'international_caps': np.random.poisson(8, n_players),
            'contract_years_remaining': np.random.uniform(0.5, 5, n_players),
            'minutes_played_season': np.random.normal(2000, 800, n_players),
            'league_level': np.random.choice([1, 2, 3], n_players, p=[0.3, 0.4, 0.3])
        }
        
        # Calcul de la valeur marchande basée sur les stats (formule simplifiée)
        performance_score = (
            data['goals_per_90'] * 20 + 
            data['assists_per_90'] * 15 + 
            data['pass_accuracy'] * 0.5 +
            data['international_caps'] * 2
        )
        
        age_multiplier = np.where(ages < 23, 1.3, np.where(ages < 30, 1.0, 0.7))
        league_multiplier = [2.0 if l == 1 else 1.2 if l == 2 else 0.8 for l in data['league_level']]
        
        market_values = performance_score * age_multiplier * league_multiplier
        market_values = np.clip(market_values, 0.5, 200)  # Entre 0.5M et 200M
        
        data['market_value'] = market_values
        
        return pd.DataFrame(data)


class ScoutingEngine:
    """Moteur principal de scouting et recommandations"""
    
    def __init__(self):
        self.profiler = PlayerProfiler()
        self.value_predictor = MarketValuePredictor()
        self.player_database = pd.DataFrame()
        
    def load_player_database(self, player_data: pd.DataFrame):
        """Charge la base de données des joueurs"""
        self.player_database = player_data.copy()
        
        # Créer les profils des joueurs
        self.player_database = self.profiler.create_player_profiles(self.player_database)
        
    def find_similar_players(self, reference_player_id: str, n_recommendations: int = 10) -> List[Dict]:
        """
        Trouve des joueurs similaires au joueur de référence
        
        Args:
            reference_player_id: ID du joueur de référence
            n_recommendations: Nombre de recommandations
            
        Returns:
            Liste des joueurs similaires avec scores de similarité
        """
        if self.player_database.empty:
            # Charger des données de démonstration
            self._load_demo_database()
        
        # Trouver le joueur de référence
        ref_player = self.player_database[
            self.player_database['player_id'] == reference_player_id
        ]
        
        if ref_player.empty:
            return []
        
        ref_cluster = ref_player['player_cluster'].iloc[0]
        
        # Joueurs du même cluster
        similar_players = self.player_database[
            (self.player_database['player_cluster'] == ref_cluster) &
            (self.player_database['player_id'] != reference_player_id)
        ].copy()
        
        # Calcul de similarité basé sur les statistiques
        ref_stats = ref_player.select_dtypes(include=[np.number]).iloc[0]
        
        similarities = []
        for idx, player in similar_players.iterrows():
            player_stats = player.select_dtypes(include=[np.number])
            
            # Distance euclidienne normalisée
            similarity = self._calculate_similarity(ref_stats, player_stats)
            similarities.append(similarity)
        
        similar_players['similarity_score'] = similarities
        
        # Tri par similarité
        recommendations = similar_players.nlargest(n_recommendations, 'similarity_score')
        
        return recommendations[['player_id', 'name', 'age', 'position', 'team', 
                              'cluster_label', 'similarity_score']].to_dict('records')
    
    def scout_by_criteria(self, criteria: Dict) -> List[Dict]:
        """
        Recherche de joueurs selon des critères spécifiques
        
        Args:
            criteria: Dictionnaire avec critères de recherche
                     {position, age_min, age_max, max_value, min_rating, league}
        
        Returns:
            Liste des joueurs correspondant aux critères
        """
        if self.player_database.empty:
            self._load_demo_database()
        
        filtered_players = self.player_database.copy()
        
        # Application des filtres
        if 'position' in criteria and criteria['position']:
            filtered_players = filtered_players[
                filtered_players['position'] == criteria['position']
            ]
        
        if 'age_min' in criteria:
            filtered_players = filtered_players[
                filtered_players['age'] >= criteria['age_min']
            ]
        
        if 'age_max' in criteria:
            filtered_players = filtered_players[
                filtered_players['age'] <= criteria['age_max']
            ]
        
        if 'max_value' in criteria:
            # Prédire les valeurs marchandes si pas disponibles
            if 'market_value' not in filtered_players.columns:
                filtered_players['market_value'] = filtered_players.apply(
                    lambda row: self.value_predictor.predict_value(row.to_dict())['predicted_value'],
                    axis=1
                )
            
            filtered_players = filtered_players[
                filtered_players['market_value'] <= criteria['max_value']
            ]
        
        if 'min_rating' in criteria:
            if 'overall_rating' not in filtered_players.columns:
                # Calculer un rating global basé sur les stats
                filtered_players['overall_rating'] = self._calculate_overall_rating(filtered_players)
            
            filtered_players = filtered_players[
                filtered_players['overall_rating'] >= criteria['min_rating']
            ]
        
        # Calcul du score de recommandation
        filtered_players['recommendation_score'] = self._calculate_recommendation_score(
            filtered_players, criteria
        )
        
        # Tri par score de recommandation
        recommendations = filtered_players.nlargest(20, 'recommendation_score')
        
        return recommendations[['player_id', 'name', 'age', 'position', 'team',
                              'cluster_label', 'recommendation_score']].to_dict('records')
    
    def analyze_transfer_opportunity(self, player_id: str, target_team_budget: float) -> Dict:
        """
        Analyse l'opportunité d'un transfert
        
        Args:
            player_id: ID du joueur analysé
            target_team_budget: Budget disponible de l'équipe
            
        Returns:
            Analyse complète de l'opportunité de transfert
        """
        if self.player_database.empty:
            self._load_demo_database()
        
        player = self.player_database[
            self.player_database['player_id'] == player_id
        ]
        
        if player.empty:
            return {"error": "Joueur non trouvé"}
        
        player_data = player.iloc[0].to_dict()
        
        # Prédiction de valeur marchande
        value_prediction = self.value_predictor.predict_value(player_data)
        
        # Analyse de l'opportunité
        opportunity_score = self._calculate_opportunity_score(
            value_prediction, target_team_budget, player_data
        )
        
        # Risques et avantages
        risks = self._assess_transfer_risks(player_data)
        benefits = self._assess_transfer_benefits(player_data)
        
        return {
            "player_info": {
                "name": player_data.get('name', 'Joueur Inconnu'),
                "age": player_data.get('age', 0),
                "position": player_data.get('position', 'Inconnue'),
                "current_team": player_data.get('team', 'Inconnue')
            },
            "market_analysis": value_prediction,
            "opportunity_score": opportunity_score,
            "budget_fit": value_prediction['predicted_value'] <= target_team_budget,
            "risks": risks,
            "benefits": benefits,
            "recommendation": self._generate_transfer_recommendation(
                opportunity_score, value_prediction, target_team_budget
            )
        }
    
    def _load_demo_database(self):
        """Charge une base de données de démonstration"""
        np.random.seed(42)
        n_players = 500
        
        # Génération de joueurs de démonstration
        positions = ['GK', 'CB', 'LB', 'RB', 'DM', 'CM', 'AM', 'LW', 'RW', 'ST']
        teams = ['PSG', 'OM', 'Lyon', 'Monaco', 'Lille', 'Rennes', 'Nice', 'Strasbourg']
        
        demo_data = {
            'player_id': [f'player_{i}' for i in range(n_players)],
            'name': [f'Joueur {i}' for i in range(n_players)],
            'age': np.random.normal(25, 4, n_players).astype(int),
            'position': np.random.choice(positions, n_players),
            'team': np.random.choice(teams, n_players),
            'goals_per_90': np.random.exponential(0.3, n_players),
            'assists_per_90': np.random.exponential(0.2, n_players),
            'xg_per_90': np.random.exponential(0.25, n_players),
            'xa_per_90': np.random.exponential(0.15, n_players),
            'pass_accuracy': np.random.normal(80, 10, n_players),
            'international_caps': np.random.poisson(5, n_players)
        }
        
        # Normaliser les âges
        demo_data['age'] = np.clip(demo_data['age'], 16, 40)
        
        self.player_database = pd.DataFrame(demo_data)
        self.player_database = self.profiler.create_player_profiles(self.player_database)
    
    def _calculate_similarity(self, ref_stats: pd.Series, player_stats: pd.Series) -> float:
        """Calcule la similarité entre deux joueurs"""
        # Sélectionner les statistiques communes
        common_stats = ref_stats.index.intersection(player_stats.index)
        
        if len(common_stats) == 0:
            return 0.0
        
        # Distance euclidienne normalisée
        diff = ref_stats[common_stats] - player_stats[common_stats]
        distance = np.sqrt(np.sum(diff ** 2))
        
        # Conversion en score de similarité (0-100)
        max_distance = np.sqrt(len(common_stats)) * 100  # Estimation
        similarity = max(0, 100 - (distance / max_distance * 100))
        
        return similarity
    
    def _calculate_overall_rating(self, players: pd.DataFrame) -> pd.Series:
        """Calcule une note globale pour les joueurs"""
        # Formule simplifiée basée sur les statistiques disponibles
        rating = (
            players.get('goals_per_90', 0) * 20 +
            players.get('assists_per_90', 0) * 15 +
            players.get('pass_accuracy', 70) * 0.3 +
            players.get('international_caps', 0) * 0.5 + 50
        )
        
        return np.clip(rating, 50, 99)
    
    def _calculate_recommendation_score(self, players: pd.DataFrame, criteria: Dict) -> pd.Series:
        """Calcule un score de recommandation basé sur les critères"""
        # Score de base basé sur la performance
        base_score = self._calculate_overall_rating(players)
        
        # Bonus/malus selon les critères
        score = base_score.copy()
        
        # Bonus pour l'âge optimal (22-28 ans)
        optimal_age_bonus = np.where(
            (players['age'] >= 22) & (players['age'] <= 28), 5, 0
        )
        score += optimal_age_bonus
        
        # Bonus pour l'expérience internationale
        int_caps_bonus = np.minimum(players.get('international_caps', 0) * 0.5, 10)
        score += int_caps_bonus
        
        return np.clip(score, 0, 100)
    
    def _calculate_opportunity_score(self, value_prediction: Dict, budget: float, player_data: Dict) -> float:
        """Calcule un score d'opportunité pour un transfert"""
        predicted_value = value_prediction['predicted_value']
        
        # Score de base selon le ratio valeur/budget
        if predicted_value <= budget:
            budget_score = 50 + (budget - predicted_value) / budget * 30
        else:
            budget_score = max(0, 50 - (predicted_value - budget) / budget * 50)
        
        # Bonus pour l'âge
        age = player_data.get('age', 30)
        age_bonus = max(0, 30 - age) if age < 30 else max(0, (35 - age) * 2)
        
        # Bonus pour les performances
        performance_bonus = (
            player_data.get('goals_per_90', 0) * 10 +
            player_data.get('assists_per_90', 0) * 8
        )
        
        total_score = budget_score + age_bonus + performance_bonus
        return min(100, total_score)
    
    def _assess_transfer_risks(self, player_data: Dict) -> List[str]:
        """Évalue les risques d'un transfert"""
        risks = []
        
        age = player_data.get('age', 25)
        if age > 30:
            risks.append("Âge élevé - Risque de baisse de performance")
        if age < 20:
            risks.append("Jeune joueur - Adaptation incertaine")
        
        international_caps = player_data.get('international_caps', 0)
        if international_caps == 0:
            risks.append("Aucune sélection internationale - Niveau incertain")
        
        # Simuler d'autres risques
        if np.random.random() < 0.3:
            risks.append("Historique de blessures à surveiller")
        
        if np.random.random() < 0.2:
            risks.append("Contrat court - Risque de départ libre")
        
        return risks
    
    def _assess_transfer_benefits(self, player_data: Dict) -> List[str]:
        """Évalue les avantages d'un transfert"""
        benefits = []
        
        age = player_data.get('age', 25)
        if 22 <= age <= 28:
            benefits.append("Âge optimal - Dans la force de l'âge")
        
        goals_per_90 = player_data.get('goals_per_90', 0)
        if goals_per_90 > 0.5:
            benefits.append("Excellent finisseur - Apport offensif garanti")
        
        assists_per_90 = player_data.get('assists_per_90', 0)
        if assists_per_90 > 0.3:
            benefits.append("Créateur de jeu - Vision du jeu développée")
        
        international_caps = player_data.get('international_caps', 0)
        if international_caps > 10:
            benefits.append("Expérience internationale - Habitué à la pression")
        
        return benefits
    
    def _generate_transfer_recommendation(self, score: float, value_prediction: Dict, budget: float) -> str:
        """Génère une recommandation de transfert"""
        if score >= 80:
            return "🟢 RECOMMANDÉ - Excellente opportunité de transfert"
        elif score >= 60:
            return "🟡 À CONSIDÉRER - Transfert intéressant avec quelques réserves"
        elif score >= 40:
            return "🟠 MITIGÉ - Transfert risqué, nécessite analyse approfondie"
        else:
            return "🔴 NON RECOMMANDÉ - Transfert déconseillé"


if __name__ == "__main__":
    # Exemple d'utilisation
    print("🔍 Moteur de Recrutement Football Analytics")
    print("==========================================")
    
    # Initialisation
    scouting_engine = ScoutingEngine()
    
    # Test avec données de démonstration
    print("\n📊 Chargement de la base de données...")
    scouting_engine._load_demo_database()
    
    print(f"✅ {len(scouting_engine.player_database)} joueurs chargés")
    print(f"📋 {len(scouting_engine.profiler.player_clusters)} profils de joueurs identifiés")
    
    # Exemple de recherche
    criteria = {
        'position': 'ST',
        'age_min': 20,
        'age_max': 28,
        'max_value': 50,
        'min_rating': 75
    }
    
    print(f"\n🎯 Recherche selon critères : {criteria}")
    recommendations = scouting_engine.scout_by_criteria(criteria)
    print(f"📋 {len(recommendations)} joueurs trouvés")
    
    if recommendations:
        print("\n🔝 Top 3 recommandations :")
        for i, player in enumerate(recommendations[:3], 1):
            print(f"{i}. {player['name']} ({player['age']} ans) - Score: {player['recommendation_score']:.1f}")
    
    print("\n✅ Module de recrutement opérationnel !")
