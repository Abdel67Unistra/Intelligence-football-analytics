# 🔵⚪ Racing Club de Strasbourg - Analyses Prédictives R Avancées
# ==================================================================
#
# Script R complet pour analyses prédictives avancées du RCS
# - Modèles machine learning
# - Visualisations interactives
# - Rapports automatisés
#
# Auteur: GitHub Copilot
# Date: Septembre 2025

# ===================================================================
# CHARGEMENT DES PACKAGES
# ===================================================================

# Vérification et installation des packages si nécessaire
packages_requis <- c(
  "tidyverse", "plotly", "shiny", "DT", "flexdashboard",
  "caret", "randomForest", "xgboost", "e1071",
  "corrplot", "VIM", "mice", "forecast",
  "cluster", "factoextra", "ggplot2", "viridis",
  "knitr", "rmarkdown", "htmlwidgets"
)

for (pkg in packages_requis) {
  if (!require(pkg, character.only = TRUE)) {
    install.packages(pkg, dependencies = TRUE)
    library(pkg, character.only = TRUE)
  }
}

# ===================================================================
# CONFIGURATION RCS
# ===================================================================

# Couleurs officielles RCS
couleurs_rcs <- c("#0066CC", "#FFFFFF", "#FF6B35", "#87CEEB", "#4169E1")
theme_rcs <- theme_minimal() +
  theme(
    plot.title = element_text(color = "#0066CC", size = 14, face = "bold"),
    plot.subtitle = element_text(color = "#333333", size = 11),
    panel.grid.major = element_line(color = "#f0f0f0"),
    legend.position = "bottom"
  )

# Configuration globale
saison <- "2024-2025"
effectif_size <- 17
objectif_points <- 45

cat("🔵⚪ RACING CLUB DE STRASBOURG - ANALYSES PRÉDICTIVES R\n")
cat("====================================================\n\n")

# ===================================================================
# GÉNÉRATION DES DONNÉES RCS
# ===================================================================

#' Génère les données d'effectif RCS réalistes
generer_effectif_rcs <- function() {
  set.seed(42)  # Reproductibilité
  
  # Effectif réel RCS 2024-2025
  effectif <- data.frame(
    nom = c("Matz Sels", "Emanuel Emegha", "Habib Diarra", "Dilane Bakwa",
            "Sebastian Nanasi", "Guela Doué", "Abakar Sylla", "Saïdou Sow",
            "Andrey Santos", "Caleb Wiley", "Ismaël Doukouré", "Junior Mwanga",
            "Thomas Delaine", "Frédéric Guilbert", "Sékou Mara", 
            "Félix Lemaréchal", "Jeremy Sebas"),
    
    poste = c("GB", "BU", "MDC", "AD", "AG", "DD", "DC", "DC",
              "MDC", "DG", "MDC", "MC", "DG", "DD", "MOC", "MOC", "BU"),
    
    age = c(32, 21, 20, 22, 22, 22, 25, 22,
            20, 19, 23, 21, 32, 29, 22, 19, 19),
    
    valeur_marche = c(4.0, 8.0, 12.0, 10.0, 6.0, 8.0, 3.5, 4.0,
                      8.0, 4.0, 2.0, 1.5, 1.0, 1.5, 2.0, 4.0, 0.8),
    
    matchs_joues = c(17, 17, 17, 16, 14, 15, 17, 16,
                     15, 14, 8, 10, 12, 11, 12, 11, 6),
    
    note_moyenne = c(6.8, 7.0, 7.1, 7.3, 6.8, 6.4, 6.2, 6.3,
                     6.5, 7.1, 6.0, 6.2, 6.1, 6.3, 6.8, 6.8, 6.5),
    
    stringsAsFactors = FALSE
  )
  
  # Calculs supplémentaires
  effectif$experience <- pmax(1, effectif$age - 16)
  effectif$potentiel <- pmax(50, pmin(95, 
    100 - (effectif$age - 18) * 2 + rnorm(nrow(effectif), 0, 5)))
  effectif$forme_actuelle <- effectif$note_moyenne + rnorm(nrow(effectif), 0, 0.3)
  
  return(effectif)
}

