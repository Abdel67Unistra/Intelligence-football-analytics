"""
🔵⚪ Racing Club de Strasbourg - Assets Manager
Gestionnaire des assets visuels et logos RCS
"""

import base64
from pathlib import Path

class AssetsRCS:
    """Gestionnaire des assets visuels du Racing Club de Strasbourg"""
    
    # Logo SVG officiel du Racing Club de Strasbourg
    LOGO_SVG = """
    <svg width="120" height="120" viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg">
        <!-- Écusson principal -->
        <path d="M60 5 L105 30 L105 90 L60 115 L15 90 L15 30 Z" 
              fill="#0066CC" stroke="#FFFFFF" stroke-width="3"/>
        
        <!-- Bandes blanches -->
        <rect x="20" y="40" width="80" height="8" fill="#FFFFFF"/>
        <rect x="20" y="52" width="80" height="8" fill="#FFFFFF"/>
        <rect x="20" y="64" width="80" height="8" fill="#FFFFFF"/>
        
        <!-- RCS stylisé -->
        <text x="60" y="35" text-anchor="middle" fill="#FFFFFF" 
              font-family="Arial Black" font-size="14" font-weight="bold">RCS</text>
        <text x="60" y="85" text-anchor="middle" fill="#FFFFFF" 
              font-family="Arial" font-size="10">STRASBOURG</text>
        
        <!-- Étoile -->
        <polygon points="60,15 62,21 68,21 63,25 65,31 60,27 55,31 57,25 52,21 58,21" 
                 fill="#FFD700"/>
    </svg>
    """
    
    # Logo compact pour header
    LOGO_COMPACT_SVG = """
    <svg width="60" height="60" viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg">
        <path d="M60 5 L105 30 L105 90 L60 115 L15 90 L15 30 Z" 
              fill="#0066CC" stroke="#FFFFFF" stroke-width="2"/>
        <text x="60" y="45" text-anchor="middle" fill="#FFFFFF" 
              font-family="Arial Black" font-size="18" font-weight="bold">RCS</text>
        <polygon points="60,15 62,21 68,21 63,25 65,31 60,27 55,31 57,25 52,21 58,21" 
                 fill="#FFD700"/>
    </svg>
    """
    
    # Favicon
    FAVICON_SVG = """
    <svg width="32" height="32" viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg">
        <path d="M60 5 L105 30 L105 90 L60 115 L15 90 L15 30 Z" fill="#0066CC"/>
        <text x="60" y="70" text-anchor="middle" fill="#FFFFFF" 
              font-family="Arial Black" font-size="24" font-weight="bold">R</text>
    </svg>
    """
    
    # Couleurs officielles RCS
    COLORS = {
        'primary': '#0066CC',      # Bleu RCS
        'secondary': '#FFFFFF',    # Blanc
        'accent': '#FFD700',       # Or pour les étoiles
        'dark_blue': '#003366',    # Bleu foncé
        'light_blue': '#4A90E2',   # Bleu clair
        'success': '#28A745',      # Vert succès
        'warning': '#FFC107',      # Orange alerte
        'danger': '#DC3545',       # Rouge danger
        'background': '#F8F9FA',   # Fond clair
        'text': '#212529'          # Texte sombre
    }
    
    # CSS personnalisé pour Streamlit
    STREAMLIT_CSS = """
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    /* Variables CSS RCS */
    :root {
        --rcs-primary: #0066CC;
        --rcs-secondary: #FFFFFF;
        --rcs-accent: #FFD700;
        --rcs-dark: #003366;
        --rcs-light: #4A90E2;
    }
    
    /* Style global */
    .main {
        background: linear-gradient(135deg, var(--rcs-primary), var(--rcs-light));
        font-family: 'Inter', sans-serif;
    }
    
    /* Header principal */
    .rcs-header {
        background: linear-gradient(90deg, var(--rcs-primary), var(--rcs-dark));
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 4px 15px rgba(0,102,204,0.3);
    }
    
    /* Titre principal */
    .rcs-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: var(--rcs-secondary);
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        margin: 0;
    }
    
    /* Sous-titre */
    .rcs-subtitle {
        font-size: 1.2rem;
        color: var(--rcs-accent);
        margin: 0.5rem 0;
        font-weight: 400;
    }
    
    /* Cards de métriques */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border-left: 5px solid var(--rcs-primary);
        margin: 1rem 0;
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 20px rgba(0,102,204,0.2);
    }
    
    /* Boutons RCS */
    .stButton > button {
        background: linear-gradient(45deg, var(--rcs-primary), var(--rcs-light));
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
        transition: all 0.3s ease;
        box-shadow: 0 2px 10px rgba(0,102,204,0.2);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(0,102,204,0.4);
    }
    
    /* Sidebar */
    .css-1d391kg {
        background: linear-gradient(180deg, var(--rcs-primary), var(--rcs-dark));
    }
    
    /* Métriques Streamlit */
    [data-testid="metric-container"] {
        background: white;
        border: 1px solid #E0E0E0;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid var(--rcs-primary);
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    /* Tables */
    .stDataFrame {
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 2px 15px rgba(0,0,0,0.1);
    }
    
    /* Graphiques */
    .js-plotly-plot {
        border-radius: 8px;
        box-shadow: 0 2px 15px rgba(0,0,0,0.1);
    }
    
    /* Footer RCS */
    .rcs-footer {
        text-align: center;
        padding: 2rem 0;
        color: var(--rcs-primary);
        font-weight: 600;
        border-top: 2px solid var(--rcs-primary);
        margin-top: 3rem;
    }
    
    /* Animations */
    @keyframes pulse-rcs {
        0% { box-shadow: 0 0 0 0 rgba(0,102,204,0.4); }
        70% { box-shadow: 0 0 0 10px rgba(0,102,204,0); }
        100% { box-shadow: 0 0 0 0 rgba(0,102,204,0); }
    }
    
    .pulse-animation {
        animation: pulse-rcs 2s infinite;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .rcs-title { font-size: 2rem; }
        .rcs-subtitle { font-size: 1rem; }
        .metric-card { padding: 1rem; }
    }
    </style>
    """
    
    @classmethod
    def get_logo_html(cls, size="120") -> str:
        """Retourne le logo RCS en HTML avec taille personnalisée"""
        logo = cls.LOGO_SVG.replace('width="120"', f'width="{size}"')
        logo = logo.replace('height="120"', f'height="{size}"')
        return logo
    
    @classmethod
    def get_logo_compact_html(cls, size="60") -> str:
        """Retourne le logo compact RCS en HTML"""
        logo = cls.LOGO_COMPACT_SVG.replace('width="60"', f'width="{size}"')
        logo = logo.replace('height="60"', f'height="{size}"')
        return logo
    
    @classmethod
    def get_header_rcs(cls, title: str, subtitle: str = "") -> str:
        """Génère un header complet avec logo RCS"""
        subtitle_html = f'<div class="rcs-subtitle">{subtitle}</div>' if subtitle else ""
        
        return f"""
        <div class="rcs-header">
            <div style="display: flex; align-items: center; justify-content: center; gap: 20px;">
                {cls.get_logo_compact_html("80")}
                <div>
                    <h1 class="rcs-title">{title}</h1>
                    {subtitle_html}
                </div>
                {cls.get_logo_compact_html("80")}
            </div>
        </div>
        """
    
    @classmethod
    def get_metric_card(cls, title: str, value: str, icon: str = "⚽") -> str:
        """Génère une carte de métrique stylée RCS"""
        return f"""
        <div class="metric-card">
            <div style="display: flex; align-items: center; gap: 15px;">
                <div style="font-size: 2rem;">{icon}</div>
                <div>
                    <h3 style="margin: 0; color: var(--rcs-primary); font-weight: 600;">{title}</h3>
                    <p style="margin: 0; font-size: 1.5rem; font-weight: 700; color: var(--rcs-dark);">{value}</p>
                </div>
            </div>
        </div>
        """
    
    @classmethod
    def get_footer_rcs(cls) -> str:
        """Génère un footer RCS"""
        return f"""
        <div class="rcs-footer">
            <div style="display: flex; align-items: center; justify-content: center; gap: 15px;">
                {cls.get_logo_compact_html("40")}
                <div>
                    <strong>Racing Club de Strasbourg</strong><br>
                    <small>Analytics Platform - Saison 2024-2025</small>
                </div>
                {cls.get_logo_compact_html("40")}
            </div>
        </div>
        """
    
    @classmethod
    def save_favicon(cls, output_path: str = "favicon.ico"):
        """Sauvegarde le favicon RCS"""
        # Convertir SVG en base64 pour le favicon
        favicon_data = base64.b64encode(cls.FAVICON_SVG.encode()).decode()
        return f"data:image/svg+xml;base64,{favicon_data}"
    
    @classmethod
    def get_plotly_theme(cls) -> dict:
        """Retourne le thème Plotly aux couleurs RCS"""
        return {
            'layout': {
                'colorway': [cls.COLORS['primary'], cls.COLORS['accent'], 
                           cls.COLORS['light_blue'], cls.COLORS['success'],
                           cls.COLORS['warning'], cls.COLORS['danger']],
                'paper_bgcolor': cls.COLORS['background'],
                'plot_bgcolor': 'white',
                'font': {'family': 'Inter, Arial', 'color': cls.COLORS['text']},
                'title': {'font': {'size': 20, 'color': cls.COLORS['primary']}},
                'xaxis': {'gridcolor': '#E0E0E0'},
                'yaxis': {'gridcolor': '#E0E0E0'}
            }
        }

# Instance globale
assets_rcs = AssetsRCS()