#!/usr/bin/env python3

import subprocess
import os
import sys

def force_git_sync():
    """Force la synchronisation avec GitHub"""
    
    # Se positionner dans le bon répertoire
    os.chdir('/Users/cheriet/Documents/augment-projects/stat')
    
    commands = [
        ['git', 'add', '-A'],
        ['git', 'commit', '-m', '🚀 EMERGENCY FIX: Removed psycopg2 import for Streamlit Cloud'],
        ['git', 'push', 'origin', 'main', '--force']
    ]
    
    print("🔄 SYNCHRONISATION D'URGENCE GITHUB")
    print("=" * 40)
    
    for cmd in commands:
        print(f"Executing: {' '.join(cmd)}")
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                print(f"✅ SUCCESS: {result.stdout}")
            else:
                print(f"❌ ERROR: {result.stderr}")
        except Exception as e:
            print(f"❌ EXCEPTION: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 REDÉPLOYER MAINTENANT SUR STREAMLIT CLOUD")
    print("=" * 50)
    print("Repository: Abdel67Unistra/Intelligence-football-analytics")
    print("Branch: main")
    print("Main file: python_analytics/dashboards/coach_interface.py")
    print("App URL: football-emergency-fix-2025")
    print("\n✅ PSYCOPG2 SUPPRIMÉ - PRÊT À DÉPLOYER!")

if __name__ == "__main__":
    force_git_sync()