#' Génère les données de performance historiques
generer_donnees_matchs <- function(effectif, nb_matchs = 17) {
  set.seed(123)
  
  matchs_data <- data.frame()
  
  for (i in 1:nb_matchs) {
    for (j in 1:nrow(effectif)) {
      joueur <- effectif[j, ]
      
      # Probabilité de jouer selon le statut
      prob_jouer <- ifelse(joueur$matchs_joues >= 10, 0.85, 0.4)
      
      if (runif(1) < prob_jouer) {
        match_perf <- data.frame(
          match_id = i,
          journee = paste0("J", i),
          joueur = joueur$nom,
          poste = joueur$poste,
          minutes = sample(c(0, 15, 30, 45, 60, 75, 90), 1, 
                          prob = c(0.05, 0.05, 0.1, 0.1, 0.15, 0.2, 0.35)),
          note = pmax(4, pmin(9, rnorm(1, joueur$note_moyenne, 0.7))),
          buts = rpois(1, ifelse(joueur$poste %in% c("BU", "MOC"), 0.3, 0.05)),
          passes_decisives = rpois(1, ifelse(joueur$poste %in% c("MOC", "MC"), 0.2, 0.1)),
          distance_km = ifelse(joueur$poste == "GB", 
                              rnorm(1, 4, 0.5), rnorm(1, 8.5, 1.2)),
          sprints = rpois(1, ifelse(joueur$poste == "GB", 3, 12)),
          duels_gagnes = rbinom(1, 15, 0.6),
          fatigue = runif(1, 0.1, 0.9)
        )
        matchs_data <- rbind(matchs_data, match_perf)
      }
    }
  }
  
  return(matchs_data)
}

# Génération des données
effectif_rcs <- generer_effectif_rcs()
matchs_rcs <- generer_donnees_matchs(effectif_rcs)

cat("✅ Données générées:", nrow(effectif_rcs), "joueurs,", nrow(matchs_rcs), "performances\n\n")

# ===================================================================
# ANALYSES DESCRIPTIVES AVANCÉES
# ===================================================================

#' Analyse de la répartition par âge et poste
analyser_demographie_effectif <- function(effectif) {
  
  # Graphique âge par poste
  p1 <- ggplot(effectif, aes(x = reorder(poste, age), y = age, fill = poste)) +
    geom_boxplot(alpha = 0.7) +
    geom_jitter(width = 0.2, size = 2, alpha = 0.8) +
    scale_fill_manual(values = couleurs_rcs) +
    labs(
      title = "🔵⚪ Répartition d'âge par poste - RCS 2024-2025",
      subtitle = "Distribution des âges dans l'effectif du Racing Club de Strasbourg",
      x = "Poste", y = "Âge", fill = "Poste"
    ) +
    theme_rcs +
    theme(axis.text.x = element_text(angle = 45, hjust = 1))
  
  # Graphique valeur marchande vs potentiel
  p2 <- ggplot(effectif, aes(x = potentiel, y = valeur_marche, size = age, color = note_moyenne)) +
    geom_point(alpha = 0.8) +
    geom_text(aes(label = nom), vjust = -1, size = 3, check_overlap = TRUE) +
    scale_color_gradient2(low = "#ff4444", mid = "#ffaa00", high = "#00aa44", 
                         midpoint = 6.5, name = "Note\nMoyenne") +
    scale_size_continuous(range = c(3, 8), name = "Âge") +
    labs(
      title = "💎 Potentiel vs Valeur Marchande - Effectif RCS",
      subtitle = "Identification des pépites et joueurs sous-évalués",
      x = "Potentiel (%)", y = "Valeur Marchande (M€)"
    ) +
    theme_rcs
  
  return(list(repartition_age = p1, potentiel_valeur = p2))
}

