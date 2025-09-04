# ========================================================================
# Analyses Prédictives Racing Club de Strasbourg
# ========================================================================
# 
# Modèles prédictifs spécialisés pour le RCS avec code entièrement en français.
# Focus sur les besoins spécifiques du club alsacien.
#
# Auteur: Football Analytics Platform
# Équipe: Racing Club de Strasbourg
# Version: 2.0 - Spécialisée RCS
# ========================================================================

# Chargement des bibliothèques
suppressPackageStartupMessages({
  library(dplyr)
  library(ggplot2)
  library(randomForest)
  library(caret)
  library(plotly)
  library(corrplot)
  library(VIM)
  library(mice)
  library(survival)
  library(survminer)
  library(forecast)
  library(tidyr)
  library(lubridate)
})

# ========================================================================
# CONFIGURATION SPÉCIFIQUE RCS
# ========================================================================

# Paramètres du club
nom_club <- "Racing Club de Strasbourg"
nom_court <- "RCS" 
stade <- "Stade de la Meinau"
couleurs_club <- c("#0066CC", "#FFFFFF")  # Bleu et blanc
budget_transfert_max <- 15  # Millions d'euros
objectif_saison <- "Maintien confortable"

# Style de jeu RCS
style_jeu_rcs <- list(
  formation_principale = "4-2-3-1",
  possession_cible = 47,  # % possession moyenne
  pressing = "Médian coordonné",
  transitions = "Rapides",
  points_forts = c("Contre-attaque", "Cohésion défensive", "Jeunesse")
)

cat("🔵⚪ Analyses Prédictives Racing Club de Strasbourg\n")
cat("====================================================\n\n")

# ========================================================================
# FONCTIONS DE GÉNÉRATION DE DONNÉES RCS
# ========================================================================

