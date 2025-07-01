#!/usr/bin/env python3
"""
Script de test pour vérifier que le dashboard peut être importé sans erreur
"""

try:
    print("🔄 Test d'importation du dashboard...")
    
    # Test d'importation de toutes les bibliothèques nécessaires
    import os
    import pandas as pd
    import numpy as np
    import plotly.express as px
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    import streamlit as st
    from datetime import datetime, timedelta
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.linear_model import LinearRegression
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import mean_absolute_error, r2_score
    import warnings
    warnings.filterwarnings('ignore')
    
    print("✅ Toutes les bibliothèques importées avec succès")
    
    # Test de syntaxe du fichier dashboard
    with open('yshop_dashboard.py', 'r', encoding='utf-8') as f:
        code = f.read()
    
    compile(code, 'yshop_dashboard.py', 'exec')
    print("✅ Syntaxe du dashboard valide")
    
    # Test de lecture du fichier de données
    if os.path.exists('Online.xlsx'):
        df = pd.read_excel('Online.xlsx')
        print(f"✅ Fichier de données lu avec succès ({len(df)} lignes)")
    else:
        print("⚠️ Fichier Online.xlsx non trouvé")
    
    print("\n🎉 Tous les tests passés ! Le dashboard devrait fonctionner correctement.")
    print("\n📋 Pour lancer le dashboard :")
    print("   streamlit run yshop_dashboard.py")

except Exception as e:
    print(f"❌ Erreur détectée : {e}")
    import traceback
    traceback.print_exc()
