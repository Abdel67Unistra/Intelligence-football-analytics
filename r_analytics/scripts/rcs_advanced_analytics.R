# ================================================================================
# 🔵⚪ RACING CLUB DE STRASBOURG - ANALYTICS R AVANCÉES ⚪🔵
# ================================================================================
# 
# Script R pour analyses statistiques avancées du Racing Club de Strasbourg
# Analyses prédictives, visualisations et modélisation statistique
#
# Auteur: Analytics Team RCS
# Date: Septembre 2025
# Version: 2.0
# ================================================================================

# Chargement des bibliothèques nécessaires
if (!require("pacman")) install.packages("pacman")
pacman::p_load(
  tidyverse,      # Manipulation de données
  ggplot2,        # Visualisations
  plotly,         # Graphiques interactifs
  corrplot,       # Matrices de corrélation
  cluster,        # Clustering
  factoextra,     # Analyses factorielles
  caret,          # Machine learning
  randomForest,   # Forêts aléatoires
  glmnet,         # Régression pénalisée
  VIM,            # Valeurs manquantes
  gridExtra,      # Arrangement graphiques
  RColorBrewer,   # Palettes de couleurs
  knitr,          # Rapports
  DT,             # Tableaux interactifs
  lubridate,      # Dates
  forecast,       # Séries temporelles
  e1071           # SVM
)

# Configuration globale
options(scipen = 999)  # Désactiver notation scientifique
set.seed(42)          # Reproductibilité

# Couleurs RCS
rcs_colors <- list(
  primary = "#0066CC",
  secondary = "#FFFFFF", 
  accent = "#FFD700",
  success = "#28a745",
  warning = "#ffc107",
  danger = "#dc3545"
)

# ================================================================================
# FONCTIONS UTILITAIRES
# ================================================================================

#' Génère des données RCS simulées mais réalistes
#' 
#' @return data.frame contenant les données des joueurs RCS
generate_rcs_data <- function() {
  
  # Données joueurs RCS 2025
  joueurs <- data.frame(
    nom = c("Emegha", "Thomasson", "Diallo", "Djiku", "Doué", 
            "Santos", "Sahi", "Nanasi", "Bellegarde", "Prcic",
            "Guilbert", "Nyamsi", "Le Marchand", "Fila", "Sarr"),
    poste = c("BU", "MC", "AT", "DC", "MC", "DG", "GB", "AD", 
              "MC", "MC", "DD", "DC", "DC", "BU", "MG"),
    age = c(26, 30, 24, 29, 22, 28, 27, 21, 26, 29, 30, 27, 32, 23, 20),
    matchs = c(5, 5, 4, 5, 5, 4, 5, 3, 4, 3, 5, 4, 3, 2, 1),
    buts = c(4, 2, 3, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0),
    passes_decisives = c(0, 3, 1, 2, 4, 2, 0, 2, 2, 1, 3, 0, 1, 0, 1),
    minutes = c(450, 420, 360, 450, 400, 340, 450, 180, 320, 150, 400, 300, 200, 90, 30),
    note = c(8.3, 7.8, 8.1, 7.2, 7.5, 7.1, 6.9, 7.4, 7.3, 6.8, 7.0, 7.1, 6.9, 7.2, 6.5),
    valeur_marche = c(8, 12, 15, 5, 18, 3, 2, 10, 8, 4, 2, 3, 1, 5, 2), # en millions €
    salaire = c(80, 120, 200, 60, 150, 40, 50, 90, 100, 70, 45, 55, 35, 60, 25), # en milliers €/mois
    nationalite = c("NGA", "FRA", "SEN", "GHA", "FRA", "BRA", "FRA", "SWE", 
                    "FRA", "BIH", "FRA", "CMR", "FRA", "SEN", "FRA")
  )
  
  # Calcul métriques avancées
  joueurs <- joueurs %>%
    mutate(
      but_par_match = round(buts / matchs, 2),
      passe_par_match = round(passes_decisives / matchs, 2),
      minutes_par_match = round(minutes / matchs, 0),
      efficacite = round((buts + passes_decisives) / (minutes / 90), 2),
      rapport_valeur_note = round(valeur_marche / note, 2),
      categorie_age = case_when(
        age <= 22 ~ "Jeune",
        age <= 28 ~ "Expérimenté", 
        TRUE ~ "Vétéran"
      ),
      statut_titulaire = ifelse(minutes >= 300, "Titulaire", "Remplaçant")
    )
  
  return(joueurs)
}

