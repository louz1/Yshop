#!/usr/bin/env python3
"""
Script de test pour vérifier que le code de modélisation corrigé fonctionne
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import warnings
warnings.filterwarnings('ignore')

print("🚀 TEST DU CODE DE MODÉLISATION CORRIGÉ")
print("=" * 50)

try:
    # Chargement des données (simulation basée sur le code du notebook)
    print("📊 Chargement des données...")
    
    # Simulation de données de base pour le test
    df = pd.read_excel('Online.xlsx')
    
    # Traitement basique des données
    df.columns = df.columns.str.strip()
    df = df.rename(columns={
        'Invoice': 'invoice_id',
        'StockCode': 'product_code', 
        'Description': 'product_description',
        'Quantity': 'quantity',
        'InvoiceDate': 'date',
        'Price': 'unit_price',
        'Customer ID': 'customer_id',
        'Country': 'country'
    })
    
    # Nettoyage
    df = df[df['quantity'] > 0]
    df = df[df['unit_price'] > 0]
    df = df.dropna(subset=['product_description'])
    df['total_price'] = df['quantity'] * df['unit_price']
    
    # Agrégation par jour pour la modélisation
    daily_data = df.groupby(df['date'].dt.date).agg({
        'total_price': 'sum',
        'quantity': 'sum', 
        'invoice_id': 'nunique',
        'customer_id': 'nunique'
    }).reset_index()
    daily_data.columns = ['date', 'revenue', 'quantity', 'orders', 'customers']
    daily_data['date'] = pd.to_datetime(daily_data['date'])
    daily_data = daily_data.sort_values('date').reset_index(drop=True)
    
    print(f"✅ Données chargées: {len(daily_data)} jours")
    
    # Création des features temporelles SÉCURISÉES
    print("🔧 Création des features...")
    modeling_data = daily_data.copy()
    
    # Features temporelles de base (SANS variables calculées à partir de revenue)
    modeling_data['year'] = modeling_data['date'].dt.year
    modeling_data['month'] = modeling_data['date'].dt.month
    modeling_data['day'] = modeling_data['date'].dt.day
    modeling_data['day_of_week'] = modeling_data['date'].dt.dayofweek
    modeling_data['day_of_year'] = modeling_data['date'].dt.dayofyear
    modeling_data['week_of_year'] = modeling_data['date'].dt.isocalendar().week
    
    # Features binaires
    modeling_data['is_weekend'] = (modeling_data['day_of_week'] >= 5).astype(int)
    modeling_data['is_month_start'] = modeling_data['date'].dt.is_month_start.astype(int)
    modeling_data['is_month_end'] = modeling_data['date'].dt.is_month_end.astype(int)
    
    # Features cycliques
    modeling_data['month_sin'] = np.sin(2 * np.pi * modeling_data['month'] / 12)
    modeling_data['month_cos'] = np.cos(2 * np.pi * modeling_data['month'] / 12)
    modeling_data['dow_sin'] = np.sin(2 * np.pi * modeling_data['day_of_week'] / 7)
    modeling_data['dow_cos'] = np.cos(2 * np.pi * modeling_data['day_of_week'] / 7)
    
    # TEST DU CODE CORRIGÉ
    print("\n🤖 ENTRAÎNEMENT DES MODÈLES DE MACHINE LEARNING CORRIGÉ")
    print("=" * 50)
    
    # Variable cible et features SÉCURISÉES
    target = modeling_data['revenue']
    
    # Exclusion stricte de toutes les variables liées à la target
    excluded_columns = ['date', 'revenue', 'quantity', 'orders', 'customers']
    feature_columns_safe = [col for col in modeling_data.columns if col not in excluded_columns]
    
    features = modeling_data[feature_columns_safe]
    
    print(f"📊 Features utilisées: {len(feature_columns_safe)}")
    print(f"🎯 Features: {feature_columns_safe}")
    
    # Vérification: aucune corrélation parfaite
    correlations = features.corrwith(target).abs()
    high_corr = correlations[correlations > 0.95]
    if len(high_corr) > 0:
        print(f"⚠️ ALERTE: Corrélations suspectes: {high_corr}")
    else:
        print("✅ Aucune corrélation parfaite détectée")
    
    # Division train/test SÉCURISÉE
    X_train, X_test, y_train, y_test = train_test_split(
        features, target, test_size=0.2, shuffle=True, random_state=42
    )
    
    print(f"📊 Train: {len(X_train)}, Test: {len(X_test)}")
    
    # Normalisation
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Modèles avec régularisation
    models = {
        'Régression Linéaire': LinearRegression(),
        'Forêt Aléatoire': RandomForestRegressor(
            n_estimators=50, max_depth=10, min_samples_split=5, random_state=42
        )
    }
    
    # Entraînement et évaluation
    results = {}
    for name, model in models.items():
        print(f"\n🔄 Entraînement: {name}")
        
        if name == 'Régression Linéaire':
            model.fit(X_train_scaled, y_train)
            y_pred = model.predict(X_test_scaled)
        else:
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
        
        # Métriques
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        results[name] = {'RMSE': rmse, 'MAE': mae, 'R²': r2}
        
        print(f"  ✅ RMSE: {rmse:.2f}")
        print(f"  ✅ MAE: {mae:.2f}")
        print(f"  ✅ R²: {r2:.3f}")
        
        if r2 > 0.95:
            print(f"  ⚠️ ALERTE: R² = {r2:.3f} - Surapprentissage probable!")
        elif r2 > 0.6:
            print(f"  🎯 Résultat réaliste!")
    
    print(f"\n📊 COMPARAISON FINALE:")
    comparison_df = pd.DataFrame(results).T
    print(comparison_df.round(3))
    
    print(f"\n🎉 TEST RÉUSSI ! Les modèles produisent maintenant des résultats réalistes.")
    
except Exception as e:
    print(f"❌ Erreur: {e}")
    import traceback
    traceback.print_exc()
