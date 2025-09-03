# =====================================================
# FOOTBALL ANALYTICS - VISUALISATIONS AVANCÉES R
# =====================================================
# Graphiques et visualisations spécialisées pour le football
# Heatmaps, pass networks, radar charts, animations
# 
# Author: Football Analytics Platform
# =====================================================

# === CHARGEMENT DES LIBRAIRIES ===
suppressMessages({
  library(tidyverse)      # Manipulation et graphiques
  library(ggplot2)        # Graphiques
  library(plotly)         # Graphiques interactifs
  library(gganimate)      # Animations
  library(ggrepel)        # Labels sans superposition
  library(viridis)        # Palettes de couleurs
  library(RColorBrewer)   # Couleurs
  library(patchwork)      # Assemblage de graphiques
  library(corrplot)       # Matrices de corrélation
  library(igraph)         # Graphiques de réseau
  library(networkD3)      # Réseaux interactifs
  library(leaflet)        # Cartes interactives
  library(DT)             # Tables interactives
  library(scales)         # Formatage des axes
  library(cowplot)        # Thèmes et assemblage
  library(ggtext)         # Formatage de texte avancé
})

# === CONFIGURATION GRAPHIQUE ===
# Thème personnalisé pour les graphiques football
theme_football <- function() {
  theme_minimal(base_size = 12) +
    theme(
      plot.title = element_text(size = 16, face = "bold", hjust = 0.5),
      plot.subtitle = element_text(size = 12, hjust = 0.5, color = "gray50"),
      legend.position = "bottom",
      panel.grid.minor = element_blank(),
      strip.text = element_text(face = "bold"),
      axis.title = element_text(face = "bold")
    )
}

# Palette de couleurs football
football_colors <- c(
  "PSG" = "#004B87",
  "OM" = "#00A2E8", 
  "Lyon" = "#FF0000",
  "Monaco" = "#DC143C",
  "Lille" = "#B22222",
  "Rennes" = "#8B0000",
  "Nice" = "#DC143C",
  "Nantes" = "#FFD700"
)

# === FONCTIONS DE DONNÉES ===

#' Génère des données de positions pour heatmap
#' @param player_name Nom du joueur
#' @param n_events Nombre d'événements
#' @return DataFrame avec positions x,y
generate_heatmap_data <- function(player_name = "Mbappé", n_events = 200) {
  set.seed(42)
  
  # Position selon le type de joueur (simulation)
  if (grepl("Mbappé|ST|CF", player_name)) {
    # Attaquant - zone offensive
    x_center <- 75
    y_center <- 50
    x_spread <- 15
    y_spread <- 20
  } else if (grepl("Verratti|CM|DM", player_name)) {
    # Milieu - zone centrale
    x_center <- 55
    y_center <- 50
    x_spread <- 20
    y_spread <- 25
  } else {
    # Défenseur - zone défensive
    x_center <- 25
    y_center <- 50
    x_spread <- 15
    y_spread <- 30
  }
  
  data.frame(
    x = pmax(0, pmin(100, rnorm(n_events, x_center, x_spread))),
    y = pmax(0, pmin(100, rnorm(n_events, y_center, y_spread))),
    event_type = sample(c("Pass", "Shot", "Tackle", "Dribble"), n_events, 
                       replace = TRUE, prob = c(0.6, 0.1, 0.2, 0.1)),
    minute = sample(1:90, n_events, replace = TRUE)
  )
}

#' Génère des données de passes entre joueurs
#' @param team_name Nom de l'équipe
#' @return DataFrame avec connexions de passes
generate_pass_network_data <- function(team_name = "PSG") {
  
  players <- c("Donnarumma", "Hakimi", "Marquinhos", "Ramos", "Mendes",
               "Verratti", "Vitinha", "Fabián", "Dembélé", "Mbappé", "Neymar")
  
  # Matrice de passes (simulation basée sur les positions)
  n_players <- length(players)
  pass_matrix <- matrix(0, n_players, n_players)
  
  set.seed(42)
  for (i in 1:n_players) {
    for (j in 1:n_players) {
      if (i != j) {
        # Plus de passes entre joueurs proches positionnellement
        distance_factor <- abs(i - j)
        pass_count <- rpois(1, max(1, 20 - distance_factor * 2))
        pass_matrix[i, j] <- pass_count
      }
    }
  }
  
  # Convertir en format long
  pass_data <- expand.grid(
    from = players,
    to = players,
    stringsAsFactors = FALSE
  ) %>%
    mutate(
      passes = as.vector(pass_matrix),
      from_id = rep(1:n_players, each = n_players),
      to_id = rep(1:n_players, times = n_players)
    ) %>%
    filter(from != to, passes > 0)
  
  return(pass_data)
}

