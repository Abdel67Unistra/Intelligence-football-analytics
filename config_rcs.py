"""
🔵⚪ Racing Club de Strasbourg - Configuration Principale
=======================================================

Configuration globale et constantes pour la plateforme d'analytics RCS.

Auteur: GitHub Copilot  
Date: Septembre 2025
"""

import os
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, List, Tuple

# ========================================================================================
# CONFIGURATION RACING CLUB DE STRASBOURG
# ========================================================================================

@dataclass
class ConfigurationRCS:
    """Configuration principale du Racing Club de Strasbourg"""
    
    # Informations club
    nom_club: str = "Racing Club de Strasbourg"
    nom_court: str = "RCS"
    ville: str = "Strasbourg"
    stade: str = "Stade de la Meinau"
    capacite_stade: int = 26109
    
    # Couleurs officielles
    couleur_primaire: str = "#0066CC"  # Bleu RCS
    couleur_secondaire: str = "#FFFFFF"  # Blanc
    couleur_accent: str = "#FF6B35"  # Orange accent
    
    # Saison actuelle
    saison: str = "2024-2025"
    competition_principale: str = "Ligue 1"
    
    # Objectifs sportifs
    objectif_classement: str = "Maintien confortable (8ème-14ème place)"
    objectif_points: int = 45
    objectif_buts_marques: int = 45
    objectif_buts_encaisses: int = 55
    
    # Budget et contraintes
    budget_transfert_max: float = 15.0  # Millions d'euros
    salaire_max: float = 80000  # Euros par mois
    age_cible_recrutement: Tuple[int, int] = (18, 28)
    
    # Style de jeu
    formation_principale: str = "4-2-3-1"
    style_jeu: str = "Contre-attaque rapide et pressing coordonné"
    possession_cible: float = 47.0  # Pourcentage
    
    # Métriques personnalisées
    bonus_xg_contre_attaque: float = 0.35
    ppda_cible: Tuple[float, float] = (8.0, 12.0)
    
    # Ligues de scouting prioritaires
    ligues_scouting: List[str] = [
        "Ligue 2", "Championship", "Eredivisie", 
        "2. Bundesliga", "Serie B", "Segunda División"
    ]

# Configuration des chemins
class CheminsProjet:
    """Chemins et répertoires du projet"""
    
    BASE_DIR = Path(__file__).parent
    
    # Répertoires principaux
    SRC_DIR = BASE_DIR / "src"
    DATA_DIR = BASE_DIR / "data"
    ANALYTICS_DIR = BASE_DIR / "python_analytics"
    R_ANALYTICS_DIR = BASE_DIR / "r_analytics"
    DOCS_DIR = BASE_DIR / "docs"
    TESTS_DIR = BASE_DIR / "tests"
    WEB_DIR = BASE_DIR / "web"
    
    # Fichiers de données
    EFFECTIF_RCS = DATA_DIR / "effectif_rcs_2024_2025.json"
    RESULTATS_MATCHS = DATA_DIR / "resultats_matchs_rcs.json"
    METRIQUES_JOUEURS = DATA_DIR / "metriques_joueurs_rcs.json"
    BASE_SCOUTING = DATA_DIR / "base_scouting_rcs.json"
    
    # Sorties et rapports
    RAPPORTS_DIR = BASE_DIR / "rapports"
    GRAPHIQUES_DIR = BASE_DIR / "graphiques"
    EXPORTS_DIR = BASE_DIR / "exports"

# Configuration des APIs et sources de données
class ConfigurationAPIs:
    """Configuration des APIs et sources de données externes"""
    
    # URLs de base
    FOOTBALL_DATA_API = "https://api.football-data.org/v4"
    TRANSFERMARKT_BASE = "https://www.transfermarkt.fr"
    LEQUIPE_BASE = "https://www.lequipe.fr"
    
    # Headers pour les requêtes
    HEADERS_STANDARD = {
        'User-Agent': 'RCS-Analytics-Platform/1.0 (Strasbourg Football Club)',
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    
    # Timeouts et limites
    TIMEOUT_REQUETE = 10  # secondes
    MAX_RETRIES = 3
    CACHE_DURATION = 3600  # 1 heure en secondes

# Configuration des métriques football
class MetriquesFootball:
    """Configuration des métriques et calculs football"""
    
    # Coefficients xG personnalisés RCS
    BONUS_JOUEURS_XG = {
        "Emanuel Emegha": 0.25,      # Finisseur exceptionnel
        "Dilane Bakwa": 0.15,        # Précision et placement
        "Habib Diarra": 0.10,        # Vision de jeu
        "Sebastian Nanasi": 0.08,    # Technique nordique
        "Félix Lemaréchal": 0.05     # Jeune talent prometteur
    }
    
    # Bonus situations de jeu
    BONUS_SITUATIONS = {
        "contre_attaque": 0.35,
        "coup_franc_direct": 0.20,
        "corner": 0.10,
        "penalty": 0.95,
        "action_individuelle": 0.15
    }
    
    # Seuils d'alerte performance
    SEUILS_PERFORMANCE = {
        "note_minimale": 6.0,
        "minutes_fatigue": 75,
        "cartons_jaunes_limite": 4,
        "blessures_consecutives": 2
    }

# Configuration de l'interface utilisateur
class ConfigurationUI:
    """Configuration de l'interface utilisateur"""
    
    # Thème RCS
    THEME_RCS = {
        "primary_color": "#0066CC",
        "background_color": "#FAFAFA", 
        "secondary_background_color": "#F0F8FF",
        "text_color": "#262730",
        "font": "sans serif"
    }
    
    # Langues supportées
    LANGUES = ["fr", "en", "de"]  # Français, Anglais, Allemand (Alsace)
    LANGUE_DEFAUT = "fr"
    
    # Formats d'export
    FORMATS_EXPORT = ["PDF", "Excel", "CSV", "PNG", "SVG"]

# Configuration de développement et production
class Environnements:
    """Configuration selon l'environnement"""
    
    DEVELOPPEMENT = {
        "debug": True,
        "cache_enabled": False,
        "log_level": "DEBUG",
        "database_url": "sqlite:///rcs_analytics_dev.db"
    }
    
    PRODUCTION = {
        "debug": False,
        "cache_enabled": True,
        "log_level": "INFO", 
        "database_url": os.getenv("DATABASE_URL", "postgresql://localhost/rcs_analytics")
    }

# Instance globale de configuration
config_rcs = ConfigurationRCS()
chemins = CheminsProjet()
apis = ConfigurationAPIs()
metriques = MetriquesFootball()
ui_config = ConfigurationUI()

def obtenir_config_environnement():
    """Retourne la configuration selon l'environnement actuel"""
    env = os.getenv("ENVIRONMENT", "development").lower()
    
    if env == "production":
        return Environnements.PRODUCTION
    else:
        return Environnements.DEVELOPPEMENT

def afficher_configuration():
    """Affiche la configuration actuelle du système"""
    
    print("🔵⚪ CONFIGURATION RACING CLUB DE STRASBOURG")
    print("=" * 50)
    print(f"📅 Saison: {config_rcs.saison}")
    print(f"🏟️  Stade: {config_rcs.stade}")
    print(f"🎯 Objectif: {config_rcs.objectif_classement}")
    print(f"⚽ Formation: {config_rcs.formation_principale}")
    print(f"💰 Budget max: {config_rcs.budget_transfert_max}M€")
    print(f"📊 PPDA cible: {config_rcs.ppda_cible[0]}-{config_rcs.ppda_cible[1]}")
    print("=" * 50)

if __name__ == "__main__":
    afficher_configuration()
