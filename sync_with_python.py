#!/usr/bin/env python3
"""
Script Python pour synchroniser le repository avec GitHub
"""

import subprocess
import os
import sys
from datetime import datetime

def run_command(cmd):
    """Exécute une commande shell et retourne le résultat"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd='/Users/cheriet/Documents/augment-projects/stat')
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def main():
    print("🔄 SYNCHRONISATION GITHUB AVEC PYTHON")
    print("====================================")
    
    # Vérifier le répertoire
    os.chdir('/Users/cheriet/Documents/augment-projects/stat')
    
    # Status
    success, stdout, stderr = run_command("git status --porcelain")
    if stdout.strip():
        print("📝 Fichiers modifiés détectés")
    else:
        print("✅ Aucune modification locale")
    
    # Add all
    print("📦 Ajout des fichiers...")
    run_command("git add -A")
    
    # Commit
    print("💾 Commit...")
    run_command('git commit -m "🚀 FINAL: Removed psycopg2 completely for Streamlit Cloud"')
    
    # Push
    print("📤 Push vers GitHub...")
    success, stdout, stderr = run_command("git push origin main")
    
    if success:
        print("✅ SYNCHRONISATION RÉUSSIE!")
    else:
        print(f"❌ Erreur push: {stderr}")
    
    # Générer informations de déploiement
    timestamp = int(datetime.now().timestamp())
    unique_name = f"football-analytics-{timestamp}"
    
    print("\n🎯 VALEURS POUR STREAMLIT CLOUD:")
    print("================================")
    print("Repository: Abdel67Unistra/Intelligence-football-analytics")
    print("Branch: main") 
    print("Main file path: python_analytics/dashboards/coach_interface.py")
    print(f"App URL (unique): {unique_name}")
    print(f"\n🌐 URL finale: https://{unique_name}.streamlit.app")
    
    print("\n🚀 REDÉPLOYEZ MAINTENANT SUR STREAMLIT CLOUD!")

if __name__ == "__main__":
    main()
