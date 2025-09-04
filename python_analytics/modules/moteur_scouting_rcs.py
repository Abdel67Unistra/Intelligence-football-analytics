"""
Moteur de Recrutement Racing Club de Strasbourg
==============================================

Système de scouting intelligent adapté aux besoins et au budget du RCS.
Focus sur la détection de jeunes talents et les opportunités du marché français.

Auteur: Football Analytics Platform
Équipe: Racing Club de Strasbourg
"""

import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
import streamlit as st
from typing import Dict, List, Optional
import json

class MoteurScoutingRCS:
    """Moteur de recrutement spécialisé pour le Racing Club de Strasbourg"""
    
    def __init__(self):
        """Initialise le moteur avec les paramètres du RCS"""
        self.budget_transfert_max = 15_000_000  # 15M€ max par joueur
        self.budget_salaire_max = 80_000  # 80k€/mois max
        self.age_cible_min = 16
        self.age_cible_max = 28
        self.ligues_prioritaires = [
            "Ligue 1", "Ligue 2", "Bundesliga 2", "Championship", 
            "Eredivisie", "Jupiler Pro League", "Liga Portugal"
        ]
        self.nationalites_prioritaires = [
            "France", "Allemagne", "Belgique", "Pays-Bas", 
            "Portugal", "Maroc", "Algérie", "Sénégal"
        ]
        
    def generer_base_donnees_scouting(self) -> pd.DataFrame:
        """
        Génère une base de données réaliste de joueurs potentiels pour le RCS
        
        Returns:
            DataFrame avec les profils des joueurs scoutés
        """
        np.random.seed(42)
        
        # Joueurs réels ciblés ou suivis par des clubs similaires au RCS
        profils_joueurs = []
        
        # Jeunes talents Ligue 2 et National
        talents_france = [
            {"nom": "Yanis Massolin", "club": "Paris FC", "age": 20, "poste": "MC", "ligue": "Ligue 2", "nationalite": "France"},
            {"nom": "Quentin Boisgard", "club": "Laval", "age": 25, "poste": "MOC", "ligue": "Ligue 2", "nationalite": "France"},
            {"nom": "Enzo Bardeli", "club": "Guingamp", "age": 22, "poste": "AD", "ligue": "Ligue 2", "nationalite": "France"},
            {"nom": "Maxime Do Couto", "club": "Rodez", "age": 23, "poste": "DC", "ligue": "Ligue 2", "nationalite": "France"},
            {"nom": "Lorenzo Rajot", "club": "Troyes", "age": 21, "poste": "MDC", "ligue": "Ligue 2", "nationalite": "France"},
            
            # Talents Championnat belge (marché accessible)
            {"nom": "Nelson Mandela", "club": "Charleroi", "age": 19, "poste": "BU", "ligue": "Jupiler Pro League", "nationalite": "Belgique"},
            {"nom": "Theo Leoni", "club": "Genk", "age": 20, "poste": "MC", "ligue": "Jupiler Pro League", "nationalite": "Belgique"},
            {"nom": "Marco Kana", "club": "Anderlecht", "age": 21, "poste": "MDC", "ligue": "Jupiler Pro League", "nationalite": "Belgique"},
            
            # Talents portugais (bonne école technique)
            {"nom": "Gustavo Sá", "club": "Famalicão", "age": 22, "poste": "MOC", "ligue": "Liga Portugal", "nationalite": "Portugal"},
            {"nom": "João Silva", "club": "Rio Ave", "age": 20, "poste": "DD", "ligue": "Liga Portugal", "nationalite": "Portugal"},
            
            # Talents Championship (expérience physique)
            {"nom": "Tyler Adams", "club": "Luton Town", "age": 24, "poste": "MDC", "ligue": "Championship", "nationalite": "États-Unis"},
            {"nom": "Abdoullah Ba", "club": "Cardiff City", "age": 23, "poste": "AD", "ligue": "Championship", "nationalite": "Sénégal"},
            
            # Pépites Eredivisie
            {"nom": "Kian Fitz-Jim", "club": "Ajax", "age": 21, "poste": "MC", "ligue": "Eredivisie", "nationalite": "Pays-Bas"},
            {"nom": "Million Manhoef", "club": "Vitesse", "age": 22, "poste": "AD", "ligue": "Eredivisie", "nationalite": "Pays-Bas"},
        ]
        
        for joueur in talents_france:
            # Générer des statistiques réalistes selon le poste et l'âge
            stats = self._generer_statistiques_joueur(
                joueur["poste"], 
                joueur["age"], 
                joueur["ligue"]
            )
            
            # Valeur marchande selon l'âge, poste et championnat
            valeur_base = self._calculer_valeur_marche(
                joueur["age"], 
                joueur["poste"], 
                joueur["ligue"], 
                stats["note_globale"]
            )
            
            profil_complet = {
                **joueur,
                **stats,
                "valeur_marche_millions": valeur_base,
                "salaire_mensuel_k": valeur_base * 3.5,  # Ratio réaliste
                "potentiel": self._evaluer_potentiel(joueur["age"], stats["note_globale"]),
                "adaptabilite_rcs": self._evaluer_adaptabilite_rcs(joueur, stats),
                "urgence_recrutement": np.random.choice(["Faible", "Modérée", "Élevée"], p=[0.5, 0.3, 0.2])
            }
            
            profils_joueurs.append(profil_complet)
        
        return pd.DataFrame(profils_joueurs)
    
    def _generer_statistiques_joueur(self, poste: str, age: int, ligue: str) -> Dict:
        """Génère des statistiques réalistes selon le poste"""
        
        # Bonus selon le niveau de la ligue
        bonus_ligue = {
            "Ligue 1": 1.1,
            "Ligue 2": 0.95,
            "Bundesliga 2": 1.0,
            "Championship": 1.05,
            "Eredivisie": 1.08,
            "Jupiler Pro League": 0.98,
            "Liga Portugal": 1.02
        }.get(ligue, 1.0)
        
        # Bonus selon l'âge (pic vers 25-27 ans)
        bonus_age = 1 - abs(age - 26) * 0.02
        bonus_age = max(0.8, bonus_age)
        
        if poste == "GB":
            stats_base = {
                "arrets_par_match": np.random.normal(3.8, 1.2) * bonus_ligue,
                "clean_sheets_pct": np.random.normal(32, 8),
                "sorties_aeriennes": np.random.normal(1.8, 0.6),
                "precision_relances": np.random.normal(65, 12)
            }
        elif poste in ["DC", "DD", "DG"]:
            stats_base = {
                "tacles_par_match": np.random.normal(2.1, 0.8) * bonus_ligue,
                "interceptions_par_match": np.random.normal(1.6, 0.6) * bonus_ligue,
                "duels_aeriens_pct": np.random.normal(62, 15),
                "precision_passes": np.random.normal(86, 6),
                "centres_reussis": np.random.normal(0.8, 0.4) if poste in ["DD", "DG"] else 0.2
            }
        elif poste in ["MDC", "MC", "MOC"]:
            stats_base = {
                "passes_par_match": np.random.normal(58, 18) * bonus_ligue,
                "precision_passes": np.random.normal(88, 5),
                "passes_cles_par_match": np.random.normal(1.4, 0.8) * bonus_ligue,
                "tacles_par_match": np.random.normal(1.8, 0.7),
                "km_parcourus": np.random.normal(11.2, 1.1)
            }
        else:  # Attaquants
            stats_base = {
                "buts_par_match": np.random.normal(0.42, 0.25) * bonus_ligue * bonus_age,
                "passes_decisives_par_match": np.random.normal(0.18, 0.12) * bonus_ligue,
                "tirs_par_match": np.random.normal(2.8, 1.2),
                "dribbles_reussis_pct": np.random.normal(58, 12),
                "vitesse_pointe": np.random.normal(32.5, 2.1)
            }
        
        # Note globale selon les statistiques et bonus
        note_technique = np.random.normal(7.2, 1.1) * bonus_ligue * bonus_age
        note_physique = np.random.normal(7.0, 0.9) * (1 + (28 - age) * 0.02)  # Déclin physique
        note_mental = np.random.normal(7.1, 1.0) * (1 + (age - 20) * 0.01)    # Expérience
        
        note_globale = (note_technique + note_physique + note_mental) / 3
        note_globale = np.clip(note_globale, 5.5, 9.0)
        
        return {
            **stats_base,
            "note_globale": round(note_globale, 1),
            "note_technique": round(note_technique, 1),
            "note_physique": round(note_physique, 1),
            "note_mental": round(note_mental, 1)
        }
    
    def _calculer_valeur_marche(self, age: int, poste: str, ligue: str, note_globale: float) -> float:
        """Calcule une valeur marchande réaliste"""
        
        # Valeur de base selon la note
        valeur_base = (note_globale - 5) * 2.5  # 5.5 = 1.25M, 9.0 = 10M
        
        # Multiplicateur selon le poste
        mult_poste = {
            "BU": 1.4, "MOC": 1.2, "MC": 1.1, "AD": 1.15, "AG": 1.15,
            "MDC": 1.0, "DD": 0.9, "DG": 0.9, "DC": 0.95, "GB": 0.8
        }.get(poste, 1.0)
        
        # Multiplicateur selon l'âge (pic vers 24-26 ans)
        if age <= 20:
            mult_age = 0.7 + age * 0.05  # Potentiel mais inexpérimenté
        elif age <= 26:
            mult_age = 1.0 + (26 - age) * 0.02
        else:
            mult_age = 1.0 - (age - 26) * 0.08  # Déclin de valeur
        
        # Multiplicateur selon la ligue
        mult_ligue = {
            "Ligue 1": 1.0,
            "Ligue 2": 0.6,
            "Championship": 0.8,
            "Eredivisie": 0.85,
            "Jupiler Pro League": 0.7,
            "Liga Portugal": 0.75,
            "Bundesliga 2": 0.7
        }.get(ligue, 0.6)
        
        valeur_finale = valeur_base * mult_poste * mult_age * mult_ligue
        return round(max(0.5, min(25.0, valeur_finale)), 1)  # Entre 0.5M et 25M
    
    def _evaluer_potentiel(self, age: int, note_actuelle: float) -> str:
        """Évalue le potentiel d'évolution du joueur"""
        
        if age <= 20:
            if note_actuelle >= 7.5:
                return "⭐⭐⭐ Très haut potentiel"
            elif note_actuelle >= 7.0:
                return "⭐⭐ Potentiel élevé"
            else:
                return "⭐ Potentiel moyen"
        elif age <= 24:
            if note_actuelle >= 8.0:
                return "⭐⭐ Potentiel confirmé"
            else:
                return "⭐ Marge de progression"
        else:
            return "🔄 Joueur expérimenté"
    
    def _evaluer_adaptabilite_rcs(self, joueur: Dict, stats: Dict) -> float:
        """Évalue l'adaptabilité du joueur au projet RCS"""
        
        score_adaptabilite = 0.0
        
        # Bonus nationalité
        if joueur["nationalite"] in self.nationalites_prioritaires:
            score_adaptabilite += 0.15
        
        # Bonus âge (préférence jeunes)
        if joueur["age"] <= 23:
            score_adaptabilite += 0.2
        elif joueur["age"] <= 26:
            score_adaptabilite += 0.1
        
        # Bonus ligue connue
        if joueur["ligue"] in self.ligues_prioritaires:
            score_adaptabilite += 0.1
        
        # Bonus selon les stats (style de jeu RCS)
        if joueur["poste"] in ["MC", "MDC"]:
            # RCS privilégie les milieux combatifs
            if stats.get("tacles_par_match", 0) > 2.0:
                score_adaptabilite += 0.15
        elif joueur["poste"] in ["AD", "AG", "BU"]:
            # RCS aime les joueurs rapides et efficaces
            if stats.get("vitesse_pointe", 30) > 32:
                score_adaptabilite += 0.1
            if stats.get("buts_par_match", 0) > 0.4:
                score_adaptabilite += 0.15
        
        # Bonus mental (important pour l'adaptation)
        if stats.get("note_mental", 6) >= 7.5:
            score_adaptabilite += 0.1
        
        return round(min(1.0, max(0.0, score_adaptabilite)), 2)
    
    def rechercher_cibles_prioritaires(self, 
                                     poste_recherche: str = None, 
                                     budget_max: float = None) -> pd.DataFrame:
        """
        Recherche les cibles prioritaires selon les critères du RCS
        
        Args:
            poste_recherche: Poste recherché (optionnel)
            budget_max: Budget maximum (défaut: budget du club)
            
        Returns:
            DataFrame trié par pertinence pour le RCS
        """
        base_scouting = self.generer_base_donnees_scouting()
        
        if budget_max is None:
            budget_max = self.budget_transfert_max
        
        # Filtres de base
        candidats = base_scouting[
            (base_scouting['age'] >= self.age_cible_min) &
            (base_scouting['age'] <= self.age_cible_max) &
            (base_scouting['valeur_marche_millions'] <= budget_max)
        ].copy()
        
        # Filtre par poste si spécifié
        if poste_recherche:
            candidats = candidats[candidats['poste'] == poste_recherche]
        
        # Score de pertinence RCS
        candidats['score_rcs'] = (
            candidats['note_globale'] * 0.3 +
            candidats['adaptabilite_rcs'] * 10 * 0.25 +
            (10 - candidats['valeur_marche_millions']) * 0.1 * 0.2 +  # Bonus petit budget
            candidats['potentiel'].str.count('⭐') * 0.15 +
            (candidats['urgence_recrutement'] == 'Élevée').astype(int) * 0.1
        )
        
        # Trier par score décroissant
        return candidats.sort_values('score_rcs', ascending=False)
    
    def analyser_opportunite_transfert(self, nom_joueur: str) -> Dict:
        """
        Analyse détaillée d'une opportunité de transfert
        
        Args:
            nom_joueur: Nom du joueur à analyser
            
        Returns:
            Dictionnaire avec l'analyse complète
        """
        base_scouting = self.generer_base_donnees_scouting()
        joueur_data = base_scouting[base_scouting['nom'] == nom_joueur]
        
        if joueur_data.empty:
            return {"erreur": f"Joueur '{nom_joueur}' non trouvé dans la base de données"}
        
        joueur = joueur_data.iloc[0]
        
        # Analyse financière
        cout_transfert = joueur['valeur_marche_millions']
        cout_salaire_annuel = joueur['salaire_mensuel_k'] * 12
        cout_total_3ans = cout_transfert + (cout_salaire_annuel * 3 / 1000)  # En millions
        
        # Analyse des risques
        risques = self._identifier_risques_transfert(joueur)
        avantages = self._identifier_avantages_transfert(joueur)
        
        # Recommandation finale
        if cout_transfert <= self.budget_transfert_max * 0.5:
            niveau_recommandation = "🟢 Fortement recommandé"
        elif cout_transfert <= self.budget_transfert_max * 0.8:
            niveau_recommandation = "🟡 Recommandé avec conditions"
        else:
            niveau_recommandation = "🔴 Trop cher pour le budget"
        
        return {
            "joueur": {
                "nom": joueur['nom'],
                "age": joueur['age'],
                "poste": joueur['poste'],
                "club_actuel": joueur['club'],
                "nationalite": joueur['nationalite']
            },
            "evaluation_sportive": {
                "note_globale": joueur['note_globale'],
                "potentiel": joueur['potentiel'],
                "adaptabilite_rcs": joueur['adaptabilite_rcs'],
                "score_priorite": round(joueur['score_rcs'], 2)
            },
            "analyse_financiere": {
                "valeur_marche": f"{cout_transfert:.1f}M€",
                "salaire_annuel": f"{cout_salaire_annuel:.0f}k€",
                "cout_total_3ans": f"{cout_total_3ans:.1f}M€",
                "pct_budget_utilise": f"{(cout_transfert/self.budget_transfert_max)*100:.1f}%"
            },
            "risques": risques,
            "avantages": avantages,
            "recommandation": niveau_recommandation,
            "actions_suivantes": self._generer_actions_suivantes(joueur, niveau_recommandation)
        }
    
    def _identifier_risques_transfert(self, joueur: pd.Series) -> List[str]:
        """Identifie les risques spécifiques à un transfert"""
        risques = []
        
        # Risque âge
        if joueur['age'] >= 28:
            risques.append("⚠️ Âge élevé - Risque de déclin rapide")
        elif joueur['age'] <= 19:
            risques.append("⚠️ Très jeune - Adaptation incertaine en Ligue 1")
        
        # Risque financier
        if joueur['valeur_marche_millions'] > self.budget_transfert_max * 0.7:
            risques.append("💰 Investissement important - Peu de marge d'erreur")
        
        # Risque adaptation
        if joueur['nationalite'] not in self.nationalites_prioritaires:
            risques.append("🌍 Nationalité exotique - Adaptation culturelle à prévoir")
        
        # Risque concurrence
        if joueur['urgence_recrutement'] == 'Élevée':
            risques.append("🏃 Urgence élevée - Concurrence d'autres clubs")
        
        # Risque niveau
        if joueur['ligue'] not in ["Ligue 1", "Eredivisie", "Championship"]:
            risques.append("📈 Changement de niveau - Performance incertaine")
        
        return risques
    
    def _identifier_avantages_transfert(self, joueur: pd.Series) -> List[str]:
        """Identifie les avantages spécifiques à un transfert"""
        avantages = []
        
        # Avantage âge
        if 20 <= joueur['age'] <= 25:
            avantages.append("🎯 Âge optimal - Pic de performance et revente possible")
        
        # Avantage financier
        if joueur['valeur_marche_millions'] <= self.budget_transfert_max * 0.4:
            avantages.append("💎 Bon rapport qualité-prix - Faible risque financier")
        
        # Avantage adaptation
        if joueur['adaptabilite_rcs'] >= 0.6:
            avantages.append("🎯 Profil adapté au projet RCS")
        
        # Avantage technique
        if joueur['note_globale'] >= 7.8:
            avantages.append("⭐ Niveau technique élevé - Apport immédiat")
        
        # Avantage potentiel
        if "⭐⭐⭐" in joueur['potentiel'] or "⭐⭐" in joueur['potentiel']:
            avantages.append("🚀 Fort potentiel - Plus-value à terme")
        
        return avantages
    
    def _generer_actions_suivantes(self, joueur: pd.Series, recommandation: str) -> List[str]:
        """Génère la liste des actions à mener pour ce joueur"""
        
        if "Fortement recommandé" in recommandation:
            return [
                "📞 Contacter l'agent pour connaître les conditions",
                "🎥 Organiser observation en live sur 3 matchs minimum",
                "📋 Réaliser entretien avec le joueur",
                "🏥 Prévoir visite médicale approfondie",
                "💼 Préparer offre officielle"
            ]
        elif "Recommandé avec conditions" in recommandation:
            return [
                "🎥 Observation renforcée sur 5 matchs",
                "📊 Analyse comparative avec alternatives",
                "💰 Négociation prix avec agent",
                "🤝 Validation accord avec staff technique",
                "⏰ Suivre évolution marché"
            ]
        else:
            return [
                "👀 Surveillance passive de l'évolution",
                "💰 Attendre baisse de prix potentielle",
                "🔍 Chercher alternatives moins chères",
                "📅 Réévaluer dans 6 mois"
            ]

