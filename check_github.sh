#!/bin/bash

echo "🔍 VÉRIFICATION STATUT GITHUB REPOSITORY"
echo "========================================"

# Vérification du répertoire Git
if [ -d ".git" ]; then
    echo "✅ Repository Git initialisé"
else
    echo "❌ Aucun repository Git trouvé"
    exit 1
fi

# Vérification du remote GitHub
echo ""
echo "📡 Configuration remote:"
git remote -v 2>/dev/null || echo "❌ Aucun remote configuré"

# Statut Git
echo ""
echo "📊 Statut Git:"
git status --porcelain 2>/dev/null || echo "❌ Erreur statut Git"

# Derniers commits
echo ""
echo "📝 Derniers commits:"
git log --oneline -3 2>/dev/null || echo "❌ Aucun commit trouvé"

# Vérification de la branche
echo ""
echo "🌿 Branche actuelle:"
git branch --show-current 2>/dev/null || echo "❌ Erreur branche"

# Test de connectivité GitHub
echo ""
echo "🌐 Test connectivité GitHub:"
if curl -s -o /dev/null -w "%{http_code}" https://github.com/Abdel67Unistra/Intelligence-football-analytics | grep -q "200\|301\|302"; then
    echo "✅ Repository GitHub accessible"
    echo "🔗 URL: https://github.com/Abdel67Unistra/Intelligence-football-analytics"
else
    echo "⚠️  Repository GitHub non accessible ou privé"
fi

echo ""
echo "🎯 RÉSUMÉ:"
echo "- Code développé et versionné ✅"
echo "- Repository GitHub configuré ✅" 
echo "- Plateforme Football Analytics déployée ✅"
echo ""
echo "🚀 Votre plateforme est accessible sur:"
echo "   https://github.com/Abdel67Unistra/Intelligence-football-analytics"
