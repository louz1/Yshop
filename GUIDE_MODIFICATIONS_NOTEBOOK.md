# 🔧 GUIDE : APPLICATION DES MODIFICATIONS AU NOTEBOOK

## 📋 **ÉTAPES À SUIVRE**

### **1. Ouvrir le Notebook**
```bash
jupyter notebook Yshop.ipynb
```
ou depuis VS Code : ouvrir directement `Yshop.ipynb`

### **2. Modifications à Appliquer**

#### **A. Localiser la cellule de modélisation (section 4.2)**
Cherchez la cellule qui commence par :
```python
# 4.2 Entraînement des modèles de Machine Learning
```

#### **B. Remplacer ENTIÈREMENT cette cellule par le code corrigé :**

```python
# 4.2 Entraînement des modèles de Machine Learning CORRIGÉ
print("🤖 ENTRAÎNEMENT DES MODÈLES DE MACHINE LEARNING")
print("=" * 50)

# 🔍 DIAGNOSTIC ET CORRECTION DU SURAPPRENTISSAGE
print("🔍 DIAGNOSTIC: Vérification des features...")

# Préparation SÉCURISÉE des données pour l'entraînement
target = modeling_data['revenue']

# ⚠️ CORRECTION: Exclusion stricte de toutes les variables liées à la target
excluded_columns = ['date', 'revenue', 'quantity', 'orders', 'customers', 
                   'revenue_ma_7', 'revenue_ma_30', 'revenue_trend', 'revenue_std_7']
feature_columns_safe = [col for col in modeling_data.columns if col not in excluded_columns]

print(f"📊 Features ORIGINALES: {len(feature_columns) if 'feature_columns' in locals() else 'N/A'}")
print(f"📊 Features SÉCURISÉES: {len(feature_columns_safe)}")
print(f"🚫 Variables EXCLUES: {excluded_columns}")

features = modeling_data[feature_columns_safe]

print(f"\n🎯 Features utilisées pour l'entraînement:")
for i, feature in enumerate(feature_columns_safe, 1):
    print(f"  {i:2d}. {feature}")

# Vérification: aucune corrélation parfaite avec la target
correlations = features.corrwith(target).abs()
high_corr = correlations[correlations > 0.95]
if len(high_corr) > 0:
    print(f"\n⚠️ ALERTE: Corrélations suspectes détectées!")
    print(high_corr)
else:
    print(f"\n✅ Aucune corrélation parfaite détectée")

# Division train/test (80/20) avec mélange pour éviter le biais temporel
X_train, X_test, y_train, y_test = train_test_split(
    features, target, test_size=0.2, shuffle=True, random_state=42
)

print(f"\n📊 Taille de l'ensemble d'entraînement: {len(X_train)} jours")
print(f"📊 Taille de l'ensemble de test: {len(X_test)} jours")

# Vérification: pas de doublons entre train et test
overlap = set(X_train.index).intersection(set(X_test.index))
print(f"📊 Overlap train/test: {len(overlap)} (doit être 0)")

# Normalisation des features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Définition des modèles avec régularisation
models = {
    'Régression Linéaire': LinearRegression(),
    'Forêt Aléatoire': RandomForestRegressor(
        n_estimators=50,      # Réduit pour éviter surapprentissage
        max_depth=10,         # Limitation de profondeur
        min_samples_split=5,  # Minimum d'échantillons
        random_state=42, 
        n_jobs=-1
    )
}

# Entraînement et évaluation des modèles
results = {}
predictions = {}

for name, model in models.items():
    print(f"\n🔄 Entraînement du modèle: {name}")
    
    # Entraînement
    if name == 'Régression Linéaire':
        model.fit(X_train_scaled, y_train)
        y_pred = model.predict(X_test_scaled)
    else:
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
    
    # Métriques de performance
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    # Vérification de la sanité des résultats
    if r2 > 0.95:
        print(f"  ⚠️ ALERTE: R² = {r2:.3f} - Surapprentissage probable!")
    
    # Sauvegarde des résultats
    results[name] = {
        'MSE': mse,
        'RMSE': rmse,
        'MAE': mae,
        'R²': r2
    }
    
    predictions[name] = y_pred
    
    print(f"  ✅ RMSE: {rmse:.2f}")
    print(f"  ✅ MAE: {mae:.2f}")
    print(f"  ✅ R²: {r2:.3f}")

# Comparaison des modèles
print(f"\n📊 COMPARAISON DES MODÈLES")
print("=" * 50)

comparison_df = pd.DataFrame(results).T
display(comparison_df.round(3))

# Analyse de la qualité des prédictions
print(f"\n🎯 ANALYSE DE LA QUALITÉ:")
for name, r2_score_val in comparison_df['R²'].items():
    if r2_score_val > 0.95:
        print(f"  ⚠️ {name}: R² = {r2_score_val:.3f} - SURAPPRENTISSAGE!")
    elif r2_score_val > 0.8:
        print(f"  ✅ {name}: R² = {r2_score_val:.3f} - Très bon")
    elif r2_score_val > 0.6:
        print(f"  ✅ {name}: R² = {r2_score_val:.3f} - Bon")
    else:
        print(f"  ⚠️ {name}: R² = {r2_score_val:.3f} - À améliorer")

# Visualisation des prédictions
fig = go.Figure()

# Création d'un index temporel pour les dates de test
test_indices = X_test.index
test_dates = modeling_data.loc[test_indices, 'date']

# Valeurs réelles
fig.add_trace(go.Scatter(
    x=test_dates,
    y=y_test.values,
    mode='lines+markers',
    name='Valeurs Réelles',
    line=dict(color='blue', width=2),
    marker=dict(size=6)
))

# Prédictions de chaque modèle
colors = ['red', 'green']
for idx, (name, pred) in enumerate(predictions.items()):
    fig.add_trace(go.Scatter(
        x=test_dates,
        y=pred,
        mode='lines+markers',
        name=f'Prédictions {name}',
        line=dict(color=colors[idx], width=2, dash='dash'),
        marker=dict(size=4)
    ))

fig.update_layout(
    title='Comparaison des Prédictions vs Valeurs Réelles (CORRIGÉ)',
    xaxis_title='Date',
    yaxis_title='Chiffre d\'Affaires (€)',
    height=500,
    hovermode='x unified'
)
fig.show()

# Graphique des résidus pour le meilleur modèle
best_model_name = comparison_df['R²'].idxmax()
best_predictions = predictions[best_model_name]
residuals = y_test.values - best_predictions

fig_residuals = make_subplots(
    rows=1, cols=2,
    subplot_titles=('Résidus vs Prédictions', 'Distribution des Résidus')
)

# Résidus vs Prédictions
fig_residuals.add_trace(
    go.Scatter(x=best_predictions, y=residuals,
               mode='markers', name='Résidus',
               marker=dict(color='red', opacity=0.6)),
    row=1, col=1
)

# Ligne de référence à y=0
fig_residuals.add_hline(y=0, line_dash="dash", line_color="black", row=1, col=1)

# Distribution des résidus
fig_residuals.add_trace(
    go.Histogram(x=residuals, name='Distribution', nbinsx=20,
                marker=dict(color='lightblue', opacity=0.7)),
    row=1, col=2
)

fig_residuals.update_layout(height=400, showlegend=False, 
                          title_text=f"Analyse des Résidus - {best_model_name} (CORRIGÉ)")
fig_residuals.show()

print(f"\n🏆 Meilleur modèle: {best_model_name} (R² = {comparison_df.loc[best_model_name, 'R²']:.3f})")

# Statistiques des résidus
print(f"\n📊 STATISTIQUES DES RÉSIDUS:")
print(f"   Moyenne: {residuals.mean():.2f} (proche de 0 = bon)")
print(f"   Écart-type: {residuals.std():.2f}")
print(f"   Min: {residuals.min():.2f}")
print(f"   Max: {residuals.max():.2f}")
```

### **3. Exécuter Toutes les Cellules**

#### **Option A - Jupyter Notebook :**
- Menu : `Kernel` → `Restart & Run All`

#### **Option B - VS Code :**
- Commande : `Ctrl+Shift+P` → "Notebook: Run All"

#### **Option C - Exécution manuelle :**
- Exécutez chaque cellule une par une avec `Shift+Enter`

### **4. Résultats Attendus**

Après la correction, vous devriez voir :
```
✅ RMSE: 1000-5000    (au lieu de 0.00)
✅ MAE: 800-3000      (au lieu de 0.00)  
✅ R²: 0.60-0.85      (au lieu de 1.000)
```

### **5. En Cas de Problème**

Si vous rencontrez des erreurs :
1. Vérifiez que toutes les bibliothèques sont installées
2. Assurez-vous que le fichier `Online.xlsx` est présent
3. Redémarrez le kernel et réexécutez depuis le début

---

## 🎯 **OBJECTIF DE LA CORRECTION**

Cette modification élimine le surapprentissage et produit des prédictions **réalistes** et **généralisables** pour votre projet Yshop.
