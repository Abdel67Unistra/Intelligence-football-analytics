#!/usr/bin/env python3
"""
🔵⚪ LANCEMENT RACING CLUB DE STRASBOURG PLATFORM
===============================================
Script final pour lancer et accéder à la plateforme RCS
"""

import webbrowser
import time
import subprocess
from datetime import datetime

def main():
    print("🔵⚪ RACING CLUB DE STRASBOURG ANALYTICS PLATFORM")
    print("=" * 55)
    print(f"🕐 {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}")
    print()
    
    print("🎉 TRANSFORMATION ACCOMPLIE AVEC SUCCÈS !")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print()
    print("✅ Plateforme exclusivement Racing Club de Strasbourg")
    print("✅ Données réelles saison 2024-2025")
    print("✅ Interface aux couleurs RCS (#0066CC)")
    print("✅ Analytics personnalisées (xG, PPDA, projections)")
    print("✅ Effectif complet: 17 joueurs avec stats réelles")
    print("✅ Position actuelle: 10ème Ligue 1, 23 points")
    print()
    
    print("🌐 ACCÈS À LA PLATEFORME:")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    # URL de la plateforme
    url_streamlit = "https://football-analytics-platform-2025.streamlit.app/"
    url_local = "http://localhost:8501"
    
    print(f"🔗 Production: {url_streamlit}")
    print(f"🔗 Local: {url_local}")
    print()
    
    choix = input("🚀 Ouvrir la plateforme ? (o/n): ").lower()
    
    if choix in ['o', 'oui', 'y', 'yes']:
        print("🔄 Ouverture de la plateforme RCS...")
        
        # Ouvrir dans le navigateur
        try:
            webbrowser.open(url_streamlit)
            print(f"🌐 Plateforme ouverte: {url_streamlit}")
        except:
            print("⚠️  Veuillez ouvrir manuellement:", url_streamlit)
        
        time.sleep(2)
        
        # Optionnel: lancer aussi localement
        lancer_local = input("🏠 Lancer aussi en local ? (o/n): ").lower()
        if lancer_local in ['o', 'oui', 'y', 'yes']:
            try:
                print("🔄 Lancement du dashboard local...")
                subprocess.Popen(['streamlit', 'run', 'python_analytics/dashboards/coach_interface.py'])
                print(f"🚀 Dashboard local lancé: {url_local}")
            except:
                print("⚠️  Lancez manuellement: streamlit run python_analytics/dashboards/coach_interface.py")
    
    print()
    print("🏆 CARACTÉRISTIQUES DE LA PLATEFORME RCS:")
    print("   ⚽ Joueurs vedettes: Matz Sels, Emanuel Emegha, Habib Diarra")
    print("   📊 Analytics: xG style RCS, PPDA, projections maintien")
    print("   🏠 Stade: Meinau (Strasbourg)")
    print("   🎯 Objectif: Maintien confortable Ligue 1")
    print("   📈 Forme: Analyse 5 derniers matchs")
    print("   🔮 Projection: Probabilités fin de saison")
    print()
    print("🔵⚪ ALLEZ RACING ! ⚪🔵")
    print()
    print("Plateforme Racing Club de Strasbourg - EXCLUSIVE EDITION")
    print("Transformation accomplie le 4 septembre 2025")

if __name__ == "__main__":
    main()
