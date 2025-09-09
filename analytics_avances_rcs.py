"""
🔵⚪ Racing Club de Strasbourg - Analytics Avancés
=================================================

Module principal d'analyses avancées combinant Python et R
pour des insights footballistiques de niveau professionnel.

Auteur: GitHub Copilot
Date: Septembre 2025
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
from plotly.subplots import make_subplots
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor, GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, classification_report
import warnings
warnings.filterwarnings('ignore')

from config_rcs import config_rcs, metriques
from python_analytics.modules.collecteur_donnees_rcs import CollecteurDonneesRCS
from python_analytics.modules.analyseur_rcs import AnalyseurPerformanceRCS

class AnalyticsAvancesRCS:
    """
    Système d'analytics avancés pour le Racing Club de Strasbourg
    Combinant analyses statistiques, machine learning et visualisations interactives
    """
    
    def __init__(self):
        self.collecteur = CollecteurDonneesRCS()
        self.analyseur = AnalyseurPerformanceRCS()
        self.couleurs_rcs = [config_rcs.couleur_primaire, config_rcs.couleur_secondaire, 
                            config_rcs.couleur_accent, "#87CEEB", "#4169E1"]
        
        # Initialisation des données
        self.effectif = None
        self.performances = None
        self.metriques_avancees = None
        
    def charger_donnees_completes(self):
        """Charge toutes les données nécessaires pour les analyses"""
        print("📊 Chargement des données RCS...")
        
        # Données de base
        self.effectif = self.collecteur.recuperer_stats_joueurs_rcs()
        self.classement = self.collecteur.recuperer_classement_ligue1()
        
        # Génération de données de performance enrichies
        self.performances = self._generer_donnees_performance()
        self.metriques_avancees = self._calculer_metriques_avancees()
        
        print("✅ Données chargées avec succès")
        
    def _generer_donnees_performance(self):
        """Génère des données de performance réalistes pour les analyses"""
        np.random.seed(42)  # Reproductibilité
        
        performances = []
        
        for _, joueur in self.effectif.iterrows():
            # Génération de 10 derniers matchs
            for match in range(10):
                perf = {
                    'joueur': joueur['nom'],
                    'poste': joueur['poste'],
                    'match': f"J{17-match}",
                    'minutes': np.random.choice([0, 30, 45, 60, 75, 90], 
                                              p=[0.1, 0.05, 0.05, 0.1, 0.2, 0.5]),
                    'note': max(4.0, min(9.0, np.random.normal(joueur['note_moyenne'], 0.8))),
                    'distance_parcourue': np.random.normal(8500, 1200) if joueur['poste'] != 'GB' else np.random.normal(4000, 500),
                    'sprints': np.random.poisson(12) if joueur['poste'] != 'GB' else np.random.poisson(3),
                    'duels_gagnes': np.random.binomial(15, 0.6),
                    'passes_reussies': np.random.binomial(50, 0.85),
                    'centres_reussis': np.random.binomial(8, 0.3) if joueur['poste'] in ['AD', 'AG'] else np.random.binomial(3, 0.2),
                    'tirs': np.random.poisson(2) if joueur['poste'] in ['BU', 'MOC'] else np.random.poisson(0.5),
                    'interceptions': np.random.poisson(3) if joueur['poste'] in ['DC', 'MDC'] else np.random.poisson(1),
                    'fatigue': np.random.uniform(0.1, 0.9)
                }
                performances.append(perf)
                
        return pd.DataFrame(performances)
    
    def _calculer_metriques_avancees(self):
        """Calcule des métriques avancées personnalisées RCS"""
        metriques = {}
        
        for _, joueur in self.effectif.iterrows():
            perf_joueur = self.performances[self.performances['joueur'] == joueur['nom']]
            
            # Métriques de forme
            forme_recente = perf_joueur.tail(5)['note'].mean()
            regularite = 1 - (perf_joueur['note'].std() / perf_joueur['note'].mean())
            
            # Métriques physiques
            endurance = perf_joueur['distance_parcourue'].mean()
            intensite = perf_joueur['sprints'].mean()
            
            # Métriques techniques par poste
            if joueur['poste'] == 'GB':
                efficacite = np.random.uniform(0.75, 0.92)  # % arrêts
            elif joueur['poste'] in ['DC', 'DD', 'DG']:
                efficacite = perf_joueur['duels_gagnes'].mean() / 15  # % duels gagnés
            elif joueur['poste'] in ['MDC', 'MC', 'MOC']:
                efficacite = perf_joueur['passes_reussies'].mean() / 50  # % passes
            else:  # Attaquants
                efficacite = perf_joueur['tirs'].mean() * 0.15  # Dangerosité
            
            # Score composite RCS
            score_rcs = (forme_recente * 0.4 + regularite * 0.2 + 
                        (efficacite * 10) * 0.25 + (endurance/10000) * 0.15)
            
            metriques[joueur['nom']] = {
                'forme_recente': forme_recente,
                'regularite': regularite,
                'endurance': endurance,
                'intensite': intensite,
                'efficacite': efficacite,
                'score_rcs': score_rcs,
                'potentiel': self._evaluer_potentiel(joueur, perf_joueur),
                'valeur_estimee': self._estimer_valeur_marche(joueur, score_rcs)
            }
            
        return metriques
    
    def _evaluer_potentiel(self, joueur, performances):
        """Évalue le potentiel d'évolution d'un joueur"""
        age = joueur['age']
        poste = joueur['poste']
        progression = performances['note'].tail(5).mean() - performances['note'].head(5).mean()
        
        # Facteurs par âge
        if age <= 20:
            facteur_age = 0.9  # Très haut potentiel
        elif age <= 25:
            facteur_age = 0.7  # Bon potentiel
        elif age <= 28:
            facteur_age = 0.4  # Potentiel modéré
        else:
            facteur_age = 0.1  # Potentiel limité
            
        # Facteurs par poste (pic de forme)
        facteurs_poste = {
            'GB': 0.6, 'DC': 0.5, 'DD': 0.7, 'DG': 0.7,
            'MDC': 0.6, 'MC': 0.8, 'MOC': 0.9, 'AD': 0.8, 'AG': 0.8, 'BU': 0.7
        }
        
        potentiel = (facteur_age * facteurs_poste.get(poste, 0.5) * 
                    (1 + max(0, progression))) * 100
        
        return min(95, max(10, potentiel))
    
    def _estimer_valeur_marche(self, joueur, score_rcs):
        """Estime la valeur marchande actuelle d'un joueur"""
        base = joueur['valeur_marche']
        age = joueur['age']
        
        # Facteur de performance
        facteur_perf = score_rcs / 7  # Normalisation
        
        # Facteur d'âge
        if age <= 22:
            facteur_age = 1.2
        elif age <= 26:
            facteur_age = 1.1
        elif age <= 29:
            facteur_age = 0.9
        else:
            facteur_age = 0.7
            
        valeur_estimee = base * facteur_perf * facteur_age
        return round(valeur_estimee, 1)
    
    def creer_dashboard_performance(self):
        """Crée un dashboard interactif de performance d'équipe"""
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=(
                "🎯 Forme Récente par Poste",
                "⚡ Intensité vs Endurance", 
                "📈 Évolution des Notes",
                "💎 Potentiel vs Valeur Marchande"
            ),
            specs=[[{"type": "bar"}, {"type": "scatter"}],
                   [{"type": "scatter"}, {"type": "scatter"}]]
        )
        
        # 1. Forme récente par poste
        forme_par_poste = self.effectif.groupby('poste')['note_moyenne'].mean().sort_values(ascending=True)
        
        fig.add_trace(
            go.Bar(
                x=forme_par_poste.values,
                y=forme_par_poste.index,
                orientation='h',
                marker_color=config_rcs.couleur_primaire,
                name="Forme par poste"
            ),
            row=1, col=1
        )
        
        # 2. Intensité vs Endurance
        for poste in self.effectif['poste'].unique():
            joueurs_poste = self.effectif[self.effectif['poste'] == poste]
            intensites = [self.metriques_avancees[j]['intensite'] for j in joueurs_poste['nom']]
            endurances = [self.metriques_avancees[j]['endurance'] for j in joueurs_poste['nom']]
            
            fig.add_trace(
                go.Scatter(
                    x=endurances,
                    y=intensites,
                    mode='markers+text',
                    text=[j[:8] for j in joueurs_poste['nom']],
                    textposition="top center",
                    name=poste,
                    marker=dict(size=10)
                ),
                row=1, col=2
            )
        
        # 3. Évolution des notes (exemple avec top 5 joueurs)
        top_joueurs = self.effectif.nlargest(5, 'note_moyenne')
        
        for _, joueur in top_joueurs.iterrows():
            perf_joueur = self.performances[self.performances['joueur'] == joueur['nom']]
            
            fig.add_trace(
                go.Scatter(
                    x=list(range(len(perf_joueur))),
                    y=perf_joueur['note'],
                    mode='lines+markers',
                    name=joueur['nom'][:10],
                    line=dict(width=2)
                ),
                row=2, col=1
            )
        
        # 4. Potentiel vs Valeur marchande
        potentiels = [self.metriques_avancees[j]['potentiel'] for j in self.effectif['nom']]
        valeurs = [self.metriques_avancees[j]['valeur_estimee'] for j in self.effectif['nom']]
        
        fig.add_trace(
            go.Scatter(
                x=potentiels,
                y=valeurs,
                mode='markers+text',
                text=[j[:8] for j in self.effectif['nom']],
                textposition="top center",
                marker=dict(
                    size=self.effectif['age'],
                    sizemode='diameter',
                    sizeref=2,
                    color=self.effectif['note_moyenne'],
                    colorscale='RdYlBu_r',
                    showscale=True,
                    colorbar=dict(title="Note Moyenne")
                ),
                name="Joueurs RCS"
            ),
            row=2, col=2
        )
        
        # Mise en forme
        fig.update_layout(
            height=800,
            title={
                'text': f"🔵⚪ {config_rcs.nom_club} - Dashboard Performance Avancé",
                'x': 0.5,
                'font': {'size': 20, 'color': config_rcs.couleur_primaire}
            },
            showlegend=True
        )
        
        return fig
    
    def analyser_risques_blessures(self):
        """Analyse prédictive des risques de blessures"""
        print("🏥 Analyse des risques de blessures...")
        
        # Création du dataset pour ML
        features = []
        for _, joueur in self.effectif.iterrows():
            perf_joueur = self.performances[self.performances['joueur'] == joueur['nom']]
            metriques_j = self.metriques_avancees[joueur['nom']]
            
            feature_vector = [
                joueur['age'],
                joueur['matchs_joues'],
                perf_joueur['minutes'].sum(),
                perf_joueur['distance_parcourue'].mean(),
                perf_joueur['sprints'].mean(),
                metriques_j['fatigue_moyenne'] if 'fatigue_moyenne' in metriques_j else perf_joueur['fatigue'].mean(),
                joueur['cartons_jaunes'],
                metriques_j['intensite']
            ]
            features.append(feature_vector)
        
        features_df = pd.DataFrame(features, columns=[
            'age', 'matchs_joues', 'minutes_totales', 'distance_moyenne', 
            'sprints_moyens', 'fatigue_moyenne', 'cartons_jaunes', 'intensite'
        ])
        
        # Simulation de données historiques pour l'entraînement
        np.random.seed(42)
        n_samples = 200
        
        X_historique = np.random.rand(n_samples, 8)
        X_historique[:, 0] *= 15  # Age 18-33
        X_historique[:, 0] += 18
        X_historique[:, 1] *= 30  # Matchs 0-30
        X_historique[:, 2] *= 2500  # Minutes 0-2500
        X_historique[:, 3] *= 5000  # Distance 5000-10000
        X_historique[:, 3] += 5000
        
        # Génération des labels (risque blessure)
        y_historique = (
            (X_historique[:, 0] > 30) * 0.3 +  # Âge
            (X_historique[:, 1] > 20) * 0.2 +  # Nombre de matchs
            (X_historique[:, 2] > 2000) * 0.2 + # Minutes
            (X_historique[:, 5] > 0.7) * 0.3 + # Fatigue
            np.random.normal(0, 0.1, n_samples)  # Bruit
        ) > 0.5
        
        # Entraînement du modèle
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X_historique)
        
        model = GradientBoostingClassifier(n_estimators=100, random_state=42)
        model.fit(X_scaled, y_historique)
        
        # Prédictions pour l'effectif actuel
        X_current_scaled = scaler.transform(features_df.values)
        risques = model.predict_proba(X_current_scaled)[:, 1]
        
        # Résultats
        resultats_risques = pd.DataFrame({
            'joueur': self.effectif['nom'],
            'poste': self.effectif['poste'],
            'age': self.effectif['age'],
            'risque_blessure': risques,
            'niveau_risque': pd.cut(risques, bins=[0, 0.3, 0.6, 1.0], 
                                  labels=['🟢 Faible', '🟡 Moyen', '🔴 Élevé'])
        })
        
        return resultats_risques.sort_values('risque_blessure', ascending=False)
    
    def optimiser_composition_ia(self, formation="4-2-3-1", adversaire=None):
        """Optimise la composition d'équipe avec IA"""
        print(f"🎯 Optimisation de composition {formation}...")
        
        # Positions par formation
        positions_4231 = {
            'GB': 1, 'DC': 2, 'DD': 1, 'DG': 1,
            'MDC': 2, 'MOC': 1, 'AD': 1, 'AG': 1, 'BU': 1
        }
        
        composition_optimale = {}
        
        for poste, nombre in positions_4231.items():
            # Filtrer les joueurs par poste
            joueurs_poste = self.effectif[self.effectif['poste'] == poste].copy()
            
            if len(joueurs_poste) == 0:
                continue
                
            # Score composite pour sélection
            scores = []
            for _, joueur in joueurs_poste.iterrows():
                metriques_j = self.metriques_avancees[joueur['nom']]
                
                score = (
                    metriques_j['forme_recente'] * 0.4 +
                    metriques_j['score_rcs'] * 0.3 +
                    (joueur['note_moyenne'] * 0.2) +
                    (metriques_j['efficacite'] * 10 * 0.1)
                )
                
                # Bonus si pas de fatigue excessive
                if 'fatigue_moyenne' in metriques_j and metriques_j['fatigue_moyenne'] < 0.7:
                    score += 0.5
                    
                scores.append(score)
            
            joueurs_poste['score_selection'] = scores
            
            # Sélection des meilleurs joueurs
            meilleurs = joueurs_poste.nlargest(nombre, 'score_selection')
            composition_optimale[poste] = meilleurs[['nom', 'score_selection']].to_dict('records')
        
        return composition_optimale
    
    def generer_rapport_weekly(self):
        """Génère un rapport hebdomadaire automatisé"""
        print("📋 Génération du rapport hebdomadaire RCS...")
        
        rapport = {
            'date_generation': pd.Timestamp.now().strftime('%d/%m/%Y %H:%M'),
            'saison': config_rcs.saison,
            'position_ligue1': self.classement[self.classement['equipe'] == 'Racing Club de Strasbourg'].iloc[0]['position'],
            
            # Top performers
            'meilleur_joueur': self.effectif.loc[self.effectif['note_moyenne'].idxmax(), 'nom'],
            'meilleure_note': self.effectif['note_moyenne'].max(),
            
            # Métriques équipe
            'note_moyenne_equipe': self.effectif['note_moyenne'].mean(),
            'age_moyen': self.effectif['age'].mean(),
            'valeur_totale': self.effectif['valeur_marche'].sum(),
            
            # Alertes
            'joueurs_fatigue': self._detecter_fatigue(),
            'joueurs_forme_descendante': self._detecter_baisse_forme(),
            'risques_blessures': self.analyser_risques_blessures().head(3),
            
            # Recommandations
            'composition_optimale': self.optimiser_composition_ia(),
            'axes_amelioration': self._identifier_axes_amelioration()
        }
        
        return rapport
    
    def _detecter_fatigue(self):
        """Détecte les joueurs en situation de fatigue"""
        joueurs_fatigues = []
        
        for _, joueur in self.effectif.iterrows():
            if joueur['matchs_joues'] > 15:  # Beaucoup de matchs
                perf_recente = self.performances[
                    (self.performances['joueur'] == joueur['nom'])
                ].tail(3)
                
                if perf_recente['fatigue'].mean() > 0.75:
                    joueurs_fatigues.append({
                        'nom': joueur['nom'],
                        'matchs_joues': joueur['matchs_joues'],
                        'fatigue_moyenne': perf_recente['fatigue'].mean()
                    })
        
        return joueurs_fatigues
    
    def _detecter_baisse_forme(self):
        """Détecte les joueurs en baisse de forme"""
        joueurs_baisse = []
        
        for _, joueur in self.effectif.iterrows():
            perf_joueur = self.performances[self.performances['joueur'] == joueur['nom']]
            
            if len(perf_joueur) >= 8:
                forme_recente = perf_joueur.tail(4)['note'].mean()
                forme_anterieure = perf_joueur.head(4)['note'].mean()
                
                if forme_recente < forme_anterieure - 0.5:
                    joueurs_baisse.append({
                        'nom': joueur['nom'],
                        'baisse': round(forme_anterieure - forme_recente, 2),
                        'forme_actuelle': round(forme_recente, 2)
                    })
        
        return joueurs_baisse
    
    def _identifier_axes_amelioration(self):
        """Identifie les axes d'amélioration prioritaires"""
        axes = []
        
        # Analyse défensive
        defenseurs = self.effectif[self.effectif['poste'].isin(['DC', 'DD', 'DG'])]
        note_defense = defenseurs['note_moyenne'].mean()
        
        if note_defense < 6.5:
            axes.append({
                'domaine': 'Défense',
                'priorite': 'Haute',
                'note_actuelle': round(note_defense, 2),
                'recommandation': 'Renforcer la cohésion défensive et le pressing coordonné'
            })
        
        # Analyse offensive
        attaquants = self.effectif[self.effectif['poste'].isin(['BU', 'MOC', 'AD', 'AG'])]
        note_attaque = attaquants['note_moyenne'].mean()
        
        if note_attaque < 7.0:
            axes.append({
                'domaine': 'Attaque',
                'priorite': 'Moyenne',
                'note_actuelle': round(note_attaque, 2),
                'recommandation': 'Améliorer l\'efficacité offensive et les transitions'
            })
        
        return axes

# Fonction principale d'utilisation
def lancer_analytics_complet():
    """Lance une session complète d'analytics RCS"""
    
    print("🔵⚪ RACING CLUB DE STRASBOURG - ANALYTICS AVANCÉS")
    print("=" * 60)
    
    # Initialisation
    analytics = AnalyticsAvancesRCS()
    analytics.charger_donnees_completes()
    
    # Analyses principales
    print("\n📊 Génération du dashboard performance...")
    dashboard = analytics.creer_dashboard_performance()
    
    print("🏥 Analyse des risques de blessures...")
    risques = analytics.analyser_risques_blessures()
    
    print("🎯 Optimisation de la composition...")
    composition = analytics.optimiser_composition_ia()
    
    print("📋 Génération du rapport hebdomadaire...")
    rapport = analytics.generer_rapport_weekly()
    
    return {
        'dashboard': dashboard,
        'risques_blessures': risques,
        'composition_optimale': composition,
        'rapport_hebdomadaire': rapport
    }

if __name__ == "__main__":
    resultats = lancer_analytics_complet()
    print("\n✅ Analytics complets générés avec succès !")
    print("🔵⚪ ALLEZ RACING ! ⚪🔵")
