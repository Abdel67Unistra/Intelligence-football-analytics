# =====================================================
# FOOTBALL ANALYTICS - MODÈLES PRÉDICTIFS R
# =====================================================
# Analyse prédictive pour le football avec R
# Modèles de prédiction de résultats, blessures et valeurs marchandes
# 
# Author: Football Analytics Platform
# =====================================================

# === CHARGEMENT DES LIBRAIRIES ===
suppressMessages({
  library(tidyverse)      # Manipulation de données
  library(caret)          # Machine Learning
  library(randomForest)   # Random Forest
  library(xgboost)        # Gradient Boosting
  library(survival)       # Analyse de survie pour blessures
  library(survminer)      # Visualisation survival
  library(corrplot)       # Matrices de corrélation
  library(forecast)       # Séries temporelles
  library(plotly)         # Graphiques interactifs
  library(DBI)            # Connexion base de données
  library(RPostgreSQL)    # PostgreSQL
  library(lubridate)      # Dates
  library(scales)         # Formatage des graphiques
})

# === CONFIGURATION ===
set.seed(42)  # Reproductibilité
options(warn = -1)  # Supprimer les warnings

# === FONCTIONS UTILITAIRES ===

#' Connexion à la base de données PostgreSQL
#' @return Connexion à la DB football
connect_football_db <- function() {
  tryCatch({
    con <- dbConnect(
      PostgreSQL(),
      host = "localhost",
      dbname = "football_analytics", 
      user = "postgres",
      password = "password"
    )
    return(con)
  }, error = function(e) {
    message("Erreur de connexion DB - Utilisation de données simulées")
    return(NULL)
  })
}

#' Génère des données de matchs simulées
#' @param n_matches Nombre de matchs à générer
#' @return DataFrame avec données de matchs
generate_match_data <- function(n_matches = 1000) {
  
  teams <- c("PSG", "OM", "Lyon", "Monaco", "Lille", "Rennes", "Nice", "Strasbourg", 
             "Lens", "Montpellier", "Nantes", "Bordeaux", "Clermont", "Reims", 
             "Angers", "Brest", "Metz", "Troyes", "Ajaccio", "Auxerre")
  
  data.frame(
    match_id = 1:n_matches,
    home_team = sample(teams, n_matches, replace = TRUE),
    away_team = sample(teams, n_matches, replace = TRUE),
    match_date = seq.Date(as.Date("2022-08-01"), by = "day", length.out = n_matches),
    home_goals = rpois(n_matches, 1.4),
    away_goals = rpois(n_matches, 1.1),
    home_xg = rnorm(n_matches, 1.4, 0.5),
    away_xg = rnorm(n_matches, 1.1, 0.5),
    home_possession = rnorm(n_matches, 50, 10),
    home_shots = rpois(n_matches, 12),
    away_shots = rpois(n_matches, 10),
    attendance = round(rnorm(n_matches, 30000, 10000)),
    referee_strictness = runif(n_matches, 0, 1),
    weather_condition = sample(c("Ensoleillé", "Nuageux", "Pluvieux"), n_matches, 
                              replace = TRUE, prob = c(0.5, 0.3, 0.2))
  ) %>%
  filter(home_team != away_team) %>%  # Éviter qu'une équipe joue contre elle-même
  mutate(
    home_xg = pmax(0, home_xg),  # xG positif
    away_xg = pmax(0, away_xg),
    home_possession = pmax(30, pmin(70, home_possession)),  # Possession entre 30-70%
    result = case_when(
      home_goals > away_goals ~ "Home Win",
      home_goals < away_goals ~ "Away Win", 
      TRUE ~ "Draw"
    )
  )
}

