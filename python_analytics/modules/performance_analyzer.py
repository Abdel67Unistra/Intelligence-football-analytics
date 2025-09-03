"""
Football Performance Analytics Module
=====================================

Module principal pour l'analyse de performance footballistique.
Calcule les métriques avancées (xG, xA, PPDA) et fournit des analyses tactiques.

Author: Football Analytics Platform
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class FootballMetrics:
    """Classe pour calculer les métriques football avancées"""
    
    def __init__(self):
        self.xg_model = None  # Sera chargé avec un modèle ML pré-entraîné
        
    def calculate_xg(self, shots_data: pd.DataFrame) -> pd.DataFrame:
        """
        Calcule l'Expected Goals (xG) basé sur les caractéristiques des tirs
        
        Args:
            shots_data: DataFrame avec colonnes [x, y, situation, body_part, distance, angle]
        
        Returns:
            DataFrame avec colonne xG ajoutée
        """
        # Modèle simplifié d'xG basé sur la distance et l'angle
        # En production, utiliser un modèle ML entraîné
        
        shots_data = shots_data.copy()
        
        # Calcul de la distance du but (coordonnées normalisées 0-100)
        goal_x, goal_y = 100, 50  # Centre du but adverse
        shots_data['distance_to_goal'] = np.sqrt(
            (shots_data['x_coordinate'] - goal_x) ** 2 + 
            (shots_data['y_coordinate'] - goal_y) ** 2
        )
        
        # Calcul de l'angle de tir
        shots_data['angle'] = np.abs(shots_data['y_coordinate'] - goal_y) / shots_data['distance_to_goal']
        
        # Modèle xG simplifié (à remplacer par ML)
        base_xg = 1 / (1 + np.exp(0.1 * shots_data['distance_to_goal'] - 3))
        
        # Ajustements selon la situation
        situation_multiplier = shots_data['event_details'].apply(
            lambda x: self._get_situation_multiplier(x) if pd.notna(x) else 1.0
        )
        
        shots_data['xg'] = base_xg * situation_multiplier
        shots_data['xg'] = np.clip(shots_data['xg'], 0, 1)  # Limiter entre 0 et 1
        
        return shots_data
    
    def _get_situation_multiplier(self, event_details: dict) -> float:
        """Multiplicateur xG selon la situation de jeu"""
        if not isinstance(event_details, dict):
            return 1.0
            
        situation = event_details.get('situation', 'open_play')
        
        multipliers = {
            'penalty': 0.76,
            'free_kick': 0.05,
            'corner': 0.03,
            'counter_attack': 1.5,
            'set_piece': 0.1,
            'open_play': 1.0
        }
        
        return multipliers.get(situation, 1.0)
    
    def calculate_xa(self, passes_data: pd.DataFrame, shots_data: pd.DataFrame) -> pd.DataFrame:
        """
        Calcule l'Expected Assists (xA) pour les passes menant à des tirs
        
        Args:
            passes_data: DataFrame des passes
            shots_data: DataFrame des tirs avec xG
        
        Returns:
            DataFrame des passes avec xA
        """
        # Simuler la logique xA - en production, analyser les passes précédant les tirs
        passes_data = passes_data.copy()
        
        # xA = xG du tir qui suit la passe (si dans les 15 secondes)
        # Logique simplifiée pour la démo
        passes_data['xa'] = np.random.exponential(0.1, len(passes_data))  # Valeurs réalistes
        passes_data['xa'] = np.clip(passes_data['xa'], 0, 0.8)  # Plafond réaliste
        
        return passes_data
    
    def calculate_ppda(self, events_data: pd.DataFrame, team_id: str) -> float:
        """
        Calcule le PPDA (Passes per Defensive Action)
        Métrique d'intensité du pressing
        
        Args:
            events_data: DataFrame des événements du match
            team_id: ID de l'équipe analysée
        
        Returns:
            Valeur PPDA (plus faible = pressing plus intense)
        """
        # Passes adverses dans le tiers défensif de l'équipe
        opponent_passes = events_data[
            (events_data['team_id'] != team_id) & 
            (events_data['event_type'] == 'Pass') &
            (events_data['x_coordinate'] <= 33.33)  # Tiers défensif
        ]
        
        # Actions défensives de l'équipe
        defensive_actions = events_data[
            (events_data['team_id'] == team_id) & 
            (events_data['event_type'].isin(['Tackle', 'Interception', 'Foul']))
        ]
        
        if len(defensive_actions) == 0:
            return float('inf')
        
        return len(opponent_passes) / len(defensive_actions)


class PlayerPerformanceAnalyzer:
    """Analyseur de performance individuelle des joueurs"""
    
    def __init__(self, db_connection):
        self.db = db_connection
        self.metrics = FootballMetrics()
    
    def get_player_form(self, player_id: str, last_n_matches: int = 10) -> Dict:
        """
        Analyse la forme d'un joueur sur ses N derniers matchs
        
        Args:
            player_id: ID du joueur
            last_n_matches: Nombre de matchs à analyser
        
        Returns:
            Dictionnaire avec métriques de forme
        """
        query = """
        SELECT pms.*, m.match_date, t.name as opponent
        FROM player_match_stats pms
        JOIN matches m ON pms.match_id = m.match_id
        JOIN teams t ON (CASE 
            WHEN m.home_team_id = pms.team_id THEN m.away_team_id 
            ELSE m.home_team_id 
        END) = t.team_id
        WHERE pms.player_id = %s 
        AND pms.minutes_played > 0
        ORDER BY m.match_date DESC
        LIMIT %s
        """
        
        stats = pd.read_sql(query, self.db, params=[player_id, last_n_matches])
        
        if len(stats) == 0:
            return {"error": "Aucune donnée trouvée pour ce joueur"}
        
        # Calcul des tendances
        form_analysis = {
            "matches_analyzed": len(stats),
            "avg_rating": stats['rating'].mean(),
            "rating_trend": self._calculate_trend(stats['rating'].values),
            "goals_per_90": (stats['goals'].sum() / stats['minutes_played'].sum()) * 90,
            "assists_per_90": (stats['assists'].sum() / stats['minutes_played'].sum()) * 90,
            "xg_per_90": (stats['xg'].sum() / stats['minutes_played'].sum()) * 90,
            "xa_per_90": (stats['xa'].sum() / stats['minutes_played'].sum()) * 90,
            "pass_accuracy": (stats['passes_completed'].sum() / stats['passes_total'].sum()) * 100,
            "consistency_score": self._calculate_consistency(stats['rating'].values),
            "recent_performances": stats[['match_date', 'rating', 'goals', 'assists']].to_dict('records')
        }
        
        return form_analysis
    
    def _calculate_trend(self, values: np.ndarray) -> str:
        """Calcule la tendance d'une série de valeurs"""
        if len(values) < 3:
            return "Données insuffisantes"
        
        # Régression linéaire simple
        x = np.arange(len(values))
        slope = np.polyfit(x, values, 1)[0]
        
        if slope > 0.05:
            return "En hausse"
        elif slope < -0.05:
            return "En baisse"
        else:
            return "Stable"
    
    def _calculate_consistency(self, values: np.ndarray) -> float:
        """Calcule un score de consistance (inverse du coefficient de variation)"""
        if len(values) == 0 or np.mean(values) == 0:
            return 0.0
        
        cv = np.std(values) / np.mean(values)
        return max(0, 100 - (cv * 100))
    
    def compare_players(self, player_ids: List[str], position_filter: str = None) -> pd.DataFrame:
        """
        Compare plusieurs joueurs sur leurs statistiques clés
        
        Args:
            player_ids: Liste des IDs joueurs à comparer
            position_filter: Filtrer par position pour comparaison pertinente
        
        Returns:
            DataFrame de comparaison
        """
        placeholders = ','.join(['%s'] * len(player_ids))
        
        query = f"""
        SELECT 
            p.first_name || ' ' || p.last_name as player_name,
            pos.name as position,
            pss.total_goals,
            pss.total_assists,
            pss.total_xg,
            pss.total_xa,
            pss.avg_rating,
            pss.pass_accuracy_pct,
            pss.tackle_success_pct,
            pss.matches_played,
            pss.total_minutes
        FROM player_season_stats pss
        JOIN players p ON pss.player_id = p.player_id
        LEFT JOIN player_team_contracts ptc ON p.player_id = ptc.player_id 
            AND ptc.end_date IS NULL
        LEFT JOIN positions pos ON ptc.primary_position_id = pos.position_id
        WHERE pss.player_id IN ({placeholders})
        AND pss.season = '2024-2025'
        """
        
        params = player_ids
        if position_filter:
            query += " AND pos.code = %s"
            params.append(position_filter)
        
        comparison = pd.read_sql(query, self.db, params=params)
        
        # Calcul des métriques par 90 minutes
        comparison['goals_per_90'] = (comparison['total_goals'] / comparison['total_minutes']) * 90
        comparison['assists_per_90'] = (comparison['total_assists'] / comparison['total_minutes']) * 90
        comparison['xg_per_90'] = (comparison['total_xg'] / comparison['total_minutes']) * 90
        comparison['xa_per_90'] = (comparison['total_xa'] / comparison['total_minutes']) * 90
        
        return comparison
    
    def generate_player_heatmap(self, player_id: str, match_id: str = None) -> plt.Figure:
        """
        Génère une heatmap des zones d'action d'un joueur
        
        Args:
            player_id: ID du joueur
            match_id: ID du match spécifique (optionnel)
        
        Returns:
            Figure matplotlib avec heatmap
        """
        # Requête des événements avec positions
        if match_id:
            query = """
            SELECT x_coordinate, y_coordinate, event_type
            FROM match_events 
            WHERE player_id = %s AND match_id = %s
            AND x_coordinate IS NOT NULL AND y_coordinate IS NOT NULL
            """
            params = [player_id, match_id]
        else:
            query = """
            SELECT me.x_coordinate, me.y_coordinate, me.event_type
            FROM match_events me
            JOIN matches m ON me.match_id = m.match_id
            WHERE me.player_id = %s 
            AND me.x_coordinate IS NOT NULL AND me.y_coordinate IS NOT NULL
            AND m.match_date >= %s
            """
            params = [player_id, datetime.now() - timedelta(days=30)]
        
        events = pd.read_sql(query, self.db, params=params)
        
        if len(events) == 0:
            fig, ax = plt.subplots(figsize=(12, 8))
            ax.text(0.5, 0.5, 'Aucune donnée de position disponible', 
                   ha='center', va='center', transform=ax.transAxes)
            return fig
        
        # Création de la heatmap
        fig, ax = plt.subplots(figsize=(15, 10))
        
        # Grille pour la heatmap
        x_bins = np.linspace(0, 100, 21)
        y_bins = np.linspace(0, 100, 15)
        
        # Calcul de la densité
        heatmap, _, _ = np.histogram2d(events['x_coordinate'], events['y_coordinate'], 
                                     bins=[x_bins, y_bins])
        
        # Affichage
        im = ax.imshow(heatmap.T, extent=[0, 100, 0, 100], origin='lower', 
                      cmap='Reds', alpha=0.7)
        
        # Ajout du terrain de football
        self._draw_football_pitch(ax)
        
        # Colorbar
        plt.colorbar(im, ax=ax, label='Densité d\'actions')
        
        ax.set_title(f'Heatmap d\'activité - Joueur {player_id}', fontsize=16)
        ax.set_xlabel('Position X (0=But défensif, 100=But offensif)')
        ax.set_ylabel('Position Y (0=Touche gauche, 100=Touche droite)')
        
        return fig
    
    def _draw_football_pitch(self, ax):
        """Dessine les lignes principales d'un terrain de football"""
        # Lignes de touche
        ax.plot([0, 100], [0, 0], 'k-', lw=2)
        ax.plot([0, 100], [100, 100], 'k-', lw=2)
        ax.plot([0, 0], [0, 100], 'k-', lw=2)
        ax.plot([100, 100], [0, 100], 'k-', lw=2)
        
        # Ligne médiane
        ax.plot([50, 50], [0, 100], 'k-', lw=2)
        
        # Cercle central
        circle = plt.Circle((50, 50), 9.15, fill=False, color='black', lw=2)
        ax.add_patch(circle)
        
        # Surfaces de réparation
        # Surface défensive
        ax.plot([0, 16.5], [21.1, 21.1], 'k-', lw=2)
        ax.plot([0, 16.5], [78.9, 78.9], 'k-', lw=2)
        ax.plot([16.5, 16.5], [21.1, 78.9], 'k-', lw=2)
        
        # Surface offensive
        ax.plot([83.5, 100], [21.1, 21.1], 'k-', lw=2)
        ax.plot([83.5, 100], [78.9, 78.9], 'k-', lw=2)
        ax.plot([83.5, 83.5], [21.1, 78.9], 'k-', lw=2)


