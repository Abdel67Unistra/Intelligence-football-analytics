# Instructions pour GitHub Copilot - Football Analytics Platform

<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

## Contexte du Projet
Ce projet est une plateforme d'intelligence football analytics qui combine :
- Analyse de données footballistiques (performances, tactiques, recrutement)
- Base de données PostgreSQL optimisée pour le sport
- Analytics Python avec modules spécialisés football
- Modèles prédictifs et visualisations R
- Dashboard interactif pour staff technique

## Standards de Code

### Python
- Utilisez pandas pour la manipulation de données football
- Implémentez les métriques football modernes (xG, xA, PPDA)
- Créez des classes pour Player, Team, Match avec méthodes spécialisées
- Utilisez Streamlit pour les dashboards interactifs
- Intégrez les APIs football (Football-Data.org, etc.)

### Base de Données
- Schéma PostgreSQL optimisé pour les requêtes d'agrégation
- Tables partitionnées par saison
- Index spécialisés pour analyses temporelles
- Vues matérialisées pour KPI temps réel

### R
- Scripts pour modèles prédictifs (résultats, blessures, valeurs)
- Visualisations avec ggplot2 (heatmaps, pass networks)
- Analyses factorielles et clustering de joueurs
- Rapports automatisés avec R Markdown

### Métriques Football
- xG (Expected Goals) et xA (Expected Assists)
- PPDA (Passes per Defensive Action)
- Heat maps et zones d'action
- Pass networks et analyses spatiales
- Métriques de pressing et possession

### APIs et Données
- Intégration Football-Data.org
- Scraping Transfermarkt pour valeurs marchandes
- Simulation données GPS/capteurs
- Gestion données temps réel matchs

Générez du code qui démontre une compréhension approfondie du football moderne et des analytics sportives.
