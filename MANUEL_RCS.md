# Manuel d'Utilisation - Football Analytics RCS
## Racing Club de Strasbourg Intelligence Platform

> **Version spécialisée pour le Racing Club de Strasbourg**  
> Code entièrement en français - Analytics football professionnelles

---

## 🔵⚪ Aperçu de la Plateforme

Cette plateforme d'intelligence football a été spécialement adaptée pour le **Racing Club de Strasbourg**. Elle combine des analyses de performance avancées, un moteur de scouting intelligent et des métriques football modernes pour accompagner le staff technique dans ses décisions.

### ⚡ Fonctionnalités Principales

1. **📊 Analyses de Performance RCS**
   - Suivi de l'effectif actuel 2024-2025 (19 joueurs)
   - Métriques individuelles et collectives
   - Analyses de forme et tendances
   - Comparaisons avec objectifs club

2. **🎯 Moteur de Scouting Intelligent**
   - Budget adapté RCS (max 15M€ par transfert)
   - Base de données 200+ joueurs ciblés
   - Ligues prioritaires: Ligue 2, Championship, Eredivisie
   - Recommandations personnalisées

3. **📈 Métriques Football Modernes**
   - xG/xA optimisés style RCS (contre-attaque)
   - PPDA et métriques de pressing
   - Bonus finisseurs RCS (Emegha, Bakwa...)
   - Analyses spatiales et heat maps