#' Génère des données réalistes de l'effectif RCS 2024-2025
#' @return DataFrame avec les joueurs du RCS
generer_effectif_rcs <- function() {
  
  # Effectif réel RCS 2024-2025
  effectif_rcs <- data.frame(
    nom_joueur = c(
      # Gardiens
      "Matz Sels", "Alaa Bellaarouch",
      
      # Défenseurs  
      "Guela Doué", "Abakar Sylla", "Saïdou Sow", "Marvin Senaya",
      "Thomas Delaine", "Frédéric Guilbert", "Caleb Wiley",
      
      # Milieux
      "Habib Diarra", "Andrey Santos", "Ismaël Doukouré", 
      "Junior Mwanga", "Sékou Mara", "Dilane Bakwa",
      
      # Attaquants
      "Emanuel Emegha", "Félix Lemaréchal", "Jeremy Sebas", "Pape Diong"
    ),
    
    poste = c(
      # Gardiens
      "GB", "GB",
      
      # Défenseurs
      "DD", "DC", "DC", "DD", "DG", "DD", "DG",
      
      # Milieux  
      "MDC", "MC", "MC", "MDC", "MOC", "AD",
      
      # Attaquants
      "BU", "MOC", "AG", "BU"
    ),
    
    age = c(
      # Gardiens
      32, 20,
      
      # Défenseurs
      22, 24, 22, 22, 32, 29, 20,
      
      # Milieux
      20, 20, 21, 20, 22, 21,
      
      # Attaquants  
      21, 20, 19, 19
    ),
    
    nationalite = c(
      # Gardiens
      "Belgique", "Maroc",
      
      # Défenseurs
      "France", "France", "Guinée", "France", "France", "France", "États-Unis",
      
      # Milieux
      "France", "Brésil", "France", "France", "France", "France",
      
      # Attaquants
      "Pays-Bas", "France", "France", "Sénégal"
    ),
    
    numero_maillot = c(1, 30, 2, 4, 24, 28, 3, 19, 27, 18, 6, 29, 15, 14, 26, 10, 17, 37, 39),
    
    stringsAsFactors = FALSE
  )
  
  # Ajout de statistiques simulées réalistes selon l'âge et le poste
  set.seed(42)
  
  effectif_rcs <- effectif_rcs %>%
    mutate(
      # Valeur marchande selon âge, poste et potentiel
      valeur_marche_millions = case_when(
        nom_joueur == "Emanuel Emegha" ~ 8.0,    # Attaquant prometteur
        nom_joueur == "Dilane Bakwa" ~ 6.0,     # Créateur talentueux  
        nom_joueur == "Andrey Santos" ~ 5.5,    # Milieu brésilien
        nom_joueur == "Abakar Sylla" ~ 4.5,     # Défenseur expérimenté
        nom_joueur == "Matz Sels" ~ 4.0,        # Gardien établi
        age <= 20 ~ runif(n(), 1.5, 4.0),      # Jeunes talents
        age <= 24 ~ runif(n(), 2.0, 6.0),      # Joueurs confirmés
        TRUE ~ runif(n(), 1.0, 3.5)            # Joueurs expérimentés
      ),
      
      # Note technique selon poste et expérience
      note_technique = case_when(
        poste == "GB" ~ rnorm(n(), 7.2, 0.8),
        poste %in% c("DC", "DD", "DG") ~ rnorm(n(), 6.8, 0.7),
        poste %in% c("MDC", "MC", "MOC") ~ rnorm(n(), 7.3, 0.9),
        TRUE ~ rnorm(n(), 7.1, 1.0)  # Attaquants
      ),
      
      # Note physique (pic vers 23-26 ans)
      note_physique = pmax(5.5, pmin(9.0, 8.0 - abs(age - 24) * 0.15 + rnorm(n(), 0, 0.5))),
      
      # Note mental (augmente avec l'âge/expérience)
      note_mental = pmax(5.5, pmin(9.0, 6.5 + (age - 18) * 0.08 + rnorm(n(), 0, 0.6))),
      
      # Statut dans l'équipe
      statut = case_when(
        nom_joueur %in% c("Matz Sels", "Abakar Sylla", "Thomas Delaine", 
                         "Dilane Bakwa", "Emanuel Emegha") ~ "Titulaire",
        age >= 25 ~ "Cadre",
        age <= 20 ~ "Espoir", 
        TRUE ~ "Rotation"
      ),
      
      # Minutes jouées cette saison (simulation)
      minutes_jouees = case_when(
        statut == "Titulaire" ~ as.integer(rnorm(n(), 950, 150)),
        statut == "Cadre" ~ as.integer(rnorm(n(), 750, 200)),
        statut == "Rotation" ~ as.integer(rnorm(n(), 450, 150)),
        TRUE ~ as.integer(rnorm(n(), 200, 100))
      )
    ) %>%
    mutate(
      # S'assurer que les valeurs sont réalistes
      valeur_marche_millions = pmax(0.5, pmin(15.0, valeur_marche_millions)),
      note_technique = pmax(5.5, pmin(9.0, note_technique)),
      minutes_jouees = pmax(0, minutes_jouees)
    )
  
  return(effectif_rcs)
}