#' Génère des données pour graphique radar
#' @param player_name Nom du joueur
#' @return DataFrame avec métriques normalisées
generate_radar_data <- function(player_name = "Mbappé") {
  
  set.seed(42)
  
  # Ajuster les stats selon le type de joueur
  if (grepl("Mbappé|ST|CF", player_name)) {
    # Stats d'attaquant
    stats <- c(
      "Finition" = runif(1, 80, 95),
      "Vitesse" = runif(1, 85, 98),
      "Dribble" = runif(1, 75, 90),
      "Passes" = runif(1, 70, 85),
      "Défense" = runif(1, 30, 50),
      "Physique" = runif(1, 75, 88),
      "Technique" = runif(1, 80, 92),
      "Mental" = runif(1, 85, 95)
    )
  } else if (grepl("Verratti|CM", player_name)) {
    # Stats de milieu
    stats <- c(
      "Finition" = runif(1, 60, 75),
      "Vitesse" = runif(1, 70, 80),
      "Dribble" = runif(1, 80, 92),
      "Passes" = runif(1, 88, 98),
      "Défense" = runif(1, 70, 85),
      "Physique" = runif(1, 65, 80),
      "Technique" = runif(1, 85, 95),
      "Mental" = runif(1, 80, 90)
    )
  } else {
    # Stats génériques
    stats <- runif(8, 60, 85)
    names(stats) <- c("Finition", "Vitesse", "Dribble", "Passes", 
                     "Défense", "Physique", "Technique", "Mental")
  }
  
  data.frame(
    attribute = names(stats),
    value = as.numeric(stats),
    player = player_name
  )
}

# === FONCTIONS DE VISUALISATION ===

#' Crée une heatmap des zones d'action d'un joueur
#' @param player_name Nom du joueur
#' @param match_title Titre du match (optionnel)
#' @return Graphique ggplot
create_player_heatmap <- function(player_name = "Kylian Mbappé", 
                                 match_title = "PSG vs OM") {
  
  # Générer les données
  heatmap_data <- generate_heatmap_data(player_name, 300)
  
  # Créer la heatmap
  p <- ggplot(heatmap_data, aes(x = x, y = y)) +
    # Heatmap avec densité
    stat_density_2d_filled(alpha = 0.7, contour = FALSE, bins = 15) +
    scale_fill_viridis_d(option = "plasma", name = "Densité\nd'actions") +
    
    # Lignes du terrain
    # Lignes de touche
    geom_hline(yintercept = c(0, 100), color = "white", size = 1) +
    geom_vline(xintercept = c(0, 100), color = "white", size = 1) +
    
    # Ligne médiane
    geom_vline(xintercept = 50, color = "white", size = 1) +
    
    # Cercle central
    annotate("path", 
             x = 50 + 9.15 * cos(seq(0, 2*pi, length.out = 100)),
             y = 50 + 9.15 * sin(seq(0, 2*pi, length.out = 100)),
             color = "white", size = 1) +
    
    # Surfaces de réparation
    geom_rect(aes(xmin = 0, xmax = 16.5, ymin = 21.1, ymax = 78.9), 
              fill = NA, color = "white", size = 1) +
    geom_rect(aes(xmin = 83.5, xmax = 100, ymin = 21.1, ymax = 78.9), 
              fill = NA, color = "white", size = 1) +
    
    # Buts
    geom_rect(aes(xmin = 0, xmax = 5.5, ymin = 43.2, ymax = 56.8), 
              fill = NA, color = "white", size = 1) +
    geom_rect(aes(xmin = 94.5, xmax = 100, ymin = 43.2, ymax = 56.8), 
              fill = NA, color = "white", size = 1) +
    
    # Personnalisation
    coord_fixed(ratio = 1) +
    scale_x_continuous(limits = c(0, 100), expand = c(0, 0),
                      breaks = c(0, 25, 50, 75, 100),
                      labels = c("But\nDéfensif", "25m", "Milieu", "75m", "But\nOffensif")) +
    scale_y_continuous(limits = c(0, 100), expand = c(0, 0)) +
    
    labs(
      title = sprintf("Heatmap d'activité - %s", player_name),
      subtitle = match_title,
      x = "Position sur le terrain",
      y = "Largeur du terrain",
      caption = "Source: Football Analytics Platform"
    ) +
    
    theme_football() +
    theme(
      panel.background = element_rect(fill = "#2d5a2d"),  # Vert terrain
      plot.background = element_rect(fill = "white"),
      axis.text.y = element_blank(),
      axis.ticks.y = element_blank(),
      legend.position = "right"
    )
  
  return(p)
}

