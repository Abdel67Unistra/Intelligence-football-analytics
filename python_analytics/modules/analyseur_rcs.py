"""
Analyseur de Performance Racing Club de Strasbourg
=================================================

Module spécialisé pour l'analyse des performances du Racing Club de Strasbourg
Code entièrement en français pour faciliter l'usage par le staff technique français.

Auteur: Football Analytics Platform
Équipe: Racing Club de Strasbourg
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

class AnalyseurPerformanceRCS:
    """Analyseur de performance spécialisé pour le Racing Club de Strasbourg"""
    
    def __init__(self):
        """Initialise l'analyseur avec les données du RCS"""
        self.nom_club = "Racing Club de Strasbourg"
        self.nom_court = "RCS"
        self.stade = "Stade de la Meinau"
        self.capacite_stade = 26109
        self.couleurs_club = ["#0066CC", "#FFFFFF"]  # Bleu et blanc
        
    def obtenir_effectif_actuel(self) -> pd.DataFrame:
        """
        Retourne l'effectif actuel du RCS (saison 2024-2025)
        
        Returns:
            DataFrame avec les joueurs actuels du RCS
        """
        # Effectif réel du RCS 2024-2025
        effectif_rcs = [
            # Gardiens
            {"nom_complet": "Matz Sels", "poste": "GB", "age": 32, "nationalite": "Belgique", "numero": 1},
            {"nom_complet": "Alaa Bellaarouch", "poste": "GB", "age": 20, "nationalite": "Maroc", "numero": 30},
            
            # Défenseurs
            {"nom_complet": "Guela Doué", "poste": "DD", "age": 22, "nationalite": "France", "numero": 2},
            {"nom_complet": "Abakar Sylla", "poste": "DC", "age": 24, "nationalite": "France", "numero": 4},
            {"nom_complet": "Saïdou Sow", "poste": "DC", "age": 22, "nationalite": "Guinée", "numero": 24},
            {"nom_complet": "Marvin Senaya", "poste": "DD", "age": 22, "nationalite": "France", "numero": 28},
            {"nom_complet": "Thomas Delaine", "poste": "DG", "age": 32, "nationalite": "France", "numero": 3},
            {"nom_complet": "Frédéric Guilbert", "poste": "DD", "age": 29, "nationalite": "France", "numero": 19},
            {"nom_complet": "Caleb Wiley", "poste": "DG", "age": 20, "nationalite": "États-Unis", "numero": 27},
            
            # Milieux
            {"nom_complet": "Habib Diarra", "poste": "MDC", "age": 20, "nationalite": "France", "numero": 18},
            {"nom_complet": "Andrey Santos", "poste": "MC", "age": 20, "nationalite": "Brésil", "numero": 6},
            {"nom_complet": "Ismaël Doukouré", "poste": "MC", "age": 21, "nationalite": "France", "numero": 29},
            {"nom_complet": "Junior Mwanga", "poste": "MDC", "age": 20, "nationalite": "France", "numero": 15},
            {"nom_complet": "Sékou Mara", "poste": "MOC", "age": 22, "nationalite": "France", "numero": 14},
            {"nom_complet": "Dilane Bakwa", "poste": "AD", "age": 21, "nationalite": "France", "numero": 26},
            
            # Attaquants
            {"nom_complet": "Emanuel Emegha", "poste": "BU", "age": 21, "nationalite": "Pays-Bas", "numero": 10},
            {"nom_complet": "Félix Lemaréchal", "poste": "MOC", "age": 20, "nationalite": "France", "numero": 17},
            {"nom_complet": "Jeremy Sebas", "poste": "AG", "age": 19, "nationalite": "France", "numero": 37},
            {"nom_complet": "Pape Diong", "poste": "BU", "age": 19, "nationalite": "Sénégal", "numero": 39},
        ]
        
        return pd.DataFrame(effectif_rcs)
    
    def calculer_metriques_xg_rcs(self, donnees_tirs: pd.DataFrame) -> pd.DataFrame:
        """
        Calcule les Expected Goals (xG) adaptés au style de jeu du RCS
        
        Args:
            donnees_tirs: DataFrame avec les données de tirs
            
        Returns:
            DataFrame avec xG calculés
        """
        donnees_tirs = donnees_tirs.copy()
        
        # Modèle xG adapté au style de jeu du RCS (jeu rapide, contres)
        # Facteurs: distance, angle, situation de jeu, pied utilisé
        
        centre_but_x, centre_but_y = 100, 50
        
        if 'x_coordonnee' in donnees_tirs.columns:
            col_x = 'x_coordonnee'
            col_y = 'y_coordonnee'
        else:
            col_x = 'x'
            col_y = 'y'
        
        # Calcul de la distance
        donnees_tirs['distance_but'] = np.sqrt(
            (donnees_tirs[col_x] - centre_but_x)**2 + 
            (donnees_tirs[col_y] - centre_but_y)**2
        )
        
        # Calcul de l'angle
        dx = centre_but_x - donnees_tirs[col_x]
        dy = abs(donnees_tirs[col_y] - centre_but_y)
        donnees_tirs['angle_tir'] = np.arctan2(dy, dx) * 180 / np.pi
        
        # Modèle xG simplifié (à remplacer par ML en production)
        xg_base = 0.1  # xG minimum
        
        # Facteur distance (plus proche = mieux)
        facteur_distance = np.exp(-donnees_tirs['distance_but'] / 20)
        
        # Facteur angle (angle plus petit = mieux)
        facteur_angle = 1 - (donnees_tirs['angle_tir'] / 90)
        
        # Bonus selon le type de tir
        bonus_situation = donnees_tirs.get('situation_tir', 'Jeu ouvert').map({
            'Contre-attaque': 1.3,  # Le RCS excelle en contre
            'Coup franc': 1.1,
            'Corner': 0.9,
            'Penalty': 5.0,
            'Jeu ouvert': 1.0
        }).fillna(1.0)
        
        # Bonus pied fort
        bonus_pied = donnees_tirs.get('partie_corps', 'Pied droit').map({
            'Pied dominant': 1.1,
            'Pied faible': 0.9,
            'Tête': 0.8,
            'Autre': 0.7
        }).fillna(1.0)
        
        # Calcul final de l'xG
        donnees_tirs['xg'] = np.clip(
            xg_base + (facteur_distance * facteur_angle * bonus_situation * bonus_pied * 0.8),
            0.01, 0.95
        )
        
        return donnees_tirs
    
    def analyser_forme_joueur_rcs(self, nom_joueur: str, nombre_matchs: int = 10) -> Dict:
        """
        Analyse la forme récente d'un joueur du RCS
        
        Args:
            nom_joueur: Nom du joueur à analyser
            nombre_matchs: Nombre de matchs récents à considérer
            
        Returns:
            Dictionnaire avec l'analyse de forme
        """
        # Données simulées pour la démonstration
        # En production, connecter à la base de données du club
        
        np.random.seed(hash(nom_joueur) % 2**32)
        
        # Génération de données réalistes selon le poste
        effectif = self.obtenir_effectif_actuel()
        joueur_info = effectif[effectif['nom_complet'] == nom_joueur]
        
        if joueur_info.empty:
            return {"erreur": f"Joueur '{nom_joueur}' non trouvé dans l'effectif RCS"}
        
        poste = joueur_info.iloc[0]['poste']
        
        # Statistiques par poste
        if poste == 'GB':
            stats_base = {
                'note_moyenne': np.random.normal(6.8, 0.8),
                'arrets_match': np.random.normal(4.2, 1.5),
                'buts_encaisses': np.random.normal(1.1, 0.7),
                'clean_sheets': np.random.binomial(1, 0.35, nombre_matchs).sum()
            }
        elif poste in ['DC', 'DD', 'DG']:
            stats_base = {
                'note_moyenne': np.random.normal(6.5, 0.7),
                'tacles_reussis': np.random.normal(3.8, 1.2),
                'interceptions': np.random.normal(2.1, 0.8),
                'duels_aeriens_pct': np.random.normal(65, 12)
            }
        elif poste in ['MDC', 'MC', 'MOC']:
            stats_base = {
                'note_moyenne': np.random.normal(6.7, 0.8),
                'passes_reussies_pct': np.random.normal(87, 6),
                'passes_cles': np.random.normal(1.8, 0.9),
                'kilometres_parcourus': np.random.normal(11.2, 1.1)
            }
        else:  # Attaquants
            stats_base = {
                'note_moyenne': np.random.normal(6.9, 0.9),
                'buts_par_90': np.random.normal(0.45, 0.25),
                'passes_decisives_par_90': np.random.normal(0.21, 0.15),
                'tirs_par_match': np.random.normal(2.8, 1.1)
            }
        
        # Tendance de forme (amélioration, stable, déclin)
        tendances = ['amélioration', 'stable', 'déclin']
        tendance = np.random.choice(tendances, p=[0.4, 0.4, 0.2])
        
        # Calcul de la consistance (plus proche de 1 = plus régulier)
        notes_recentes = np.random.normal(stats_base['note_moyenne'], 0.5, nombre_matchs)
        consistance = 1 - (np.std(notes_recentes) / np.mean(notes_recentes))
        
        return {
            "joueur": nom_joueur,
            "poste": poste,
            "matchs_analyses": nombre_matchs,
            "statistiques_cles": stats_base,
            "tendance_forme": tendance,
            "score_consistance": round(consistance, 2),
            "recommandation": self._generer_recommandation_forme(stats_base, tendance, poste)
        }
    
    def _generer_recommandation_forme(self, stats: Dict, tendance: str, poste: str) -> str:
        """Génère une recommandation basée sur la forme du joueur"""
        
        if tendance == 'amélioration':
            if poste in ['BU', 'AG', 'AD']:
                return "🔥 Forme excellente - Titulaire indiscutable pour les prochains matchs"
            else:
                return "📈 Progression notable - Maintenir le temps de jeu actuel"
        
        elif tendance == 'stable':
            return "⚖️ Forme stable - Continuer le travail, surveiller la motivation"
        
        else:  # déclin
            if stats['note_moyenne'] < 6.0:
                return "⚠️ Forme préoccupante - Considérer rotation ou travail spécifique"
            else:
                return "📉 Léger passage à vide - Normal sur une saison, maintenir la confiance"
    
    def generer_rapport_match_rcs(self, adversaire: str, domicile: bool = True) -> Dict:
        """
        Génère un rapport de match pour le RCS
        
        Args:
            adversaire: Nom de l'équipe adverse
            domicile: True si match à domicile
            
        Returns:
            Dictionnaire avec le rapport de match
        """
        lieu = "Stade de la Meinau" if domicile else f"Extérieur vs {adversaire}"
        
        # Simulation de données de match réalistes
        np.random.seed(hash(adversaire) % 2**32)
        
        score_rcs = np.random.randint(0, 4)
        score_adversaire = np.random.randint(0, 3)
        
        # Avantage à domicile
        if domicile:
            score_rcs += np.random.choice([0, 1], p=[0.6, 0.4])
        
        # Métriques de performance
        possession_rcs = np.random.normal(48 if not domicile else 52, 8)
        possession_rcs = np.clip(possession_rcs, 25, 75)
        
        return {
            "equipe": self.nom_club,
            "adversaire": adversaire,
            "lieu": lieu,
            "score_final": f"{self.nom_court} {score_rcs} - {score_adversaire} {adversaire}",
            "possession": {
                "rcs": round(possession_rcs, 1),
                "adversaire": round(100 - possession_rcs, 1)
            },
            "xg": {
                "rcs": round(np.random.normal(1.4, 0.6), 2),
                "adversaire": round(np.random.normal(1.2, 0.5), 2)
            },
            "statistiques_detaillees": {
                "tirs_rcs": np.random.randint(8, 18),
                "tirs_cadres_rcs": np.random.randint(3, 8),
                "corners_rcs": np.random.randint(3, 12),
                "fautes_rcs": np.random.randint(8, 16),
                "cartons_jaunes_rcs": np.random.randint(0, 4),
                "cartons_rouges_rcs": np.random.randint(0, 1)
            },
            "performances_individuelles": self._generer_notes_joueurs()
        }
    
    def _generer_notes_joueurs(self) -> List[Dict]:
        """Génère les notes de performance individuelles"""
        effectif = self.obtenir_effectif_actuel()
        
        # Sélectionner 11 titulaires + quelques remplaçants
        titulaires = effectif.sample(n=min(14, len(effectif)))
        
        notes = []
        for _, joueur in titulaires.iterrows():
            note = np.random.normal(6.5, 1.2)
            note = np.clip(note, 3.0, 10.0)
            
            notes.append({
                "nom": joueur['nom_complet'],
                "poste": joueur['poste'],
                "note": round(note, 1),
                "minutes_jouees": np.random.choice([90, 60, 30, 15], p=[0.6, 0.2, 0.15, 0.05]),
                "commentaire": self._generer_commentaire_performance(note, joueur['poste'])
            })
        
        # Trier par note décroissante
        return sorted(notes, key=lambda x: x['note'], reverse=True)
    
    def _generer_commentaire_performance(self, note: float, poste: str) -> str:
        """Génère un commentaire de performance selon la note et le poste"""
        
        if note >= 8.0:
            commentaires = [
                "Performance exceptionnelle, homme du match potentiel",
                "Très grande maîtrise technique et tactique",
                "Impact majeur sur le résultat de l'équipe"
            ]
        elif note >= 7.0:
            commentaires = [
                "Bonne performance, répond aux attentes",
                "Solide dans son rôle, quelques belles actions",
                "Contribution positive au collectif"
            ]
        elif note >= 6.0:
            commentaires = [
                "Performance correcte sans être brillante",
                "Remplit sa mission basique",
                "Quelques imprécisions mais dans l'ensemble acceptable"
            ]
        elif note >= 5.0:
            commentaires = [
                "Performance en demi-teinte, peut mieux faire",
                "Plusieurs erreurs techniques ou tactiques",
                "Manque d'impact sur le jeu"
            ]
        else:
            commentaires = [
                "Performance décevante, largement en dessous du niveau",
                "Nombreuses erreurs, pénalise l'équipe",
                "Substitution logique"
            ]
        
        return np.random.choice(commentaires)
    
    def analyser_tactique_rcs(self) -> Dict:
        """
        Analyse les tendances tactiques du RCS
        
        Returns:
            Dictionnaire avec l'analyse tactique
        """
        return {
            "formation_principale": "4-2-3-1",
            "formations_alternatives": ["4-3-3", "5-3-2"],
            "style_de_jeu": {
                "possession_moyenne": 47.2,
                "passes_par_match": 412,
                "precision_passes": 83.1,
                "pressing_haute": "Modéré",
                "vitesse_transition": "Rapide"
            },
            "forces": [
                "Jeu de contre-attaque efficace",
                "Cohésion défensive",
                "Pressing coordonné en bloc médian",
                "Qualité technique sur coups de pied arrêtés"
            ],
            "axes_amelioration": [
                "Conservation du ballon en phase offensive",
                "Création d'occasions en jeu positionnel",
                "Concentration sur toute la durée du match",
                "Efficacité dans la surface adverse"
            ],
            "joueurs_cles": {
                "createur": "Dilane Bakwa",
                "finisseur": "Emanuel Emegha", 
                "leader_defensif": "Abakar Sylla",
                "metronome": "Andrey Santos"
            }
        }

def main():
    """Fonction principale pour tester l'analyseur RCS"""
    analyseur = AnalyseurPerformanceRCS()
    
    print("🔵⚪ Analyseur Racing Club de Strasbourg")
    print("=" * 50)
    
    # Test effectif
    effectif = analyseur.obtenir_effectif_actuel()
    print(f"\n📋 Effectif actuel: {len(effectif)} joueurs")
    print(effectif[['nom_complet', 'poste', 'age']].head())
    
    # Test analyse forme
    print(f"\n📊 Analyse de forme - Emanuel Emegha:")
    forme = analyseur.analyser_forme_joueur_rcs("Emanuel Emegha")
    print(f"Note moyenne: {forme['statistiques_cles']['note_moyenne']:.1f}")
    print(f"Tendance: {forme['tendance_forme']}")
    print(f"Recommandation: {forme['recommandation']}")
    
    # Test rapport de match
    print(f"\n⚽ Rapport de match vs Lyon:")
    rapport = analyseur.generer_rapport_match_rcs("Olympique Lyonnais", domicile=True)
    print(f"Score: {rapport['score_final']}")
    print(f"xG: RCS {rapport['xg']['rcs']} - {rapport['xg']['adversaire']} Lyon")

if __name__ == "__main__":
    main()