#' Génère des données de matchs réalistes pour le RCS
#' @param nb_matchs Nombre de matchs à générer
#' @return DataFrame avec les résultats de matchs
generer_matchs_rcs <- function(nb_matchs = 50) {
  
  # Adversaires typiques du RCS en Ligue 1
  adversaires_ligue1 <- c(
    "PSG", "OM", "Lyon", "Monaco", "Lille", "Rennes", "Nice", "Lens",
    "Montpellier", "Nantes", "Brest", "Reims", "Toulouse", "Clermont",
    "Angers", "Auxerre", "Troyes", "Metz", "Ajaccio"
  )
  
  set.seed(42)
  
  matchs_rcs <- data.frame(
    match_id = 1:nb_matchs,
    adversaire = sample(adversaires_ligue1, nb_matchs, replace = TRUE),
    domicile = sample(c(TRUE, FALSE), nb_matchs, replace = TRUE),
    date_match = seq.Date(as.Date("2024-08-15"), by = "week", length.out = nb_matchs),
    
    # Force de l'adversaire (impact sur probabilités)
    force_adversaire = case_when(
      adversaires_ligue1[match(sample(adversaires_ligue1, nb_matchs, replace = TRUE), adversaires_ligue1)] %in% 
        c("PSG", "OM", "Lyon", "Monaco") ~ "Forte",
      adversaires_ligue1[match(sample(adversaires_ligue1, nb_matchs, replace = TRUE), adversaires_ligue1)] %in% 
        c("Lille", "Rennes", "Nice", "Lens") ~ "Moyenne",
      TRUE ~ "Faible"
    ),
    
    stringsAsFactors = FALSE
  )
  
  # Ajustement force adversaire pour échantillon correct
  matchs_rcs$force_adversaire <- sample(c("Forte", "Moyenne", "Faible"), 
                                       nb_matchs, replace = TRUE, 
                                       prob = c(0.25, 0.45, 0.3))
  
  # Génération des résultats selon les paramètres RCS
  matchs_rcs <- matchs_rcs %>%
    mutate(
      # Bonus à domicile au Stade de la Meinau
      bonus_domicile = ifelse(domicile, 0.3, 0),
      
      # Probabilité de victoire selon force adversaire
      proba_victoire = case_when(
        force_adversaire == "Forte" ~ 0.15 + bonus_domicile,
        force_adversaire == "Moyenne" ~ 0.35 + bonus_domicile,
        TRUE ~ 0.55 + bonus_domicile
      ),
      
      # Probabilité de nul
      proba_nul = case_when(
        force_adversaire == "Forte" ~ 0.35,
        force_adversaire == "Moyenne" ~ 0.30,
        TRUE ~ 0.25
      ),
      
      # Génération du résultat
      resultat_aleatoire = runif(nb_matchs),
      
      resultat = case_when(
        resultat_aleatoire <= proba_victoire ~ "Victoire",
        resultat_aleatoire <= (proba_victoire + proba_nul) ~ "Nul",
        TRUE ~ "Défaite"
      ),
      
      # Buts marqués par le RCS (style contre-attaque)
      buts_rcs = case_when(
        resultat == "Victoire" ~ rpois(n(), 2.1),
        resultat == "Nul" ~ rpois(n(), 1.2),
        TRUE ~ rpois(n(), 0.8)
      ),
      
      # Buts encaissés
      buts_encaisses = case_when(
        resultat == "Victoire" ~ rpois(n(), 0.9),
        resultat == "Nul" ~ buts_rcs,  # Score identique pour nul
        TRUE ~ buts_rcs + rpois(n(), 1.5)
      ),
      
      # xG RCS (Expected Goals)
      xg_rcs = pmax(0.3, rnorm(n(), buts_rcs + 0.2, 0.6)),
      
      # xG adversaire  
      xg_adversaire = pmax(0.2, rnorm(n(), buts_encaisses + 0.1, 0.5)),
      
      # Possession (style RCS - possession modérée)
      possession_rcs = case_when(
        force_adversaire == "Forte" ~ rnorm(n(), 42, 8),
        force_adversaire == "Moyenne" ~ rnorm(n(), 48, 6),
        TRUE ~ rnorm(n(), 52, 7)
      ),
      
      # Contraindre possession entre 25-75%
      possession_rcs = pmax(25, pmin(75, possession_rcs)),
      
      # Points obtenus
      points = case_when(
        resultat == "Victoire" ~ 3,
        resultat == "Nul" ~ 1,
        TRUE ~ 0
      )
    ) %>%
    select(-resultat_aleatoire, -bonus_domicile, -proba_victoire, -proba_nul)
  
  return(matchs_rcs)
}

# ========================================================================
# MODÈLES PRÉDICTIFS SPÉCIALISÉS RCS
# ========================================================================