#' Crée un réseau de passes interactif
#' @param team_name Nom de l'équipe
#' @return Graphique réseau
create_pass_network <- function(team_name = "PSG") {
  
  # Générer les données
  pass_data <- generate_pass_network_data(team_name)
  
  # Calculer les statistiques des joueurs
  player_stats <- pass_data %>%
    group_by(from) %>%
    summarise(
      total_passes = sum(passes),
      .groups = 'drop'
    ) %>%
    rename(player = from)
  
  # Créer le graphique réseau avec ggplot
  # Positions des joueurs (formation 4-3-3)
  player_positions <- data.frame(
    player = c("Donnarumma", "Hakimi", "Marquinhos", "Ramos", "Mendes",
               "Verratti", "Vitinha", "Fabián", "Dembélé", "Mbappé", "Neymar"),
    x = c(10, 25, 20, 20, 25, 40, 45, 40, 70, 75, 70),
    y = c(50, 75, 60, 40, 25, 70, 50, 30, 75, 50, 25)
  )
  
  # Joindre avec les stats
  player_positions <- player_positions %>%
    left_join(player_stats, by = "player") %>%
    mutate(total_passes = ifelse(is.na(total_passes), 50, total_passes))
  
  # Créer les connexions
  connections <- pass_data %>%
    filter(passes >= 10) %>%  # Seulement les connexions importantes
    left_join(player_positions %>% select(player, x, y), 
              by = c("from" = "player")) %>%
    left_join(player_positions %>% select(player, x, y), 
              by = c("to" = "player"), suffix = c("_from", "_to"))
  
  # Graphique
  p <- ggplot() +
    # Connexions (lignes)
    geom_segment(data = connections,
                aes(x = x_from, y = y_from, xend = x_to, yend = y_to,
                    alpha = passes, size = passes),
                color = "#3498db") +
    
    # Joueurs (points)
    geom_point(data = player_positions,
               aes(x = x, y = y, size = total_passes),
               color = "#e74c3c", alpha = 0.8) +
    
    # Noms des joueurs
    geom_text_repel(data = player_positions,
                   aes(x = x, y = y, label = player),
                   size = 3, fontface = "bold",
                   box.padding = 0.3, point.padding = 0.3) +
    
    # Échelles
    scale_size_continuous(name = "Passes", range = c(1, 8)) +
    scale_alpha_continuous(name = "Passes", range = c(0.3, 0.9)) +
    
    # Thème
    coord_fixed() +
    labs(
      title = sprintf("Réseau de Passes - %s", team_name),
      subtitle = "Connexions principales entre joueurs",
      caption = "Taille des points = Volume total de passes\nÉpaisseur des lignes = Passes entre joueurs"
    ) +
    
    theme_void() +
    theme(
      plot.title = element_text(size = 16, face = "bold", hjust = 0.5),
      plot.subtitle = element_text(size = 12, hjust = 0.5),
      legend.position = "bottom"
    )
  
  return(p)
}