#' Génère des données de joueurs simulées
#' @param n_players Nombre de joueurs
#' @return DataFrame avec données joueurs
generate_player_data <- function(n_players = 500) {
  
  positions <- c("GK", "CB", "LB", "RB", "DM", "CM", "AM", "LW", "RW", "ST")
  teams <- c("PSG", "OM", "Lyon", "Monaco", "Lille", "Rennes", "Nice", "Strasbourg")
  
  ages <- round(rnorm(n_players, 26, 4))
  ages <- pmax(18, pmin(40, ages))  # Âges entre 18 et 40
  
  # Générer des stats corrélées à l'âge (pic vers 26-28 ans)
  age_factor <- 1 - abs(ages - 27) * 0.02
  age_factor <- pmax(0.7, age_factor)
  
  data.frame(
    player_id = 1:n_players,
    name = paste("Joueur", 1:n_players),
    age = ages,
    position = sample(positions, n_players, replace = TRUE),
    team = sample(teams, n_players, replace = TRUE),
    market_value = round(rnorm(n_players, 20, 15) * age_factor),
    goals_season = rpois(n_players, 8 * age_factor),
    assists_season = rpois(n_players, 6 * age_factor),
    minutes_played = round(rnorm(n_players, 2000, 500) * age_factor),
    injury_history = rpois(n_players, 2),
    international_caps = rpois(n_players, 10),
    contract_ends = sample(2024:2028, n_players, replace = TRUE),
    height_cm = round(rnorm(n_players, 180, 8)),
    weight_kg = round(rnorm(n_players, 75, 8)),
    workload_score = rnorm(n_players, 75, 15)  # Score de charge de travail
  ) %>%
  mutate(
    market_value = pmax(0.5, market_value),  # Valeur minimale 0.5M€
    minutes_played = pmax(0, minutes_played),
    workload_score = pmax(50, pmin(100, workload_score)),
    goals_per_90 = (goals_season / minutes_played) * 90,
    assists_per_90 = (assists_season / minutes_played) * 90,
    bmi = weight_kg / (height_cm/100)^2
  )
}

# === MODÈLE DE PRÉDICTION DE RÉSULTATS ===

#' Entraîne un modèle de prédiction de résultats de match
#' @param match_data DataFrame avec données historiques
#' @return Liste avec modèle et métriques
train_match_prediction_model <- function(match_data = NULL) {
  
  cat("🏈 Entraînement du modèle de prédiction de résultats...\n")
  
  # Charger ou générer les données
  if (is.null(match_data)) {
    match_data <- generate_match_data(1500)
  }
  
  # Feature engineering
  match_features <- match_data %>%
    mutate(
      home_advantage = 1,  # Avantage domicile
      xg_difference = home_xg - away_xg,
      possession_difference = home_possession - 50,  # Écart par rapport à 50%
      total_shots = home_shots + away_shots,
      shots_ratio = home_shots / (home_shots + away_shots),
      is_weekend = weekdays(match_date) %in% c("Saturday", "Sunday"),
      month = month(match_date),
      is_rain = weather_condition == "Pluvieux"
    ) %>%
    select(result, home_advantage, xg_difference, possession_difference, 
           total_shots, shots_ratio, is_weekend, month, is_rain, referee_strictness)
  
  # Conversion des facteurs
  match_features$result <- as.factor(match_features$result)
  match_features$is_weekend <- as.numeric(match_features$is_weekend)
  match_features$is_rain <- as.numeric(match_features$is_rain)
  
  # Division train/test
  set.seed(42)
  train_index <- createDataPartition(match_features$result, p = 0.8, list = FALSE)
  train_data <- match_features[train_index, ]
  test_data <- match_features[-train_index, ]
  
  # Configuration du modèle
  train_control <- trainControl(
    method = "cv",
    number = 5,
    verboseIter = FALSE,
    classProbs = TRUE,
    summaryFunction = multiClassSummary
  )
  
  # Entraînement Random Forest
  rf_model <- train(
    result ~ .,
    data = train_data,
    method = "rf",
    trControl = train_control,
    metric = "Accuracy",
    ntree = 500,
    importance = TRUE
  )
  
  # Prédictions sur le test set
  predictions <- predict(rf_model, test_data)
  
  # Métriques de performance
  confusion_matrix <- confusionMatrix(predictions, test_data$result)
  
  # Importance des variables
  importance_df <- as.data.frame(varImp(rf_model)$importance) %>%
    rownames_to_column("variable") %>%
    arrange(desc(Overall))
  
  cat("✅ Modèle entraîné avec succès!\n")
  cat(sprintf("📊 Précision: %.2f%%\n", confusion_matrix$overall['Accuracy'] * 100))
  
  return(list(
    model = rf_model,
    confusion_matrix = confusion_matrix,
    importance = importance_df,
    test_accuracy = confusion_matrix$overall['Accuracy']
  ))
}

# === MODÈLE DE PRÉDICTION DE BLESSURES ===