#' Génère les données des matchs RCS
#' 
#' @return data.frame contenant l'historique des matchs
generate_match_data <- function() {
  
  matchs <- data.frame(
    date = as.Date(c("2025-09-01", "2025-08-25", "2025-08-18", 
                     "2025-08-11", "2025-08-04", "2025-07-28",
                     "2025-07-21", "2025-07-14")),
    adversaire = c("AS Monaco", "Olympique Lyonnais", "FC Nantes",
                   "Stade Rennais", "OGC Nice", "Toulouse FC",
                   "RC Lens", "Montpellier HSC"),
    domicile = c(TRUE, FALSE, TRUE, FALSE, TRUE, FALSE, TRUE, TRUE),
    buts_pour = c(1, 0, 2, 1, 3, 1, 2, 1),
    buts_contre = c(2, 1, 1, 1, 0, 2, 1, 0),
    xg_pour = c(1.3, 0.9, 1.7, 1.2, 2.1, 1.1, 1.8, 1.4),
    xg_contre = c(1.8, 1.4, 1.1, 1.3, 0.6, 1.9, 1.2, 0.8),
    possession = c(45, 38, 52, 44, 58, 41, 49, 55),
    passes_reussies = c(387, 298, 441, 356, 489, 312, 402, 467),
    passes_totales = c(456, 378, 512, 429, 567, 398, 478, 523),
    duels_gagnes = c(48, 42, 55, 47, 61, 39, 52, 58)
  )
  
  # Calcul métriques dérivées
  matchs <- matchs %>%
    mutate(
      resultat = case_when(
        buts_pour > buts_contre ~ "V",
        buts_pour < buts_contre ~ "D",
        TRUE ~ "N"
      ),
      points = case_when(
        resultat == "V" ~ 3,
        resultat == "N" ~ 1,
        TRUE ~ 0
      ),
      difference_buts = buts_pour - buts_contre,
      difference_xg = round(xg_pour - xg_contre, 2),
      pourcentage_passes = round((passes_reussies / passes_totales) * 100, 1),
      efficacite_offensive = round(buts_pour / xg_pour, 2),
      solidite_defensive = round(xg_contre / buts_contre, 2),
      performance_globale = round((points * 2 + difference_buts + difference_xg) / 4, 2)
    ) %>%
    arrange(desc(date))
  
  return(matchs)
}

# ================================================================================
# ANALYSES DESCRIPTIVES
# ================================================================================

#' Analyse descriptive complète des joueurs RCS
#' 
#' @param data data.frame des joueurs
#' @return liste des résultats d'analyse
analyse_descriptive_joueurs <- function(data) {
  
  cat("=== ANALYSE DESCRIPTIVE - JOUEURS RCS ===\n\n")
  
  # Résumé statistique
  print("Résumé statistique des variables numériques:")
  print(summary(data %>% select_if(is.numeric)))
  
  cat("\n")
  
  # Répartition par poste
  print("Répartition par poste:")
  print(table(data$poste))
  
  cat("\n")
  
  # Top joueurs par critères
  cat("TOP 5 BUTEURS:\n")
  print(data %>% 
          arrange(desc(buts)) %>% 
          select(nom, poste, buts, matchs) %>% 
          head(5))
  
  cat("\nTOP 5 PASSEURS:\n")
  print(data %>% 
          arrange(desc(passes_decisives)) %>% 
          select(nom, poste, passes_decisives, matchs) %>% 
          head(5))
  
  cat("\nTOP 5 NOTES:\n")
  print(data %>% 
          arrange(desc(note)) %>% 
          select(nom, poste, note, matchs) %>% 
          head(5))
  
  # Corrélations
  cor_matrix <- cor(data %>% select_if(is.numeric), use = "complete.obs")
  
  return(list(
    summary_stats = summary(data %>% select_if(is.numeric)),
    correlation_matrix = cor_matrix,
    top_scorers = data %>% arrange(desc(buts)) %>% head(5),
    top_assists = data %>% arrange(desc(passes_decisives)) %>% head(5)
  ))
}

