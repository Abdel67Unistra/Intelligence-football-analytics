#!/usr/bin/env python3
"""
🔵⚪ Racing Club de Strasbourg - Application Principal Unifiée
============================================================

Application principale qui combine toutes les fonctionnalités de la plateforme
d'analytics RCS : interface web, analyses avancées, rapports automatisés et graphiques R.

Auteur: GitHub Copilot
Date: Septembre 2025
Version: 2.0 - Restructurée et optimisée
"""

import os
import sys
import subprocess
import argparse
import webbrowser
from pathlib import Path
from datetime import datetime
import time

# Ajout du répertoire parent au path pour les imports
sys.path.append(str(Path(__file__).parent))

# Import des modules RCS
try:
    from assets_rcs import AssetsRCS, assets_rcs
    from config_rcs import ConfigRCS, config_rcs
except ImportError as e:
    print(f"❌ Erreur d'import des modules RCS: {e}")
    print("Assurez-vous que tous les fichiers sont dans le bon répertoire.")

def afficher_banniere():
    """Affiche la bannière de démarrage RCS avec logo ASCII"""
    
    print("\n" + "="*70)
    print("🔵⚪ RACING CLUB DE STRASBOURG - ANALYTICS PLATFORM v2.0 ⚪🔵")
    print("="*70)
    print("🏟️  Saison 2024-2025 - Intelligence Artificielle Avancée  🏟️")
    print("="*70)
                                                                    
    ██████╗  █████╗  ██████╗██╗███╗   ██╗ ██████╗               
    ██╔══██╗██╔══██╗██╔════╝██║████╗  ██║██╔════╝               
    ██████╔╝███████║██║     ██║██╔██╗ ██║██║  ███╗              
    ██╔══██╗██╔══██║██║     ██║██║╚██╗██║██║   ██║              
    ██║  ██║██║  ██║╚██████╗██║██║ ╚████║╚██████╔╝              
    ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝╚═╝  ╚═══╝ ╚═════╝               
                                                                    
     ██████╗██╗     ██╗   ██╗██████╗     ██████╗ ███████╗        
    ██╔════╝██║     ██║   ██║██╔══██╗    ██╔══██╗██╔════╝        
    ██║     ██║     ██║   ██║██████╔╝    ██║  ██║█████╗          
    ██║     ██║     ██║   ██║██╔══██╗    ██║  ██║██╔══╝          
    ╚██████╗███████╗╚██████╔╝██████╔╝    ██████╔╝███████╗        
     ╚═════╝╚══════╝ ╚═════╝ ╚═════╝     ╚═════╝ ╚══════╝        
                                                                    
    ███████╗████████╗██████╗  █████╗ ███████╗██████╗  ██████╗     
    ██╔════╝╚══██╔══╝██╔══██╗██╔══██╗██╔════╝██╔══██╗██╔════╝     
    ███████╗   ██║   ██████╔╝███████║███████╗██████╔╝██║  ███╗    
    ╚════██║   ██║   ██╔══██╗██╔══██║╚════██║██╔══██╗██║   ██║    
    ███████║   ██║   ██║  ██║██║  ██║███████║██████╔╝╚██████╔╝    
    ╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═════╝  ╚═════╝     
                                                                    
        🏟️  Analytics Platform - Saison 2024-2025  🏟️             
                                                                    