#' Modèle de survie pour prédire les blessures
#' @param player_data DataFrame avec données joueurs
#' @return Modèle de survie Cox
train_injury_prediction_model <- function(player_data = NULL) {
  
  cat("🏥 Entraînement du modèle de prédiction de blessures...\n")
  
  # Charger ou générer les données
  if (is.null(player_data)) {
    player_data <- generate_player_data(800)
  }
  
  # Simulation de données de blessures
  injury_data <- player_data %>%
    mutate(
      # Temps jusqu'à blessure (jours)
      time_to_injury = rweibull(nrow(player_data), 
                               shape = 1.5, 
                               scale = 200 - workload_score * 2),
      
      # Événement observé (1 = blessure, 0 = censuré)
      injury_occurred = rbinom(nrow(player_data), 1, 
                              prob = pmin(0.8, 0.1 + workload_score/100 + 
                                         injury_history * 0.05 + 
                                         pmax(0, age - 30) * 0.02)),
      
      # Facteurs de risque
      high_workload = workload_score > 85,
      older_player = age > 30,
      injury_prone = injury_history > 3,
      overweight = bmi > 25,
      position_risk = case_when(
        position %in% c("ST", "LW", "RW") ~ "High",
        position %in% c("CM", "AM", "LB", "RB") ~ "Medium", 
        TRUE ~ "Low"
      )
    ) %>%
    select(player_id, name, age, position, workload_score, injury_history,
           bmi, time_to_injury, injury_occurred, high_workload, older_player,
           injury_prone, overweight, position_risk)
  
  # Création de l'objet Survival
  library(survival)
  surv_object <- Surv(time = injury_data$time_to_injury, 
                     event = injury_data$injury_occurred)
  
  # Modèle de Cox
  cox_model <- coxph(surv_object ~ age + workload_score + injury_history + 
                    bmi + high_workload + older_player + position_risk,
                    data = injury_data)
  
  # Résumé du modèle
  summary_cox <- summary(cox_model)
  
  cat("✅ Modèle de blessures entraîné!\n")
  cat(sprintf("📊 Concordance: %.3f\n", summary_cox$concordance['C']))
  
  return(list(
    model = cox_model,
    data = injury_data,
    summary = summary_cox
  ))
}

# === MODÈLE DE PRÉDICTION DE VALEUR MARCHANDE ===

#' Prédiction des valeurs marchandes avec XGBoost
#' @param player_data DataFrame avec données joueurs
#' @return Modèle XGBoost entraîné
train_market_value_model <- function(player_data = NULL) {
  
  cat("💰 Entraînement du modèle de valeur marchande...\n")
  
  # Charger ou générer les données
  if (is.null(player_data)) {
    player_data <- generate_player_data(1000)
  }
  
  # Préparation des features
  market_features <- player_data %>%
    mutate(
      age_squared = age^2,
      goals_per_minute = goals_season / pmax(1, minutes_played),
      assists_per_minute = assists_season / pmax(1, minutes_played),
      total_contributions = goals_season + assists_season,
      experience_score = international_caps + (age - 18) * 0.5,
      contract_remaining = contract_ends - 2024,
      is_striker = as.numeric(position %in% c("ST", "CF")),
      is_midfielder = as.numeric(position %in% c("CM", "AM", "DM")),
      is_defender = as.numeric(position %in% c("CB", "LB", "RB")),
      is_goalkeeper = as.numeric(position == "GK")
    ) %>%
    select(market_value, age, age_squared, goals_season, assists_season,
           minutes_played, injury_history, international_caps,
           goals_per_minute, assists_per_minute, total_contributions,
           experience_score, contract_remaining, height_cm, weight_kg,
           is_striker, is_midfielder, is_defender, is_goalkeeper) %>%
    filter(!is.na(market_value), market_value > 0)
  
  # Division train/test
  set.seed(42)
  train_index <- sample(nrow(market_features), 0.8 * nrow(market_features))
  train_data <- market_features[train_index, ]
  test_data <- market_features[-train_index, ]
  
  # Préparation pour XGBoost
  library(xgboost)
  
  train_x <- as.matrix(train_data[, -1])  # Exclure market_value
  train_y <- train_data$market_value
  test_x <- as.matrix(test_data[, -1])
  test_y <- test_data$market_value
  
  # Paramètres XGBoost
  params <- list(
    objective = "reg:squarederror",
    eval_metric = "rmse",
    max_depth = 6,
    eta = 0.1,
    subsample = 0.8,
    colsample_bytree = 0.8
  )
  
  # Entraînement avec validation croisée
  cv_result <- xgb.cv(
    params = params,
    data = train_x,
    label = train_y,
    nrounds = 1000,
    nfold = 5,
    early_stopping_rounds = 50,
    verbose = FALSE
  )
  
  # Modèle final
  xgb_model <- xgboost(
    params = params,
    data = train_x,
    label = train_y,
    nrounds = cv_result$best_iteration,
    verbose = FALSE
  )
  
  # Prédictions
  train_pred <- predict(xgb_model, train_x)
  test_pred <- predict(xgb_model, test_x)
  
  # Métriques
  train_rmse <- sqrt(mean((train_y - train_pred)^2))
  test_rmse <- sqrt(mean((test_y - test_pred)^2))
  test_r2 <- cor(test_y, test_pred)^2
  
  # Importance des features
  importance_matrix <- xgb.importance(colnames(train_x), model = xgb_model)
  
  cat("✅ Modèle de valeur marchande entraîné!\n")
  cat(sprintf("📊 RMSE Test: %.2f M€\n", test_rmse))
  cat(sprintf("📊 R² Test: %.3f\n", test_r2))
  
  return(list(
    model = xgb_model,
    train_rmse = train_rmse,
    test_rmse = test_rmse,
    test_r2 = test_r2,
    importance = importance_matrix,
    feature_names = colnames(train_x)
  ))
}