#' Modèle de prédiction de résultats pour le RCS
#' @param donnees_matchs DataFrame avec historique des matchs
#' @return Modèle Random Forest entraîné
entrainer_modele_resultats_rcs <- function(donnees_matchs = NULL) {
  
  cat("⚽ Entraînement du modèle de prédiction de résultats RCS...\n")
  
  # Charger ou générer les données
  if (is.null(donnees_matchs)) {
    donnees_matchs <- generer_matchs_rcs(100)
  }
  
  # Préparation des features pour le modèle
  donnees_modele <- donnees_matchs %>%
    mutate(
      # Variables catégorielles
      domicile_num = as.numeric(domicile),
      force_adv_forte = as.numeric(force_adversaire == "Forte"),
      force_adv_moyenne = as.numeric(force_adversaire == "Moyenne"),
      
      # Variables temporelles
      mois = month(date_match),
      
      # Forme récente (moyenne mobile des 5 derniers matchs)
      points_moyenne_5 = zoo::rollmean(points, k = 5, fill = NA, align = "right"),
      buts_moyenne_5 = zoo::rollmean(buts_rcs, k = 5, fill = NA, align = "right"),
      
      # Variable cible
      resultat_factor = factor(resultat, levels = c("Défaite", "Nul", "Victoire"))
    ) %>%
    filter(!is.na(points_moyenne_5))  # Retirer les NA dus à la moyenne mobile
  
  # Division train/test
  indices_train <- createDataPartition(donnees_modele$resultat_factor, p = 0.7, list = FALSE)
  donnees_train <- donnees_modele[indices_train, ]
  donnees_test <- donnees_modele[-indices_train, ]
  
  # Variables prédictives
  variables_pred <- c("domicile_num", "force_adv_forte", "force_adv_moyenne", 
                     "mois", "points_moyenne_5", "buts_moyenne_5")
  
  # Entraînement du modèle Random Forest
  modele_rf <- randomForest(
    x = donnees_train[, variables_pred],
    y = donnees_train$resultat_factor,
    ntree = 500,
    importance = TRUE,
    mtry = 3
  )
  
  # Prédictions sur le test set
  predictions_test <- predict(modele_rf, donnees_test[, variables_pred])
  
  # Matrice de confusion
  matrice_confusion <- confusionMatrix(predictions_test, donnees_test$resultat_factor)
  
  # Importance des variables
  importance_vars <- as.data.frame(importance(modele_rf)) %>%
    rownames_to_column("variable") %>%
    arrange(desc(MeanDecreaseGini))
  
  cat("✅ Modèle de résultats RCS entraîné avec succès!\n")
  cat(sprintf("📊 Précision globale: %.1f%%\n", matrice_confusion$overall['Accuracy'] * 100))
  
  # Variables les plus importantes
  cat("🎯 Variables les plus prédictives:\n")
  for (i in 1:min(3, nrow(importance_vars))) {
    cat(sprintf("   %d. %s\n", i, importance_vars$variable[i]))
  }
  
  return(list(
    modele = modele_rf,
    precision = matrice_confusion$overall['Accuracy'],
    matrice_confusion = matrice_confusion,
    importance_variables = importance_vars,
    donnees_test = donnees_test
  ))
}

#' Modèle de prédiction de performances individuelles
#' @param effectif_rcs DataFrame avec effectif du RCS
#' @return Modèle de régression pour prédire les notes
entrainer_modele_performances_rcs <- function(effectif_rcs = NULL) {
  
  cat("📊 Entraînement du modèle de performance individuelle RCS...\n")
  
  if (is.null(effectif_rcs)) {
    effectif_rcs <- generer_effectif_rcs()
  }
  
  # Génération de notes de performance simulées selon le profil
  set.seed(42)
  
  effectif_avec_notes <- effectif_rcs %>%
    mutate(
      # Note de performance basée sur les capacités et le temps de jeu
      note_performance = pmax(4.0, pmin(10.0,
        (note_technique * 0.4 + note_physique * 0.3 + note_mental * 0.3) +
        (minutes_jouees / 1000) * 0.5 +  # Bonus temps de jeu
        rnorm(n(), 0, 0.7)  # Variabilité aléatoire
      )),
      
      # Variables catégorielles pour le modèle
      poste_gardien = as.numeric(poste == "GB"),
      poste_defenseur = as.numeric(poste %in% c("DC", "DD", "DG")),
      poste_milieu = as.numeric(poste %in% c("MDC", "MC", "MOC")),
      poste_attaquant = as.numeric(poste %in% c("BU", "AD", "AG")),
      
      # Âge normalisé
      age_normalise = (age - mean(age)) / sd(age),
      
      # Valeur de marché normalisée  
      valeur_normalisee = (valeur_marche_millions - mean(valeur_marche_millions)) / sd(valeur_marche_millions)
    )
  
  # Variables prédictives
  variables_pred <- c("note_technique", "note_physique", "note_mental", 
                     "age_normalise", "valeur_normalisee", "minutes_jouees",
                     "poste_gardien", "poste_defenseur", "poste_milieu", "poste_attaquant")
  
  # Modèle de régression linéaire multiple
  modele_perf <- lm(note_performance ~ ., data = effectif_avec_notes[, c("note_performance", variables_pred)])
  
  # Métriques du modèle
  r_squared <- summary(modele_perf)$r.squared
  rmse <- sqrt(mean(modele_perf$residuals^2))
  
  cat("✅ Modèle de performance individuelle entraîné!\n")
  cat(sprintf("📊 R² = %.3f | RMSE = %.3f\n", r_squared, rmse))
  
  return(list(
    modele = modele_perf,
    r_squared = r_squared,
    rmse = rmse,
    donnees = effectif_avec_notes,
    variables_pred = variables_pred
  ))
}