#' Analyse des performances par match
#' 
#' @param matchs data.frame des matchs
#' @return analyse des performances
analyse_performances_matchs <- function(matchs) {
  
  cat("=== ANALYSE PERFORMANCES MATCHS ===\n\n")
  
  # Statistiques globales
  total_matchs <- nrow(matchs)
  victoires <- sum(matchs$resultat == "V")
  nuls <- sum(matchs$resultat == "N") 
  defaites <- sum(matchs$resultat == "D")
  
  cat(sprintf("Total matchs: %d\n", total_matchs))
  cat(sprintf("Victoires: %d (%.1f%%)\n", victoires, (victoires/total_matchs)*100))
  cat(sprintf("Nuls: %d (%.1f%%)\n", nuls, (nuls/total_matchs)*100))
  cat(sprintf("Défaites: %d (%.1f%%)\n", defaites, (defaites/total_matchs)*100))
  
  # Performance domicile vs extérieur
  perf_domicile <- matchs %>% 
    group_by(domicile) %>%
    summarise(
      matchs = n(),
      victoires = sum(resultat == "V"),
      points_moyens = mean(points),
      buts_moyens = mean(buts_pour),
      .groups = 'drop'
    )
  
  cat("\nPerformance Domicile vs Extérieur:\n")
  print(perf_domicile)
  
  return(list(
    bilan = c(victoires, nuls, defaites),
    performance_domicile = perf_domicile,
    moyenne_buts = mean(matchs$buts_pour),
    moyenne_xg = mean(matchs$xg_pour)
  ))
}

# ================================================================================
# VISUALISATIONS AVANCÉES
# ================================================================================

#' Crée un radar chart des performances joueurs
#' 
#' @param data data.frame des joueurs
#' @param joueur_nom nom du joueur à analyser
#' @return graphique radar
create_player_radar <- function(data, joueur_nom) {
  
  # Sélection du joueur
  player_data <- data %>% filter(nom == joueur_nom)
  
  if(nrow(player_data) == 0) {
    stop("Joueur non trouvé")
  }
  
  # Normalisation des métriques (0-100)
  metrics <- data %>%
    mutate(
      buts_norm = (buts / max(buts, na.rm = TRUE)) * 100,
      passes_norm = (passes_decisives / max(passes_decisives, na.rm = TRUE)) * 100,
      note_norm = ((note - min(note, na.rm = TRUE)) / (max(note, na.rm = TRUE) - min(note, na.rm = TRUE))) * 100,
      minutes_norm = (minutes / max(minutes, na.rm = TRUE)) * 100,
      efficacite_norm = (efficacite / max(efficacite, na.rm = TRUE)) * 100
    )
  
  player_metrics <- metrics %>% filter(nom == joueur_nom)
  
  # Données pour le radar
  radar_data <- data.frame(
    Metric = c("Buts", "Passes D.", "Note", "Minutes", "Efficacité"),
    Value = c(
      player_metrics$buts_norm,
      player_metrics$passes_norm, 
      player_metrics$note_norm,
      player_metrics$minutes_norm,
      player_metrics$efficacite_norm
    )
  )
  
  # Graphique radar avec ggplot2
  p <- ggplot(radar_data, aes(x = Metric, y = Value)) +
    geom_polygon(aes(group = 1), fill = rcs_colors$primary, alpha = 0.3, color = rcs_colors$primary, size = 2) +
    geom_point(color = rcs_colors$primary, size = 4) +
    coord_polar() +
    ylim(0, 100) +
    labs(
      title = paste("Radar de Performance -", joueur_nom),
      subtitle = paste("Poste:", player_data$poste, "| Note:", player_data$note)
    ) +
    theme_minimal() +
    theme(
      plot.title = element_text(hjust = 0.5, size = 16, color = rcs_colors$primary),
      plot.subtitle = element_text(hjust = 0.5, size = 12),
      axis.text.y = element_blank(),
      axis.ticks.y = element_blank(),
      panel.grid.major = element_line(color = "gray90"),
      panel.grid.minor = element_blank()
    )
  
  return(p)
}

#' Heatmap des corrélations entre variables
#' 
#' @param data data.frame
#' @return graphique heatmap
create_correlation_heatmap <- function(data) {
  
  # Sélection variables numériques
  numeric_vars <- data %>% 
    select_if(is.numeric) %>%
    select(-c(matchs)) # Exclure certaines variables si nécessaire
  
  # Matrice de corrélation
  cor_matrix <- cor(numeric_vars, use = "complete.obs")
  
  # Conversion en format long pour ggplot
  cor_long <- cor_matrix %>%
    as.data.frame() %>%
    rownames_to_column("Var1") %>%
    pivot_longer(-Var1, names_to = "Var2", values_to = "Correlation")
  
  # Heatmap
  p <- ggplot(cor_long, aes(x = Var1, y = Var2, fill = Correlation)) +
    geom_tile(color = "white") +
    scale_fill_gradient2(
      low = rcs_colors$danger, 
      high = rcs_colors$success, 
      mid = "white",
      midpoint = 0,
      name = "Corrélation"
    ) +
    geom_text(aes(label = round(Correlation, 2)), size = 3) +
    labs(
      title = "Matrice de Corrélation - Variables RCS",
      x = "", y = ""
    ) +
    theme_minimal() +
    theme(
      plot.title = element_text(hjust = 0.5, size = 14, color = rcs_colors$primary),
      axis.text.x = element_text(angle = 45, hjust = 1),
      panel.grid = element_blank()
    )
  
  return(p)
}

