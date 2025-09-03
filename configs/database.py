"""
Configuration Database Football Analytics
========================================

Module de configuration et connexion à la base de données PostgreSQL.
Gestion des paramètres d'environnement et initialisation.

Author: Football Analytics Platform
"""

import os
import psycopg2
from psycopg2.extras import RealDictCursor
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
import logging
from typing import Optional, Dict, Any

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DatabaseConfig:
    """Configuration de la base de données"""
    
    def __init__(self):
        self.host = os.getenv('DB_HOST', 'localhost')
        self.port = os.getenv('DB_PORT', '5432')
        self.database = os.getenv('DB_NAME', 'football_analytics')
        self.user = os.getenv('DB_USER', 'postgres')
        self.password = os.getenv('DB_PASSWORD', 'password')
        
    def get_connection_string(self) -> str:
        """Retourne la chaîne de connexion PostgreSQL"""
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
    
    def get_connection_params(self) -> Dict[str, str]:
        """Retourne les paramètres de connexion"""
        return {
            'host': self.host,
            'port': self.port,
            'database': self.database,
            'user': self.user,
            'password': self.password
        }

class DatabaseManager:
    """Gestionnaire de base de données"""
    
    def __init__(self, config: Optional[DatabaseConfig] = None):
        self.config = config or DatabaseConfig()
        self.connection = None
        self.engine = None
        
    def connect(self) -> bool:
        """Établit la connexion à la base de données"""
        try:
            self.connection = psycopg2.connect(**self.config.get_connection_params())
            self.engine = create_engine(self.config.get_connection_string())
            logger.info("✅ Connexion à la base de données établie")
            return True
        except Exception as e:
            logger.error(f"❌ Erreur de connexion à la base de données: {e}")
            return False
    
    def disconnect(self):
        """Ferme la connexion à la base de données"""
        if self.connection:
            self.connection.close()
            logger.info("Connexion fermée")
    
    def execute_query(self, query: str, params: tuple = None) -> Optional[list]:
        """Exécute une requête SELECT"""
        try:
            with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, params)
                return cursor.fetchall()
        except Exception as e:
            logger.error(f"Erreur lors de l'exécution de la requête: {e}")
            return None
    
    def execute_command(self, command: str, params: tuple = None) -> bool:
        """Exécute une commande INSERT/UPDATE/DELETE"""
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(command, params)
                self.connection.commit()
                return True
        except Exception as e:
            logger.error(f"Erreur lors de l'exécution de la commande: {e}")
            self.connection.rollback()
            return False
    
    def read_sql(self, query: str, params: dict = None) -> pd.DataFrame:
        """Lit les données dans un DataFrame pandas"""
        try:
            return pd.read_sql(query, self.engine, params=params)
        except Exception as e:
            logger.error(f"Erreur lors de la lecture SQL: {e}")
            return pd.DataFrame()
    
    def to_sql(self, df: pd.DataFrame, table_name: str, if_exists: str = 'append') -> bool:
        """Écrit un DataFrame dans la base de données"""
        try:
            df.to_sql(table_name, self.engine, if_exists=if_exists, index=False)
            logger.info(f"✅ Données écrites dans la table {table_name}")
            return True
        except Exception as e:
            logger.error(f"❌ Erreur lors de l'écriture dans {table_name}: {e}")
            return False

# Instance globale du gestionnaire de base de données
db_manager = DatabaseManager()

def get_db_connection():
    """Fonction utilitaire pour obtenir une connexion DB"""
    if not db_manager.connection:
        db_manager.connect()
    return db_manager.connection

def get_db_engine():
    """Fonction utilitaire pour obtenir l'engine SQLAlchemy"""
    if not db_manager.engine:
        db_manager.connect()
    return db_manager.engine

if __name__ == "__main__":
    # Test de connexion
    print("🔗 Test de connexion à la base de données...")
    
    if db_manager.connect():
        print("✅ Connexion réussie!")
        
        # Test de requête simple
        result = db_manager.execute_query("SELECT version();")
        if result:
            print(f"📊 Version PostgreSQL: {result[0]['version']}")
        
        db_manager.disconnect()
    else:
        print("❌ Échec de la connexion")
