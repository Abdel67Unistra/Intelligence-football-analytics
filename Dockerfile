FROM python:3.9-slim

WORKDIR /app

# Copier les fichiers de requirements
COPY requirements_streamlit.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements_streamlit.txt

# Copier le code source
COPY . .

# Exposer le port
EXPOSE 8501

# Variables d'environnement
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_ENABLE_CORS=false
ENV STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=false

# Commande de démarrage
CMD ["streamlit", "run", "python_analytics/dashboards/coach_interface.py", "--server.port=8501", "--server.address=0.0.0.0"]