class TacticalAnalyzer:
    """Analyseur de données tactiques et d'équipe"""
    
    def __init__(self, db_connection):
        self.db = db_connection
        self.metrics = FootballMetrics()
    
    def analyze_team_formation(self, team_id: str, match_id: str) -> Dict:
        """
        Analyse la formation et le système de jeu d'une équipe
        
        Args:
            team_id: ID de l'équipe
            match_id: ID du match
        
        Returns:
            Dictionnaire avec analyse tactique
        """
        # Récupération des positions moyennes des joueurs
        query = """
        SELECT 
            p.first_name || ' ' || p.last_name as player_name,
            pos.code as position,
            pms.minutes_played,
            AVG(me.x_coordinate) as avg_x,
            AVG(me.y_coordinate) as avg_y,
            COUNT(me.event_id) as total_actions
        FROM player_match_stats pms
        JOIN players p ON pms.player_id = p.player_id
        JOIN positions pos ON pms.position_played_id = pos.position_id
        LEFT JOIN match_events me ON pms.player_id = me.player_id 
            AND pms.match_id = me.match_id
        WHERE pms.team_id = %s AND pms.match_id = %s
        AND pms.minutes_played > 0
        GROUP BY p.first_name, p.last_name, pos.code, pms.minutes_played
        ORDER BY pms.minutes_played DESC
        """
        
        formation_data = pd.read_sql(query, self.db, params=[team_id, match_id])
        
        # Détection automatique de la formation
        formation = self._detect_formation(formation_data)
        
        # Analyse des passes entre joueurs
        pass_network = self._analyze_pass_network(team_id, match_id)
        
        # Intensité du pressing
        ppda = self.metrics.calculate_ppda(
            self._get_match_events(match_id), team_id
        )
        
        return {
            "detected_formation": formation,
            "average_positions": formation_data.to_dict('records'),
            "pass_network": pass_network,
            "pressing_intensity": {
                "ppda": ppda,
                "intensity_level": self._categorize_ppda(ppda)
            }
        }
    
    def _detect_formation(self, formation_data: pd.DataFrame) -> str:
        """Détecte automatiquement la formation basée sur les positions"""
        # Comptage par ligne de jeu
        position_counts = formation_data['position'].apply(
            lambda x: self._get_position_line(x)
        ).value_counts()
        
        # Construction de la formation (format X-X-X)
        defenders = position_counts.get('Defence', 0)
        midfielders = position_counts.get('Midfield', 0)
        attackers = position_counts.get('Attack', 0)
        
        return f"{defenders}-{midfielders}-{attackers}"
    
    def _get_position_line(self, position_code: str) -> str:
        """Associe une position à sa ligne de jeu"""
        lines = {
            'GK': 'Goalkeeper',
            'CB': 'Defence', 'LB': 'Defence', 'RB': 'Defence', 
            'LWB': 'Defence', 'RWB': 'Defence',
            'DM': 'Midfield', 'CM': 'Midfield', 'LM': 'Midfield', 
            'RM': 'Midfield', 'AM': 'Midfield',
            'LW': 'Attack', 'RW': 'Attack', 'ST': 'Attack', 'CF': 'Attack'
        }
        return lines.get(position_code, 'Unknown')
    
    def _analyze_pass_network(self, team_id: str, match_id: str) -> Dict:
        """Analyse le réseau de passes entre joueurs"""
        # Simulation d'un réseau de passes
        # En production, analyser les passes successives
        query = """
        SELECT 
            passer.first_name || ' ' || passer.last_name as passer_name,
            receiver.first_name || ' ' || receiver.last_name as receiver_name,
            COUNT(*) as pass_count
        FROM match_events me1
        JOIN players passer ON me1.player_id = passer.player_id
        JOIN match_events me2 ON me1.match_id = me2.match_id 
            AND me2.minute = me1.minute 
            AND me2.event_type = 'Pass'
            AND me2.player_id != me1.player_id
            AND me2.team_id = me1.team_id
        JOIN players receiver ON me2.player_id = receiver.player_id
        WHERE me1.team_id = %s AND me1.match_id = %s
        AND me1.event_type = 'Pass' AND me1.success = true
        GROUP BY passer.first_name, passer.last_name, 
                receiver.first_name, receiver.last_name
        HAVING COUNT(*) >= 3
        ORDER BY pass_count DESC
        """
        
        pass_network = pd.read_sql(query, self.db, params=[team_id, match_id])
        
        return {
            "total_connections": len(pass_network),
            "strongest_connections": pass_network.head(10).to_dict('records')
        }
    
    def _get_match_events(self, match_id: str) -> pd.DataFrame:
        """Récupère tous les événements d'un match"""
        query = """
        SELECT * FROM match_events 
        WHERE match_id = %s
        ORDER BY minute, second_in_minute
        """
        return pd.read_sql(query, self.db, params=[match_id])
    
    def _categorize_ppda(self, ppda_value: float) -> str:
        """Catégorise l'intensité du pressing selon la valeur PPDA"""
        if ppda_value < 8:
            return "Pressing très intense"
        elif ppda_value < 12:
            return "Pressing intense"
        elif ppda_value < 16:
            return "Pressing modéré"
        else:
            return "Pressing faible"