def main():
    """Fonction principale pour tester le moteur de scouting"""
    moteur = MoteurScoutingRCS()
    
    print("🔵⚪ Moteur de Scouting Racing Club de Strasbourg")
    print("=" * 55)
    
    # Test base de données
    base_scouting = moteur.generer_base_donnees_scouting()
    print(f"\n📊 Base de données: {len(base_scouting)} joueurs référencés")
    
    # Top 5 cibles toutes positions
    print(f"\n🎯 Top 5 cibles prioritaires RCS:")
    top_cibles = moteur.rechercher_cibles_prioritaires().head()
    for _, joueur in top_cibles.iterrows():
        print(f"• {joueur['nom']} ({joueur['age']}ans, {joueur['poste']}) - "
              f"{joueur['club']} - {joueur['valeur_marche_millions']}M€ - "
              f"Score: {joueur['score_rcs']:.2f}")
    
    # Analyse détaillée d'un joueur
    print(f"\n🔍 Analyse détaillée - Yanis Massolin:")
    analyse = moteur.analyser_opportunite_transfert("Yanis Massolin")
    if "erreur" not in analyse:
        print(f"Note globale: {analyse['evaluation_sportive']['note_globale']}")
        print(f"Valeur: {analyse['analyse_financiere']['valeur_marche']}")
        print(f"Recommandation: {analyse['recommandation']}")
        print(f"Principaux avantages: {len(analyse['avantages'])} identifiés")

if __name__ == "__main__":
    main()
