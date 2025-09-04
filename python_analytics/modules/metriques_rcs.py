"""
Métriques Football Racing Club de Strasbourg
===========================================

Calculs de métriques football avancées adaptées au style de jeu du RCS.
Implémentation des formules modernes avec optimisations spécifiques au club.

Auteur: Football Analytics Platform
Équipe: Racing Club de Strasbourg
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
import math
from datetime import datetime, timedelta

class MetriquesFootballRCS:
    """
    Classe de calcul des métriques football avancées pour le RCS
    
    Métriques incluses:
    - Expected Goals (xG) et Expected Assists (xA)
    - PPDA (Passes per Defensive Action)
    - Métriques de pressing et possession
    - Analyses spatiales et heat maps
    - KPIs spécifiques au style RCS
    """
    
    def __init__(self):
        """Initialise les constantes et paramètres du RCS"""
        self.nom_equipe = "Racing Club de Strasbourg"
        self.style_jeu = "contre_attaque_rapide"
        self.formation_principale = "4-2-3-1"
        
        # Paramètres terrain (coordonnées normalisées 0-100)
        self.longueur_terrain = 100
        self.largeur_terrain = 100
        self.coordonnees_but_adverse = (100, 50)
        self.coordonnees_but_propre = (0, 50)
        
        # Zones tactiques spécifiques RCS
        self.zones_defensives = [(0, 35), (0, 100)]    # Tiers défensif
        self.zones_milieu = [(35, 65), (0, 100)]       # Tiers milieu
        self.zones_offensives = [(65, 100), (0, 100)]  # Tiers offensif
        
        # Coefficients xG adaptés au style RCS (préférence contres)
        self.coefficients_xg = {
            'distance_base': 0.12,
            'angle_multiplicateur': 1.8,
            'situation_contre': 1.35,  # Bonus contre-attaque
            'situation_normale': 1.0,
            'situation_arret_jeu': 0.85,
            'pied_dominant': 1.15,
            'pied_faible': 0.90,
            'tete': 0.95,
            'penalty': 0.76  # Taux de réussite penalty Ligue 1
        }
    
    def calculer_xg_tir(self, 
                        x_coordonnee: float, 
                        y_coordonnee: float,
                        situation: str = "jeu_ouvert",
                        partie_corps: str = "pied_droit",
                        joueur_tireur: str = None) -> float:
        """
        Calcule l'Expected Goal (xG) pour un tir donné
        
        Args:
            x_coordonnee: Position X du tir (0-100)
            y_coordonnee: Position Y du tir (0-100)  
            situation: Type de situation ("contre_attaque", "jeu_ouvert", "coup_franc", etc.)
            partie_corps: Partie du corps utilisée
            joueur_tireur: Nom du joueur (pour bonus individuels)
            
        Returns:
            Valeur xG entre 0 et 1
        """
        
        # Calcul de la distance au but (en mètres approximatifs)
        distance_but = self._calculer_distance_but(x_coordonnee, y_coordonnee)
        
        # Calcul de l'angle de tir
        angle_tir = self._calculer_angle_tir(x_coordonnee, y_coordonnee)
        
        # xG de base selon la distance
        if distance_but <= 6:  # Dans les 6 mètres
            xg_base = 0.45
        elif distance_but <= 11:  # Surface de réparation
            xg_base = 0.25
        elif distance_but <= 16:  # Juste devant la surface
            xg_base = 0.12
        elif distance_but <= 25:  # 25 mètres
            xg_base = 0.05
        else:  # Tirs lointains
            xg_base = 0.02
        
        # Modification selon l'angle (plus l'angle est petit, plus c'est difficile)
        facteur_angle = max(0.3, math.sin(math.radians(angle_tir)))
        
        # Bonus/malus selon la situation de jeu
        facteur_situation = self.coefficients_xg.get(f'situation_{situation}', 1.0)
        
        # Bonus/malus selon la partie du corps
        if partie_corps in ["pied_gauche", "pied_droit"]:
            facteur_corps = self.coefficients_xg['pied_dominant']
        elif partie_corps == "tete":
            facteur_corps = self.coefficients_xg['tete']
        else:
            facteur_corps = 0.8  # Autre partie du corps
        
        # Bonus joueur spécifique (finisseurs reconnus)
        bonus_joueur = self._obtenir_bonus_finisseur(joueur_tireur)
        
        # Calcul final de l'xG
        xg_final = xg_base * facteur_angle * facteur_situation * facteur_corps * bonus_joueur
        
        # Contraindre entre 0.005 et 0.95
        return max(0.005, min(0.95, xg_final))
    
    def calculer_xa_passe(self,
                         x_passe: float,
                         y_passe: float, 
                         x_reception: float,
                         y_reception: float,
                         type_passe: str = "normale",
                         joueur_passeur: str = None) -> float:
        """
        Calcule l'Expected Assist (xA) pour une passe donnée
        
        Args:
            x_passe: Position X du passeur
            y_passe: Position Y du passeur
            x_reception: Position X du réceptionneur
            y_reception: Position Y du réceptionneur
            type_passe: Type de passe ("normale", "centre", "passe_cle", etc.)
            joueur_passeur: Nom du passeur
            
        Returns:
            Valeur xA entre 0 et 1
        """
        
        # Distance au but depuis la réception
        distance_but_reception = self._calculer_distance_but(x_reception, y_reception)
        
        # Angle de réception
        angle_reception = self._calculer_angle_tir(x_reception, y_reception)
        
        # xA de base selon la position de réception
        if distance_but_reception <= 6:
            xa_base = 0.25
        elif distance_but_reception <= 11:
            xa_base = 0.15
        elif distance_but_reception <= 16:
            xa_base = 0.08
        elif distance_but_reception <= 22:
            xa_base = 0.04
        else:
            xa_base = 0.01
        
        # Facteur selon l'angle de réception
        facteur_angle = max(0.4, math.sin(math.radians(angle_reception)))
        
        # Bonus selon le type de passe
        bonus_type_passe = {
            'passe_cle': 1.8,      # Passe décisive directe
            'centre': 1.3,         # Centre dans la surface
            'passe_profondeur': 1.5, # Passe en profondeur
            'normale': 1.0,
            'relance': 0.7
        }.get(type_passe, 1.0)
        
        # Difficulté de la passe (distance et précision requise)
        distance_passe = math.sqrt((x_reception - x_passe)**2 + (y_reception - y_passe)**2)
        if distance_passe > 30:  # Passe longue
            facteur_distance = 1.2
        elif distance_passe > 15:  # Passe moyenne
            facteur_distance = 1.1
        else:  # Passe courte
            facteur_distance = 1.0
        
        # Bonus créateur spécifique
        bonus_joueur = self._obtenir_bonus_createur(joueur_passeur)
        
        # Calcul final de l'xA
        xa_final = xa_base * facteur_angle * bonus_type_passe * facteur_distance * bonus_joueur
        
        return max(0.001, min(0.8, xa_final))
    
    def calculer_ppda_equipe(self, 
                            donnees_evenements: pd.DataFrame,
                            equipe_analysee: str = "RCS") -> float:
        """
        Calcule le PPDA (Passes per Defensive Action) pour mesurer l'intensité du pressing
        
        Args:
            donnees_evenements: DataFrame avec les événements du match
            equipe_analysee: Nom de l'équipe à analyser
            
        Returns:
            Valeur PPDA (plus c'est bas, plus le pressing est intense)
        """
        
        # Filtrer les événements de l'adversaire dans leur tiers défensif
        adversaire = donnees_evenements[donnees_evenements['equipe'] != equipe_analysee]
        
        # Passes adverses dans leur tiers défensif (où RCS peut presser)
        passes_adversaire_def = adversaire[
            (adversaire['type_evenement'] == 'passe') &
            (adversaire['x_coordonnee'] <= 35)  # Tiers défensif adverse
        ]
        
        # Actions défensives du RCS dans le tiers adverse
        actions_defensives_rcs = donnees_evenements[
            (donnees_evenements['equipe'] == equipe_analysee) &
            (donnees_evenements['type_evenement'].isin(['tacle', 'interception', 'faute'])) &
            (donnees_evenements['x_coordonnee'] >= 65)  # Pressing haut
        ]
        
        # Calcul PPDA
        nb_passes_adversaire = len(passes_adversaire_def)
        nb_actions_defensives = len(actions_defensives_rcs)
        
        if nb_actions_defensives > 0:
            ppda = nb_passes_adversaire / nb_actions_defensives
        else:
            ppda = float('inf')  # Pas de pressing
        
        return round(ppda, 2)
    
    def analyser_zones_recuperation(self, 
                                   donnees_evenements: pd.DataFrame,
                                   equipe_analysee: str = "RCS") -> Dict:
        """
        Analyse les zones de récupération du ballon pour évaluer le pressing
        
        Args:
            donnees_evenements: DataFrame avec les événements
            equipe_analysee: Équipe à analyser
            
        Returns:
            Dictionnaire avec les statistiques par zone
        """
        
        # Récupérations de l'équipe
        recuperations = donnees_evenements[
            (donnees_evenements['equipe'] == equipe_analysee) &
            (donnees_evenements['type_evenement'].isin(['interception', 'tacle_reussi']))
        ]
        
        # Classification par zones
        recuperations_zones = {
            'zone_defensive': 0,    # 0-35
            'zone_milieu': 0,       # 35-65  
            'zone_offensive': 0     # 65-100
        }
        
        for _, recup in recuperations.iterrows():
            x = recup['x_coordonnee']
            if x <= 35:
                recuperations_zones['zone_defensive'] += 1
            elif x <= 65:
                recuperations_zones['zone_milieu'] += 1
            else:
                recuperations_zones['zone_offensive'] += 1
        
        total_recuperations = sum(recuperations_zones.values())
        
        # Calcul des pourcentages
        if total_recuperations > 0:
            pourcentages = {
                zone: (count / total_recuperations) * 100 
                for zone, count in recuperations_zones.items()
            }
        else:
            pourcentages = {zone: 0 for zone in recuperations_zones.keys()}
        
        # Évaluation du style de pressing
        if pourcentages['zone_offensive'] > 25:
            style_pressing = "Pressing très haut - Style agressif"
        elif pourcentages['zone_offensive'] > 15:
            style_pressing = "Pressing haut - Style proactif"
        elif pourcentages['zone_milieu'] > 50:
            style_pressing = "Pressing médian - Style équilibré"
        else:
            style_pressing = "Pressing bas - Style défensif"
        
        return {
            'recuperations_par_zone': recuperations_zones,
            'pourcentages_par_zone': pourcentages,
            'total_recuperations': total_recuperations,
            'style_pressing': style_pressing,
            'efficacite_pressing': pourcentages['zone_offensive'] + pourcentages['zone_milieu'] / 2
        }
    
    def calculer_metriques_possession(self, 
                                     donnees_evenements: pd.DataFrame,
                                     equipe_analysee: str = "RCS") -> Dict:
        """
        Calcule les métriques avancées de possession
        
        Args:
            donnees_evenements: DataFrame avec les événements
            equipe_analysee: Équipe à analyser
            
        Returns:
            Dictionnaire avec les métriques de possession
        """
        
        # Événements de l'équipe
        evenements_equipe = donnees_evenements[donnees_evenements['equipe'] == equipe_analysee]
        
        # Passes de l'équipe
        passes = evenements_equipe[evenements_equipe['type_evenement'] == 'passe']
        passes_reussies = evenements_equipe[evenements_equipe['type_evenement'] == 'passe_reussie']
        
        # Métriques de base
        total_passes = len(passes)
        total_passes_reussies = len(passes_reussies)
        precision_passes = (total_passes_reussies / total_passes * 100) if total_passes > 0 else 0
        
        # Passes par zone
        passes_par_zone = {
            'zone_defensive': len(passes[passes['x_coordonnee'] <= 35]),
            'zone_milieu': len(passes[(passes['x_coordonnee'] > 35) & (passes['x_coordonnee'] <= 65)]),
            'zone_offensive': len(passes[passes['x_coordonnee'] > 65])
        }
        
        # Passes courtes vs longues
        passes['distance_passe'] = np.sqrt(
            (passes['x_coordonnee'] - passes['x_reception'])**2 + 
            (passes['y_coordonnee'] - passes['y_reception'])**2
        )
        
        passes_courtes = len(passes[passes['distance_passe'] <= 15])
        passes_longues = len(passes[passes['distance_passe'] > 30])
        passes_moyennes = total_passes - passes_courtes - passes_longues
        
        # Vitesse de jeu (passes par minute de possession effective)
        duree_possession = donnees_evenements['minute'].max() - donnees_evenements['minute'].min()
        vitesse_jeu = total_passes / duree_possession if duree_possession > 0 else 0
        
        return {
            'total_passes': total_passes,
            'precision_passes_pct': round(precision_passes, 1),
            'passes_par_zone': passes_par_zone,
            'repartition_distance': {
                'courtes': passes_courtes,
                'moyennes': passes_moyennes,
                'longues': passes_longues
            },
            'vitesse_jeu': round(vitesse_jeu, 1),
            'style_possession': self._evaluer_style_possession(passes_par_zone, precision_passes)
        }
    
    def generer_heatmap_joueur(self, 
                              donnees_positions: pd.DataFrame,
                              nom_joueur: str) -> Dict:
        """
        Génère une heatmap des positions d'un joueur
        
        Args:
            donnees_positions: DataFrame avec les positions du joueur
            nom_joueur: Nom du joueur
            
        Returns:
            Dictionnaire avec les données de heatmap
        """
        
        # Filtrer les données du joueur
        positions_joueur = donnees_positions[donnees_positions['joueur'] == nom_joueur]
        
        if positions_joueur.empty:
            return {"erreur": f"Aucune donnée de position trouvée pour {nom_joueur}"}
        
        # Créer une grille pour la heatmap
        x_bins = np.linspace(0, 100, 21)  # 20 zones en largeur
        y_bins = np.linspace(0, 100, 21)  # 20 zones en longueur
        
        # Calculer la densité par zone
        hist, x_edges, y_edges = np.histogram2d(
            positions_joueur['x_coordonnee'],
            positions_joueur['y_coordonnee'],
            bins=[x_bins, y_bins]
        )
        
        # Position moyenne du joueur
        x_moyen = positions_joueur['x_coordonnee'].mean()
        y_moyen = positions_joueur['y_coordonnee'].mean()
        
        # Zone d'activité principale
        zone_principale = self._identifier_zone_activite(x_moyen, y_moyen)
        
        # Mobilité du joueur (écart-type des positions)
        mobilite_x = positions_joueur['x_coordonnee'].std()
        mobilite_y = positions_joueur['y_coordonnee'].std()
        score_mobilite = math.sqrt(mobilite_x**2 + mobilite_y**2)
        
        return {
            'joueur': nom_joueur,
            'heatmap_data': hist,
            'x_edges': x_edges,
            'y_edges': y_edges,
            'position_moyenne': (round(x_moyen, 1), round(y_moyen, 1)),
            'zone_principale': zone_principale,
            'score_mobilite': round(score_mobilite, 1),
            'interpretation': self._interpreter_heatmap(zone_principale, score_mobilite)
        }
    
    def calculer_metriques_defensives(self, 
                                     donnees_evenements: pd.DataFrame,
                                     equipe_analysee: str = "RCS") -> Dict:
        """
        Calcule les métriques défensives avancées
        
        Args:
            donnees_evenements: DataFrame avec les événements
            equipe_analysee: Équipe à analyser
            
        Returns:
            Dictionnaire avec les métriques défensives
        """
        
        # Événements défensifs de l'équipe
        evenements_defensifs = donnees_evenements[
            (donnees_evenements['equipe'] == equipe_analysee) &
            (donnees_evenements['type_evenement'].isin([
                'tacle', 'interception', 'degagement', 'duel_aerien'
            ]))
        ]
        
        # Calculs par type d'action
        tacles = evenements_defensifs[evenements_defensifs['type_evenement'] == 'tacle']
        interceptions = evenements_defensifs[evenements_defensifs['type_evenement'] == 'interception']
        duels_aeriens = evenements_defensifs[evenements_defensifs['type_evenement'] == 'duel_aerien']
        
        # Taux de réussite
        taux_reussite_tacles = len(tacles[tacles['reussi'] == True]) / len(tacles) * 100 if len(tacles) > 0 else 0
        taux_reussite_duels = len(duels_aeriens[duels_aeriens['reussi'] == True]) / len(duels_aeriens) * 100 if len(duels_aeriens) > 0 else 0
        
        # Intensité défensive par zone
        intensite_par_zone = {
            'defensive': len(evenements_defensifs[evenements_defensifs['x_coordonnee'] <= 35]),
            'milieu': len(evenements_defensifs[(evenements_defensifs['x_coordonnee'] > 35) & 
                                             (evenements_defensifs['x_coordonnee'] <= 65)]),
            'offensive': len(evenements_defensifs[evenements_defensifs['x_coordonnee'] > 65])
        }
        
        return {
            'total_actions_defensives': len(evenements_defensifs),
            'tacles_tentes': len(tacles),
            'taux_reussite_tacles': round(taux_reussite_tacles, 1),
            'interceptions': len(interceptions),
            'duels_aeriens_tentes': len(duels_aeriens),
            'taux_reussite_duels_aeriens': round(taux_reussite_duels, 1),
            'intensite_par_zone': intensite_par_zone,
            'evaluation_defensive': self._evaluer_performance_defensive(
                taux_reussite_tacles, taux_reussite_duels, intensite_par_zone
            )
        }
    
    # Méthodes utilitaires privées
    
    def _calculer_distance_but(self, x: float, y: float) -> float:
        """Calcule la distance au but adverse en mètres approximatifs"""
        distance_pixels = math.sqrt((100 - x)**2 + (50 - y)**2)
        # Conversion approximative : 100 pixels = 105 mètres
        distance_metres = distance_pixels * 1.05
        return distance_metres
    
    def _calculer_angle_tir(self, x: float, y: float) -> float:
        """Calcule l'angle de tir en degrés"""
        # Points du but (coordonnées approximatives)
        but_gauche_y = 44  # Poteau gauche
        but_droit_y = 56   # Poteau droit
        but_x = 100        # Ligne de but
        
        # Angles vers chaque poteau
        angle_gauche = math.atan2(abs(y - but_gauche_y), abs(x - but_x))
        angle_droit = math.atan2(abs(y - but_droit_y), abs(x - but_x))
        
        # Angle de tir = différence entre les deux angles
        angle_tir = abs(angle_gauche - angle_droit)
        
        return math.degrees(angle_tir)
    
    def _obtenir_bonus_finisseur(self, nom_joueur: str) -> float:
        """Retourne un bonus pour les finisseurs reconnus du RCS"""
        finisseurs_rcs = {
            'Emanuel Emegha': 1.15,
            'Dilane Bakwa': 1.10,
            'Félix Lemaréchal': 1.05,
            'Sékou Mara': 1.08
        }
        return finisseurs_rcs.get(nom_joueur, 1.0)
    
    def _obtenir_bonus_createur(self, nom_joueur: str) -> float:
        """Retourne un bonus pour les créateurs reconnus du RCS"""
        createurs_rcs = {
            'Dilane Bakwa': 1.20,
            'Andrey Santos': 1.15,
            'Félix Lemaréchal': 1.12,
            'Habib Diarra': 1.08
        }
        return createurs_rcs.get(nom_joueur, 1.0)
    
    def _evaluer_style_possession(self, passes_par_zone: Dict, precision: float) -> str:
        """Évalue le style de possession de l'équipe"""
        total_passes = sum(passes_par_zone.values())
        
        if total_passes == 0:
            return "Données insuffisantes"
        
        pct_offensive = passes_par_zone['zone_offensive'] / total_passes * 100
        pct_defensive = passes_par_zone['zone_defensive'] / total_passes * 100
        
        if pct_offensive > 35 and precision > 85:
            return "Possession offensive - Construction élaborée"
        elif pct_offensive > 30:
            return "Jeu vers l'avant - Style direct"
        elif pct_defensive > 40:
            return "Jeu de conservation - Construction prudente"
        else:
            return "Jeu équilibré - Style hybride"
    
    def _identifier_zone_activite(self, x_moyen: float, y_moyen: float) -> str:
        """Identifie la zone principale d'activité d'un joueur"""
        if x_moyen <= 25:
            return "Défenseur central/Gardien"
        elif x_moyen <= 35:
            return "Défense"
        elif x_moyen <= 50:
            return "Milieu défensif"
        elif x_moyen <= 65:
            return "Milieu offensif"
        elif x_moyen <= 80:
            return "Attaque"
        else:
            return "Avant-centre/Finisseur"
    
    def _interpreter_heatmap(self, zone: str, mobilite: float) -> str:
        """Interprète la heatmap d'un joueur"""
        if mobilite > 25:
            type_mobilite = "Très mobile"
        elif mobilite > 15:
            type_mobilite = "Mobile"
        else:
            type_mobilite = "Statique"
        
        return f"{type_mobilite} - Zone principale: {zone}"
    
    def _evaluer_performance_defensive(self, 
                                     taux_tacles: float, 
                                     taux_duels: float, 
                                     intensite: Dict) -> str:
        """Évalue la performance défensive globale"""
        
        score_efficacite = (taux_tacles + taux_duels) / 2
        score_intensite = sum(intensite.values())
        
        if score_efficacite > 70 and score_intensite > 50:
            return "🟢 Excellente - Efficace et intense"
        elif score_efficacite > 60 and score_intensite > 30:
            return "🟡 Bonne - Performance solide"
        elif score_efficacite > 50:
            return "🟡 Correcte - Peut mieux faire en intensité"
        else:
            return "🔴 Problématique - Amélioration nécessaire"

def main():
    """Fonction principale pour tester les métriques"""
    print("🔵⚪ Métriques Football Racing Club de Strasbourg")
    print("=" * 55)
    
    # Initialisation
    metriques = MetriquesFootballRCS()
    
    # Test xG
    print("\n⚽ Test calcul xG:")
    xg_emegha = metriques.calculer_xg_tir(
        x_coordonnee=85, 
        y_coordonnee=48,
        situation="contre_attaque",
        partie_corps="pied_droit",
        joueur_tireur="Emanuel Emegha"
    )
    print(f"xG Emegha (tir surface contre-attaque): {xg_emegha:.3f}")
    
    # Test xA
    print("\n🎯 Test calcul xA:")
    xa_bakwa = metriques.calculer_xa_passe(
        x_passe=70, y_passe=25,
        x_reception=88, y_reception=45,
        type_passe="passe_cle",
        joueur_passeur="Dilane Bakwa"
    )
    print(f"xA Bakwa (passe décisive): {xa_bakwa:.3f}")
    
    # Test données simulées
    print("\n📊 Test avec données simulées:")
    
    # Simulation d'événements de match
    np.random.seed(42)
    evenements_simules = pd.DataFrame({
        'equipe': ['RCS'] * 100 + ['Adversaire'] * 80,
        'type_evenement': np.random.choice(['passe', 'tacle', 'interception'], 180),
        'x_coordonnee': np.random.uniform(0, 100, 180),
        'y_coordonnee': np.random.uniform(0, 100, 180),
        'minute': np.random.randint(1, 90, 180),
        'reussi': np.random.choice([True, False], 180, p=[0.7, 0.3])
    })
    
    # Test PPDA
    ppda = metriques.calculer_ppda_equipe(evenements_simules)
    print(f"PPDA RCS: {ppda}")
    
    # Test métriques possession
    possession = metriques.calculer_metriques_possession(evenements_simules)
    print(f"Précision passes: {possession['precision_passes_pct']}%")
    print(f"Style possession: {possession['style_possession']}")

if __name__ == "__main__":
    main()
