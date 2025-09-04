#!/usr/bin/env python3
"""
Dashboard RCS Simplifié
=====================

Version allégée du dashboard RCS pour tests et démonstrations
Sans dépendances complexes - Fonctionne partout
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class AnalyseurRCSSimple:
    """Version simplifiée de l'analyseur RCS"""
    
    def __init__(self):
        self.effectif_rcs = self._charger_effectif()
    
    def _charger_effectif(self):
        """Charge l'effectif actuel du RCS"""
        effectif_data = [
            # Gardiens
            {"nom": "Matz Sels", "age": 32, "poste": "GB", "valeur_marche": 4.0, "titulaire": True},
            {"nom": "Alaa Bellaarouch", "age": 20, "poste": "GB", "valeur_marche": 0.5, "titulaire": False},
            
            # Défenseurs
            {"nom": "Guela Doué", "age": 22, "poste": "DD", "valeur_marche": 8.0, "titulaire": True},
            {"nom": "Abakar Sylla", "age": 25, "poste": "DC", "valeur_marche": 3.5, "titulaire": True},
            {"nom": "Saïdou Sow", "age": 22, "poste": "DC", "valeur_marche": 4.0, "titulaire": True},
            {"nom": "Mamadou Sarr", "age": 26, "poste": "DG", "valeur_marche": 3.0, "titulaire": True},
            {"nom": "Marvin Senaya", "age": 22, "poste": "DD", "valeur_marche": 2.5, "titulaire": False},
            {"nom": "Ismaël Doukouré", "age": 23, "poste": "DC", "valeur_marche": 2.0, "titulaire": False},
            
            # Milieux
            {"nom": "Habib Diarra", "age": 20, "poste": "MC", "valeur_marche": 12.0, "titulaire": True},
            {"nom": "Andrey Santos", "age": 20, "poste": "MDC", "valeur_marche": 8.0, "titulaire": True},
            {"nom": "Dilane Bakwa", "age": 21, "poste": "AD", "valeur_marche": 10.0, "titulaire": True},
            {"nom": "Sebastian Nanasi", "age": 22, "poste": "AG", "valeur_marche": 6.0, "titulaire": True},
            {"nom": "Caleb Wiley", "age": 19, "poste": "DG", "valeur_marche": 4.0, "titulaire": False},
            {"nom": "Pape Diong", "age": 20, "poste": "MC", "valeur_marche": 1.5, "titulaire": False},
            
            # Attaquants
            {"nom": "Emanuel Emegha", "age": 21, "poste": "BU", "valeur_marche": 8.0, "titulaire": True},
            {"nom": "Félix Lemaréchal", "age": 19, "poste": "MOC", "valeur_marche": 4.0, "titulaire": False},
            {"nom": "Abdoul Ouattara", "age": 18, "poste": "AD", "valeur_marche": 2.0, "titulaire": False},
            {"nom": "Moïse Sahi", "age": 18, "poste": "BU", "valeur_marche": 1.0, "titulaire": False},
            {"nom": "Jeremy Sebas", "age": 19, "poste": "BU", "valeur_marche": 0.8, "titulaire": False}
        ]
        
        return pd.DataFrame(effectif_data)
    
    def obtenir_effectif_actuel(self):
        """Retourne l'effectif actuel"""
        return self.effectif_rcs
    
    def analyser_forme_joueur_rcs(self, nom_joueur):
        """Analyse la forme d'un joueur"""
        joueur = self.effectif_rcs[self.effectif_rcs['nom'] == nom_joueur]
        
        if joueur.empty:
            return {"erreur": f"Joueur {nom_joueur} non trouvé"}
        
        # Simulation analyse forme
        forme_score = np.random.uniform(6.0, 8.5)
        tendance = "excellente" if forme_score > 8.0 else "bonne" if forme_score > 7.0 else "correcte"
        
        return {
            "joueur": nom_joueur,
            "note_forme": round(forme_score, 1),
            "tendance_forme": tendance,
            "matches_recents": 5,
            "progression": "+15%" if forme_score > 7.5 else "+5%"
        }
    
    def projeter_composition_ideale(self):
        """Projette la composition idéale en 4-2-3-1"""
        titulaires = self.effectif_rcs[self.effectif_rcs['titulaire'] == True]
        
        composition = {
            "formation": "4-2-3-1",
            "gardien": titulaires[titulaires['poste'] == 'GB'].iloc[0]['nom'],
            "defenseurs": titulaires[titulaires['poste'].isin(['DD', 'DC', 'DG'])]['nom'].tolist()[:4],
            "milieux_defensifs": titulaires[titulaires['poste'].isin(['MDC', 'MC'])]['nom'].tolist()[:2],
            "milieux_offensifs": titulaires[titulaires['poste'].isin(['AD', 'AG', 'MOC'])]['nom'].tolist()[:3],
            "attaquant": titulaires[titulaires['poste'] == 'BU'].iloc[0]['nom']
        }
        
        return composition