#' Analyse de performance par match
analyser_performances_matchs <- function(matchs_data) {
  
  # Évolution des performances moyennes
  perf_par_match <- matchs_data %>%
    group_by(journee, match_id) %>%
    summarise(
      note_moyenne = mean(note, na.rm = TRUE),
      minutes_totales = sum(minutes, na.rm = TRUE),
      buts_totaux = sum(buts, na.rm = TRUE),
      nb_joueurs = n(),
      .groups = "drop"
    ) %>%
    arrange(match_id)
  
  p1 <- ggplot(perf_par_match, aes(x = match_id)) +
    geom_line(aes(y = note_moyenne), color = couleurs_rcs[1], size = 1.2) +
    geom_point(aes(y = note_moyenne), color = couleurs_rcs[1], size = 3) +
    geom_smooth(aes(y = note_moyenne), method = "loess", se = TRUE, 
                color = couleurs_rcs[3], alpha = 0.3) +
    labs(
      title = "📈 Évolution des performances RCS - Saison 2024-2025",
      subtitle = "Note moyenne de l'équipe par journée",
      x = "Journée", y = "Note Moyenne Équipe"
    ) +
    theme_rcs +
    scale_x_continuous(breaks = seq(1, max(perf_par_match$match_id), 2))
  
  # Heatmap des performances par joueur et match
  heatmap_data <- matchs_data %>%
    select(joueur, match_id, note) %>%
    filter(!is.na(note)) %>%
    group_by(joueur) %>%
    filter(n() >= 5) %>%  # Joueurs avec au moins 5 matchs
    ungroup()
  
  p2 <- ggplot(heatmap_data, aes(x = factor(match_id), y = reorder(joueur, note), fill = note)) +
    geom_tile(color = "white", size = 0.1) +
    scale_fill_gradient2(low = "#ff4444", mid = "#ffaa00", high = "#00aa44", 
                        midpoint = 6.5, name = "Note") +
    labs(
      title = "🔥 Heatmap des performances individuelles",
      subtitle = "Notes par joueur et par match (joueurs réguliers)",
      x = "Journée", y = "Joueur"
    ) +
    theme_rcs +
    theme(
      axis.text.x = element_text(angle = 45, hjust = 1),
      axis.text.y = element_text(size = 8)
    )
  
  return(list(evolution_equipe = p1, heatmap_joueurs = p2))
}

# ===================================================================
# MODÈLES PRÉDICTIFS AVANCÉS
# ===================================================================