#' Analyse de tendance pour le RCS (série temporelle)
#' @param donnees_matchs DataFrame avec historique
#' @return Modèle ARIMA et prédictions
analyser_tendance_rcs <- function(donnees_matchs = NULL) {
  
  cat("📈 Analyse de tendance Racing Club de Strasbourg...\n")
  
  if (is.null(donnees_matchs)) {
    donnees_matchs <- generer_matchs_rcs(80)
  }
  
  # Préparation de la série temporelle
  serie_points <- donnees_matchs %>%
    arrange(date_match) %>%
    mutate(
      points_cumules = cumsum(points),
      moyenne_mobile_5 = zoo::rollmean(points, k = 5, fill = NA, align = "right"),
      forme_recente = case_when(
        moyenne_mobile_5 >= 1.8 ~ "Excellente",
        moyenne_mobile_5 >= 1.4 ~ "Bonne", 
        moyenne_mobile_5 >= 1.0 ~ "Correcte",
        TRUE ~ "Préoccupante"
      )
    )
  
  # Série temporelle des points par match
  ts_points <- ts(serie_points$points, frequency = 1)
  
  # Modèle ARIMA automatique
  if (length(ts_points) >= 10) {
    modele_arima <- auto.arima(ts_points, seasonal = FALSE)
    
    # Prédictions pour les 10 prochains matchs
    predictions_futures <- forecast(modele_arima, h = 10)
    
    # Projection points fin de saison (38 matchs)
    matchs_restants <- max(0, 38 - nrow(donnees_matchs))
    points_actuels <- sum(serie_points$points)
    
    if (matchs_restants > 0) {
      pred_moyenne <- mean(predictions_futures$mean[1:min(10, matchs_restants)])
      projection_finale <- points_actuels + (pred_moyenne * matchs_restants)
    } else {
      projection_finale <- points_actuels
    }
    
    # Évaluation de la projection
    evaluation_projection <- case_when(
      projection_finale >= 45 ~ "🟢 Maintien largement assuré",
      projection_finale >= 38 ~ "🟡 Maintien probable", 
      projection_finale >= 32 ~ "🟠 Lutte pour le maintien",
      TRUE ~ "🔴 Situation critique"
    )
    
    cat("✅ Analyse de tendance terminée!\n")
    cat(sprintf("📊 Points actuels: %d\n", points_actuels))
    cat(sprintf("📊 Projection fin de saison: %.1f points\n", projection_finale))
    cat(sprintf("📊 Évaluation: %s\n", evaluation_projection))
    
    return(list(
      modele_arima = modele_arima,
      serie_points = serie_points,
      predictions = predictions_futures,
      projection_finale = projection_finale,
      evaluation = evaluation_projection,
      forme_actuelle = tail(serie_points$forme_recente[!is.na(serie_points$forme_recente)], 1)
    ))
    
  } else {
    cat("⚠️ Données insuffisantes pour l'analyse de tendance (minimum 10 matchs)\n")
    return(NULL)
  }
}