#' Crée un graphique radar pour un joueur
#' @param player_name Nom du joueur
#' @param comparison_player Joueur de comparaison (optionnel)
#' @return Graphique radar
create_radar_chart <- function(player_name = "Kylian Mbappé", 
                              comparison_player = NULL) {
  
  # Générer les données
  player_data <- generate_radar_data(player_name)
  
  if (!is.null(comparison_player)) {
    comp_data <- generate_radar_data(comparison_player)
    radar_data <- bind_rows(player_data, comp_data)
  } else {
    radar_data <- player_data
  }
  
  # Préparer pour le graphique radar
  radar_data <- radar_data %>%
    mutate(
      angle = (seq_len(n()) - 1) * 2 * pi / 8,  # 8 attributs
      x = value * cos(angle),
      y = value * sin(angle)
    )
  
  # Créer le graphique
  p <- ggplot(radar_data, aes(x = x, y = y, color = player, fill = player)) +
    # Grille circulaire
    annotate("path", 
             x = 20 * cos(seq(0, 2*pi, length.out = 100)),
             y = 20 * sin(seq(0, 2*pi, length.out = 100)),
             color = "gray80", linetype = "dashed") +
    annotate("path", 
             x = 40 * cos(seq(0, 2*pi, length.out = 100)),
             y = 40 * sin(seq(0, 2*pi, length.out = 100)),
             color = "gray80", linetype = "dashed") +
    annotate("path", 
             x = 60 * cos(seq(0, 2*pi, length.out = 100)),
             y = 60 * sin(seq(0, 2*pi, length.out = 100)),
             color = "gray80", linetype = "dashed") +
    annotate("path", 
             x = 80 * cos(seq(0, 2*pi, length.out = 100)),
             y = 80 * sin(seq(0, 2*pi, length.out = 100)),
             color = "gray80", linetype = "dashed") +
    
    # Axes radiaux
    geom_segment(data = radar_data[1:8,],  # Premier joueur pour les axes
                aes(x = 0, y = 0, xend = 100 * cos(angle), yend = 100 * sin(angle)),
                color = "gray70", inherit.aes = FALSE) +
    
    # Polygone du joueur
    geom_polygon(alpha = 0.3, size = 1.5) +
    geom_point(size = 3) +
    
    # Labels des attributs
    geom_text(data = radar_data %>% filter(player == player_name),
             aes(x = 110 * cos(angle), y = 110 * sin(angle), label = attribute),
             color = "black", fontface = "bold", size = 3.5,
             inherit.aes = FALSE) +
    
    # Valeurs
    geom_text(data = radar_data,
             aes(x = (value + 8) * cos(angle), y = (value + 8) * sin(angle), 
                 label = round(value, 1)),
             color = "black", size = 2.5, fontface = "bold") +
    
    # Échelles et thème
    scale_color_manual(values = c("#e74c3c", "#3498db"), name = "Joueur") +
    scale_fill_manual(values = c("#e74c3c", "#3498db"), name = "Joueur") +
    
    coord_fixed() +
    scale_x_continuous(limits = c(-120, 120)) +
    scale_y_continuous(limits = c(-120, 120)) +
    
    labs(
      title = ifelse(is.null(comparison_player),
                    sprintf("Profil de %s", player_name),
                    sprintf("Comparaison: %s vs %s", player_name, comparison_player)),
      subtitle = "Attributs techniques et physiques (sur 100)",
      caption = "Source: Football Analytics Platform"
    ) +
    
    theme_void() +
    theme(
      plot.title = element_text(size = 16, face = "bold", hjust = 0.5),
      plot.subtitle = element_text(size = 12, hjust = 0.5),
      legend.position = "bottom"
    )
  
  return(p)
}