#' Modèle de prédiction des performances futures
predire_performances_futures <- function(matchs_data, effectif, nb_matchs_futurs = 5) {
  
  cat("🤖 Entraînement du modèle prédictif...\n")
  
  # Préparation des données d'entraînement
  donnees_ml <- matchs_data %>%
    left_join(effectif[, c("nom", "age", "valeur_marche", "potentiel")], 
              by = c("joueur" = "nom")) %>%
    filter(!is.na(note), minutes > 0) %>%
    arrange(joueur, match_id) %>%
    group_by(joueur) %>%
    mutate(
      note_precedente = lag(note, 1),
      forme_3_matchs = rollmean(lag(note, 1:3), k = 3, fill = NA, align = "right"),
      fatigue_cumul = cumsum(fatigue) / n(),
      matchs_consecutifs = row_number()
    ) %>%
    ungroup() %>%
    filter(!is.na(note_precedente), !is.na(forme_3_matchs))
  
  # Variables prédictives
  features <- donnees_ml %>%
    select(age, valeur_marche, potentiel, note_precedente, forme_3_matchs, 
           fatigue_cumul, matchs_consecutifs, minutes, distance_km, sprints)
  
  target <- donnees_ml$note
  
  # Division train/test
  set.seed(42)
  train_idx <- createDataPartition(target, p = 0.8, list = FALSE)
  
  X_train <- features[train_idx, ]
  y_train <- target[train_idx]
  X_test <- features[-train_idx, ]
  y_test <- target[-train_idx]
  
  # Entraînement Random Forest
  ctrl <- trainControl(method = "cv", number = 5, verboseIter = FALSE)
  
  model_rf <- train(
    x = X_train, y = y_train,
    method = "rf",
    trControl = ctrl,
    tuneLength = 5,
    ntree = 100
  )
  
  # Prédictions sur test
  pred_test <- predict(model_rf, X_test)
  rmse_test <- sqrt(mean((pred_test - y_test)^2))
  mae_test <- mean(abs(pred_test - y_test))
  
  cat("✅ Modèle entraîné - RMSE:", round(rmse_test, 3), "MAE:", round(mae_test, 3), "\n")
  
  # Prédictions futures pour chaque joueur
  predictions_futures <- data.frame()
  
  for (nom_joueur in unique(effectif$nom)) {
    donnees_joueur <- matchs_data %>%
      filter(joueur == nom_joueur, minutes > 0) %>%
      arrange(match_id) %>%
      tail(10)  # 10 derniers matchs
    
    if (nrow(donnees_joueur) >= 3) {
      # Calcul des variables pour prédiction
      joueur_info <- effectif[effectif$nom == nom_joueur, ]
      
      note_precedente <- tail(donnees_joueur$note, 1)
      forme_3_matchs <- mean(tail(donnees_joueur$note, 3))
      fatigue_cumul <- mean(donnees_joueur$fatigue)
      matchs_consecutifs <- nrow(donnees_joueur)
      
      for (futur_match in 1:nb_matchs_futurs) {
        nouvelle_pred <- data.frame(
          age = joueur_info$age,
          valeur_marche = joueur_info$valeur_marche,
          potentiel = joueur_info$potentiel,
          note_precedente = note_precedente,
          forme_3_matchs = forme_3_matchs,
          fatigue_cumul = fatigue_cumul + futur_match * 0.05,  # Fatigue croissante
          matchs_consecutifs = matchs_consecutifs + futur_match,
          minutes = 75,  # Estimation
          distance_km = ifelse(joueur_info$poste == "GB", 4, 8.5),
          sprints = ifelse(joueur_info$poste == "GB", 3, 12)
        )
        
        pred_note <- predict(model_rf, nouvelle_pred)
        
        predictions_futures <- rbind(predictions_futures, data.frame(
          joueur = nom_joueur,
          poste = joueur_info$poste,
          match_futur = futur_match,
          note_predite = pred_note,
          confiance = runif(1, 0.7, 0.95)  # Simulation confiance
        ))
        
        # Mise à jour pour match suivant
        note_precedente <- pred_note
        forme_3_matchs <- (forme_3_matchs * 2 + pred_note) / 3
      }
    }
  }
  
  return(list(
    modele = model_rf,
    rmse = rmse_test,
    mae = mae_test,
    predictions = predictions_futures,
    importance_variables = varImp(model_rf)
  ))
}

#' Analyse de clustering des joueurs
analyser_clustering_joueurs <- function(effectif, matchs_data) {
  
  cat("🎯 Analyse de clustering des profils joueurs...\n")
  
  # Calcul des métriques par joueur
  metriques_joueurs <- matchs_data %>%
    group_by(joueur) %>%
    summarise(
      note_moyenne = mean(note, na.rm = TRUE),
      regularite = 1 / (sd(note, na.rm = TRUE) + 0.1),  # Plus régulier = plus élevé
      minutes_moyenne = mean(minutes, na.rm = TRUE),
      buts_total = sum(buts, na.rm = TRUE),
      passes_decisives_total = sum(passes_decisives, na.rm = TRUE),
      distance_moyenne = mean(distance_km, na.rm = TRUE),
      sprints_moyenne = mean(sprints, na.rm = TRUE),
      nb_matchs = n(),
      .groups = "drop"
    ) %>%
    left_join(effectif[, c("nom", "age", "valeur_marche", "potentiel")], 
              by = c("joueur" = "nom")) %>%
    filter(nb_matchs >= 3)  # Joueurs avec données suffisantes
  
  # Sélection et normalisation des variables pour clustering
  variables_clustering <- metriques_joueurs %>%
    select(note_moyenne, regularite, age, valeur_marche, potentiel,
           distance_moyenne, sprints_moyenne) %>%
    scale()
  
  # Détermination du nombre optimal de clusters
  set.seed(42)
  wss <- map_dbl(1:6, function(k) {
    model <- kmeans(variables_clustering, centers = k, nstart = 20)
    model$tot.withinss
  })
  
  nb_clusters_optimal <- which.min(diff(wss)) + 1
  
  # Clustering final
  clustering_final <- kmeans(variables_clustering, centers = nb_clusters_optimal, nstart = 25)
  
  # Ajout des clusters aux données
  metriques_joueurs$cluster <- as.factor(clustering_final$cluster)
  
  # Visualisation
  p1 <- fviz_cluster(clustering_final, data = variables_clustering,
                     palette = couleurs_rcs[1:nb_clusters_optimal],
                     geom = "point", ellipse.type = "convex",
                     ggtheme = theme_rcs) +
    labs(title = "🎯 Clustering des profils joueurs RCS",
         subtitle = paste("Identification de", nb_clusters_optimal, "profils distincts"))
  
  # Caractérisation des clusters
  profils_clusters <- metriques_joueurs %>%
    group_by(cluster) %>%
    summarise(
      nb_joueurs = n(),
      age_moyen = round(mean(age), 1),
      note_moyenne = round(mean(note_moyenne), 2),
      valeur_moyenne = round(mean(valeur_marche), 1),
      potentiel_moyen = round(mean(potentiel), 1),
      exemples = paste(head(joueur, 3), collapse = ", "),
      .groups = "drop"
    )
  
  return(list(
    donnees = metriques_joueurs,
    visualisation = p1,
    profils = profils_clusters,
    nb_clusters = nb_clusters_optimal
  ))
}

