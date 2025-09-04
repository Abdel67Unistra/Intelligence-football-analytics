#!/usr/bin/env python3
"""
Racing Club de Strasbourg - Analytics Console
============================================

Version ultra-simplifiée du dashboard RCS
Fonctionne sans dépendances externes
"""

def afficher_logo_rcs():
    """Affiche le logo ASCII du RCS"""
    print("""
    🔵⚪ RACING CLUB DE STRASBOURG ⚪🔵
    ═══════════════════════════════════════
    
          🏟️  Stade de la Meinau  🏟️
    ═══════════════════════════════════════
    """)

def afficher_effectif_rcs():
    """Affiche l'effectif RCS 2024-2025"""
    
    effectif = {
        "Gardiens": [
            {"nom": "Matz Sels", "age": 32, "valeur": "4.0M€", "statut": "Titulaire"},
            {"nom": "Alaa Bellaarouch", "age": 20, "valeur": "0.5M€", "statut": "Remplaçant"}
        ],
        "Défenseurs": [
            {"nom": "Guela Doué", "age": 22, "valeur": "8.0M€", "statut": "Titulaire"},
            {"nom": "Abakar Sylla", "age": 25, "valeur": "3.5M€", "statut": "Titulaire"},
            {"nom": "Saïdou Sow", "age": 22, "valeur": "4.0M€", "statut": "Titulaire"},
            {"nom": "Mamadou Sarr", "age": 26, "valeur": "3.0M€", "statut": "Titulaire"},
            {"nom": "Marvin Senaya", "age": 22, "valeur": "2.5M€", "statut": "Remplaçant"},
            {"nom": "Ismaël Doukouré", "age": 23, "valeur": "2.0M€", "statut": "Remplaçant"}
        ],
        "Milieux": [
            {"nom": "Habib Diarra", "age": 20, "valeur": "12.0M€", "statut": "Titulaire"},
            {"nom": "Andrey Santos", "age": 20, "valeur": "8.0M€", "statut": "Titulaire"},
            {"nom": "Dilane Bakwa", "age": 21, "valeur": "10.0M€", "statut": "Titulaire"},
            {"nom": "Sebastian Nanasi", "age": 22, "valeur": "6.0M€", "statut": "Titulaire"},
            {"nom": "Caleb Wiley", "age": 19, "valeur": "4.0M€", "statut": "Remplaçant"},
            {"nom": "Pape Diong", "age": 20, "valeur": "1.5M€", "statut": "Remplaçant"}
        ],
        "Attaquants": [
            {"nom": "Emanuel Emegha", "age": 21, "valeur": "8.0M€", "statut": "Titulaire"},
            {"nom": "Félix Lemaréchal", "age": 19, "valeur": "4.0M€", "statut": "Remplaçant"},
            {"nom": "Abdoul Ouattara", "age": 18, "valeur": "2.0M€", "statut": "Remplaçant"},
            {"nom": "Moïse Sahi", "age": 18, "valeur": "1.0M€", "statut": "Remplaçant"},
            {"nom": "Jeremy Sebas", "age": 19, "valeur": "0.8M€", "statut": "Remplaçant"}
        ]
    }
    
    print("👥 EFFECTIF ACTUEL 2024-2025")
    print("═" * 50)
    
    total_joueurs = 0
    valeur_totale = 0.0
    age_total = 0
    
    for poste, joueurs in effectif.items():
        print(f"\n🏷️  {poste.upper()}")
        print("-" * 30)
        
        for joueur in joueurs:
            statut_icon = "⭐" if joueur["statut"] == "Titulaire" else "🔄"
            valeur_num = float(joueur["valeur"].replace("M€", ""))
            
            print(f"  {statut_icon} {joueur['nom']:<18} {joueur['age']:>2}ans  {joueur['valeur']:>6}")
            
            total_joueurs += 1
            valeur_totale += valeur_num
            age_total += joueur["age"]
    
    print("\n📊 STATISTIQUES GLOBALES")
    print("-" * 30)
    print(f"  👥 Total joueurs: {total_joueurs}")
    print(f"  💰 Valeur totale: {valeur_totale:.1f}M€")
    print(f"  📈 Âge moyen: {age_total/total_joueurs:.1f} ans")
    
    return effectif

def afficher_composition_ideale():
    """Affiche la composition idéale 4-2-3-1"""
    
    print("\n🎯 COMPOSITION IDÉALE - Formation 4-2-3-1")
    print("═" * 50)
    
    composition = {
        "Gardien": "Matz Sels",
        "Défense": ["Guela Doué", "Abakar Sylla", "Saïdou Sow", "Mamadou Sarr"],
        "Milieu défensif": ["Andrey Santos", "Habib Diarra"],
        "Milieu offensif": ["Dilane Bakwa", "Sebastian Nanasi", "Caleb Wiley"],
        "Attaque": ["Emanuel Emegha"]
    }
    
    print(f"🥅 Gardien:          {composition['Gardien']}")
    print(f"🛡️  Défense:          {' - '.join(composition['Défense'])}")
    print(f"⚙️  Milieu défensif:  {' - '.join(composition['Milieu défensif'])}")
    print(f"🎨 Milieu offensif:   {' - '.join(composition['Milieu offensif'])}")
    print(f"⚽ Attaque:          {composition['Attaque'][0]}")