#' Crée un graphique d'évolution de performance
#' @param player_name Nom du joueur
#' @param season Saison
#' @return Graphique temporel
create_performance_timeline <- function(player_name = "Kylian Mbappé", 
                                       season = "2024-25") {
  
  # Générer des données temporelles
  set.seed(42)
  n_matches <- 20
  
  performance_data <- data.frame(
    match_date = seq.Date(as.Date("2024-08-01"), by = "weeks", length.out = n_matches),
    match_number = 1:n_matches,
    rating = pmax(5, pmin(10, rnorm(n_matches, 7.5, 1.2))),
    goals = rpois(n_matches, 0.6),
    assists = rpois(n_matches, 0.4),
    minutes = sample(c(90, 78, 85, 45, 90), n_matches, replace = TRUE),
    opponent = sample(c("OM", "Lyon", "Monaco", "Lille", "Rennes", "Nice"), 
                     n_matches, replace = TRUE)
  ) %>%
    mutate(
      goals_per_90 = (goals / minutes) * 90,
      performance_index = (rating - 5) * 20 + goals * 10 + assists * 8,
      trend = zoo::rollmean(performance_index, k = 3, fill = NA, align = "right")
    )
  
  # Graphique principal
  p1 <- ggplot(performance_data, aes(x = match_date)) +
    # Note de performance
    geom_line(aes(y = rating, color = "Note"), size = 1.2) +
    geom_point(aes(y = rating, color = "Note"), size = 2.5) +
    
    # Tendance
    geom_line(aes(y = trend/10, color = "Tendance"), size = 1, linetype = "dashed") +
    
    # Événements spéciaux (goals)
    geom_point(data = performance_data %>% filter(goals > 0),
              aes(y = rating, size = goals), color = "#e74c3c", alpha = 0.7) +
    
    scale_color_manual(values = c("Note" = "#3498db", "Tendance" = "#e67e22"),
                      name = "Métrique") +
    scale_size_continuous(name = "Goals", range = c(3, 8)) +
    
    scale_y_continuous(
      name = "Note (sur 10)",
      sec.axis = sec_axis(~.*10, name = "Indice de Performance")
    ) +
    
    labs(
      title = sprintf("Évolution des Performances - %s", player_name),
      subtitle = sprintf("Saison %s", season),
      x = "Date du Match",
      caption = "Taille des points = Nombre de buts marqués"
    ) +
    
    theme_football()
  
  # Graphique secondaire - Stats par match
  p2 <- ggplot(performance_data, aes(x = match_date)) +
    geom_col(aes(y = goals, fill = "Goals"), alpha = 0.7, width = 5) +
    geom_col(aes(y = assists, fill = "Assists"), alpha = 0.7, width = 5, 
             position = position_nudge(x = 3)) +
    
    scale_fill_manual(values = c("Goals" = "#e74c3c", "Assists" = "#f39c12"),
                     name = "Contributions") +
    
    labs(
      y = "Nombre",
      x = "Date du Match"
    ) +
    
    theme_football() +
    theme(axis.title.x = element_blank())
  
  # Combiner les graphiques
  combined_plot <- p1 / p2 + plot_layout(heights = c(2, 1))
  
  return(combined_plot)
}

#' Crée une analyse comparative d'équipes
#' @param teams Vecteur des noms d'équipes
#' @return Graphique comparatif
create_team_comparison <- function(teams = c("PSG", "OM", "Lyon", "Monaco")) {
  
  # Générer des données d'équipes
  set.seed(42)
  team_data <- data.frame(
    team = rep(teams, each = 8),
    metric = rep(c("Goals/Match", "xG/Match", "Possession %", "Passes/Match",
                  "Shots/Match", "Tackles/Match", "Saves/Match", "Clean Sheets %"), 
                length(teams)),
    value = c(
      # PSG
      2.3, 2.1, 62, 587, 15.2, 12.8, 3.2, 45,
      # OM  
      1.8, 1.6, 48, 421, 12.1, 18.3, 4.8, 35,
      # Lyon
      2.0, 1.9, 53, 456, 13.8, 15.2, 4.1, 40,
      # Monaco
      2.1, 2.0, 55, 478, 14.3, 14.6, 3.7, 38
    )
  ) %>%
    # Normaliser les valeurs pour la comparaison
    group_by(metric) %>%
    mutate(
      value_norm = (value - min(value)) / (max(value) - min(value)) * 100
    ) %>%
    ungroup()
  
  # Graphique radar comparatif
  p <- ggplot(team_data, aes(x = metric, y = value_norm, color = team, group = team)) +
    geom_line(size = 1.5, alpha = 0.8) +
    geom_point(size = 3, alpha = 0.9) +
    
    # Valeurs brutes en annotations
    geom_text(aes(label = round(value, 1)), 
             position = position_dodge(width = 0.3), 
             size = 2.5, vjust = -1) +
    
    scale_color_manual(values = football_colors[teams], name = "Équipe") +
    
    # Coordonnées polaires pour effet radar
    coord_polar() +
    
    scale_y_continuous(limits = c(0, 100), breaks = c(0, 25, 50, 75, 100)) +
    
    labs(
      title = "Comparaison Multi-Critères des Équipes",
      subtitle = "Valeurs normalisées sur 100 (performances relatives)",
      y = "Performance Relative",
      x = "Métriques",
      caption = "Valeurs indiquées = statistiques brutes"
    ) +
    
    theme_football() +
    theme(
      axis.text.x = element_text(face = "bold"),
      legend.position = "bottom"
    )
  
  return(p)
}