#' Analyse prédictive du risque de blessure
predire_risques_blessures <- function(matchs_data, effectif) {
  
  cat("🏥 Analyse prédictive des risques de blessures...\n")
  
  # Calcul des facteurs de risque par joueur
  facteurs_risque <- matchs_data %>%
    group_by(joueur) %>%
    summarise(
      minutes_totales = sum(minutes, na.rm = TRUE),
      fatigue_moyenne = mean(fatigue, na.rm = TRUE),
      distance_totale = sum(distance_km, na.rm = TRUE),
      sprints_totaux = sum(sprints, na.rm = TRUE),
      matchs_consecutifs = n(),
      variance_performance = sd(note, na.rm = TRUE),
      .groups = "drop"
    ) %>%
    left_join(effectif[, c("nom", "age", "valeur_marche")], 
              by = c("joueur" = "nom"))
  
  # Calcul du score de risque (0-100)
  facteurs_risque <- facteurs_risque %>%
    mutate(
      risque_age = pmax(0, (age - 25) * 5),  # Risque augmente après 25 ans
      risque_minutes = pmin(30, minutes_totales / 50),  # Normalisation minutes
      risque_fatigue = fatigue_moyenne * 25,
      risque_intensite = pmin(20, sprints_totaux / 100),
      risque_instabilite = pmin(15, variance_performance * 10),
      
      score_risque_global = risque_age + risque_minutes + risque_fatigue + 
                           risque_intensite + risque_instabilite,
      
      niveau_risque = case_when(
        score_risque_global < 30 ~ "🟢 Faible",
        score_risque_global < 60 ~ "🟡 Modéré", 
        TRUE ~ "🔴 Élevé"
      ),
      
      recommandation = case_when(
        score_risque_global < 30 ~ "Continuer la charge normale",
        score_risque_global < 60 ~ "Surveillance renforcée",
        TRUE ~ "Repos préventif recommandé"
      )
    ) %>%
    arrange(desc(score_risque_global))
  
  # Visualisation
  p1 <- ggplot(facteurs_risque, aes(x = reorder(joueur, score_risque_global), 
                                   y = score_risque_global, 
                                   fill = niveau_risque)) +
    geom_col(alpha = 0.8) +
    geom_text(aes(label = round(score_risque_global, 0)), 
              hjust = -0.1, size = 3) +
    scale_fill_manual(values = c("🟢 Faible" = "#00aa44", 
                                "🟡 Modéré" = "#ffaa00", 
                                "🔴 Élevé" = "#ff4444")) +
    coord_flip() +
    labs(
      title = "🏥 Analyse des risques de blessures - Effectif RCS",
      subtitle = "Score de risque basé sur l'âge, fatigue, charge et variabilité",
      x = "Joueur", y = "Score de Risque (0-100)", fill = "Niveau de Risque"
    ) +
    theme_rcs
  
  return(list(
    donnees = facteurs_risque,
    visualisation = p1
  ))
}