class MetriquesRCSSimple:
    """Version simplifiée des métriques RCS"""
    
    def __init__(self):
        self.bonus_finisseurs = {
            "Emanuel Emegha": 1.15,
            "Dilane Bakwa": 1.10,
            "Habib Diarra": 1.08
        }
    
    def calculer_xg_tir(self, x, y, type_action, pied, joueur):
        """Calcule l'Expected Goals d'un tir"""
        # Distance du but
        distance = np.sqrt((100-x)**2 + (50-y)**2)
        
        # xG de base selon distance
        xg_base = max(0.05, 1.0 - (distance / 100))
        
        # Bonus type d'action
        if type_action == "contre_attaque":
            xg_base *= 1.35
        elif type_action == "coup_franc":
            xg_base *= 0.8
        
        # Bonus joueur
        if joueur in self.bonus_finisseurs:
            xg_base *= self.bonus_finisseurs[joueur]
        
        return min(0.95, xg_base)
    
    def calculer_ppda_equipe(self, passes_adverses, actions_defensives):
        """Calcule les Passes per Defensive Action"""
        return round(passes_adverses / actions_defensives, 2)

def afficher_dashboard_console():
    """Affiche le dashboard dans la console"""
    
    print("🔵⚪ RACING CLUB DE STRASBOURG - Analytics Platform")
    print("=" * 65)
    
    # Initialisation
    analyseur = AnalyseurRCSSimple()
    metriques = MetriquesRCSSimple()
    
    # Section 1: Effectif
    print("\n👥 EFFECTIF ACTUEL 2024-2025")
    print("-" * 35)
    
    effectif = analyseur.obtenir_effectif_actuel()
    
    # Stats par poste
    gardiens = effectif[effectif['poste'] == 'GB']
    defenseurs = effectif[effectif['poste'].isin(['DD', 'DC', 'DG'])]
    milieux = effectif[effectif['poste'].isin(['MDC', 'MC', 'MOC', 'AD', 'AG'])]
    attaquants = effectif[effectif['poste'].isin(['BU'])]
    
    print(f"📊 Gardiens: {len(gardiens)} | Défenseurs: {len(defenseurs)} | Milieux: {len(milieux)} | Attaquants: {len(attaquants)}")
    print(f"💰 Valeur totale effectif: {effectif['valeur_marche'].sum():.1f}M€")
    print(f"📈 Âge moyen: {effectif['age'].mean():.1f} ans")
    
    # Section 2: Top Joueurs
    print("\n⭐ TOP JOUEURS (VALEUR MARCHANDE)")
    print("-" * 40)
    
    top_joueurs = effectif.nlargest(5, 'valeur_marche')[['nom', 'poste', 'valeur_marche', 'age']]
    for _, joueur in top_joueurs.iterrows():
        print(f"  {joueur['nom']:<20} {joueur['poste']:<5} {joueur['valeur_marche']:>4.1f}M€ ({joueur['age']}ans)")
    
    # Section 3: Composition Idéale
    print("\n🎯 COMPOSITION IDÉALE (4-2-3-1)")
    print("-" * 35)
    
    compo = analyseur.projeter_composition_ideale()
    print(f"🥅 Gardien: {compo['gardien']}")
    print(f"🛡️  Défense: {' - '.join(compo['defenseurs'])}")
    print(f"⚙️  Milieu défensif: {' - '.join(compo['milieux_defensifs'])}")
    print(f"🎨 Milieu offensif: {' - '.join(compo['milieux_offensifs'])}")
    print(f"⚽ Attaque: {compo['attaquant']}")
    
    # Section 4: Analyses Forme
    print("\n📈 ANALYSE FORME JOUEURS CLÉS")
    print("-" * 35)
    
    joueurs_cles = ["Emanuel Emegha", "Habib Diarra", "Dilane Bakwa", "Matz Sels"]
    for joueur in joueurs_cles:
        forme = analyseur.analyser_forme_joueur_rcs(joueur)
        if "erreur" not in forme:
            print(f"  {forme['joueur']:<18} Note: {forme['note_forme']}/10 | Forme: {forme['tendance_forme']}")
    
    # Section 5: Métriques Exemple
    print("\n⚽ MÉTRIQUES FOOTBALL (EXEMPLES)")
    print("-" * 35)
    
    # xG Emanuel Emegha (tir surface contre-attaque)
    xg_emegha = metriques.calculer_xg_tir(85, 50, "contre_attaque", "pied_droit", "Emanuel Emegha")
    print(f"🎯 xG tir Emegha (surface, contre-attaque): {xg_emegha:.3f}")
    
    # xG Dilane Bakwa (tir extérieur)
    xg_bakwa = metriques.calculer_xg_tir(75, 30, "jeu_place", "pied_gauche", "Dilane Bakwa")
    print(f"🎯 xG tir Bakwa (20m, pied gauche): {xg_bakwa:.3f}")
    
    # PPDA équipe (style pressing RCS)
    ppda = metriques.calculer_ppda_equipe(450, 42)
    print(f"📊 PPDA équipe (pressing coordonné): {ppda}")
    
    # Section 6: Objectifs Saison
    print("\n🎯 OBJECTIFS SAISON 2024-2025")
    print("-" * 35)
    print("  📍 Classement: Maintien confortable (14e-17e)")
    print("  ⚽ Buts marqués: 45+ (amélioration finition)")
    print("  🛡️  Buts encaissés: <55 (solidité défensive)")
    print("  👥 Jeunes: Intégration 3+ talents centre formation")
    print("  💰 Budget: Optimisation masse salariale")
    
    print("\n" + "=" * 65)
    print("🔵⚪ Racing Club de Strasbourg - Intelligence Football")
    print("📱 Version complète: http://localhost:8502")

if __name__ == "__main__":
    afficher_dashboard_console()