#' Modèle de recommandation de composition d'équipe
#' @param effectif_rcs DataFrame avec effectif
#' @param adversaire_force Force de l'adversaire ("Forte", "Moyenne", "Faible")
#' @param domicile Booléen indiquant si le match est à domicile
#' @return Composition recommandée
recommander_composition_rcs <- function(effectif_rcs = NULL, 
                                       adversaire_force = "Moyenne", 
                                       domicile = TRUE) {
  
  cat(sprintf("⚙️ Recommandation de composition RCS vs adversaire %s (%s)...\n", 
              adversaire_force, ifelse(domicile, "Domicile", "Extérieur")))
  
  if (is.null(effectif_rcs)) {
    effectif_rcs <- generer_effectif_rcs()
  }
  
  # Score de forme selon différents facteurs
  effectif_scores <- effectif_rcs %>%
    mutate(
      # Score de forme basé sur les notes et temps de jeu
      score_forme = (note_technique + note_physique + note_mental) / 3 +
                   (minutes_jouees / max(minutes_jouees)) * 1.5,
      
      # Bonus selon l'adversaire
      bonus_adversaire = case_when(
        adversaire_force == "Forte" & poste %in% c("DC", "MDC") ~ 0.5,  # Renforcer défense
        adversaire_force == "Faible" & poste %in% c("MOC", "BU") ~ 0.5, # Privilégier attaque
        TRUE ~ 0
      ),
      
      # Bonus domicile pour jeunes joueurs
      bonus_domicile = ifelse(domicile & age <= 22, 0.3, 0),
      
      # Score final
      score_final = score_forme + bonus_adversaire + bonus_domicile
    ) %>%
    arrange(desc(score_final))
  
  # Sélection par poste (formation 4-2-3-1)
  composition <- list(
    gardien = effectif_scores %>% filter(poste == "GB") %>% slice(1),
    
    defense = bind_rows(
      effectif_scores %>% filter(poste == "DG") %>% slice(1),  # DG
      effectif_scores %>% filter(poste == "DC") %>% slice(1:2), # DC x2
      effectif_scores %>% filter(poste == "DD") %>% slice(1)   # DD
    ),
    
    milieu = bind_rows(
      effectif_scores %>% filter(poste == "MDC") %>% slice(1:2), # MDC x2
      effectif_scores %>% filter(poste %in% c("MOC", "AD")) %>% slice(1:3) # MOC + ailiers
    ),
    
    attaque = effectif_scores %>% filter(poste == "BU") %>% slice(1)
  )
  
  # Joueurs titulaires
  titulaires <- bind_rows(
    composition$gardien,
    composition$defense, 
    composition$milieu,
    composition$attaque
  )
  
  # Remplaçants (5 meilleurs restants)
  remplacants <- effectif_scores %>%
    filter(!nom_joueur %in% titulaires$nom_joueur) %>%
    slice(1:5)
  
  # Évaluation de la composition
  note_moyenne_titulaires <- mean(titulaires$score_final)
  age_moyen_titulaires <- mean(titulaires$age)
  
  evaluation_compo <- case_when(
    note_moyenne_titulaires >= 7.5 ~ "🟢 Composition très forte",
    note_moyenne_titulaires >= 7.0 ~ "🟡 Composition équilibrée",
    TRUE ~ "🟠 Composition défensive"
  )
  
  cat("✅ Composition recommandée générée!\n")
  cat(sprintf("📊 Note moyenne titulaires: %.2f\n", note_moyenne_titulaires))
  cat(sprintf("📊 Âge moyen: %.1f ans\n", age_moyen_titulaires))
  cat(sprintf("📊 Évaluation: %s\n", evaluation_compo))
  
  return(list(
    formation = "4-2-3-1",
    titulaires = titulaires %>% select(nom_joueur, poste, age, score_final),
    remplacants = remplacants %>% select(nom_joueur, poste, age, score_final),
    evaluation = evaluation_compo,
    note_moyenne = note_moyenne_titulaires,
    tactique_recommandee = case_when(
      adversaire_force == "Forte" ~ "Jeu défensif - Contres rapides",
      adversaire_force == "Faible" ~ "Pressing haut - Domination",
      TRUE ~ "Jeu équilibré - Adaptation"
    )
  ))
}

# ========================================================================
# FONCTIONS DE VISUALISATION RCS
# ========================================================================

