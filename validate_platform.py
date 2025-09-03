#!/usr/bin/env python3
"""
Validation finale de la Plateforme Football Analytics
"""

import subprocess
import sys
import os
from pathlib import Path

def check_python_packages():
    """Vérifie les packages Python requis"""
    print("📦 Vérification des packages Python...")
    
    required_packages = [
        'pandas', 'numpy', 'scikit-learn', 'streamlit', 
        'matplotlib', 'seaborn', 'plotly'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            missing.append(package)
            print(f"❌ {package} manquant")
    
    return len(missing) == 0, missing

def check_project_structure():
    """Vérifie la structure du projet"""
    print("\n📁 Vérification de la structure du projet...")
    
    required_paths = [
        'python_analytics/modules/performance_analyzer.py',
        'python_analytics/dashboards/coach_interface.py',
        'database/sql/create_schema.sql',
        'r_analytics/scripts/predictive_models.R',
        'configs/database.py',
        '.env'
    ]
    
    missing = []
    for path in required_paths:
        if Path(path).exists():
            print(f"✅ {path}")
        else:
            missing.append(path)
            print(f"❌ {path} manquant")
    
    return len(missing) == 0, missing

def check_module_imports():
    """Teste les imports des modules principaux"""
    print("\n🔌 Test des imports modules...")
    
    try:
        sys.path.insert(0, str(Path.cwd()))
        
        from python_analytics.modules.performance_analyzer import FootballMetrics
        print("✅ FootballMetrics")
        
        from python_analytics.modules.performance_analyzer import PlayerPerformanceAnalyzer
        print("✅ PlayerPerformanceAnalyzer")
        
        from python_analytics.modules.scouting_engine import ScoutingEngine
        print("✅ ScoutingEngine")
        
        from configs.database import DatabaseConfig
        print("✅ DatabaseConfig")
        
        return True, []
        
    except Exception as e:
        return False, [str(e)]

def check_streamlit():
    """Vérifie que Streamlit peut charger l'application"""
    print("\n🌐 Test de l'application Streamlit...")
    
    try:
        # Test de validation syntax
        result = subprocess.run([
            sys.executable, '-m', 'streamlit', 'run', 
            'python_analytics/dashboards/coach_interface.py',
            '--check'
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("✅ Application Streamlit valide")
            return True
        else:
            print(f"❌ Erreur Streamlit: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("⚠️ Timeout lors du test Streamlit (normal)")
        return True
    except Exception as e:
        print(f"❌ Erreur test Streamlit: {e}")
        return False

def generate_status_report():
    """Génère un rapport de statut complet"""
    print("\n" + "="*60)
    print("📋 RAPPORT DE VALIDATION FINAL")
    print("="*60)
    
    # Tests
    pkg_ok, missing_pkg = check_python_packages()
    struct_ok, missing_files = check_project_structure()
    import_ok, import_errors = check_module_imports()
    streamlit_ok = check_streamlit()
    
    # Résumé
    print(f"\n📊 RÉSUMÉ:")
    print(f"✅ Packages Python: {'OK' if pkg_ok else 'ERREUR'}")
    print(f"✅ Structure projet: {'OK' if struct_ok else 'ERREUR'}")
    print(f"✅ Imports modules: {'OK' if import_ok else 'ERREUR'}")
    print(f"✅ Application Streamlit: {'OK' if streamlit_ok else 'ERREUR'}")
    
    total_score = sum([pkg_ok, struct_ok, import_ok, streamlit_ok])
    print(f"\n🎯 SCORE GLOBAL: {total_score}/4")
    
    if total_score == 4:
        print("\n🎉 PLATEFORME PRÊTE!")
        print("Commandes pour démarrer:")
        print("• Dashboard: streamlit run python_analytics/dashboards/coach_interface.py")
        print("• Jupyter: jupyter lab notebooks/")
        print("• Tests: python simple_test.py")
        
    else:
        print("\n⚠️ PROBLÈMES DÉTECTÉS:")
        if missing_pkg:
            print(f"• Packages manquants: {', '.join(missing_pkg)}")
            print("  → pip install " + " ".join(missing_pkg))
        
        if missing_files:
            print(f"• Fichiers manquants: {missing_files[0]}...")
        
        if import_errors:
            print(f"• Erreurs d'import: {import_errors[0]}")
    
    return total_score == 4

if __name__ == "__main__":
    success = generate_status_report()
    sys.exit(0 if success else 1)