# === ANALYSE DE SÉRIES TEMPORELLES ===

#' Analyse de l'évolution des performances d'équipe
#' @param team_name Nom de l'équipe
#' @param match_data Données de matchs
#' @return Modèle de prédiction ARIMA
analyze_team_performance_trend <- function(team_name = "PSG", match_data = NULL) {
  
  cat(sprintf("📈 Analyse des tendances pour %s...\n", team_name))
  
  # Charger ou générer les données
  if (is.null(match_data)) {
    match_data <- generate_match_data(500)
  }
  
  # Filtrer les matchs de l'équipe
  team_matches <- match_data %>%
    filter(home_team == team_name | away_team == team_name) %>%
    arrange(match_date) %>%
    mutate(
      is_home = home_team == team_name,
      team_goals = ifelse(is_home, home_goals, away_goals),
      opponent_goals = ifelse(is_home, away_goals, home_goals),
      team_xg = ifelse(is_home, home_xg, away_xg),
      result_numeric = case_when(
        team_goals > opponent_goals ~ 3,  # Victoire
        team_goals == opponent_goals ~ 1, # Nul
        TRUE ~ 0  # Défaite
      ),
      points_cumsum = cumsum(result_numeric),
      goals_ma = zoo::rollmean(team_goals, k = 5, fill = NA, align = "right"),
      xg_ma = zoo::rollmean(team_xg, k = 5, fill = NA, align = "right")
    )
  
  # Série temporelle des points
  if (nrow(team_matches) >= 10) {
    
    # Modèle ARIMA pour prédire les points futurs
    points_ts <- ts(team_matches$result_numeric, frequency = 1)
    
    # Ajustement automatique ARIMA
    library(forecast)
    arima_model <- auto.arima(points_ts, seasonal = FALSE)
    
    # Prédictions futures (10 prochains matchs)
    future_pred <- forecast(arima_model, h = 10)
    
    cat("✅ Analyse de tendance terminée!\n")
    cat(sprintf("📊 Modèle: %s\n", arima_model$method))
    cat(sprintf("📊 AIC: %.2f\n", AIC(arima_model)))
    
    return(list(
      team_data = team_matches,
      model = arima_model,
      forecast = future_pred,
      recent_form = tail(team_matches$result_numeric, 5)
    ))
    
  } else {
    cat("⚠️ Pas assez de données pour l'analyse de tendance\n")
    return(NULL)
  }
}

# === FONCTION PRINCIPALE D'EXÉCUTION ===

#' Exécute tous les modèles prédictifs
run_all_predictive_models <- function() {
  
  cat("🚀 DÉMARRAGE DES MODÈLES PRÉDICTIFS FOOTBALL\n")
  cat("=" %R% 50, "\n")
  
  # 1. Modèle de prédiction de résultats
  cat("\n1️⃣ PRÉDICTION DE RÉSULTATS DE MATCHS\n")
  match_model <- train_match_prediction_model()
  
  # 2. Modèle de prédiction de blessures
  cat("\n2️⃣ PRÉDICTION DE BLESSURES\n")
  injury_model <- train_injury_prediction_model()
  
  # 3. Modèle de valeur marchande
  cat("\n3️⃣ PRÉDICTION DE VALEUR MARCHANDE\n")
  value_model <- train_market_value_model()
  
  # 4. Analyse de tendances
  cat("\n4️⃣ ANALYSE DE TENDANCES D'ÉQUIPE\n")
  trend_analysis <- analyze_team_performance_trend("PSG")
  
  cat("\n🎉 TOUS LES MODÈLES SONT OPÉRATIONNELS!\n")
  cat("=" %R% 50, "\n")
  
  # Retourner les résultats
  return(list(
    match_prediction = match_model,
    injury_prediction = injury_model,
    market_value = value_model,
    trend_analysis = trend_analysis
  ))
}

# === UTILITAIRES D'AFFICHAGE ===

# Opérateur de répétition pour l'affichage
`%R%` <- function(x, n) paste(rep(x, n), collapse = "")

# === EXÉCUTION SI SCRIPT LANCÉ DIRECTEMENT ===
if (!interactive()) {
  results <- run_all_predictive_models()
  cat("\n✅ Script terminé avec succès!\n")
}