#' Crée un graphique de performance saisonnière du RCS
#' @param donnees_matchs DataFrame avec les matchs
#' @return Graphique ggplot
visualiser_performance_saison_rcs <- function(donnees_matchs = NULL) {
  
  if (is.null(donnees_matchs)) {
    donnees_matchs <- generer_matchs_rcs(25)
  }
  
  # Préparation des données
  evolution <- donnees_matchs %>%
    arrange(date_match) %>%
    mutate(
      match_numero = row_number(),
      points_cumules = cumsum(points),
      moyenne_mobile = zoo::rollmean(points, k = 5, fill = NA, align = "right")
    )
  
  # Graphique principal
  p <- ggplot(evolution, aes(x = match_numero)) +
    
    # Points cumulés
    geom_line(aes(y = points_cumules), color = "#0066CC", size = 1.2, alpha = 0.8) +
    geom_point(aes(y = points_cumules, color = resultat), size = 2.5) +
    
    # Moyenne mobile
    geom_line(aes(y = moyenne_mobile * 10), color = "#FF6600", size = 1, linetype = "dashed", alpha = 0.7) +
    
    # Couleurs selon le résultat
    scale_color_manual(values = c("Victoire" = "#00AA00", "Nul" = "#FFAA00", "Défaite" = "#FF3333")) +
    
    # Échelles doubles
    scale_y_continuous(
      name = "Points cumulés",
      sec.axis = sec_axis(~ . / 10, name = "Moyenne mobile (points/match)")
    ) +
    
    # Thème et labels
    labs(
      title = paste("Performance Saisonnière -", nom_club),
      subtitle = "Évolution des points et forme récente",
      x = "Numéro de match",
      color = "Résultat",
      caption = "Source: Football Analytics RCS"
    ) +
    
    theme_minimal() +
    theme(
      plot.title = element_text(size = 16, face = "bold", color = "#0066CC"),
      plot.subtitle = element_text(size = 12),
      legend.position = "bottom",
      panel.grid.minor = element_blank()
    )
  
  return(p)
}

#' Crée un radar chart pour comparer les joueurs RCS
#' @param effectif_rcs DataFrame avec effectif
#' @param joueurs_compares Vecteur des noms de joueurs à comparer
#' @return Graphique radar
creer_radar_joueurs_rcs <- function(effectif_rcs = NULL, 
                                   joueurs_compares = c("Emanuel Emegha", "Dilane Bakwa")) {
  
  if (is.null(effectif_rcs)) {
    effectif_rcs <- generer_effectif_rcs()
  }
  
  # Filtrer les joueurs sélectionnés
  donnees_radar <- effectif_rcs %>%
    filter(nom_joueur %in% joueurs_compares) %>%
    select(nom_joueur, note_technique, note_physique, note_mental, valeur_marche_millions) %>%
    mutate(
      # Normaliser la valeur marchande sur 10
      valeur_normalisee = (valeur_marche_millions / max(effectif_rcs$valeur_marche_millions)) * 10
    ) %>%
    select(-valeur_marche_millions)
  
  # Conversion pour radar chart
  donnees_radar_long <- donnees_radar %>%
    pivot_longer(cols = -nom_joueur, names_to = "attribut", values_to = "valeur") %>%
    mutate(
      attribut = case_when(
        attribut == "note_technique" ~ "Technique",
        attribut == "note_physique" ~ "Physique", 
        attribut == "note_mental" ~ "Mental",
        attribut == "valeur_normalisee" ~ "Valeur Marchande"
      )
    )
  
  # Graphique radar avec ggplot
  p <- ggplot(donnees_radar_long, aes(x = attribut, y = valeur, fill = nom_joueur)) +
    geom_polygon(alpha = 0.3, color = "black") +
    geom_point(size = 3) +
    
    coord_polar() +
    
    scale_y_continuous(limits = c(0, 10), breaks = seq(0, 10, 2)) +
    scale_fill_manual(values = c("#0066CC", "#FF6600")) +
    
    labs(
      title = "Comparaison de Joueurs RCS",
      subtitle = paste("Profils:", paste(joueurs_compares, collapse = " vs ")),
      fill = "Joueur",
      caption = "Notes sur 10"
    ) +
    
    theme_minimal() +
    theme(
      plot.title = element_text(size = 14, face = "bold", hjust = 0.5),
      axis.text.y = element_text(size = 8),
      legend.position = "bottom"
    )
  
  return(p)
}

# ========================================================================
# EXÉCUTION DES ANALYSES PRINCIPALES
# ========================================================================

