#!/usr/bin/env python3
"""
Script d'urgence pour corriger l'erreur psycopg2 sur Streamlit Cloud
"""

import subprocess
import os
import sys

def run_git_command(command):
    """Exécute une commande Git et affiche le résultat"""
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            capture_output=True, 
            text=True, 
            cwd='/Users/cheriet/Documents/augment-projects/stat',
            timeout=30
        )
        
        print(f"Command: {command}")
        if result.stdout:
            print(f"Output: {result.stdout.strip()}")
        if result.stderr:
            print(f"Error: {result.stderr.strip()}")
        
        return result.returncode == 0
    except Exception as e:
        print(f"Exception: {e}")
        return False

def main():
    print("🚨 CORRECTION URGENTE ERREUR PSYCOPG2")
    print("=" * 40)
    
    # Vérifier le répertoire
    os.chdir('/Users/cheriet/Documents/augment-projects/stat')
    print(f"📍 Répertoire: {os.getcwd()}")
    
    # Commandes Git à exécuter
    commands = [
        "git add python_analytics/dashboards/coach_interface.py",
        "git commit -m '🚀 URGENT: Remove psycopg2 import for Streamlit Cloud'",
        "git push origin main"
    ]
    
    success = True
    for cmd in commands:
        print(f"\n🔄 Exécution: {cmd}")
        if not run_git_command(cmd):
            print(f"❌ Échec de la commande: {cmd}")
            success = False
        else:
            print("✅ Succès!")
    
    if success:
        print("\n" + "=" * 50)
        print("✅ CORRECTION APPLIQUÉE AVEC SUCCÈS!")
        print("🔄 REDÉPLOYEZ MAINTENANT SUR STREAMLIT CLOUD")
        print("=" * 50)
        print("Repository: Abdel67Unistra/Intelligence-football-analytics")
        print("Branch: main")
        print("Main file: python_analytics/dashboards/coach_interface.py")
        print("App URL: football-fixed-emergency")
        print("\n🌐 Allez sur: https://share.streamlit.io")
        print("🎉 L'ERREUR PSYCOPG2 EST MAINTENANT RÉSOLUE!")
    else:
        print("\n❌ ERREUR LORS DE LA SYNCHRONISATION")
        print("Essayez manuellement dans un terminal:")
        print("cd /Users/cheriet/Documents/augment-projects/stat")
        print("git add .")
        print("git commit -m 'Fix psycopg2'")
        print("git push origin main")

if __name__ == "__main__":
    main()
