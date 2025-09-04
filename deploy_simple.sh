#!/bin/bash

echo "🔵⚪ DÉPLOIEMENT RACING CLUB DE STRASBOURG"
echo "========================================="

cd /Users/cheriet/Documents/augment-projects/stat

echo "📁 Ajout des fichiers..."
git add .

echo "💾 Commit..."
git commit -m "RCS Final Deploy - Racing Club de Strasbourg Platform"

echo "🚀 Push vers GitHub..."
git push origin main

echo "✅ DÉPLOIEMENT TERMINÉ!"
echo "🌐 URL: https://football-analytics-platform-2025.streamlit.app/"
echo "🔵⚪ Racing Club de Strasbourg Analytics - LIVE!"