#' Crée un dashboard de visualisations
#' @param player_name Nom du joueur principal
#' @param team_name Nom de l'équipe
#' @return Liste de graphiques
create_football_dashboard <- function(player_name = "Kylian Mbappé", 
                                     team_name = "PSG") {
  
  cat("📊 Création du dashboard football...\n")
  
  # 1. Heatmap du joueur
  heatmap_plot <- create_player_heatmap(player_name)
  
  # 2. Réseau de passes de l'équipe
  network_plot <- create_pass_network(team_name)
  
  # 3. Graphique radar du joueur
  radar_plot <- create_radar_chart(player_name, "Marco Verratti")
  
  # 4. Évolution de performance
  timeline_plot <- create_performance_timeline(player_name)
  
  # 5. Comparaison d'équipes
  comparison_plot <- create_team_comparison()
  
  cat("✅ Dashboard créé avec succès!\n")
  
  return(list(
    heatmap = heatmap_plot,
    pass_network = network_plot,
    radar_chart = radar_plot,
    performance_timeline = timeline_plot,
    team_comparison = comparison_plot
  ))
}

# === FONCTION D'EXPORT ===

#' Sauvegarde tous les graphiques
#' @param dashboard Liste des graphiques
#' @param output_dir Dossier de sortie
save_dashboard_plots <- function(dashboard, output_dir = "plots") {
  
  # Créer le dossier s'il n'existe pas
  if (!dir.exists(output_dir)) {
    dir.create(output_dir, recursive = TRUE)
  }
  
  # Sauvegarder chaque graphique
  for (plot_name in names(dashboard)) {
    filename <- file.path(output_dir, paste0(plot_name, ".png"))
    ggsave(filename, dashboard[[plot_name]], 
           width = 12, height = 8, dpi = 300, bg = "white")
    cat(sprintf("💾 Sauvegardé: %s\n", filename))
  }
}

# === EXÉCUTION PRINCIPALE ===

#' Fonction principale pour générer toutes les visualisations
main_visualizations <- function() {
  
  cat("🎨 DÉMARRAGE DES VISUALISATIONS FOOTBALL\n")
  cat(strrep("=", 50), "\n")
  
  # Créer le dashboard complet
  dashboard <- create_football_dashboard("Kylian Mbappé", "PSG")
  
  # Afficher les graphiques (si en mode interactif)
  if (interactive()) {
    print(dashboard$heatmap)
    print(dashboard$pass_network)
    print(dashboard$radar_chart)
    print(dashboard$performance_timeline)
    print(dashboard$team_comparison)
  }
  
  # Sauvegarder les graphiques
  save_dashboard_plots(dashboard)
  
  cat("\n🎉 TOUTES LES VISUALISATIONS SONT CRÉÉES!\n")
  cat(strrep("=", 50), "\n")
  
  return(dashboard)
}

# === EXÉCUTION SI SCRIPT LANCÉ DIRECTEMENT ===
if (!interactive()) {
  dashboard_results <- main_visualizations()
  cat("\n✅ Script de visualisation terminé avec succès!\n")
}