main_analyse_rcs <- function() {
  
  cat("🔵⚪ LANCEMENT DES ANALYSES RACING CLUB DE STRASBOURG\n")
  cat("=========================================================\n\n")
  
  # 1. Génération des données de base
  cat("📊 Génération des données RCS...\n")
  effectif_rcs <- generer_effectif_rcs()
  matchs_rcs <- generer_matchs_rcs(30)
  
  cat(sprintf("✅ Effectif généré: %d joueurs\n", nrow(effectif_rcs)))
  cat(sprintf("✅ Historique généré: %d matchs\n", nrow(matchs_rcs)))
  
  # 2. Modèle de prédiction de résultats
  cat("\n⚽ Entraînement modèle de résultats...\n")
  modele_resultats <- entrainer_modele_resultats_rcs(matchs_rcs)
  
  # 3. Modèle de performance des joueurs
  cat("\n👥 Entraînement modèle de performances...\n")
  modele_performances <- entrainer_modele_performances_rcs(effectif_rcs)
  
  # 4. Analyse de tendance
  cat("\n📈 Analyse de tendance saisonnière...\n")
  analyse_tendance <- analyser_tendance_rcs(matchs_rcs)
  
  # 5. Recommandation de composition
  cat("\n⚙️ Recommandation de composition type...\n")
  composition_type <- recommander_composition_rcs(effectif_rcs, "Moyenne", TRUE)
  
  # 6. Visualisations
  cat("\n📊 Génération des visualisations...\n")
  
  # Graphique de performance
  graph_performance <- visualiser_performance_saison_rcs(matchs_rcs)
  
  # Radar des joueurs clés
  joueurs_cles <- c("Emanuel Emegha", "Dilane Bakwa")
  radar_joueurs <- creer_radar_joueurs_rcs(effectif_rcs, joueurs_cles)
  
  # 7. Résumé des analyses
  cat("\n📋 RÉSUMÉ DES ANALYSES RCS\n")
  cat("===========================\n")
  
  # Statistiques effectif
  age_moyen <- mean(effectif_rcs$age)
  valeur_totale <- sum(effectif_rcs$valeur_marche_millions)
  
  cat(sprintf("👥 Effectif: %d joueurs | Âge moyen: %.1f ans\n", nrow(effectif_rcs), age_moyen))
  cat(sprintf("💰 Valeur totale effectif: %.1f M€\n", valeur_totale))
  
  # Performance récente
  points_obtenus <- sum(matchs_rcs$points)
  points_possibles <- nrow(matchs_rcs) * 3
  pourcentage_points <- (points_obtenus / points_possibles) * 100
  
  cat(sprintf("⚽ Points obtenus: %d/%d (%.1f%%)\n", points_obtenus, points_possibles, pourcentage_points))
  
  # Prédiction
  if (!is.null(analyse_tendance)) {
    cat(sprintf("📈 Projection saison: %.1f points\n", analyse_tendance$projection_finale))
    cat(sprintf("📊 Évaluation: %s\n", analyse_tendance$evaluation))
  }
  
  # Composition recommandée
  cat(sprintf("⚙️ Formation recommandée: %s\n", composition_type$formation))
  cat(sprintf("🎯 Tactique: %s\n", composition_type$tactique_recommandee))
  
  cat("\n✅ Analyses terminées! Graphiques générés.\n")
  
  # Retourner les résultats
  return(list(
    effectif = effectif_rcs,
    matchs = matchs_rcs,
    modele_resultats = modele_resultats,
    modele_performances = modele_performances,
    analyse_tendance = analyse_tendance,
    composition_recommandee = composition_type,
    visualisations = list(
      performance = graph_performance,
      radar_joueurs = radar_joueurs
    )
  ))
}

# ========================================================================
# POINT D'ENTRÉE PRINCIPAL
# ========================================================================

if (interactive()) {
  # Lancer les analyses si le script est exécuté interactivement
  resultats_analyses <- main_analyse_rcs()
  
  # Afficher les graphiques
  print(resultats_analyses$visualisations$performance)
  print(resultats_analyses$visualisations$radar_joueurs)
  
} else {
  cat("📋 Script d'analyses RCS chargé. Utiliser main_analyse_rcs() pour lancer les analyses.\n")
}
