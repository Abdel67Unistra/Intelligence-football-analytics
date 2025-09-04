#!/usr/bin/env python3
"""
Test Simple des Modules RCS
===========================

Test basique des fonctionnalités core sans dépendances lourdes
"""

import sys
import os
import pandas as pd
import numpy as np

# Ajouter le chemin des modules
sys.path.append('/Users/cheriet/Documents/augment-projects/stat/python_analytics/modules')

print("🔵⚪ Test Simple - Racing Club de Strasbourg")
print("=" * 50)

try:
    # Test 1: Import analyseur RCS
    print("\n📦 Test 1: Import analyseur_rcs...")
    exec(open('/Users/cheriet/Documents/augment-projects/stat/python_analytics/modules/analyseur_rcs.py').read())
    print("✅ analyseur_rcs chargé")
    
    # Test 2: Import métriques RCS
    print("\n📊 Test 2: Import metriques_rcs...")
    exec(open('/Users/cheriet/Documents/augment-projects/stat/python_analytics/modules/metriques_rcs.py').read())
    print("✅ metriques_rcs chargé")
    
    # Test 3: Création instances
    print("\n🏗️ Test 3: Création des instances...")
    analyseur = AnalyseurPerformanceRCS()
    print("✅ Analyseur RCS créé")
    
    metriques = MetriquesFootballRCS()
    print("✅ Métriques RCS créées")
    
    # Test 4: Données effectif
    print("\n👥 Test 4: Effectif RCS...")
    effectif = analyseur.obtenir_effectif_actuel()
    print(f"✅ Effectif: {len(effectif)} joueurs")
    
    # Test 5: Métriques de base
    print("\n📈 Test 5: Calcul métriques...")
    xg = metriques.calculer_xg_tir(85, 50, "centre", "pied_droit", "Emanuel Emegha")
    print(f"✅ xG calculé: {xg:.3f}")
    
    print("\n🎉 Tous les tests sont réussis !")
    
except Exception as e:
    print(f"❌ Erreur: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 50)