#' Graphique évolution des performances par match
#' 
#' @param matchs data.frame des matchs
#' @return graphique temporel
create_performance_timeline <- function(matchs) {
  
  # Calcul points cumulés
  matchs_ordered <- matchs %>% 
    arrange(date) %>%
    mutate(
      points_cumules = cumsum(points),
      match_number = row_number(),
      performance_mobile = zoo::rollmean(performance_globale, k = 3, fill = NA, align = "right")
    )
  
  # Graphique principal
  p1 <- ggplot(matchs_ordered, aes(x = date)) +
    geom_line(aes(y = points_cumules), color = rcs_colors$primary, size = 2) +
    geom_point(aes(y = points_cumules), color = rcs_colors$primary, size = 4) +
    labs(
      title = "Évolution des Points Cumulés - RCS",
      x = "Date", 
      y = "Points Cumulés"
    ) +
    theme_minimal() +
    theme(
      plot.title = element_text(hjust = 0.5, size = 14, color = rcs_colors$primary)
    )
  
  # Graphique performance mobile
  p2 <- ggplot(matchs_ordered, aes(x = date)) +
    geom_line(aes(y = performance_mobile), color = rcs_colors$accent, size = 2) +
    geom_point(aes(y = performance_mobile), color = rcs_colors$accent, size = 3) +
    labs(
      title = "Performance Mobile (Moyenne 3 matchs)",
      x = "Date",
      y = "Performance"
    ) +
    theme_minimal() +
    theme(
      plot.title = element_text(hjust = 0.5, size = 14, color = rcs_colors$primary)
    )
  
  # Combinaison des graphiques
  combined_plot <- grid.arrange(p1, p2, ncol = 1)
  
  return(combined_plot)
}

# ================================================================================
# MODÉLISATION PRÉDICTIVE
# ================================================================================

#' Modèle prédictif pour les notes des joueurs
#' 
#' @param data data.frame des joueurs
#' @return modèle et prédictions
predict_player_ratings <- function(data) {
  
  cat("=== MODÉLISATION PRÉDICTIVE - NOTES JOUEURS ===\n\n")
  
  # Préparation des données
  model_data <- data %>%
    select(note, buts, passes_decisives, minutes, age, valeur_marche) %>%
    na.omit()
  
  # Division train/test (70/30)
  train_index <- createDataPartition(model_data$note, p = 0.7, list = FALSE)
  train_data <- model_data[train_index, ]
  test_data <- model_data[-train_index, ]
  
  # 1. Régression linéaire multiple
  lm_model <- lm(note ~ ., data = train_data)
  lm_pred <- predict(lm_model, test_data)
  lm_rmse <- sqrt(mean((test_data$note - lm_pred)^2))
  
  cat("Régression Linéaire Multiple:\n")
  print(summary(lm_model))
  cat(sprintf("RMSE: %.3f\n\n", lm_rmse))
  
  # 2. Random Forest
  rf_model <- randomForest(note ~ ., data = train_data, ntree = 500)
  rf_pred <- predict(rf_model, test_data)
  rf_rmse <- sqrt(mean((test_data$note - rf_pred)^2))
  
  cat("Random Forest:\n")
  print(rf_model)
  cat(sprintf("RMSE: %.3f\n\n", rf_rmse))
  
  # 3. Support Vector Machine
  svm_model <- svm(note ~ ., data = train_data)
  svm_pred <- predict(svm_model, test_data)
  svm_rmse <- sqrt(mean((test_data$note - svm_pred)^2))
  
  cat("Support Vector Machine:\n")
  cat(sprintf("RMSE: %.3f\n\n", svm_rmse))
  
  # Comparaison des modèles
  model_comparison <- data.frame(
    Modele = c("Régression Linéaire", "Random Forest", "SVM"),
    RMSE = c(lm_rmse, rf_rmse, svm_rmse)
  ) %>%
    arrange(RMSE)
  
  cat("Comparaison des modèles:\n")
  print(model_comparison)
  
  # Graphique comparaison prédictions vs réalité
  predictions_df <- data.frame(
    Reel = test_data$note,
    LM = lm_pred,
    RF = rf_pred,
    SVM = svm_pred
  ) %>%
    pivot_longer(-Reel, names_to = "Modele", values_to = "Prediction")
  
  p <- ggplot(predictions_df, aes(x = Reel, y = Prediction, color = Modele)) +
    geom_point(alpha = 0.7, size = 3) +
    geom_abline(intercept = 0, slope = 1, linetype = "dashed", color = "gray50") +
    facet_wrap(~Modele) +
    labs(
      title = "Prédictions vs Réalité - Notes Joueurs",
      x = "Note Réelle",
      y = "Note Prédite"
    ) +
    theme_minimal() +
    theme(
      plot.title = element_text(hjust = 0.5, size = 14, color = rcs_colors$primary),
      legend.position = "none"
    )
  
  return(list(
    models = list(lm = lm_model, rf = rf_model, svm = svm_model),
    comparison = model_comparison,
    plot = p
  ))
}

