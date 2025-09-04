#!/usr/bin/env python3
"""
Script de Lancement Dashboard RCS
================================

Lance le dashboard spécialisé Racing Club de Strasbourg
"""

import os
import sys
import subprocess

def lancer_dashboard_rcs():
    """Lance le dashboard RCS"""
    
    print("🔵⚪ Lancement Dashboard Racing Club de Strasbourg")
    print("=" * 55)
    
    # Chemin vers le dashboard
    dashboard_path = "/Users/cheriet/Documents/augment-projects/stat/python_analytics/dashboards/dashboard_rcs.py"
    
    if not os.path.exists(dashboard_path):
        print(f"❌ Dashboard non trouvé: {dashboard_path}")
        return
    
    print("📱 Démarrage de l'interface web...")
    print("🌐 URL: http://localhost:8502")
    print("⚠️  Utilisez Ctrl+C pour arrêter")
    print("-" * 55)
    
    try:
        # Changer vers le répertoire du projet
        os.chdir("/Users/cheriet/Documents/augment-projects/stat")
        
        # Lancer streamlit
        cmd = [
            "streamlit", 
            "run", 
            "python_analytics/dashboards/dashboard_rcs.py",
            "--server.port", "8502",
            "--browser.gatherUsageStats", "false"
        ]
        
        subprocess.run(cmd)
        
    except KeyboardInterrupt:
        print("\n\n🔴 Dashboard arrêté par l'utilisateur")
    except Exception as e:
        print(f"❌ Erreur lors du lancement: {e}")
        print("Vérifiez que Streamlit est installé: pip install streamlit")

if __name__ == "__main__":
    lancer_dashboard_rcs()
