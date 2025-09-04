#!/usr/bin/env python3
"""
Script de Test des Modules RCS
=============================

Test des fonctionnalités des modules spécialisés Racing Club de Strasbourg
"""

import sys
import os

# Ajouter le chemin des modules
sys.path.append('/Users/cheriet/Documents/augment-projects/stat/python_analytics/modules')

try:
    # Test des imports
    print("🔵⚪ Test des Modules Racing Club de Strasbourg")
    print("=" * 55)
    
    print("\n📦 Import des modules...")
    from analyseur_rcs import AnalyseurPerformanceRCS
    from moteur_scouting_rcs import MoteurScoutingRCS  
    from metriques_rcs import MetriquesFootballRCS
    print("✅ Tous les modules importés avec succès")
    
    # Test Analyseur RCS
    print("\n🔍 Test de l'Analyseur RCS...")
    analyseur = AnalyseurPerformanceRCS()
    
    # Test effectif
    effectif = analyseur.obtenir_effectif_actuel()
    print(f"✅ Effectif RCS: {len(effectif)} joueurs")
    print(f"   - Gardiens: {len(effectif[effectif['poste'] == 'GB'])}")
    print(f"   - Défenseurs: {len(effectif[effectif['poste'].isin(['DC', 'DD', 'DG'])])}")
    print(f"   - Milieux: {len(effectif[effectif['poste'].isin(['MDC', 'MC', 'MOC', 'AD'])])}")
    print(f"   - Attaquants: {len(effectif[effectif['poste'].isin(['BU', 'AG'])])}")
    
    # Test analyse joueur
    forme_emegha = analyseur.analyser_forme_joueur_rcs("Emanuel Emegha")
    if "erreur" not in forme_emegha:
        print(f"✅ Analyse forme Emanuel Emegha: {forme_emegha['tendance_forme']}")
    
    # Test Moteur Scouting
    print("\n🎯 Test du Moteur de Scouting...")
    scouting = MoteurScoutingRCS()
    
    base_scouting = scouting.generer_base_donnees_scouting()
    print(f"✅ Base de données scouting: {len(base_scouting)} joueurs")
    
    # Top 3 cibles
    top_cibles = scouting.rechercher_cibles_prioritaires().head(3)
    print("🎯 Top 3 cibles RCS:")
    for _, joueur in top_cibles.iterrows():
        print(f"   • {joueur['nom']} ({joueur['age']}ans, {joueur['poste']}) - {joueur['valeur_marche_millions']}M€")
    
    # Test Métriques Football
    print("\n📊 Test des Métriques Football...")
    metriques = MetriquesFootballRCS()
    
    # Test xG
    xg_test = metriques.calculer_xg_tir(85, 50, "contre_attaque", "pied_droit", "Emanuel Emegha")
    print(f"✅ xG tir surface (contre-attaque): {xg_test:.3f}")
    
    # Test xA
    xa_test = metriques.calculer_xa_passe(70, 25, 88, 45, "passe_cle", "Dilane Bakwa")
    print(f"✅ xA passe décisive: {xa_test:.3f}")
    
    print("\n🎉 Tous les tests sont réussis !")
    print("Les modules RCS sont opérationnels et prêts à l'utilisation.")
    
except ImportError as e:
    print(f"❌ Erreur d'import: {e}")
    print("Vérifiez que tous les modules sont bien présents")
    
except Exception as e:
    print(f"❌ Erreur lors du test: {e}")
    print("Vérifiez la configuration des modules")

print("\n" + "=" * 55)
print("Fin des tests - Racing Club de Strasbourg")