def analyser_metriques_rcs():
    """Affiche les métriques football RCS"""
    
    print("\n📈 MÉTRIQUES FOOTBALL RCS")
    print("═" * 50)
    
    # Métriques exemple avec formules spécialisées RCS
    print("🎯 Expected Goals (xG) - Style contre-attaque RCS:")
    print("-" * 48)
    
    # Simulation xG Emanuel Emegha
    distance_emegha = 12  # mètres du but
    xg_base = max(0.05, 1.0 - (distance_emegha / 40))
    xg_contre_attaque = xg_base * 1.35  # Bonus style RCS
    xg_finisseur = xg_contre_attaque * 1.15  # Bonus Emegha
    
    print(f"  ⚽ Emanuel Emegha (surface, contre-attaque): {xg_finisseur:.3f}")
    
    # Simulation xG Dilane Bakwa
    distance_bakwa = 20  # mètres du but
    xg_base_bakwa = max(0.05, 1.0 - (distance_bakwa / 40))
    xg_bakwa = xg_base_bakwa * 1.10  # Bonus Bakwa
    
    print(f"  🎨 Dilane Bakwa (20m, pied gauche): {xg_bakwa:.3f}")
    
    print("\n📊 PPDA (Passes per Defensive Action):")
    print("-" * 40)
    passes_adverses = 450
    actions_defensives = 42
    ppda = passes_adverses / actions_defensives
    
    print(f"  🔄 PPDA équipe (pressing coordonné): {ppda:.1f}")
    print(f"  🎯 Objectif RCS: 8-12 PPDA (pressing moyen-haut)")
    
    style_pressing = "Coordonné" if 8 <= ppda <= 12 else "À ajuster"
    print(f"  📈 Style actuel: {style_pressing}")

def afficher_objectifs_saison():
    """Affiche les objectifs saison RCS"""
    
    print("\n🎯 OBJECTIFS SAISON 2024-2025")
    print("═" * 50)
    
    objectifs = [
        {"icone": "📍", "categorie": "Classement", "objectif": "Maintien confortable (14e-17e place)"},
        {"icone": "⚽", "categorie": "Attaque", "objectif": "45+ buts marqués (amélioration finition)"},
        {"icone": "🛡️", "categorie": "Défense", "objectif": "<55 buts encaissés (solidité)"},
        {"icone": "👥", "categorie": "Jeunes", "objectif": "Intégration 3+ talents centre formation"},
        {"icone": "💰", "categorie": "Budget", "objectif": "Optimisation masse salariale"},
        {"icone": "🏆", "categorie": "Coupe", "objectif": "Parcours honorable Coupe de France"}
    ]
    
    for obj in objectifs:
        print(f"  {obj['icone']} {obj['categorie']:<12} : {obj['objectif']}")

def afficher_scouting_cibles():
    """Affiche les cibles scouting RCS"""
    
    print("\n🎯 CIBLES SCOUTING PRIORITAIRES")
    print("═" * 50)
    
    cibles = [
        {"nom": "Quentin Boisgard", "age": 25, "poste": "MOC", "club": "Laval", "valeur": "3M€", "priorite": "HAUTE"},
        {"nom": "Gustavo Sá", "age": 23, "poste": "BU", "club": "FC Porto B", "valeur": "5M€", "priorite": "HAUTE"},
        {"nom": "Ellis Simms", "age": 23, "poste": "BU", "club": "Coventry", "valeur": "8M€", "priorite": "MOYENNE"},
        {"nom": "Mees Hilgers", "age": 23, "poste": "DC", "club": "FC Twente", "valeur": "12M€", "priorite": "MOYENNE"},
        {"nom": "Ryan Manning", "age": 28, "poste": "DG", "club": "Southampton", "valeur": "6M€", "priorite": "BASSE"}
    ]
    
    print("Contraintes budget RCS:")
    print("  💰 Transfert max: 15M€")
    print("  💵 Salaire max: 80k€/mois")
    print("  🎯 Âge optimal: 18-26 ans")
    print()
    
    for cible in cibles:
        priorite_icon = "🔴" if cible["priorite"] == "HAUTE" else "🟡" if cible["priorite"] == "MOYENNE" else "🟢"
        print(f"  {priorite_icon} {cible['nom']:<18} {cible['age']:>2}ans {cible['poste']:<4} {cible['club']:<15} {cible['valeur']:>5}")

def main():
    """Fonction principale du dashboard console RCS"""
    
    afficher_logo_rcs()
    
    print("📱 RACING CLUB DE STRASBOURG - Football Analytics")
    print("🔹 Version Console - Septembre 2025")
    print("🔹 Plateforme d'intelligence football spécialisée RCS")
    print()
    
    # Menu principal
    while True:
        print("\n🔵 MENU PRINCIPAL")
        print("=" * 30)
        print("1. 👥 Effectif actuel")
        print("2. 🎯 Composition idéale")
        print("3. 📈 Métriques football")
        print("4. 🎯 Objectifs saison")
        print("5. 🔍 Cibles scouting")
        print("6. 🌐 Lancer interface web")
        print("0. ❌ Quitter")
        
        choix = input("\n🔹 Votre choix: ").strip()
        
        if choix == "1":
            afficher_effectif_rcs()
        elif choix == "2":
            afficher_composition_ideale()
        elif choix == "3":
            analyser_metriques_rcs()
        elif choix == "4":
            afficher_objectifs_saison()
        elif choix == "5":
            afficher_scouting_cibles()
        elif choix == "6":
            print("\n🌐 Lancement interface web...")
            print("📋 Commande: streamlit run python_analytics/dashboards/dashboard_rcs.py --server.port 8502")
            print("🔗 URL: http://localhost:8502")
            break
        elif choix == "0":
            print("\n🔵⚪ Au revoir et allez Racing ! ⚪🔵")
            break
        else:
            print("\n❌ Choix invalide. Réessayez.")
        
        input("\n⏳ Appuyez sur Entrée pour continuer...")

if __name__ == "__main__":
    main()
