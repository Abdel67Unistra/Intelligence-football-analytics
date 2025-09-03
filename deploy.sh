#!/bin/bash

echo "🚀 Football Analytics Platform - Git Deploy Script"
echo "================================================="

# Vérifier si nous sommes dans un repo git
if [ ! -d ".git" ]; then
    echo "❌ Erreur: Pas un repository Git"
    exit 1
fi

# Afficher le statut
echo "📊 Statut Git actuel:"
git status --porcelain

# Nettoyer les fichiers temporaires
echo "🧹 Nettoyage des fichiers temporaires..."
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
find . -name "*.pyc" -delete 2>/dev/null || true
find . -name ".DS_Store" -delete 2>/dev/null || true

# Ajouter les changements
echo "➕ Ajout des changements..."
git add .

# Exclure les fichiers sensibles
git reset HEAD .env 2>/dev/null || true
git reset HEAD *.log 2>/dev/null || true

# Demander le message de commit
echo ""
read -p "💬 Message de commit (optionnel): " commit_message

if [ -z "$commit_message" ]; then
    commit_message="📝 Update: $(date '+%Y-%m-%d %H:%M')"
fi

# Committer
echo "✅ Création du commit..."
git commit -m "$commit_message"

# Pousser vers GitHub
echo "🌐 Push vers GitHub..."
git push origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 Déploiement réussi!"
    echo "🔗 Repository: https://github.com/Abdel67Unistra/Intelligence-football-analytics"
else
    echo ""
    echo "❌ Erreur lors du push. Vérifiez votre authentification GitHub."
    echo "💡 Astuce: Configurez un token d'accès personnel si nécessaire."
fi
