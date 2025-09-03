-- ===== FOOTBALL ANALYTICS DATABASE SCHEMA =====
-- Système d'analyse de performance et aide à la décision pour clubs de football
-- Optimisé pour requêtes d'agrégation et analyses temporelles

-- Extension pour types géographiques et fonctions avancées
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "postgis";

-- ===== TABLES PRINCIPALES =====

-- Table des Championnats/Ligues
CREATE TABLE leagues (
    league_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    country VARCHAR(50) NOT NULL,
    level INTEGER NOT NULL, -- 1=première division, 2=deuxième...
    season VARCHAR(9) NOT NULL, -- "2024-2025"
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(name, country, season)
);

-- Table des Équipes
CREATE TABLE teams (
    team_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    short_name VARCHAR(10),
    league_id UUID REFERENCES leagues(league_id),
    city VARCHAR(50),
    stadium_name VARCHAR(100),
    stadium_capacity INTEGER,
    founded_year INTEGER,
    budget_millions DECIMAL(10,2),
    color_home VARCHAR(7), -- Code couleur hex
    color_away VARCHAR(7),
    website VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table des Joueurs avec données complètes
CREATE TABLE players (
    player_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    birth_date DATE NOT NULL,
    nationality VARCHAR(50),
    second_nationality VARCHAR(50), -- Double nationalité
    height_cm INTEGER,
    weight_kg INTEGER,
    foot VARCHAR(5) CHECK (foot IN ('Left', 'Right', 'Both')),
    market_value_millions DECIMAL(10,2),
    salary_annual_millions DECIMAL(10,2),
    contract_end_date DATE,
    jersey_number INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table des Positions (système moderne)
CREATE TABLE positions (
    position_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    code VARCHAR(5) NOT NULL UNIQUE, -- GK, CB, LB, RB, DM, CM, AM, LW, RW, ST
    name VARCHAR(30) NOT NULL,
    line VARCHAR(10) NOT NULL CHECK (line IN ('Goalkeeper', 'Defence', 'Midfield', 'Attack')),
    zone VARCHAR(10) CHECK (zone IN ('Left', 'Center', 'Right'))
);

-- Table de liaison Joueur-Équipe-Position (historique)
CREATE TABLE player_team_contracts (
    contract_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    player_id UUID REFERENCES players(player_id),
    team_id UUID REFERENCES teams(team_id),
    primary_position_id UUID REFERENCES positions(position_id),
    secondary_position_id UUID REFERENCES positions(position_id),
    start_date DATE NOT NULL,
    end_date DATE,
    transfer_fee_millions DECIMAL(10,2),
    salary_millions DECIMAL(8,2),
    is_loan BOOLEAN DEFAULT FALSE,
    loan_parent_team_id UUID REFERENCES teams(team_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table des Matchs (partitionnée par saison)
CREATE TABLE matches (
    match_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    league_id UUID REFERENCES leagues(league_id),
    home_team_id UUID REFERENCES teams(team_id),
    away_team_id UUID REFERENCES teams(team_id),
    match_date TIMESTAMP NOT NULL,
    matchday INTEGER, -- Journée de championnat
    venue VARCHAR(100),
    referee VARCHAR(100),
    attendance INTEGER,
    
    -- Scores
    home_score INTEGER,
    away_score INTEGER,
    home_score_halftime INTEGER,
    away_score_halftime INTEGER,
    
    -- Conditions
    weather VARCHAR(50),
    temperature INTEGER,
    humidity INTEGER,
    
    -- Status
    status VARCHAR(20) DEFAULT 'Scheduled' CHECK (status IN ('Scheduled', 'Live', 'Finished', 'Postponed', 'Cancelled')),
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) PARTITION BY RANGE (match_date);

-- Partitions par saison pour optimiser les performances
CREATE TABLE matches_2024_2025 PARTITION OF matches
    FOR VALUES FROM ('2024-07-01') TO ('2025-06-30');
CREATE TABLE matches_2025_2026 PARTITION OF matches
    FOR VALUES FROM ('2025-07-01') TO ('2026-06-30');

-- Table des Performances Joueurs par Match (métriques détaillées)
CREATE TABLE player_match_stats (
    stat_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    match_id UUID REFERENCES matches(match_id),
    player_id UUID REFERENCES players(player_id),
    team_id UUID REFERENCES teams(team_id),
    position_played_id UUID REFERENCES positions(position_id),
    
    -- Temps de jeu
    minutes_played INTEGER NOT NULL DEFAULT 0,
    is_starter BOOLEAN DEFAULT FALSE,
    substitution_minute_in INTEGER,
    substitution_minute_out INTEGER,
    
    -- Statistiques offensives
    goals INTEGER DEFAULT 0,
    assists INTEGER DEFAULT 0,
    shots_total INTEGER DEFAULT 0,
    shots_on_target INTEGER DEFAULT 0,
    shots_off_target INTEGER DEFAULT 0,
    shots_blocked INTEGER DEFAULT 0,
    xg DECIMAL(5,3) DEFAULT 0.000, -- Expected Goals
    xa DECIMAL(5,3) DEFAULT 0.000, -- Expected Assists
    
    -- Statistiques de passes
    passes_total INTEGER DEFAULT 0,
    passes_completed INTEGER DEFAULT 0,
    passes_accuracy DECIMAL(5,2) DEFAULT 0.00,
    passes_key INTEGER DEFAULT 0, -- Passes clés
    passes_forward INTEGER DEFAULT 0,
    passes_backward INTEGER DEFAULT 0,
    passes_left INTEGER DEFAULT 0,
    passes_right INTEGER DEFAULT 0,
    crosses_total INTEGER DEFAULT 0,
    crosses_completed INTEGER DEFAULT 0,
    
    -- Statistiques défensives
    tackles_total INTEGER DEFAULT 0,
    tackles_won INTEGER DEFAULT 0,
    interceptions INTEGER DEFAULT 0,
    clearances INTEGER DEFAULT 0,
    blocks INTEGER DEFAULT 0,
    duels_total INTEGER DEFAULT 0,
    duels_won INTEGER DEFAULT 0,
    aerial_duels_total INTEGER DEFAULT 0,
    aerial_duels_won INTEGER DEFAULT 0,
    
    -- Fautes et cartons
    fouls_committed INTEGER DEFAULT 0,
    fouls_suffered INTEGER DEFAULT 0,
    yellow_cards INTEGER DEFAULT 0,
    red_cards INTEGER DEFAULT 0,
    
    -- Données physiques
    distance_km DECIMAL(4,2) DEFAULT 0.00,
    sprints INTEGER DEFAULT 0,
    top_speed_kmh DECIMAL(4,1) DEFAULT 0.0,
    
    -- Touches de balle et zones
    touches INTEGER DEFAULT 0,
    touches_penalty_area INTEGER DEFAULT 0,
    touches_defensive_third INTEGER DEFAULT 0,
    touches_middle_third INTEGER DEFAULT 0,
    touches_attacking_third INTEGER DEFAULT 0,
    
    -- Note de performance (1-10)
    rating DECIMAL(3,1),
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) PARTITION BY RANGE (created_at);

-- Partitions pour player_match_stats
CREATE TABLE player_match_stats_2024_2025 PARTITION OF player_match_stats
    FOR VALUES FROM ('2024-07-01') TO ('2025-06-30');
CREATE TABLE player_match_stats_2025_2026 PARTITION OF player_match_stats
    FOR VALUES FROM ('2025-07-01') TO ('2026-06-30');

-- Table des Événements de Match (timeline détaillée)
CREATE TABLE match_events (
    event_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    match_id UUID REFERENCES matches(match_id),
    minute INTEGER NOT NULL,
    second_in_minute INTEGER DEFAULT 0,
    event_type VARCHAR(20) NOT NULL CHECK (event_type IN (
        'Goal', 'Assist', 'Yellow Card', 'Red Card', 'Substitution',
        'Shot', 'Pass', 'Tackle', 'Foul', 'Offside', 'Corner', 'Throw-in'
    )),
    player_id UUID REFERENCES players(player_id),
    team_id UUID REFERENCES teams(team_id),
    
    -- Position sur le terrain (coordonnées normalisées 0-100)
    x_coordinate DECIMAL(5,2), -- 0=ligne de but défensive, 100=ligne de but offensive
    y_coordinate DECIMAL(5,2), -- 0=touche gauche, 100=touche droite
    
    -- Détails spécifiques
    event_details JSONB, -- Stockage flexible pour détails spécifiques
    
    -- Résultat de l'action
    success BOOLEAN,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table des Données Physiques et GPS (simulation capteurs)
CREATE TABLE physical_data (
    data_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    player_id UUID REFERENCES players(player_id),
    date DATE NOT NULL,
    session_type VARCHAR(20) CHECK (session_type IN ('Training', 'Match', 'Recovery')),
    
    -- Métriques d'intensité
    total_distance_m INTEGER,
    high_intensity_distance_m INTEGER, -- >19.8 km/h
    sprint_distance_m INTEGER, -- >25.2 km/h
    accelerations INTEGER,
    decelerations INTEGER,
    max_speed_kmh DECIMAL(4,1),
    avg_speed_kmh DECIMAL(4,1),
    
    -- Charge physique
    training_load INTEGER, -- RPE * durée
    heart_rate_avg INTEGER,
    heart_rate_max INTEGER,
    calories_burned INTEGER,
    
    -- Fatigue et récupération
    fatigue_score INTEGER CHECK (fatigue_score BETWEEN 1 AND 10),
    sleep_hours DECIMAL(3,1),
    sleep_quality INTEGER CHECK (sleep_quality BETWEEN 1 AND 5),
    muscle_soreness INTEGER CHECK (muscle_soreness BETWEEN 1 AND 5),
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table des Transferts et Valeurs Marchandes
CREATE TABLE transfers (
    transfer_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    player_id UUID REFERENCES players(player_id),
    from_team_id UUID REFERENCES teams(team_id),
    to_team_id UUID REFERENCES teams(team_id),
    transfer_date DATE NOT NULL,
    transfer_type VARCHAR(20) CHECK (transfer_type IN ('Transfer', 'Loan', 'Free', 'End of Loan')),
    transfer_fee_millions DECIMAL(10,2),
    market_value_at_transfer DECIMAL(10,2),
    contract_length_years INTEGER,
    agent_fee_millions DECIMAL(8,2),
    performance_bonuses JSONB, -- Bonus conditionnels en JSON
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ===== INDEX OPTIMISÉS POUR ANALYTICS =====

-- Index sur les matchs pour requêtes fréquentes
CREATE INDEX idx_matches_date ON matches (match_date);
CREATE INDEX idx_matches_teams ON matches (home_team_id, away_team_id);
CREATE INDEX idx_matches_league_date ON matches (league_id, match_date);

-- Index sur les statistiques joueurs
CREATE INDEX idx_player_stats_match ON player_match_stats (match_id);
CREATE INDEX idx_player_stats_player ON player_match_stats (player_id);
CREATE INDEX idx_player_stats_player_date ON player_match_stats (player_id, created_at);
CREATE INDEX idx_player_stats_team_date ON player_match_stats (team_id, created_at);

-- Index composites pour analyses de performance
CREATE INDEX idx_player_stats_goals_assists ON player_match_stats (goals, assists) WHERE minutes_played > 0;
CREATE INDEX idx_player_stats_xg_xa ON player_match_stats (xg, xa) WHERE minutes_played > 0;

-- Index sur les événements
CREATE INDEX idx_events_match_minute ON match_events (match_id, minute);
CREATE INDEX idx_events_player ON match_events (player_id, event_type);
CREATE INDEX idx_events_position ON match_events (x_coordinate, y_coordinate) WHERE x_coordinate IS NOT NULL;

-- Index sur les données physiques
CREATE INDEX idx_physical_player_date ON physical_data (player_id, date);
CREATE INDEX idx_physical_load ON physical_data (training_load) WHERE session_type = 'Training';

-- ===== VUES MATÉRIALISÉES POUR KPI TEMPS RÉEL =====

-- Vue des statistiques saisonnières par joueur
CREATE MATERIALIZED VIEW player_season_stats AS
SELECT 
    p.player_id,
    p.first_name,
    p.last_name,
    t.name as team_name,
    l.season,
    COUNT(pms.stat_id) as matches_played,
    SUM(pms.minutes_played) as total_minutes,
    SUM(pms.goals) as total_goals,
    SUM(pms.assists) as total_assists,
    SUM(pms.xg) as total_xg,
    SUM(pms.xa) as total_xa,
    ROUND(AVG(pms.rating), 2) as avg_rating,
    SUM(pms.passes_completed)::FLOAT / NULLIF(SUM(pms.passes_total), 0) * 100 as pass_accuracy_pct,
    SUM(pms.tackles_won)::FLOAT / NULLIF(SUM(pms.tackles_total), 0) * 100 as tackle_success_pct
FROM players p
JOIN player_match_stats pms ON p.player_id = pms.player_id
JOIN matches m ON pms.match_id = m.match_id
JOIN teams t ON pms.team_id = t.team_id
JOIN leagues l ON m.league_id = l.league_id
WHERE pms.minutes_played > 0
GROUP BY p.player_id, p.first_name, p.last_name, t.name, l.season;

-- Index sur la vue matérialisée
CREATE INDEX idx_player_season_stats_player ON player_season_stats (player_id);
CREATE INDEX idx_player_season_stats_season ON player_season_stats (season);

-- Vue des performances par équipe
CREATE MATERIALIZED VIEW team_performance_stats AS
SELECT 
    t.team_id,
    t.name as team_name,
    l.season,
    COUNT(DISTINCT m.match_id) as matches_played,
    SUM(CASE WHEN m.home_team_id = t.team_id THEN m.home_score ELSE m.away_score END) as goals_for,
    SUM(CASE WHEN m.home_team_id = t.team_id THEN m.away_score ELSE m.home_score END) as goals_against,
    SUM(CASE 
        WHEN (m.home_team_id = t.team_id AND m.home_score > m.away_score) OR 
             (m.away_team_id = t.team_id AND m.away_score > m.home_score) THEN 3
        WHEN m.home_score = m.away_score THEN 1
        ELSE 0 
    END) as points,
    COUNT(CASE 
        WHEN (m.home_team_id = t.team_id AND m.home_score > m.away_score) OR 
             (m.away_team_id = t.team_id AND m.away_score > m.home_score) THEN 1 
    END) as wins,
    COUNT(CASE WHEN m.home_score = m.away_score THEN 1 END) as draws,
    COUNT(CASE 
        WHEN (m.home_team_id = t.team_id AND m.home_score < m.away_score) OR 
             (m.away_team_id = t.team_id AND m.away_score < m.home_score) THEN 1 
    END) as losses
FROM teams t
JOIN matches m ON t.team_id = m.home_team_id OR t.team_id = m.away_team_id
JOIN leagues l ON m.league_id = l.league_id
WHERE m.status = 'Finished'
GROUP BY t.team_id, t.name, l.season;

-- ===== TRIGGERS POUR MISE À JOUR AUTOMATIQUE =====

-- Fonction de mise à jour timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger sur la table players
CREATE TRIGGER update_players_updated_at 
    BEFORE UPDATE ON players 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- Trigger sur la table matches
CREATE TRIGGER update_matches_updated_at 
    BEFORE UPDATE ON matches 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- Fonction de rafraîchissement des vues matérialisées
CREATE OR REPLACE FUNCTION refresh_materialized_views()
RETURNS void AS $$
BEGIN
    REFRESH MATERIALIZED VIEW CONCURRENTLY player_season_stats;
    REFRESH MATERIALIZED VIEW CONCURRENTLY team_performance_stats;
END;
$$ LANGUAGE plpgsql;

-- ===== DONNÉES D'EXEMPLE POUR LES POSITIONS =====
INSERT INTO positions (code, name, line, zone) VALUES
('GK', 'Goalkeeper', 'Goalkeeper', 'Center'),
('CB', 'Centre-back', 'Defence', 'Center'),
('LB', 'Left-back', 'Defence', 'Left'),
('RB', 'Right-back', 'Defence', 'Right'),
('LWB', 'Left Wing-back', 'Defence', 'Left'),
('RWB', 'Right Wing-back', 'Defence', 'Right'),
('DM', 'Defensive Midfielder', 'Midfield', 'Center'),
('CM', 'Central Midfielder', 'Midfield', 'Center'),
('LM', 'Left Midfielder', 'Midfield', 'Left'),
('RM', 'Right Midfielder', 'Midfield', 'Right'),
('AM', 'Attacking Midfielder', 'Midfield', 'Center'),
('LW', 'Left Winger', 'Attack', 'Left'),
('RW', 'Right Winger', 'Attack', 'Right'),
('ST', 'Striker', 'Attack', 'Center'),
('CF', 'Centre Forward', 'Attack', 'Center');

-- ===== COMMENTAIRES POUR DOCUMENTATION =====
COMMENT ON TABLE leagues IS 'Championnats et ligues de football avec saisons';
COMMENT ON TABLE teams IS 'Équipes de football avec informations complètes';
COMMENT ON TABLE players IS 'Joueurs avec données personnelles et contractuelles';
COMMENT ON TABLE matches IS 'Matchs avec scores et conditions (partitionnée par date)';
COMMENT ON TABLE player_match_stats IS 'Statistiques détaillées par joueur et match';
COMMENT ON TABLE match_events IS 'Événements chronologiques des matchs';
COMMENT ON TABLE physical_data IS 'Données physiques et GPS des joueurs';
COMMENT ON TABLE transfers IS 'Historique des transferts et valeurs marchandes';

-- Schéma créé avec succès !
-- Pour utiliser : psql -U username -d football_analytics -f create_schema.sql
