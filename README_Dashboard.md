
# 🚀 YSHOP DASHBOARD - GUIDE DE LANCEMENT

## 📋 Fichiers créés:
- **yshop_dashboard.py**: Application Streamlit complète
- **lancer_dashboard.bat**: Script de lancement automatique (Windows)

## 🎯 Option 1: Lancement Simple (Windows)
1. Double-cliquez sur le fichier `lancer_dashboard.bat`
2. Le dashboard s'ouvrira automatiquement dans votre navigateur
3. Adresse: http://localhost:8501

## 🔧 Option 2: Lancement Manuel
1. Ouvrez un terminal/invite de commande
2. Naviguez vers le dossier du projet:
   ```
   cd "C:\Users\kadem\PAV\Projet"
   ```
3. Installez les dépendances (si nécessaire):
   ```
   pip install streamlit plotly pandas openpyxl
   ```
4. Lancez l'application:
   ```
   streamlit run yshop_dashboard.py
   ```

## ✨ Fonctionnalités du Dashboard:
- 📊 **KPIs en temps réel** avec métriques interactives
- 🔍 **Filtres dynamiques** par date, pays, catégorie
- 📈 **Visualisations interactives** avec Plotly
- 🌍 **Analyse géographique** avec cartes choroplèthes
- 🏷️ **Analyse produits** détaillée par catégories
- 📊 **Patterns saisonniers** avec heatmaps
- 🔮 **Prédictions avancées** avec intervalles de confiance
- 📥 **Export des données** en CSV

## 🎨 Interface:
- Design moderne et responsive
- Navigation par onglets
- Graphiques interactifs
- Métriques colorées
- Filtres dans la barre latérale

## 📱 Utilisation:
1. **Ajustez les filtres** dans la barre latérale
2. **Explorez les onglets** pour différentes analyses
3. **Interagissez avec les graphiques** (zoom, survol, etc.)
4. **Générez des prédictions** dans l'onglet correspondant
5. **Téléchargez les résultats** si nécessaire

## 🔧 Dépannage:
- Vérifiez que le fichier `Online.xlsx` est présent
- Assurez-vous d'avoir Python installé
- Installez les packages requis si nécessaire
- Redémarrez l'application en cas de problème

Le dashboard est maintenant prêt à être utilisé ! 🎉