# Fonctions utilitaires
def create_radar_chart(player_stats: Dict, categories: List[str]) -> plt.Figure:
    """
    Crée un graphique radar pour visualiser les stats d'un joueur
    
    Args:
        player_stats: Dictionnaire des statistiques
        categories: Liste des catégories à afficher
    
    Returns:
        Figure matplotlib
    """
    # Nombre de variables
    N = len(categories)
    
    # Angles pour chaque axe
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]  # Fermer le cercle
    
    # Valeurs (normalisées 0-100)
    values = [player_stats.get(cat, 0) for cat in categories]
    values += values[:1]
    
    # Création du graphique
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
    
    # Tracé
    ax.plot(angles, values, 'o-', linewidth=2, label='Joueur')
    ax.fill(angles, values, alpha=0.25)
    
    # Personnalisation
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories)
    ax.set_ylim(0, 100)
    ax.set_yticks([20, 40, 60, 80, 100])
    ax.set_yticklabels(['20', '40', '60', '80', '100'])
    ax.grid(True)
    
    plt.title('Profil du joueur - Graphique radar', size=16, y=1.1)
    
    return fig


if __name__ == "__main__":
    # Tests et exemples d'utilisation
    print("🏈 Football Performance Analytics Module")
    print("========================================")
    print("Module d'analyse de performance footballistique")
    print("Fonctionnalités : xG, xA, PPDA, heatmaps, analyses tactiques")
    print("\nUtilisez les classes :")
    print("- FootballMetrics : Calculs métriques avancées")
    print("- PlayerPerformanceAnalyzer : Analyses individuelles")  
    print("- TacticalAnalyzer : Analyses d'équipe et tactiques")