#' Clustering des joueurs par performance
#' 
#' @param data data.frame des joueurs
#' @return résultats du clustering
cluster_players_performance <- function(data) {
  
  cat("=== CLUSTERING DES JOUEURS ===\n\n")
  
  # Sélection des variables pour clustering
  cluster_vars <- data %>%
    select(buts, passes_decisives, note, minutes, efficacite, valeur_marche) %>%
    scale() # Standardisation
  
  # Détermination du nombre optimal de clusters (méthode du coude)
  wss <- map_dbl(1:10, ~{
    kmeans(cluster_vars, .x, nstart = 20)$tot.withinss
  })
  
  # Graphique du coude
  elbow_plot <- data.frame(k = 1:10, wss = wss) %>%
    ggplot(aes(x = k, y = wss)) +
    geom_line(color = rcs_colors$primary, size = 1.5) +
    geom_point(color = rcs_colors$primary, size = 3) +
    labs(
      title = "Méthode du Coude - Nombre Optimal de Clusters",
      x = "Nombre de Clusters (k)",
      y = "Within Sum of Squares"
    ) +
    theme_minimal() +
    theme(
      plot.title = element_text(hjust = 0.5, size = 14, color = rcs_colors$primary)
    )
  
  # K-means avec k=3 (optimal estimé)
  k_optimal <- 3
  kmeans_result <- kmeans(cluster_vars, centers = k_optimal, nstart = 20)
  
  # Ajout des clusters aux données originales
  data_with_clusters <- data %>%
    mutate(cluster = as.factor(kmeans_result$cluster))
  
  # Caractérisation des clusters
  cluster_summary <- data_with_clusters %>%
    group_by(cluster) %>%
    summarise(
      effectif = n(),
      note_moyenne = round(mean(note), 2),
      buts_moyens = round(mean(buts), 2),
      passes_moyennes = round(mean(passes_decisives), 2),
      valeur_moyenne = round(mean(valeur_marche), 1),
      .groups = 'drop'
    )
  
  cat("Caractérisation des clusters:\n")
  print(cluster_summary)
  
  # Visualisation PCA
  pca_result <- prcomp(cluster_vars, scale. = FALSE)
  pca_data <- data.frame(
    PC1 = pca_result$x[,1],
    PC2 = pca_result$x[,2],
    Cluster = data_with_clusters$cluster,
    Nom = data_with_clusters$nom,
    Poste = data_with_clusters$poste
  )
  
  pca_plot <- ggplot(pca_data, aes(x = PC1, y = PC2, color = Cluster)) +
    geom_point(size = 4, alpha = 0.8) +
    geom_text(aes(label = Nom), hjust = 0, vjust = 0, size = 3, nudge_x = 0.1) +
    scale_color_manual(values = c(rcs_colors$primary, rcs_colors$accent, rcs_colors$danger)) +
    labs(
      title = "Clustering des Joueurs - Projection PCA",
      x = paste0("PC1 (", round(summary(pca_result)$importance[2,1]*100, 1), "%)"),
      y = paste0("PC2 (", round(summary(pca_result)$importance[2,2]*100, 1), "%)")
    ) +
    theme_minimal() +
    theme(
      plot.title = element_text(hjust = 0.5, size = 14, color = rcs_colors$primary)
    )
  
  return(list(
    elbow_plot = elbow_plot,
    cluster_data = data_with_clusters,
    cluster_summary = cluster_summary,
    pca_plot = pca_plot,
    kmeans_model = kmeans_result
  ))
}

