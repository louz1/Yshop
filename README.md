# 🛍️ Yshop - Prédiction des Ventes

## 📋 Description du Projet

**Yshop** est un projet d'analyse prédictive des ventes pour une boutique en ligne spécialisée dans les produits artisanaux. Ce projet utilise des techniques de machine learning pour prédire les ventes futures et optimiser la gestion des stocks.

## 🎯 Objectifs

- Analyser les données de ventes historiques
- Développer un modèle de prédiction des ventes robuste
- Créer des visualisations interactives des tendances
- Fournir un dashboard de pilotage business
- Générer des recommandations stratégiques

## 📊 Données

- **Source** : Dataset de transactions e-commerce (Online.xlsx)
- **Période** : 13 mois de données historiques
- **Volume** : 397,884 transactions nettoyées
- **Chiffre d'affaires** : 8,5M€
- **Géographie** : 38 pays
- **Produits** : 3,665 références uniques

## 🧠 Modélisation

### Approche Méthodologique
- **Préparation** : Nettoyage, enrichissement temporel, catégorisation
- **Features** : Variables temporelles pures (sans fuite de données)
- **Modèles** : Ridge, Lasso, Random Forest avec régularisation
- **Validation** : Division temporelle 80/20

### Résultats
- **Modèle retenu** : Random Forest (50 arbres, max_depth=5)
- **Performance** : R² = 0.0013 (réaliste, sans surapprentissage)
- **Prédictions** : 30 jours futurs cohérents

## 📁 Structure du Projet

```
📦 Yshop-Prediction
├── 📊 Yshop.ipynb                    # Notebook principal d'analyse
├── 📈 yshop_dashboard.py             # Dashboard Streamlit interactif
├── 🔧 lancer_dashboard.ps1           # Script de lancement PowerShell
├── 🔧 lancer_dashboard.bat           # Script de lancement Batch
├── 📄 Online.xlsx                    # Données sources
├── 📄 yshop_daily_data.csv           # Données quotidiennes préparées
├── 📄 yshop_predictions_coherent.csv # Prédictions futures
├── 📖 README_Dashboard.md            # Documentation dashboard
└── 📋 README.md                      # Ce fichier
```

## 🚀 Installation et Utilisation

### Prérequis
```bash
Python 3.8+
```

### Installation des dépendances
```bash
pip install pandas numpy scikit-learn plotly streamlit openpyxl seaborn matplotlib
```

### Lancement du Dashboard
```bash
# Méthode 1 : Streamlit direct
streamlit run yshop_dashboard.py

# Méthode 2 : Script PowerShell
.\lancer_dashboard.ps1

# Méthode 3 : Double-clic sur lancer_dashboard.bat
```

Le dashboard sera accessible à l'adresse : `http://localhost:8501`

## 📈 Fonctionnalités du Dashboard

- 📊 **KPIs en temps réel** (CA, commandes, clients)
- 📈 **Visualisations interactives** (tendances, géographie, catégories)
- 🔮 **Prédictions futures** basées sur le modèle ML
- 🎯 **Analyses détaillées** par pays, produits, saisonnalité
- 📋 **Recommandations business** automatisées

## 🔍 Analyses Principales

### Insights Business
- **Saisonnalité** : Pics de vente en novembre-décembre
- **Géographie** : UK représente 90% du CA
- **Catégories** : Éclairage & Bougies = segment le plus rentable
- **Comportement** : Panier moyen de 349€, 1,7 commandes/client

### Recommandations
1. **Stocks** : Renforcer l'approvisionnement en fin d'année
2. **Marketing** : Cibler les marchés européens émergents
3. **Produits** : Développer la gamme éclairage/décoration
4. **Fidélisation** : Programmes de rétention client

## 🛠️ Technologies Utilisées

- **Python** : Langage principal
- **Pandas/NumPy** : Manipulation de données
- **Scikit-learn** : Machine Learning
- **Plotly** : Visualisations interactives
- **Streamlit** : Interface web
- **Jupyter** : Développement et analyse

## 📊 Métriques de Performance

| Métrique | Valeur |
|----------|--------|
| **Chiffre d'affaires** | 8,5M€ |
| **Transactions** | 397,884 |
| **Clients uniques** | 4,361 |
| **Panier moyen** | 349€ |
| **Taux de prédiction** | R² = 0.0013 |
| **Erreur moyenne** | 42.5% |

## 🤝 Contribution

Ce projet a été développé dans le cadre d'un projet académique d'analyse prédictive.

## 📄 Licence

Projet académique - Usage éducatif uniquement

## 👨‍💻 Auteur

**Kadem** - Projet PAV - Prédiction des Ventes Yshop

---

*Dernière mise à jour : Juillet 2025*