4. **🎮 Dashboard Interactif**
   - Interface aux couleurs du club (#0066CC)
   - 7 sections spécialisées
   - Visualisations temps réel
   - Rapports automatisés

---

## 🚀 Installation et Lancement

### Prérequis
```bash
pip install streamlit pandas plotly numpy
```

### Lancement Rapide
```bash
# Option 1: Script automatique
python lancer_rcs.py

# Option 2: Commande directe
streamlit run python_analytics/dashboards/dashboard_rcs.py --server.port 8502
```

### Accès
- **URL locale**: http://localhost:8502
- **Version en ligne**: https://football-analytics-platform-2025.streamlit.app

---

## 📋 Guide des Modules

### 1. **Analyseur RCS** (`analyseur_rcs.py`)

**Effectif Actuel 2024-2025:**
- **Gardiens**: Matz Sels, Alaa Bellaarouch
- **Défenseurs**: Guela Doué, Abakar Sylla, Saïdou Sow, Mamadou Sarr, Marvin Senaya, Ismaël Doukouré
- **Milieux**: Habib Diarra, Andrey Santos, Dilane Bakwa, Sebastian Nanasi, Caleb Wiley, Pape Diong
- **Attaquants**: Emanuel Emegha, Félix Lemaréchal, Abdoul Ouattara, Moïse Sahi, Jeremy Sebas

**Fonctions Principales:**
```python
analyseur = AnalyseurPerformanceRCS()

# Obtenir l'effectif
effectif = analyseur.obtenir_effectif_actuel()

# Analyser la forme d'un joueur
forme = analyseur.analyser_forme_joueur_rcs("Emanuel Emegha")

# Projeter la composition
compo = analyseur.projeter_composition_ideale()
```

### 2. **Moteur Scouting** (`moteur_scouting_rcs.py`)

**Contraintes Budgétaires:**
- Transfert max: 15M€
- Salaire max: 80k€/mois
- Âge optimal: 18-26 ans

**Cibles Prioritaires Intégrées:**
- **Ligue 2**: Quentin Boisgard, Gustavo Sá, Ilyes Hamache
- **Championship**: Ellis Simms, Ryan Manning, Ethan Laird
- **Eredivisie**: Milan van Ewijk, Mees Hilgers

**Utilisation:**
```python
scouting = MoteurScoutingRCS()

# Rechercher des cibles
cibles = scouting.rechercher_cibles_prioritaires()

# Analyser un joueur spécifique
rapport = scouting.generer_rapport_cible("Quentin Boisgard")
```

### 3. **Métriques Football** (`metriques_rcs.py`)

**Formules Spécialisées RCS:**

**Expected Goals (xG):**
- Bonus contre-attaque: +35%
- Bonus finisseurs RCS:
  - Emanuel Emegha: +15%
  - Dilane Bakwa: +10%
  - Habib Diarra: +8%

**PPDA (Passes per Defensive Action):**
- Style RCS: Pressing coordonné moyen-haut
- Objectif: 8-12 PPDA

**Utilisation:**
```python
metriques = MetriquesFootballRCS()

# Calculer xG d'un tir
xg = metriques.calculer_xg_tir(85, 50, "contre_attaque", "pied_droit", "Emanuel Emegha")

# Calculer xA d'une passe
xa = metriques.calculer_xa_passe(70, 25, 88, 45, "passe_cle", "Dilane Bakwa")

# PPDA équipe
ppda = metriques.calculer_ppda_equipe(450, 38)
```

---

## 🎮 Guide du Dashboard

### Section 1: **Tableau de Bord Principal**
- KPI temps réel de l'équipe
- Objectifs saison (maintien confortable)
- Indicateurs de performance globaux

### Section 2: **Gestion Effectif**
- Vue d'ensemble 19 joueurs
- Statuts (titulaire, remplaçant, blessé)
- Valeurs marchandes actualisées

### Section 3: **Analyse Joueur Individuelle**
- Sélection par nom de joueur
- Métriques détaillées
- Évolution forme et performance

### Section 4: **Performance Match**
- Analyses post-match
- Métriques collectives xG/xA
- Heat maps et zones d'action

### Section 5: **Scouting Intelligence**
- Recherche par poste et budget
- Comparaisons avec effectif actuel
- Recommandations adaptées RCS

### Section 6: **Analyses Tactiques**
- Formation 4-2-3-1 optimisée
- Pressing et transitions
- Statistiques défensives

### Section 7: **Rapports Automatisés**
- Rapports pré-match
- Bilans post-match
- Résumés hebdomadaires

---

## 📊 Scripts R Complémentaires

Le script `analyses_rcs.R` fournit:

### Modèles Prédictifs
- **Prédiction résultats**: Probabilités victoire/nul/défaite adaptées niveau RCS
- **Projection classement**: Estimation maintien (objectif 14e-17e place)
- **Analyse opposition**: Tendances contre différents styles

### Visualisations Avancées
- **Pass networks**: Réseaux de passes aux couleurs RCS
- **Heat maps**: Zones d'activité par joueur
- **Progression saisonnière**: Évolution performance

**Lancement R:**
```r
source("/Users/cheriet/Documents/augment-projects/stat/r_analytics/scripts/analyses_rcs.R")
```

---

## ⚙️ Configuration Avancée

### Personnalisation Métriques
```python
# Dans metriques_rcs.py
BONUS_FINISSEURS_RCS = {
    "Emanuel Emegha": 1.15,    # Buteur principal
    "Dilane Bakwa": 1.10,      # Ailier technique 
    "Habib Diarra": 1.08       # Milieu polyvalent
}

COEFFICIENT_CONTRE_ATTAQUE = 1.35  # Style RCS
```

### Adaptation Budget Scouting
```python
# Dans moteur_scouting_rcs.py
BUDGET_MAX_TRANSFERT = 15_000_000      # 15M€
SALAIRE_MAX_MENSUEL = 80_000           # 80k€/mois
LIGUES_PRIORITAIRES = ["Ligue 2", "Championship", "Eredivisie"]
```

---

## 🔧 Tests et Validation

### Tests Automatisés
```bash
# Test complet des modules
python test_modules_rcs.py

# Test simplifié
python test_simple_rcs.py
```

### Validation Données
- Effectif RCS vérifié au 15/01/2025
- Valeurs marchandes Transfermarkt
- Budgets réalistes club

---

## 📱 Support et Contact

### Documentation Technique
- Code source: `/python_analytics/modules/`
- Tests: `/test_modules_rcs.py`
- Déploiement: `/deploy_rcs.sh`

### Mise à Jour
Le système se met à jour automatiquement avec:
- Transferts RCS (mercatos)
- Nouvelles métriques
- Ajustements tactiques

---

## 🎯 Prochaines Évolutions

1. **Intégration APIs réelles**
   - Football-Data.org
   - Données officielles RCS
   - APIs transferts temps réel

2. **Analyses avancées**
   - Modèles ML blessures
   - Prédictions résultats
   - Optimisation compositions

3. **Interface mobile**
   - Application dédiée
   - Notifications temps réel
   - Synchronisation staff

---

**Racing Club de Strasbourg - Football Analytics Platform**  
*"L'intelligence au service de la performance"* 🔵⚪