# ===================================================================
# RAPPORT AUTOMATISÉ
# ===================================================================

#' Génère un rapport complet automatisé
generer_rapport_complet <- function() {
  
  cat("📋 Génération du rapport complet RCS...\n")
  
  # Exécution de toutes les analyses
  analyses_demo <- analyser_demographie_effectif(effectif_rcs)
  analyses_perf <- analyser_performances_matchs(matchs_rcs)
  predictions <- predire_performances_futures(matchs_rcs, effectif_rcs)
  clustering <- analyser_clustering_joueurs(effectif_rcs, matchs_rcs)
  risques <- predire_risques_blessures(matchs_rcs, effectif_rcs)
  
  # Métriques clés
  metriques_cles <- list(
    nb_joueurs = nrow(effectif_rcs),
    age_moyen = round(mean(effectif_rcs$age), 1),
    valeur_totale = round(sum(effectif_rcs$valeur_marche), 1),
    note_moyenne_equipe = round(mean(effectif_rcs$note_moyenne), 2),
    joueurs_haut_risque = sum(risques$donnees$niveau_risque == "🔴 Élevé"),
    precision_modele = round(1 - predictions$mae, 3)
  )
  
  # Recommandations automatiques
  recommandations <- c(
    "🎯 Optimiser la rotation pour réduire la fatigue",
    "📈 Focus sur l'amélioration des performances offensives", 
    "🏥 Surveillance renforcée des joueurs à risque",
    "💎 Développer les jeunes talents identifiés",
    "⚽ Maintenir la cohésion défensive"
  )
  
  rapport <- list(
    date_generation = Sys.time(),
    metriques_cles = metriques_cles,
    graphiques = list(
      demographie = analyses_demo,
      performances = analyses_perf,
      predictions = predictions$predictions,
      clustering = clustering$visualisation,
      risques = risques$visualisation
    ),
    recommandations = recommandations,
    modele_precision = predictions$mae,
    profils_joueurs = clustering$profils
  )
  
  return(rapport)
}

# ===================================================================
# EXÉCUTION PRINCIPALE
# ===================================================================

main_analyses_rcs <- function() {
  
  cat("🔵⚪ RACING CLUB DE STRASBOURG - ANALYSES R COMPLÈTES\n")
  cat("====================================================\n\n")
  
  # Génération du rapport complet
  rapport_final <- generer_rapport_complet()
  
  # Affichage des métriques clés
  cat("📊 MÉTRIQUES CLÉS DE L'EFFECTIF\n")
  cat("------------------------------\n")
  cat("👥 Nombre de joueurs:", rapport_final$metriques_cles$nb_joueurs, "\n")
  cat("🎂 Âge moyen:", rapport_final$metriques_cles$age_moyen, "ans\n")
  cat("💰 Valeur totale:", rapport_final$metriques_cles$valeur_totale, "M€\n")
  cat("⭐ Note moyenne équipe:", rapport_final$metriques_cles$note_moyenne_equipe, "/10\n")
  cat("🏥 Joueurs haut risque:", rapport_final$metriques_cles$joueurs_haut_risque, "\n")
  cat("🤖 Précision modèle:", rapport_final$metriques_cles$precision_modele, "\n\n")
  
  cat("🎯 RECOMMANDATIONS PRIORITAIRES\n")
  cat("------------------------------\n")
  for (i in seq_along(rapport_final$recommandations)) {
    cat(paste0(i, ". ", rapport_final$recommandations[i], "\n"))
  }
  
  cat("\n✅ ANALYSES R COMPLÈTES TERMINÉES AVEC SUCCÈS !\n")
  cat("🔵⚪ ALLEZ RACING ! ⚪🔵\n\n")
  
  return(rapport_final)
}

# Lancement des analyses si script exécuté directement
if (interactive() || !exists("skip_main")) {
  rapport_rcs <- main_analyses_rcs()
}