🔵⚪ ════════════════════════════════════════════════════════════ ⚪🔵
""")
    
    print(f"📅 {datetime.now().strftime('%A %d %B %Y - %H:%M:%S')}")
    print("🏟️  Stade de la Meinau - Strasbourg, France")
    print("⚽ Ligue 1 - Position actuelle: 10ème place, 23 points")
    print("👥 Effectif: 17 joueurs professionnels")
    print()

def verifier_dependances():
    """Vérifie que toutes les dépendances sont installées"""
    
    print("🔍 Vérification des dépendances...")
    
    dependances_requises = [
        'streamlit', 'pandas', 'numpy', 'plotly', 'matplotlib', 
        'seaborn', 'scikit-learn', 'requests', 'beautifulsoup4'
    ]
    
    dependances_manquantes = []
    
    for dep in dependances_requises:
        try:
            __import__(dep)
            print(f"   ✅ {dep}")
        except ImportError:
            dependances_manquantes.append(dep)
            print(f"   ❌ {dep} - manquant")
    
    if dependances_manquantes:
        print(f"\n⚠️  Dépendances manquantes: {', '.join(dependances_manquantes)}")
        print("💡 Installer avec: pip install " + " ".join(dependances_manquantes))
        return False
    
    print("✅ Toutes les dépendances sont installées")
    return True

def verifier_structure_projet():
    """Vérifie que la structure du projet est correcte"""
    
    print("📁 Vérification de la structure du projet...")
    
    fichiers_requis = [
        'config_rcs.py',
        'analytics_avances_rcs.py', 
        'webapp_rcs_moderne.py',
        'generateur_rapports_rcs.py',
        'python_analytics/modules/collecteur_donnees_rcs.py',
        'python_analytics/modules/analyseur_rcs.py',
        'r_analytics/scripts/analyses_predictives_avancees_rcs.R'
    ]
    
    fichiers_manquants = []
    
    for fichier in fichiers_requis:
        chemin = Path(fichier)
        if chemin.exists():
            print(f"   ✅ {fichier}")
        else:
            fichiers_manquants.append(fichier)
            print(f"   ❌ {fichier} - manquant")
    
    if fichiers_manquants:
        print(f"\n⚠️  Fichiers manquants: {len(fichiers_manquants)}")
        return False
    
    print("✅ Structure du projet correcte")
    return True

def lancer_interface_web(port=8501, debug=False):
    """Lance l'interface web Streamlit"""
    
    print(f"🌐 Lancement de l'interface web sur le port {port}...")
    
    try:
        cmd = ["streamlit", "run", "webapp_rcs_moderne.py", "--server.port", str(port)]
        
        if not debug:
            cmd.extend(["--server.headless", "true"])
        
        print(f"🚀 Interface web accessible sur: http://localhost:{port}")
        print("⏱️  Chargement en cours...")
        
        # Lancement en arrière-plan
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Attendre un peu pour le démarrage
        time.sleep(3)
        
        # Ouvrir automatiquement le navigateur
        if not debug:
            webbrowser.open(f"http://localhost:{port}")
        
        return process
        
    except Exception as e:
        print(f"❌ Erreur lors du lancement de l'interface web: {e}")
        return None