# ================================================================================
# PRÉDICTIONS DE MATCHS
# ================================================================================

#' Modèle prédictif pour les résultats de matchs
#' 
#' @param matchs data.frame des matchs
#' @return modèle et prédictions futures
predict_match_outcomes <- function(matchs) {
  
  cat("=== PRÉDICTION RÉSULTATS MATCHS ===\n\n")
  
  # Feature engineering
  model_data <- matchs %>%
    mutate(
      adversaire_force = case_when(
        adversaire %in% c("Paris Saint-Germain", "AS Monaco", "Olympique Lyonnais") ~ "Fort",
        adversaire %in% c("OGC Nice", "Stade Rennais", "RC Lens") ~ "Moyen",
        TRUE ~ "Faible"
      ),
      mois = month(date),
      jour_semaine = wday(date),
      forme_recente = lag(zoo::rollmean(points, k = 3, fill = NA, align = "right"), 1)
    ) %>%
    na.omit()
  
  # Variables prédictives
  predictors <- c("domicile", "adversaire_force", "possession", "xg_pour", "forme_recente")
  
  # Conversion variables catégorielles
  model_data$domicile <- as.factor(model_data$domicile)
  model_data$adversaire_force <- as.factor(model_data$adversaire_force)
  model_data$resultat <- as.factor(model_data$resultat)
  
  # Modèle Random Forest pour classification
  if(nrow(model_data) >= 5) {
    rf_match_model <- randomForest(
      resultat ~ domicile + adversaire_force + possession + xg_pour,
      data = model_data,
      ntree = 100
    )
    
    print("Modèle Random Forest - Prédiction Résultats:")
    print(rf_match_model)
    
    # Prédictions pour prochains matchs (simulation)
    prochains_matchs <- data.frame(
      adversaire = c("Olympique de Marseille", "Lille OSC", "Paris Saint-Germain", "Montpellier HSC"),
      domicile = c(TRUE, FALSE, TRUE, FALSE),
      adversaire_force = c("Fort", "Fort", "Fort", "Faible"),
      possession = c(50, 45, 52, 55), # Estimation
      xg_pour = c(1.5, 1.2, 1.8, 1.6) # Estimation
    )
    
    prochains_matchs$domicile <- as.factor(prochains_matchs$domicile)
    prochains_matchs$adversaire_force <- as.factor(prochains_matchs$adversaire_force)
    
    # Prédictions
    predictions <- predict(rf_match_model, prochains_matchs, type = "prob")
    
    resultats_predictions <- data.frame(
      Adversaire = prochains_matchs$adversaire,
      Domicile = prochains_matchs$domicile,
      Prob_Victoire = round(predictions[,"V"] * 100, 1),
      Prob_Nul = round(predictions[,"N"] * 100, 1),
      Prob_Defaite = round(predictions[,"D"] * 100, 1)
    )
    
    cat("\nPrédictions prochains matchs:\n")
    print(resultats_predictions)
    
    # Visualisation des prédictions
    pred_long <- resultats_predictions %>%
      select(Adversaire, Prob_Victoire, Prob_Nul, Prob_Defaite) %>%
      pivot_longer(-Adversaire, names_to = "Resultat", values_to = "Probabilite") %>%
      mutate(
        Resultat = str_remove(Resultat, "Prob_"),
        Couleur = case_when(
          Resultat == "Victoire" ~ rcs_colors$success,
          Resultat == "Nul" ~ rcs_colors$warning,
          Resultat == "Defaite" ~ rcs_colors$danger
        )
      )
    
    pred_plot <- ggplot(pred_long, aes(x = Adversaire, y = Probabilite, fill = Resultat)) +
      geom_col(position = "dodge") +
      scale_fill_manual(values = c("Defaite" = rcs_colors$danger, 
                                   "Nul" = rcs_colors$warning, 
                                   "Victoire" = rcs_colors$success)) +
      labs(
        title = "Prédictions Prochains Matchs RCS",
        x = "Adversaire",
        y = "Probabilité (%)",
        fill = "Résultat"
      ) +
      theme_minimal() +
      theme(
        plot.title = element_text(hjust = 0.5, size = 14, color = rcs_colors$primary),
        axis.text.x = element_text(angle = 45, hjust = 1)
      )
    
    return(list(
      model = rf_match_model,
      predictions = resultats_predictions,
      plot = pred_plot
    ))
  } else {
    cat("Données insuffisantes pour la modélisation prédictive\n")
    return(NULL)
  }
}

