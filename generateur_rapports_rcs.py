"""
🔵⚪ Racing Club de Strasbourg - Système de Rapports Automatisés
===============================================================

Générateur de rapports automatisés pour le staff technique du RCS
avec analyses complètes, recommandations IA et export multi-format.

Auteur: GitHub Copilot
Date: Septembre 2025
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import warnings
import os
import json
from pathlib import Path
import base64
from io import BytesIO
warnings.filterwarnings('ignore')

# Configuration matplotlib pour les exports
plt.style.use('default')
sns.set_palette("husl")

class GenerateurRapportsRCS:
    """
    Générateur de rapports automatisés pour le Racing Club de Strasbourg
    """
    
    def __init__(self):
        self.couleurs_rcs = ['#0066CC', '#FFFFFF', '#FF6B35', '#87CEEB', '#4169E1']
        self.date_generation = datetime.now()
        self.saison = "2024-2025"
        
        # Répertoires de sortie
        self.repertoire_rapports = Path("rapports_rcs")
        self.repertoire_graphiques = Path("graphiques_rcs")
        
        # Création des répertoires si nécessaire
        self.repertoire_rapports.mkdir(exist_ok=True)
        self.repertoire_graphiques.mkdir(exist_ok=True)
        
    def charger_donnees_complete(self):
        """Charge toutes les données nécessaires pour les rapports"""
        
        # Import des modules (avec gestion d'erreur)
        try:
            from python_analytics.modules.collecteur_donnees_rcs import CollecteurDonneesRCS
            from python_analytics.modules.analyseur_rcs import AnalyseurPerformanceRCS
            from analytics_avances_rcs import AnalyticsAvancesRCS
        except ImportError:
            print("⚠️ Modules non disponibles - Génération de données simulées")
            return self._generer_donnees_simulees()
        
        print("📊 Chargement des données RCS complètes...")
        
        try:
            # Collecteurs de données
            collecteur = CollecteurDonneesRCS()
            analyseur = AnalyseurPerformanceRCS()
            analytics = AnalyticsAvancesRCS()
            
            # Chargement
            effectif = collecteur.recuperer_stats_joueurs_rcs()
            classement = collecteur.recuperer_classement_ligue1()
            
            # Analytics avancés
            analytics.charger_donnees_completes()
            
            donnees = {
                'effectif': effectif,
                'classement': classement,
                'analytics': analytics,
                'analyseur': analyseur
            }
            
            print("✅ Données chargées avec succès")
            return donnees
            
        except Exception as e:
            print(f"⚠️ Erreur lors du chargement: {e}")
            return self._generer_donnees_simulees()
    
    def _generer_donnees_simulees(self):
        """Génère des données simulées pour la démonstration"""
        print("🎭 Génération de données simulées RCS...")
        
        np.random.seed(42)
        
        # Effectif simulé
        noms_joueurs = [
            "Matz Sels", "Emanuel Emegha", "Habib Diarra", "Dilane Bakwa",
            "Sebastian Nanasi", "Guela Doué", "Abakar Sylla", "Saïdou Sow",
            "Andrey Santos", "Caleb Wiley", "Ismaël Doukouré", "Junior Mwanga",
            "Thomas Delaine", "Frédéric Guilbert", "Sékou Mara", "Félix Lemaréchal", "Jeremy Sebas"
        ]
        
        postes = ["GB", "BU", "MDC", "AD", "AG", "DD", "DC", "DC", "MDC", "DG", 
                 "MDC", "MC", "DG", "DD", "MOC", "MOC", "BU"]
        
        effectif = pd.DataFrame({
            'nom': noms_joueurs,
            'poste': postes,
            'age': np.random.randint(18, 35, len(noms_joueurs)),
            'note_moyenne': np.random.normal(6.5, 0.8, len(noms_joueurs)),
            'valeur_marche': np.random.exponential(3, len(noms_joueurs)),
            'matchs_joues': np.random.randint(5, 18, len(noms_joueurs)),
            'buts': np.random.poisson(2, len(noms_joueurs)),
            'passes_decisives': np.random.poisson(1.5, len(noms_joueurs)),
            'cartons_jaunes': np.random.poisson(2, len(noms_joueurs))
        })
        
        # Ajustement réaliste par poste
        for i, poste in enumerate(effectif['poste']):
            if poste == 'GB':
                effectif.loc[i, 'buts'] = 0
                effectif.loc[i, 'passes_decisives'] = 0
            elif poste in ['BU', 'MOC']:
                effectif.loc[i, 'buts'] *= 2
                effectif.loc[i, 'passes_decisives'] *= 1.5
        
        # Classement simulé
        classement = pd.DataFrame({
            'position': range(1, 19),
            'equipe': [
                'Paris Saint-Germain', 'AS Monaco', 'Olympique de Marseille', 'LOSC Lille',
                'OGC Nice', 'RC Lens', 'Olympique Lyonnais', 'Stade Rennais',
                'Stade Brestois', 'Racing Club de Strasbourg', 'Stade de Reims',
                'FC Nantes', 'Toulouse FC', 'Angers SCO', 'AS Saint-Étienne',
                'Le Havre AC', 'AJ Auxerre', 'Montpellier HSC'
            ],
            'pts': [45, 37, 35, 32, 30, 29, 28, 26, 25, 23, 22, 21, 20, 18, 16, 15, 14, 12],
            'j': [17] * 18,
            'diff': [31, 12, 8, 5, 3, 1, 0, -2, -3, -5, -6, -8, -10, -12, -15, -18, -20, -25]
        })
        
        return {
            'effectif': effectif,
            'classement': classement,
            'analytics': None,
            'analyseur': None
        }
    
    def generer_rapport_performance_equipe(self, donnees):
        """Génère un rapport de performance d'équipe complet"""
        
        print("📈 Génération du rapport de performance d'équipe...")
        
        effectif = donnees['effectif']
        classement = donnees['classement']
        
        # Métriques clés de l'équipe
        position_rcs = classement[classement['equipe'] == 'Racing Club de Strasbourg'].iloc[0]['position']
        points_rcs = classement[classement['equipe'] == 'Racing Club de Strasbourg'].iloc[0]['pts']
        
        metriques_equipe = {
            'position_actuelle': position_rcs,
            'points_actuels': points_rcs,
            'nb_joueurs': len(effectif),
            'age_moyen': effectif['age'].mean(),
            'note_moyenne_equipe': effectif['note_moyenne'].mean(),
            'valeur_totale_effectif': effectif['valeur_marche'].sum(),
            'buts_totaux': effectif['buts'].sum(),
            'passes_decisives_totales': effectif['passes_decisives'].sum()
        }
        
        # Analyses par poste
        analyses_poste = effectif.groupby('poste').agg({
            'note_moyenne': ['mean', 'std', 'count'],
            'age': 'mean',
            'valeur_marche': 'sum',
            'matchs_joues': 'mean'
        }).round(2)
        
        # Top et flop performers
        top_performers = effectif.nlargest(5, 'note_moyenne')[['nom', 'poste', 'note_moyenne']]
        joueurs_amelioration = effectif.nsmallest(3, 'note_moyenne')[['nom', 'poste', 'note_moyenne']]
        
        # Graphiques de performance
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=(
                "📊 Performance par poste",
                "👥 Répartition d'âge",
                "💰 Valeur par poste", 
                "⭐ Distribution des notes"
            ),
            specs=[[{"type": "bar"}, {"type": "histogram"}],
                   [{"type": "pie"}, {"type": "box"}]]
        )
        
        # 1. Performance par poste
        perf_poste = effectif.groupby('poste')['note_moyenne'].mean().sort_values(ascending=True)
        fig.add_trace(
            go.Bar(x=perf_poste.values, y=perf_poste.index, orientation='h',
                   marker_color=self.couleurs_rcs[0], name="Note moyenne"),
            row=1, col=1
        )
        
        # 2. Répartition d'âge
        fig.add_trace(
            go.Histogram(x=effectif['age'], nbinsx=10, marker_color=self.couleurs_rcs[1],
                        name="Distribution âge"),
            row=1, col=2
        )
        
        # 3. Valeur par poste
        valeur_poste = effectif.groupby('poste')['valeur_marche'].sum()
        fig.add_trace(
            go.Pie(labels=valeur_poste.index, values=valeur_poste.values,
                   name="Valeur par poste"),
            row=2, col=1
        )
        
        # 4. Distribution des notes
        for poste in effectif['poste'].unique()[:5]:  # Top 5 postes
            donnees_poste = effectif[effectif['poste'] == poste]
            fig.add_trace(
                go.Box(y=donnees_poste['note_moyenne'], name=poste),
                row=2, col=2
            )
        
        fig.update_layout(
            height=800,
            title_text=f"🔵⚪ Rapport Performance Équipe RCS - {self.date_generation.strftime('%d/%m/%Y')}",
            showlegend=True
        )
        
        # Sauvegarde du graphique
        chemin_graphique = self.repertoire_graphiques / f"performance_equipe_{self.date_generation.strftime('%Y%m%d')}.html"
        fig.write_html(str(chemin_graphique))
        
        rapport = {
            'type': 'performance_equipe',
            'date_generation': self.date_generation.isoformat(),
            'metriques_equipe': metriques_equipe,
            'analyses_poste': analyses_poste.to_dict(),
            'top_performers': top_performers.to_dict('records'),
            'joueurs_amelioration': joueurs_amelioration.to_dict('records'),
            'graphique_chemin': str(chemin_graphique)
        }
        
        return rapport
    
    def generer_rapport_scouting(self, donnees):
        """Génère un rapport de scouting et recrutement"""
        
        print("🎯 Génération du rapport de scouting...")
        
        effectif = donnees['effectif']
        
        # Analyse des besoins par poste
        besoins_poste = {}
        
        for poste in effectif['poste'].unique():
            joueurs_poste = effectif[effectif['poste'] == poste]
            
            besoins_poste[poste] = {
                'nb_joueurs': len(joueurs_poste),
                'age_moyen': joueurs_poste['age'].mean(),
                'note_moyenne': joueurs_poste['note_moyenne'].mean(),
                'valeur_moyenne': joueurs_poste['valeur_marche'].mean(),
                'besoin_recrutement': 'Élevé' if len(joueurs_poste) < 2 or joueurs_poste['note_moyenne'].mean() < 6.0 else 'Modéré'
            }
        
        # Profils de joueurs recommandés (simulés)
        np.random.seed(123)
        profils_recommandes = []
        
        postes_prioritaires = [poste for poste, info in besoins_poste.items() 
                              if info['besoin_recrutement'] == 'Élevé']
        
        for poste in postes_prioritaires[:5]:  # Top 5 besoins
            profil = {
                'poste_cible': poste,
                'age_ideal': np.random.randint(20, 26),
                'budget_estime': np.random.uniform(2, 12),  # Millions
                'note_minimale': 6.5,
                'experience_requise': 'Ligue 2 ou équivalent',
                'priorite': 'Haute' if besoins_poste[poste]['nb_joueurs'] < 2 else 'Moyenne'
            }
            profils_recommandes.append(profil)
        
        # Opportunités de marché (simulées)
        opportunites = [
            {
                'nom': f"Joueur A - {postes_prioritaires[0] if postes_prioritaires else 'MC'}",
                'club_actuel': 'FC Metz',
                'age': 23,
                'valeur_estimee': 4.5,
                'potentiel': 85,
                'disponibilite': 'Janvier 2025'
            },
            {
                'nom': f"Joueur B - {postes_prioritaires[1] if len(postes_prioritaires) > 1 else 'DC'}",
                'club_actuel': 'SC Bastia',
                'age': 21,
                'valeur_estimee': 2.8,
                'potentiel': 78,
                'disponibilite': 'Été 2025'
            }
        ]
        
        # Graphique d'analyse des besoins
        fig_besoins = go.Figure()
        
        postes = list(besoins_poste.keys())
        notes_moyennes = [besoins_poste[p]['note_moyenne'] for p in postes]
        nb_joueurs = [besoins_poste[p]['nb_joueurs'] for p in postes]
        
        fig_besoins.add_trace(
            go.Scatter(
                x=notes_moyennes, y=nb_joueurs,
                mode='markers+text',
                text=postes,
                textposition="top center",
                marker=dict(
                    size=[besoins_poste[p]['valeur_moyenne'] * 3 for p in postes],
                    color=[1 if besoins_poste[p]['besoin_recrutement'] == 'Élevé' else 0 for p in postes],
                    colorscale='RdYlGn_r',
                    showscale=True,
                    colorbar=dict(title="Besoin Recrutement")
                )
            )
        )
        
        fig_besoins.update_layout(
            title="🎯 Analyse des besoins de recrutement par poste",
            xaxis_title="Note moyenne du poste",
            yaxis_title="Nombre de joueurs",
            height=500
        )
        
        # Sauvegarde
        chemin_graphique = self.repertoire_graphiques / f"scouting_analyse_{self.date_generation.strftime('%Y%m%d')}.html"
        fig_besoins.write_html(str(chemin_graphique))
        
        rapport = {
            'type': 'scouting',
            'date_generation': self.date_generation.isoformat(),
            'besoins_poste': besoins_poste,
            'profils_recommandes': profils_recommandes,
            'opportunites_marche': opportunites,
            'budget_total_estime': sum([p['budget_estime'] for p in profils_recommandes]),
            'graphique_chemin': str(chemin_graphique)
        }
        
        return rapport
    
    def generer_rapport_medical(self, donnees):
        """Génère un rapport médical et de condition physique"""
        
        print("🏥 Génération du rapport médical...")
        
        effectif = donnees['effectif']
        
        # Simulation de données médicales
        np.random.seed(456)
        
        donnees_medicales = effectif.copy()
        donnees_medicales['fatigue_score'] = np.random.uniform(0.2, 0.9, len(effectif))
        donnees_medicales['risque_blessure'] = np.random.uniform(0.1, 0.8, len(effectif))
        donnees_medicales['jours_depuis_blessure'] = np.random.randint(0, 200, len(effectif))
        donnees_medicales['condition_physique'] = np.random.uniform(70, 95, len(effectif))
        
        # Classification des risques
        donnees_medicales['niveau_risque'] = pd.cut(
            donnees_medicales['risque_blessure'],
            bins=[0, 0.3, 0.6, 1.0],
            labels=['🟢 Faible', '🟡 Modéré', '🔴 Élevé']
        )
        
        # Recommandations automatiques
        recommandations = []
        
        for _, joueur in donnees_medicales.iterrows():
            if joueur['fatigue_score'] > 0.8:
                recommandations.append({
                    'joueur': joueur['nom'],
                    'type': 'Repos',
                    'urgence': 'Haute',
                    'description': f"Fatigue élevée ({joueur['fatigue_score']:.1%}) - Repos recommandé"
                })
            
            if joueur['risque_blessure'] > 0.7:
                recommandations.append({
                    'joueur': joueur['nom'],
                    'type': 'Prévention',
                    'urgence': 'Haute',
                    'description': f"Risque de blessure élevé - Suivi médical renforcé"
                })
            
            if joueur['condition_physique'] < 75:
                recommandations.append({
                    'joueur': joueur['nom'],
                    'type': 'Préparation',
                    'urgence': 'Moyenne',
                    'description': f"Condition physique à améliorer ({joueur['condition_physique']:.0f}%)"
                })
        
        # Statistiques médicales
        stats_medicales = {
            'joueurs_risque_eleve': len(donnees_medicales[donnees_medicales['niveau_risque'] == '🔴 Élevé']),
            'fatigue_moyenne_equipe': donnees_medicales['fatigue_score'].mean(),
            'condition_moyenne_equipe': donnees_medicales['condition_physique'].mean(),
            'jours_moyen_depuis_blessure': donnees_medicales['jours_depuis_blessure'].mean()
        }
        
        # Graphique médical
        fig_medical = make_subplots(
            rows=1, cols=2,
            subplot_titles=("🏥 Risques de blessure", "🔋 Condition physique"),
            specs=[[{"type": "bar"}, {"type": "scatter"}]]
        )
        
        # Risques par niveau
        risques_count = donnees_medicales['niveau_risque'].value_counts()
        fig_medical.add_trace(
            go.Bar(x=risques_count.index, y=risques_count.values,
                   marker_color=['green', 'orange', 'red'], name="Niveaux de risque"),
            row=1, col=1
        )
        
        # Condition physique vs fatigue
        fig_medical.add_trace(
            go.Scatter(
                x=donnees_medicales['condition_physique'],
                y=donnees_medicales['fatigue_score'],
                mode='markers+text',
                text=donnees_medicales['nom'].str[:8],
                textposition="top center",
                marker=dict(
                    size=10,
                    color=donnees_medicales['risque_blessure'],
                    colorscale='RdYlGn_r',
                    showscale=True
                ),
                name="Joueurs"
            ),
            row=1, col=2
        )
        
        fig_medical.update_layout(
            height=500,
            title_text="🏥 Rapport Médical - État de l'effectif RCS"
        )
        
        # Sauvegarde
        chemin_graphique = self.repertoire_graphiques / f"rapport_medical_{self.date_generation.strftime('%Y%m%d')}.html"
        fig_medical.write_html(str(chemin_graphique))
        
        rapport = {
            'type': 'medical',
            'date_generation': self.date_generation.isoformat(),
            'donnees_medicales': donnees_medicales.to_dict('records'),
            'stats_medicales': stats_medicales,
            'recommandations': recommandations,
            'graphique_chemin': str(chemin_graphique)
        }
        
        return rapport
    
    def generer_rapport_complet(self, donnees):
        """Génère un rapport exécutif complet"""
        
        print("📋 Génération du rapport exécutif complet...")
        
        # Génération de tous les sous-rapports
        rapport_performance = self.generer_rapport_performance_equipe(donnees)
        rapport_scouting = self.generer_rapport_scouting(donnees)
        rapport_medical = self.generer_rapport_medical(donnees)
        
        # Synthèse exécutive
        synthese = {
            'resume_executif': {
                'position_ligue1': rapport_performance['metriques_equipe']['position_actuelle'],
                'points_actuels': rapport_performance['metriques_equipe']['points_actuels'],
                'note_moyenne_equipe': round(rapport_performance['metriques_equipe']['note_moyenne_equipe'], 2),
                'valeur_effectif': round(rapport_performance['metriques_equipe']['valeur_totale_effectif'], 1),
                'joueurs_risque_medical': rapport_medical['stats_medicales']['joueurs_risque_eleve'],
                'besoins_recrutement': len(rapport_scouting['profils_recommandes'])
            },
            
            'points_cles': [
                f"🏆 Position: {rapport_performance['metriques_equipe']['position_actuelle']}ème en Ligue 1",
                f"⭐ Performance: Note équipe {rapport_performance['metriques_equipe']['note_moyenne_equipe']:.2f}/10",
                f"💰 Valeur: {rapport_performance['metriques_equipe']['valeur_totale_effectif']:.1f}M€ d'effectif",
                f"🏥 Santé: {rapport_medical['stats_medicales']['joueurs_risque_eleve']} joueur(s) à risque",
                f"🎯 Recrutement: {len(rapport_scouting['profils_recommandes'])} besoin(s) identifié(s)"
            ],
            
            'recommandations_strategiques': [
                "🎯 Priorité au maintien en Ligue 1 avec l'effectif actuel",
                "📈 Améliorer les performances offensives (moyenne d'équipe)",
                "🏥 Surveillance médicale renforcée des joueurs à risque",
                "💰 Recrutement ciblé sur les postes en déficit",
                "👥 Développer les jeunes talents du centre de formation"
            ]
        }
        
        # Compilation du rapport complet
        rapport_complet = {
            'type': 'rapport_complet',
            'date_generation': self.date_generation.isoformat(),
            'saison': self.saison,
            'synthese_executive': synthese,
            'rapport_performance': rapport_performance,
            'rapport_scouting': rapport_scouting,
            'rapport_medical': rapport_medical,
            'prochaines_actions': [
                "📅 Planifier la rotation pour réduire la fatigue",
                "🎯 Identifier les cibles de mercato hivernal",
                "📊 Analyser les performances post-match suivant",
                "🏥 Programmer les bilans médicaux complets"
            ]
        }
        
        return rapport_complet
    
    def exporter_rapport_json(self, rapport, nom_fichier=None):
        """Exporte un rapport en format JSON"""
        
        if nom_fichier is None:
            nom_fichier = f"rapport_rcs_{rapport['type']}_{self.date_generation.strftime('%Y%m%d_%H%M')}.json"
        
        chemin_fichier = self.repertoire_rapports / nom_fichier
        
        with open(chemin_fichier, 'w', encoding='utf-8') as f:
            json.dump(rapport, f, ensure_ascii=False, indent=2, default=str)
        
        print(f"📄 Rapport JSON exporté: {chemin_fichier}")
        return str(chemin_fichier)
    
    def exporter_rapport_html(self, rapport, nom_fichier=None):
        """Exporte un rapport en format HTML"""
        
        if nom_fichier is None:
            nom_fichier = f"rapport_rcs_{rapport['type']}_{self.date_generation.strftime('%Y%m%d_%H%M')}.html"
        
        chemin_fichier = self.repertoire_rapports / nom_fichier
        
        # Template HTML simple
        html_template = f"""
        <!DOCTYPE html>
        <html lang="fr">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Rapport RCS - {rapport['type'].title()}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; color: #333; }}
                .header {{ background: linear-gradient(90deg, #0066CC, #4169E1); color: white; padding: 20px; border-radius: 10px; text-align: center; }}
                .section {{ margin: 20px 0; padding: 15px; border-left: 4px solid #0066CC; background: #f8f9fa; }}
                .metric {{ display: inline-block; margin: 10px; padding: 10px; background: white; border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
                table {{ width: 100%; border-collapse: collapse; margin: 10px 0; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #0066CC; color: white; }}
                .alert {{ padding: 10px; margin: 10px 0; border-radius: 5px; }}
                .alert-info {{ background: #d1ecf1; border: 1px solid #bee5eb; }}
                .alert-warning {{ background: #fff3cd; border: 1px solid #ffeaa7; }}
                .footer {{ text-align: center; margin-top: 40px; color: #666; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🔵⚪ Racing Club de Strasbourg</h1>
                <h2>Rapport {rapport['type'].title()}</h2>
                <p>Généré le {self.date_generation.strftime('%d/%m/%Y à %H:%M:%S')}</p>
            </div>
        """
        
        # Contenu selon le type de rapport
        if rapport['type'] == 'rapport_complet':
            html_template += self._generer_html_rapport_complet(rapport)
        elif rapport['type'] == 'performance_equipe':
            html_template += self._generer_html_performance(rapport)
        elif rapport['type'] == 'scouting':
            html_template += self._generer_html_scouting(rapport)
        elif rapport['type'] == 'medical':
            html_template += self._generer_html_medical(rapport)
        
        html_template += """
            <div class="footer">
                <p>🔵⚪ Racing Club de Strasbourg Analytics Platform - Saison 2024-2025</p>
                <p>Rapport généré automatiquement</p>
            </div>
        </body>
        </html>
        """
        
        with open(chemin_fichier, 'w', encoding='utf-8') as f:
            f.write(html_template)
        
        print(f"📄 Rapport HTML exporté: {chemin_fichier}")
        return str(chemin_fichier)
    
    def _generer_html_rapport_complet(self, rapport):
        """Génère le HTML pour un rapport complet"""
        
        synthese = rapport['synthese_executive']
        
        html = f"""
        <div class="section">
            <h3>📊 Résumé Exécutif</h3>
            <div class="metric">🏆 Position: {synthese['resume_executif']['position_ligue1']}ème</div>
            <div class="metric">⭐ Note équipe: {synthese['resume_executif']['note_moyenne_equipe']}/10</div>
            <div class="metric">💰 Valeur: {synthese['resume_executif']['valeur_effectif']}M€</div>
            <div class="metric">🏥 Risques: {synthese['resume_executif']['joueurs_risque_medical']} joueur(s)</div>
        </div>
        
        <div class="section">
            <h3>🎯 Points Clés</h3>
            <ul>
        """
        
        for point in synthese['points_cles']:
            html += f"<li>{point}</li>"
        
        html += """
            </ul>
        </div>
        
        <div class="section">
            <h3>💡 Recommandations Stratégiques</h3>
            <ul>
        """
        
        for recommandation in synthese['recommandations_strategiques']:
            html += f"<li>{recommandation}</li>"
        
        html += """
            </ul>
        </div>
        
        <div class="alert alert-info">
            <h4>📅 Prochaines Actions</h4>
            <ul>
        """
        
        for action in rapport['prochaines_actions']:
            html += f"<li>{action}</li>"
        
        html += "</ul></div>"
        
        return html
    
    def _generer_html_performance(self, rapport):
        """Génère le HTML pour un rapport de performance"""
        
        metriques = rapport['metriques_equipe']
        
        return f"""
        <div class="section">
            <h3>📊 Métriques Équipe</h3>
            <div class="metric">👥 Joueurs: {metriques['nb_joueurs']}</div>
            <div class="metric">🎂 Âge moyen: {metriques['age_moyen']:.1f} ans</div>
            <div class="metric">⚽ Buts totaux: {metriques['buts_totaux']}</div>
            <div class="metric">🎯 Passes décisives: {metriques['passes_decisives_totales']}</div>
        </div>
        
        <div class="section">
            <h3>⭐ Top Performers</h3>
            <table>
                <tr><th>Joueur</th><th>Poste</th><th>Note</th></tr>
        """ + "".join([
            f"<tr><td>{p['nom']}</td><td>{p['poste']}</td><td>{p['note_moyenne']:.2f}</td></tr>"
            for p in rapport['top_performers']
        ]) + """
            </table>
        </div>
        """
    
    def _generer_html_scouting(self, rapport):
        """Génère le HTML pour un rapport de scouting"""
        
        return f"""
        <div class="section">
            <h3>🎯 Profils Recommandés</h3>
            <table>
                <tr><th>Poste</th><th>Âge Idéal</th><th>Budget</th><th>Priorité</th></tr>
        """ + "".join([
            f"<tr><td>{p['poste_cible']}</td><td>{p['age_ideal']}</td><td>{p['budget_estime']:.1f}M€</td><td>{p['priorite']}</td></tr>"
            for p in rapport['profils_recommandes']
        ]) + f"""
            </table>
            <p><strong>Budget total estimé:</strong> {rapport['budget_total_estime']:.1f}M€</p>
        </div>
        
        <div class="section">
            <h3>💎 Opportunités Marché</h3>
            <table>
                <tr><th>Joueur</th><th>Club</th><th>Âge</th><th>Valeur</th><th>Disponibilité</th></tr>
        """ + "".join([
            f"<tr><td>{o['nom']}</td><td>{o['club_actuel']}</td><td>{o['age']}</td><td>{o['valeur_estimee']}M€</td><td>{o['disponibilite']}</td></tr>"
            for o in rapport['opportunites_marche']
        ]) + """
            </table>
        </div>
        """
    
    def _generer_html_medical(self, rapport):
        """Génère le HTML pour un rapport médical"""
        
        stats = rapport['stats_medicales']
        
        html = f"""
        <div class="section">
            <h3>🏥 Statistiques Médicales</h3>
            <div class="metric">🔴 Risque élevé: {stats['joueurs_risque_eleve']} joueur(s)</div>
            <div class="metric">🔋 Fatigue moyenne: {stats['fatigue_moyenne_equipe']:.1%}</div>
            <div class="metric">💪 Condition moyenne: {stats['condition_moyenne_equipe']:.1f}%</div>
        </div>
        
        <div class="section">
            <h3>⚠️ Recommandations Médicales</h3>
        """
        
        for rec in rapport['recommandations']:
            urgence_class = "alert-warning" if rec['urgence'] == 'Haute' else "alert-info"
            html += f'<div class="alert {urgence_class}"><strong>{rec["joueur"]}</strong> - {rec["description"]}</div>'
        
        html += "</div>"
        
        return html
    
    def generer_tous_rapports(self):
        """Génère tous les types de rapports"""
        
        print("🔵⚪ GÉNÉRATION COMPLÈTE DES RAPPORTS RCS")
        print("=" * 50)
        
        # Chargement des données
        donnees = self.charger_donnees_complete()
        
        if donnees is None:
            print("❌ Impossible de charger les données")
            return None
        
        # Génération de tous les rapports
        rapport_complet = self.generer_rapport_complet(donnees)
        
        # Exports
        fichiers_generes = {}
        
        # JSON
        fichiers_generes['json'] = self.exporter_rapport_json(rapport_complet)
        
        # HTML
        fichiers_generes['html'] = self.exporter_rapport_html(rapport_complet)
        
        # Rapports individuels
        for sous_rapport_type in ['performance_equipe', 'scouting', 'medical']:
            sous_rapport = rapport_complet[f'rapport_{sous_rapport_type}']
            fichiers_generes[f'{sous_rapport_type}_json'] = self.exporter_rapport_json(sous_rapport)
            fichiers_generes[f'{sous_rapport_type}_html'] = self.exporter_rapport_html(sous_rapport)
        
        print("\n✅ RAPPORTS GÉNÉRÉS AVEC SUCCÈS !")
        print("=" * 50)
        print(f"📁 Répertoire rapports: {self.repertoire_rapports}")
        print(f"📊 Répertoire graphiques: {self.repertoire_graphiques}")
        print(f"📄 Fichiers générés: {len(fichiers_generes)}")
        
        for nom, chemin in fichiers_generes.items():
            print(f"   • {nom}: {Path(chemin).name}")
        
        print("\n🔵⚪ ALLEZ RACING ! ⚪🔵")
        
        return {
            'rapport_complet': rapport_complet,
            'fichiers_generes': fichiers_generes
        }

def main():
    """Fonction principale pour génération des rapports"""
    
    generateur = GenerateurRapportsRCS()
    resultats = generateur.generer_tous_rapports()
    
    return resultats

if __name__ == "__main__":
    main()