def executer_analyses_r():
    """Exécute les analyses R avancées"""
    
    print("📊 Exécution des analyses R avancées...")
    
    script_r = "r_analytics/scripts/analyses_predictives_avancees_rcs.R"
    
    if not Path(script_r).exists():
        print(f"❌ Script R non trouvé: {script_r}")
        return False
    
    try:
        # Vérifier que R est installé
        result = subprocess.run(["Rscript", "--version"], 
                              capture_output=True, text=True, timeout=10)
        
        if result.returncode != 0:
            print("❌ R n'est pas installé ou accessible")
            return False
        
        print("✅ R détecté, exécution du script...")
        
        # Exécuter le script R
        result = subprocess.run(["Rscript", script_r], 
                              capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print("✅ Analyses R terminées avec succès")
            if result.stdout:
                print("📊 Résultats:")
                print(result.stdout)
            return True
        else:
            print("❌ Erreur dans l'exécution du script R")
            print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("⏱️  Timeout: Script R trop long")
        return False
    except FileNotFoundError:
        print("❌ Rscript non trouvé. Installer R d'abord.")
        return False
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")
        return False

def generer_rapports_automatises():
    """Génère les rapports automatisés"""
    
    print("📋 Génération des rapports automatisés...")
    
    try:
        from generateur_rapports_rcs import GenerateurRapportsRCS
        
        generateur = GenerateurRapportsRCS()
        resultats = generateur.generer_tous_rapports()
        
        if resultats:
            print("✅ Rapports générés avec succès")
            print(f"📁 Fichiers: {len(resultats['fichiers_generes'])}")
            return True
        else:
            print("❌ Erreur lors de la génération des rapports")
            return False
            
    except ImportError as e:
        print(f"❌ Erreur d'import: {e}")
        return False
    except Exception as e:
        print(f"❌ Erreur lors de la génération: {e}")
        return False

def executer_analytics_avances():
    """Exécute les analytics avancés Python"""
    
    print("🤖 Exécution des analytics avancés...")
    
    try:
        from analytics_avances_rcs import lancer_analytics_complet
        
        resultats = lancer_analytics_complet()
        
        if resultats:
            print("✅ Analytics avancés terminés")
            print("📊 Dashboard, prédictions et analyses générés")
            return True
        else:
            print("❌ Erreur dans les analytics avancés")
            return False
            
    except ImportError as e:
        print(f"❌ Erreur d'import: {e}")
        return False
    except Exception as e:
        print(f"❌ Erreur lors de l'exécution: {e}")
        return False

def afficher_menu_principal():
    """Affiche le menu principal interactif"""
    
    print("🎮 MENU PRINCIPAL - Racing Club de Strasbourg Analytics")
    print("=" * 60)
    print("1. 🌐 Lancer l'interface web complète")
    print("2. 📊 Exécuter les analyses R avancées")  
    print("3. 🤖 Lancer les analytics Python IA")
    print("4. 📋 Générer les rapports automatisés")
    print("5. 🔄 Suite complète (tout exécuter)")
    print("6. 🛠️  Mode développeur (debug)")
    print("7. ℹ️  Informations système")
    print("8. 🚪 Quitter")
    print("=" * 60)

def mode_interactif():
    """Mode interactif avec menu"""
    
    while True:
        afficher_menu_principal()
        
        try:
            choix = input("\n🎯 Sélectionnez une option (1-8): ").strip()
            
            if choix == '1':
                print("\n🌐 LANCEMENT INTERFACE WEB")
                print("-" * 30)
                port = input("Port (défaut 8501): ").strip() or "8501"
                process = lancer_interface_web(int(port))
                if process:
                    input("\n⏸️  Appuyez sur Entrée pour arrêter l'interface web...")
                    process.terminate()
                    print("🛑 Interface web arrêtée")
            
            elif choix == '2':
                print("\n📊 ANALYSES R AVANCÉES")
                print("-" * 30)
                executer_analyses_r()
                input("\n⏸️  Appuyez sur Entrée pour continuer...")
            
            elif choix == '3':
                print("\n🤖 ANALYTICS PYTHON IA")
                print("-" * 30)
                executer_analytics_avances()
                input("\n⏸️  Appuyez sur Entrée pour continuer...")
            
            elif choix == '4':
                print("\n📋 RAPPORTS AUTOMATISÉS")
                print("-" * 30)
                generer_rapports_automatises()
                input("\n⏸️  Appuyez sur Entrée pour continuer...")
            
            elif choix == '5':
                print("\n🔄 SUITE COMPLÈTE")
                print("-" * 30)
                print("🚀 Exécution de toutes les analyses...")
                
                # Ordre d'exécution optimisé
                etapes = [
                    ("📊 Analyses R", executer_analyses_r),
                    ("🤖 Analytics Python", executer_analytics_avances), 
                    ("📋 Rapports", generer_rapports_automatises)
                ]
                
                resultats = []
                for nom, fonction in etapes:
                    print(f"\n{nom}...")
                    succes = fonction()
                    resultats.append((nom, succes))
                    time.sleep(1)
                
                # Bilan
                print(f"\n🏁 BILAN DE LA SUITE COMPLÈTE")
                print("-" * 30)
                for nom, succes in resultats:
                    statut = "✅" if succes else "❌"
                    print(f"{statut} {nom}")
                
                # Lancement de l'interface web en dernier
                print(f"\n🌐 Lancement de l'interface web finale...")
                lancer_interface_web()
                
                input("\n⏸️  Appuyez sur Entrée pour continuer...")
            
            elif choix == '6':
                print("\n🛠️  MODE DÉVELOPPEUR")
                print("-" * 30)
                print("🔍 Vérifications supplémentaires...")
                verifier_dependances()
                verifier_structure_projet()
                
                print("\n🌐 Interface web en mode debug...")
                lancer_interface_web(debug=True)
                input("\n⏸️  Appuyez sur Entrée pour continuer...")
            
            elif choix == '7':
                print("\n ℹ️ INFORMATIONS SYSTÈME")
                print("-" * 30)
                afficher_informations_systeme()
                input("\n⏸️  Appuyez sur Entrée pour continuer...")
            
            elif choix == '8':
                print("\n🚪 Fermeture de l'application...")
                print("🔵⚪ Merci d'avoir utilisé RCS Analytics Platform ! ⚪🔵")
                break
            
            else:
                print("❌ Option invalide. Choisissez entre 1 et 8.")
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\n\n🛑 Interruption détectée")
            break
        except Exception as e:
            print(f"❌ Erreur: {e}")
            time.sleep(2)

def afficher_informations_systeme():
    """Affiche les informations système et du projet"""
    
    print("🔵⚪ RACING CLUB DE STRASBOURG - INFORMATIONS SYSTÈME")
    print("=" * 60)
    
    # Informations générales
    print("📋 INFORMATIONS GÉNÉRALES")
    print("-" * 30)
    print(f"🏟️  Club: Racing Club de Strasbourg")
    print(f"📅 Saison: 2024-2025")
    print(f"🏆 Competition: Ligue 1")
    print(f"📍 Position: 10ème place (23 points)")
    print(f"👥 Effectif: 17 joueurs")
    print(f"🏟️  Stade: Meinau (26,109 places)")
    
    # Informations techniques
    print(f"\n💻 INFORMATIONS TECHNIQUES")
    print("-" * 30)
    print(f"🐍 Python: {sys.version.split()[0]}")
    print(f"📁 Répertoire: {Path.cwd()}")
    print(f"🕐 Dernière MAJ: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    
    # Modules disponibles
    print(f"\n📦 MODULES DISPONIBLES")
    print("-" * 30)
    
    modules = [
        ('config_rcs.py', 'Configuration RCS'),
        ('analytics_avances_rcs.py', 'Analytics IA avancés'),
        ('webapp_rcs_moderne.py', 'Interface web moderne'),
        ('generateur_rapports_rcs.py', 'Rapports automatisés'),
        ('python_analytics/', 'Modules Python analytics'),
        ('r_analytics/', 'Scripts R prédictifs')
    ]
    
    for fichier, description in modules:
        statut = "✅" if Path(fichier).exists() else "❌"
        print(f"{statut} {fichier:<30} - {description}")
    
    # Fonctionnalités
    print(f"\n🚀 FONCTIONNALITÉS PRINCIPALES")
    print("-" * 30)
    fonctionnalites = [
        "📊 Dashboard temps réel Streamlit",
        "🤖 Prédictions IA (blessures, performances)",
        "📈 Modèles ML (Random Forest, XGBoost)",
        "📋 Rapports automatisés (HTML, JSON)",
        "🎯 Optimisation compositions IA",
        "🏥 Analyses médicales préventives",
        "💎 Scouting intelligent",
        "📊 Visualisations R interactives"
    ]
    
    for feature in fonctionnalites:
        print(f"  • {feature}")

def mode_commande_ligne(args):
    """Mode ligne de commande avec arguments"""
    
    if args.web:
        port = args.port or 8501
        lancer_interface_web(port, args.debug)
    
    if args.analytics:
        executer_analytics_avances()
    
    if args.rapports:
        generer_rapports_automatises()
    
    if args.r_analyses:
        executer_analyses_r()
    
    if args.complet:
        executer_analyses_r()
        executer_analytics_avances()
        generer_rapports_automatises()
        lancer_interface_web()

def main():
    """Fonction principale de l'application"""
    
    # Parser d'arguments
    parser = argparse.ArgumentParser(
        description="🔵⚪ Racing Club de Strasbourg - Analytics Platform",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples d'utilisation:
  python main_rcs.py                    # Mode interactif
  python main_rcs.py --web              # Lance l'interface web
  python main_rcs.py --analytics        # Exécute les analytics Python
  python main_rcs.py --rapports         # Génère les rapports
  python main_rcs.py --complet          # Suite complète
  python main_rcs.py --web --port 8502  # Interface web sur port 8502
        """
    )
    
    parser.add_argument('--web', action='store_true', help='Lancer l\'interface web')
    parser.add_argument('--analytics', action='store_true', help='Exécuter les analytics avancés')
    parser.add_argument('--rapports', action='store_true', help='Générer les rapports')
    parser.add_argument('--r-analyses', action='store_true', help='Exécuter les analyses R')
    parser.add_argument('--complet', action='store_true', help='Exécuter la suite complète')
    parser.add_argument('--port', type=int, help='Port pour l\'interface web (défaut: 8501)')
    parser.add_argument('--debug', action='store_true', help='Mode debug')
    parser.add_argument('--check', action='store_true', help='Vérifier les dépendances')
    
    args = parser.parse_args()
    
    # Affichage de la bannière
    afficher_banniere()
    
    # Vérification si arguments fournis
    if any([args.web, args.analytics, args.rapports, args.r_analyses, args.complet, args.check]):
        
        if args.check:
            verifier_dependances()
            verifier_structure_projet()
            return
        
        # Vérifications préliminaires
        if not verifier_dependances() or not verifier_structure_projet():
            print("❌ Vérifications échouées. Impossible de continuer.")
            return
        
        # Mode ligne de commande
        mode_commande_ligne(args)
    
    else:
        # Vérifications préliminaires
        if not verifier_dependances() or not verifier_structure_projet():
            print("❌ Vérifications échouées. Veuillez corriger les erreurs.")
            return
        
        # Mode interactif
        mode_interactif()

if __name__ == "__main__":
    main()
