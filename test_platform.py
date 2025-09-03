#!/usr/bin/env python3
"""
Tests d'intégration pour la Plateforme Football Analytics
"""

import sys
import os
import traceback
from pathlib import Path

# Ajouter le répertoire racine au path
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Test des imports principaux"""
    print("🧪 Test des imports...")
    
    try:
        import pandas as pd
        import numpy as np
        import streamlit as st
        print("✅ Imports de base OK")
    except ImportError as e:
        print(f"❌ Erreur d'import: {e}")
        return False
    
    try:
        from python_analytics.modules.performance_analyzer import PlayerPerformanceAnalyzer
        from python_analytics.modules.tactical_analyzer import TacticalAnalyzer
        from python_analytics.modules.scouting_engine import ScoutingEngine
        print("✅ Modules analytics OK")
    except ImportError as e:
        print(f"❌ Erreur modules analytics: {e}")
        return False
    
    return True

def test_database_config():
    """Test de la configuration base de données"""
    print("🗄️  Test configuration base de données...")
    
    try:
        from configs.database import DatabaseConfig
        config = DatabaseConfig()
        print("✅ Configuration DB OK")
        return True
    except Exception as e:
        print(f"❌ Erreur configuration DB: {e}")
        return False

def test_football_metrics():
    """Test des métriques football"""
    print("⚽ Test des métriques football...")
    
    try:
        from python_analytics.modules.performance_analyzer import FootballMetrics
        
        # Test calcul xG
        metrics = FootballMetrics()
        xg = metrics.calculate_xg(
            distance=15,
            angle=30,
            shot_type='foot',
            assist_type='pass'
        )
        
        assert 0 <= xg <= 1, "xG doit être entre 0 et 1"
        print(f"✅ Calcul xG OK (xG = {xg:.3f})")
        
        # Test calcul xA
        xa = metrics.calculate_xa(
            pass_distance=25,
            pass_angle=45,
            receiver_position='penalty_area'
        )
        
        assert 0 <= xa <= 1, "xA doit être entre 0 et 1"
        print(f"✅ Calcul xA OK (xA = {xa:.3f})")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur métriques: {e}")
        traceback.print_exc()
        return False

def test_data_generation():
    """Test de la génération de données démo"""
    print("📊 Test génération données démo...")
    
    try:
        from database.migrations.populate_demo_data import FootballDataGenerator
        
        generator = FootballDataGenerator()
        
        # Test génération joueur
        player = generator.generate_player_stats()
        assert 'name' in player
        assert 'position' in player
        assert 'goals' in player
        print("✅ Génération joueur OK")
        
        # Test génération match
        match = generator.generate_match_data()
        assert 'home_team' in match
        assert 'away_team' in match
        assert 'events' in match
        print("✅ Génération match OK")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur génération données: {e}")
        traceback.print_exc()
        return False

def run_all_tests():
    """Exécute tous les tests"""
    print("🚀 Lancement des tests de la Plateforme Football Analytics")
    print("=" * 60)
    
    tests = [
        test_imports,
        test_database_config,
        test_football_metrics,
        test_data_generation
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ Erreur inattendue dans {test.__name__}: {e}")
            failed += 1
        print()
    
    print("📊 Résultats des tests:")
    print(f"✅ Tests réussis: {passed}")
    print(f"❌ Tests échoués: {failed}")
    
    if failed == 0:
        print("🎉 Tous les tests sont passés! La plateforme est prête.")
        return True
    else:
        print("⚠️  Certains tests ont échoué. Vérifiez les erreurs ci-dessus.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