# ================================================================================
# GÉNÉRATION DE RAPPORT COMPLET
# ================================================================================

#' Génère un rapport complet d'analyse RCS
#' 
#' @param save_plots booléen pour sauvegarder les graphiques
#' @return rapport complet
generate_rcs_report <- function(save_plots = TRUE) {
  
  cat("=================================================================\n")
  cat("🔵⚪ RAPPORT D'ANALYSE COMPLET - RACING CLUB DE STRASBOURG ⚪🔵\n")
  cat("=================================================================\n\n")
  
  cat("Date de génération:", format(Sys.time(), "%d/%m/%Y %H:%M:%S"), "\n")
  cat("Saison: 2025/2026\n\n")
  
  # Chargement des données
  cat("📊 Chargement des données...\n")
  joueurs_data <- generate_rcs_data()
  matchs_data <- generate_match_data()
  
  # Analyses descriptives
  cat("\n🔍 Analyses descriptives...\n")
  desc_joueurs <- analyse_descriptive_joueurs(joueurs_data)
  perf_matchs <- analyse_performances_matchs(matchs_data)
  
  # Visualisations
  cat("\n📈 Génération des visualisations...\n")
  
  if(save_plots) {
    
    # Création du dossier de sortie
    output_dir <- "rcs_analytics_output"
    if(!dir.exists(output_dir)) dir.create(output_dir)
    
    # 1. Radar des top joueurs
    top_players <- head(joueurs_data[order(-joueurs_data$note),], 3)
    for(i in 1:nrow(top_players)) {
      radar_plot <- create_player_radar(joueurs_data, top_players$nom[i])
      ggsave(
        filename = file.path(output_dir, paste0("radar_", gsub(" ", "_", top_players$nom[i]), ".png")),
        plot = radar_plot,
        width = 10, height = 8, dpi = 300
      )
    }
    
    # 2. Heatmap corrélations
    heatmap_plot <- create_correlation_heatmap(joueurs_data)
    ggsave(
      filename = file.path(output_dir, "correlation_heatmap.png"),
      plot = heatmap_plot,
      width = 12, height = 10, dpi = 300
    )
    
    # 3. Timeline performances
    timeline_plot <- create_performance_timeline(matchs_data)
    ggsave(
      filename = file.path(output_dir, "performance_timeline.png"),
      plot = timeline_plot,
      width = 14, height = 10, dpi = 300
    )
    
    cat("✅ Graphiques sauvegardés dans", output_dir, "\n")
  }
  
  # Modélisation prédictive
  cat("\n🤖 Modélisation prédictive...\n")
  prediction_results <- predict_player_ratings(joueurs_data)
  
  if(save_plots && !is.null(prediction_results)) {
    ggsave(
      filename = file.path(output_dir, "predictions_comparison.png"),
      plot = prediction_results$plot,
      width = 12, height = 8, dpi = 300
    )
  }
  
  # Clustering
  cat("\n🎯 Clustering des joueurs...\n")
  cluster_results <- cluster_players_performance(joueurs_data)
  
  if(save_plots) {
    ggsave(
      filename = file.path(output_dir, "elbow_plot.png"),
      plot = cluster_results$elbow_plot,
      width = 10, height = 6, dpi = 300
    )
    
    ggsave(
      filename = file.path(output_dir, "pca_clustering.png"),
      plot = cluster_results$pca_plot,
      width = 12, height = 8, dpi = 300
    )
  }
  
  # Prédictions matchs
  cat("\n⚽ Prédictions de matchs...\n")
  match_predictions <- predict_match_outcomes(matchs_data)
  
  if(save_plots && !is.null(match_predictions)) {
    ggsave(
      filename = file.path(output_dir, "match_predictions.png"),
      plot = match_predictions$plot,
      width = 12, height = 8, dpi = 300
    )
  }
  
  # Résumé exécutif
  cat("\n" %+% "=" %+% rep("=", 60) %+% "\n")
  cat("📋 RÉSUMÉ EXÉCUTIF\n")
  cat("=" %+% rep("=", 60) %+% "\n\n")
  
  cat("🔵 ÉQUIPE:\n")
  cat(sprintf("  • Effectif analysé: %d joueurs\n", nrow(joueurs_data)))
  cat(sprintf("  • Note moyenne équipe: %.2f\n", mean(joueurs_data$note)))
  cat(sprintf("  • Valeur marchande totale: %.1fM€\n", sum(joueurs_data$valeur_marche)))
  
  cat("\n⚽ PERFORMANCES:\n")
  cat(sprintf("  • Matchs analysés: %d\n", nrow(matchs_data)))
  cat(sprintf("  • Bilan: %dV %dN %dD\n", perf_matchs$bilan[1], perf_matchs$bilan[2], perf_matchs$bilan[3]))
  cat(sprintf("  • Moyenne buts/match: %.1f\n", perf_matchs$moyenne_buts))
  cat(sprintf("  • xG moyen: %.2f\n", perf_matchs$moyenne_xg))
  
  cat("\n📊 INSIGHTS CLÉS:\n")
  cat("  • Meilleur buteur:", joueurs_data$nom[which.max(joueurs_data$buts)], 
      sprintf("(%d buts)\n", max(joueurs_data$buts)))
  cat("  • Meilleur passeur:", joueurs_data$nom[which.max(joueurs_data$passes_decisives)], 
      sprintf("(%d passes D.)\n", max(joueurs_data$passes_decisives)))
  cat("  • Joueur le mieux noté:", joueurs_data$nom[which.max(joueurs_data$note)], 
      sprintf("(%.1f)\n", max(joueurs_data$note)))
  
  if(!is.null(match_predictions)) {
    prochaine_victoire <- match_predictions$predictions[which.max(match_predictions$predictions$Prob_Victoire),]
    cat("  • Prochain match le plus favorable:", prochaine_victoire$Adversaire, 
        sprintf("(%.1f%% victoire)\n", prochaine_victoire$Prob_Victoire))
  }
  
  cat("\n🎯 RECOMMANDATIONS:\n")
  
  # Recommandations basées sur l'analyse
  jeunes_talents <- joueurs_data %>% filter(age <= 22 & note >= 7.0)
  if(nrow(jeunes_talents) > 0) {
    cat("  • Développer les jeunes talents:", paste(jeunes_talents$nom, collapse = ", "), "\n")
  }
  
  veterants <- joueurs_data %>% filter(age >= 30 & note < 7.0)
  if(nrow(veterants) > 0) {
    cat("  • Envisager rotation pour:", paste(veterants$nom, collapse = ", "), "\n")
  }
  
  efficaces <- joueurs_data %>% filter(efficacite >= quantile(joueurs_data$efficacite, 0.8, na.rm = TRUE))
  if(nrow(efficaces) > 0) {
    cat("  • Valoriser les joueurs efficaces:", paste(efficaces$nom, collapse = ", "), "\n")
  }
  
  cat("\n🔵⚪ ALLEZ RACING ! ⚪🔵\n")
  cat("=" %+% rep("=", 60) %+% "\n")
  
  # Retour des résultats
  return(list(
    joueurs = joueurs_data,
    matchs = matchs_data,
    analyses_desc = desc_joueurs,
    performances = perf_matchs,
    predictions = prediction_results,
    clustering = cluster_results,
    match_pred = match_predictions,
    timestamp = Sys.time()
  ))
}

# ================================================================================
# EXÉCUTION PRINCIPALE
# ================================================================================

# Exécution du script principal
if(interactive() || !exists("sourced")) {
  
  cat("🚀 Démarrage de l'analyse RCS...\n\n")
  
  # Génération du rapport complet
  rcs_analysis <- generate_rcs_report(save_plots = TRUE)
  
  cat("\n✅ Analyse terminée avec succès !\n")
  cat("📁 Fichiers générés dans le dossier 'rcs_analytics_output/'\n\n")
  
  # Affichage des objets créés
  cat("📊 Objets R disponibles:\n")
  cat("  • rcs_analysis$joueurs - Données joueurs\n")
  cat("  • rcs_analysis$matchs - Données matchs\n") 
  cat("  • rcs_analysis$predictions - Modèles prédictifs\n")
  cat("  • rcs_analysis$clustering - Résultats clustering\n")
  cat("  • rcs_analysis$match_pred - Prédictions matchs\n\n")
  
  cat("🔵⚪ Racing Club de Strasbourg - Analytics R terminé ! ⚪🔵\n")
}

# ================================================================================
# FIN DU SCRIPT
# ================================================================================
