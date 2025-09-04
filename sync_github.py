#!/usr/bin/env python3
"""
Synchronisation GitHub pour déployer la transformation RCS
========================================================
"""

import subprocess
import sys
import os
from datetime import datetime

def main():
    print("🔵⚪ SYNCHRONISATION GITHUB - Racing Club de Strasbourg")
    print("=" * 60)
    
    # Changement vers le répertoire du projet
    try:
        os.chdir("/Users/cheriet/Documents/augment-projects/stat")
        print("📁 Répertoire de travail défini")
    except:
        print("❌ Erreur: Impossible de changer de répertoire")
        return
    
    try:
        # Vérification du statut Git
        print("\n🔍 Vérification du statut Git...")
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            if result.stdout.strip():
                print(f"📝 {len(result.stdout.strip().split())} fichier(s) modifié(s) détecté(s)")
            else:
                print("✅ Aucune modification en attente")
        
        # Ajout des fichiers
        print("\n📁 Ajout des fichiers...")
        subprocess.run(['git', 'add', '.'], check=True)
        print("✅ Fichiers ajoutés au staging")
        
        # Commit
        commit_message = """🔵⚪ DÉPLOIEMENT FINAL RCS - Transformation Racing Club de Strasbourg

✅ TRANSFORMATION COMPLÈTE ACCOMPLIE:
- Platform exclusively dedicated to Racing Club de Strasbourg
- Real 2024-2025 season data: 17 players with real stats
- Current position: 10th place Ligue 1, 23 points
- RCS official colors: Blue #0066CC theme
- Advanced analytics: custom xG formulas, PPDA analysis, projections
- Real-time data collection system with secure fallback

🏆 KEY FEATURES:
- Squad: Matz Sels, Emanuel Emegha, Habib Diarra, Dilane Bakwa...
- Recent results: defeats vs Marseille & Lille, victory vs Rennes
- Analytics: RCS-style xG calculations, pressing metrics
- Projections: end-of-season maintenance probability
- Interface: 100% Racing Club de Strasbourg branding

🚀 STREAMLIT CLOUD READY:
- coach_interface.py fully transformed to RCS exclusive
- Real-time data modules operational
- CSS styling matching official RCS colors
- Comprehensive fallback system for robustness

Allez Racing! 🔵⚪"""

        print("\n💾 Création du commit...")
        subprocess.run(['git', 'commit', '-m', commit_message], check=True)
        print("✅ Commit créé avec succès")
        
        # Push vers GitHub
        print("\n🚀 Push vers GitHub...")
        subprocess.run(['git', 'push', 'origin', 'main'], check=True)
        print("✅ Push réussi vers GitHub!")
        
        print("\n" + "=" * 60)
        print("🎉 SYNCHRONISATION TERMINÉE AVEC SUCCÈS !")
        print("🌐 Les changements RCS seront visibles sur Streamlit Cloud dans 2-3 minutes")
        print("🔗 URL: https://football-analytics-platform-2025.streamlit.app/")
        print("\n🔵⚪ Racing Club de Strasbourg Analytics Platform - LIVE! ⚪🔵")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors de l'exécution de git: {e}")
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")

if __name__ == "__main__":
    main()
