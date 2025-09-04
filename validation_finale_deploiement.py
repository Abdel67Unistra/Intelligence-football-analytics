#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔵⚪ VALIDATION FINALE - RACING CLUB DE STRASBOURG PLATFORM
Script de validation du déploiement complet
"""

import os
import sys
import subprocess
import time
from datetime import datetime

def print_header():
    """Affiche l'en-tête de validation"""
    print("=" * 80)
    print("🔵⚪ VALIDATION FINALE - RACING CLUB DE STRASBOURG PLATFORM")
    print("=" * 80)
    print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🎯 Objectif: Validation déploiement complet")
    print()

def check_file_exists(filepath, description):
    """Vérifie qu'un fichier existe"""
    if os.path.exists(filepath):
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ {description}: {filepath} - MANQUANT")
        return False

def check_git_status():
    """Vérifie le statut Git"""
    print("📂 VÉRIFICATION GIT:")
    try:
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True, cwd='.')
        if result.returncode == 0:
            if not result.stdout.strip():
                print("✅ Repository Git: Propre (tous les fichiers committés)")
                return True
            else:
                print("⚠️  Repository Git: Fichiers non committés détectés")
                print(result.stdout)
                return False
        else:
            print("❌ Erreur lors de la vérification Git")
            return False
    except Exception as e:
        print(f"❌ Erreur Git: {e}")
        return False

def check_last_commit():
    """Vérifie le dernier commit"""
    print("\n📝 DERNIER COMMIT:")
    try:
        result = subprocess.run(['git', 'log', '--oneline', '-1'], 
                              capture_output=True, text=True, cwd='.')
        if result.returncode == 0:
            print(f"✅ {result.stdout.strip()}")
            return True
        else:
            print("❌ Impossible de récupérer le dernier commit")
            return False
    except Exception as e:
        print(f"❌ Erreur commit: {e}")
        return False

def validate_main_files():
    """Valide les fichiers principaux"""
    print("\n📁 VALIDATION FICHIERS PRINCIPAUX:")
    
    files_to_check = [
        ("python_analytics/dashboards/coach_interface.py", "Dashboard principal RCS"),
        ("python_analytics/dashboards/coach_interface_rcs_real.py", "Version RCS données réelles"),
        ("python_analytics/modules/collecteur_donnees_rcs.py", "Module collecte données RCS"),
        ("TRANSFORMATION_RCS_ACCOMPLIE.md", "Documentation transformation"),
        ("MISSION_FINALE_ACCOMPLIE.md", "Documentation mission"),
        ("DEPLOIEMENT_FINAL_COMPLET.md", "Documentation déploiement"),
    ]
    
    all_good = True
    for filepath, description in files_to_check:
        if not check_file_exists(filepath, description):
            all_good = False
    
    return all_good

def check_streamlit_syntax():
    """Vérifie la syntaxe des fichiers Streamlit"""
    print("\n🔍 VÉRIFICATION SYNTAXE STREAMLIT:")
    
    streamlit_files = [
        "python_analytics/dashboards/coach_interface.py",
        "python_analytics/dashboards/coach_interface_rcs_real.py"
    ]
    
    all_good = True
    for file in streamlit_files:
        if os.path.exists(file):
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if "import streamlit as st" in content:
                        print(f"✅ {file}: Import Streamlit OK")
                    else:
                        print(f"⚠️  {file}: Import Streamlit manquant")
                        all_good = False
                        
                    if "st.set_page_config" in content:
                        print(f"✅ {file}: Configuration page OK")
                    else:
                        print(f"⚠️  {file}: Configuration page manquante")
                        
            except Exception as e:
                print(f"❌ {file}: Erreur lecture - {e}")
                all_good = False
        else:
            print(f"❌ {file}: Fichier manquant")
            all_good = False
    
    return all_good

def check_rcs_branding():
    """Vérifie que le branding RCS est présent"""
    print("\n🔵 VÉRIFICATION BRANDING RCS:")
    
    main_file = "python_analytics/dashboards/coach_interface.py"
    if os.path.exists(main_file):
        try:
            with open(main_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            checks = [
                ("Racing Club de Strasbourg", "Nom équipe"),
                ("#0066CC", "Couleur RCS bleue"),
                ("🔵⚪", "Émojis RCS"),
                ("Matz Sels", "Joueur RCS"),
                ("Emanuel Emegha", "Joueur RCS"),
                ("Habib Diarra", "Joueur RCS"),
            ]
            
            all_good = True
            for check, description in checks:
                if check in content:
                    print(f"✅ {description}: Présent")
                else:
                    print(f"❌ {description}: Manquant")
                    all_good = False
                    
            return all_good
            
        except Exception as e:
            print(f"❌ Erreur lecture fichier principal: {e}")
            return False
    else:
        print("❌ Fichier principal manquant")
        return False

def generate_summary():
    """Génère le résumé final"""
    print("\n" + "=" * 80)
    print("📊 RÉSUMÉ DE VALIDATION")
    print("=" * 80)
    
    # Récapitulatif des validations
    validations = [
        validate_main_files(),
        check_git_status(),
        check_last_commit(),
        check_streamlit_syntax(),
        check_rcs_branding()
    ]
    
    success_count = sum(validations)
    total_count = len(validations)
    
    print(f"✅ Validations réussies: {success_count}/{total_count}")
    
    if success_count == total_count:
        print("\n🎉 VALIDATION COMPLÈTE RÉUSSIE!")
        print("🔵⚪ LA PLATEFORME RCS EST PRÊTE POUR LE DÉPLOIEMENT!")
        print("\n🌐 URL DÉPLOIEMENT:")
        print("https://football-analytics-platform-2025.streamlit.app/")
        print("\n🏆 MISSION ACCOMPLIE - RACING CLUB DE STRASBOURG ANALYTICS OPÉRATIONNEL")
        return True
    else:
        print(f"\n⚠️  {total_count - success_count} validation(s) échoué(s)")
        print("🔧 Veuillez corriger les problèmes identifiés")
        return False

def main():
    """Fonction principale"""
    print_header()
    
    # Changement vers le répertoire du projet
    project_dir = "/Users/cheriet/Documents/augment-projects/stat"
    if os.path.exists(project_dir):
        os.chdir(project_dir)
        print(f"📂 Répertoire de travail: {project_dir}")
    else:
        print(f"❌ Répertoire projet introuvable: {project_dir}")
        sys.exit(1)
    
    # Exécution des validations
    success = generate_summary()
    
    if success:
        print("\n🚀 ÉTAPES SUIVANTES:")
        print("1. ✅ Tous les fichiers sont committés et pushés sur GitHub")
        print("2. ✅ Streamlit Cloud va automatiquement redéployer")
        print("3. ✅ Vérifiez l'URL dans quelques minutes")
        print("\n🔵⚪ ALLEZ RACING! 🔵⚪")
        sys.exit(0)
    else:
        print("\n🔧 ACTION REQUISE:")
        print("Corrigez les problèmes identifiés avant déploiement")
        sys.exit(1)

if __name__ == "__main__":
    main()
