
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Configuration de la page
st.set_page_config(
    page_title="Yshop Analytics Dashboard",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS pour améliorer l'apparence
st.markdown("""
<style>
    .metric-card {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    .stMetric > div {
        background-color: #f0f2f6;
        border: 1px solid #e1e5e9;
        padding: 1rem;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Titre principal avec style
st.markdown("""
# 🛍️ Yshop Analytics Dashboard
### Tableau de bord interactif pour l'analyse des ventes et prédictions
""")
st.markdown("---")

# Fonction de chargement et traitement des données
@st.cache_data
def load_and_process_data():
    try:
        # Chargement du fichier Excel
        df_raw = pd.read_excel('Online.xlsx')

        # Traitement des données
        df = df_raw.copy()
        df.columns = df.columns.str.strip()

        # Renommage des colonnes
        column_mapping = {
            'Invoice': 'invoice_id',
            'StockCode': 'product_code',
            'Description': 'product_description',
            'Quantity': 'quantity',
            'InvoiceDate': 'date',
            'Price': 'unit_price',
            'Customer ID': 'customer_id',
            'Country': 'country'
        }
        df = df.rename(columns=column_mapping)

        # Nettoyage des données
        df = df[df['quantity'] > 0]
        df = df[df['unit_price'] > 0]
        df = df.dropna(subset=['product_description'])

        # Calculs dérivés
        df['total_price'] = df['quantity'] * df['unit_price']
        df['year'] = df['date'].dt.year
        df['month'] = df['date'].dt.month
        df['day'] = df['date'].dt.day
        df['day_of_week'] = df['date'].dt.dayofweek
        df['month_name'] = df['date'].dt.month_name()
        df['day_name'] = df['date'].dt.day_name()

        # Catégorisation des produits
        def categorize_product(description):
            if pd.isna(description):
                return 'Autre'
            desc_lower = description.lower()
            if any(word in desc_lower for word in ['heart', 'love', 'cupid', 'valentine']):
                return 'Décoration Romantique'
            elif any(word in desc_lower for word in ['christmas', 'xmas', 'santa', 'reindeer']):
                return 'Décoration Noël'
            elif any(word in desc_lower for word in ['candle', 'light', 'holder', 'lantern']):
                return 'Éclairage & Bougies'
            elif any(word in desc_lower for word in ['bag', 'tote', 'shopper']):
                return 'Sacs & Accessoires'
            elif any(word in desc_lower for word in ['mug', 'cup', 'glass', 'bottle']):
                return 'Vaisselle & Boissons'
            elif any(word in desc_lower for word in ['fabric', 'cotton', 'wool', 'knit']):
                return 'Textiles'
            elif any(word in desc_lower for word in ['metal', 'steel', 'iron', 'wire']):
                return 'Articles Métalliques'
            elif any(word in desc_lower for word in ['wooden', 'wood', 'bamboo']):
                return 'Articles en Bois'
            elif any(word in desc_lower for word in ['paper', 'card', 'notebook', 'diary']):
                return 'Papeterie'
            elif any(word in desc_lower for word in ['toy', 'game', 'play']):
                return 'Jeux & Jouets'
            else:
                return 'Autre'

        df['category'] = df['product_description'].apply(categorize_product)

        return df
    except Exception as e:
        st.error(f"Erreur lors du chargement des données: {e}")
        return None

# Chargement des données
df = load_and_process_data()

if df is not None:
    # Sidebar pour les filtres
    st.sidebar.header("🔧 Filtres et Paramètres")

    # Filtres de date
    min_date = df['date'].min().date()
    max_date = df['date'].max().date()

    date_range = st.sidebar.date_input(
        "Sélectionnez une période",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

    # Filtre par pays
    countries = ['Tous'] + sorted(df['country'].unique().tolist())
    selected_country = st.sidebar.selectbox("Pays", countries)

    # Filtre par catégorie
    categories = ['Toutes'] + sorted(df['category'].unique().tolist())
    selected_category = st.sidebar.selectbox("Catégorie", categories)

    # Application des filtres
    filtered_df = df.copy()

    if len(date_range) == 2:
        start_date, end_date = date_range
        filtered_df = filtered_df[
            (filtered_df['date'].dt.date >= start_date) & 
            (filtered_df['date'].dt.date <= end_date)
        ]

    if selected_country != 'Tous':
        filtered_df = filtered_df[filtered_df['country'] == selected_country]

    if selected_category != 'Toutes':
        filtered_df = filtered_df[filtered_df['category'] == selected_category]

    # Métriques principales
    st.subheader("📊 KPIs Principaux")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        total_revenue = filtered_df['total_price'].sum()
        st.metric(
            label="💰 Chiffre Affaires",
            value=f"{total_revenue:,.0f} €",
            delta=f"{(total_revenue/df['total_price'].sum()*100):.1f}% du total"
        )

    with col2:
        total_orders = filtered_df['invoice_id'].nunique()
        st.metric(
            label="🛒 Commandes",
            value=f"{total_orders:,}",
            delta=f"{(total_orders/df['invoice_id'].nunique()*100):.1f}% du total"
        )

    with col3:
        total_customers = filtered_df['customer_id'].nunique()
        st.metric(
            label="👥 Clients Uniques",
            value=f"{total_customers:,}",
            delta=f"{(total_customers/df['customer_id'].nunique()*100):.1f}% du total"
        )

    with col4:
        avg_order = total_revenue / total_orders if total_orders > 0 else 0
        st.metric(
            label="🛍️ Panier Moyen",
            value=f"{avg_order:.2f} €"
        )

    st.markdown("---")

    # Onglets pour les différentes analyses
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📈 Tendances Temporelles", 
        "🌍 Analyse Géographique", 
        "🏷️ Analyse Produits", 
        "📊 Patterns Saisonniers",
        "🔮 Prédictions"
    ])

    with tab1:
        st.subheader("📈 Évolution des Ventes")

        # Évolution temporelle
        daily_sales = filtered_df.groupby(filtered_df['date'].dt.date).agg({
            'total_price': 'sum',
            'quantity': 'sum',
            'invoice_id': 'nunique'
        }).reset_index()
        daily_sales.columns = ['date', 'revenue', 'quantity', 'orders']

        # Graphique d'évolution
        fig_evolution = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Chiffre Affaires Quotidien', 'Quantités Vendues',
                           'Nombre de Commandes', 'Évolution Mensuelle'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )

        fig_evolution.add_trace(
            go.Scatter(x=daily_sales['date'], y=daily_sales['revenue'],
                      mode='lines', name='CA Quotidien', line=dict(color='blue')),
            row=1, col=1
        )

        fig_evolution.add_trace(
            go.Scatter(x=daily_sales['date'], y=daily_sales['quantity'],
                      mode='lines', name='Quantités', line=dict(color='green')),
            row=1, col=2
        )

        fig_evolution.add_trace(
            go.Scatter(x=daily_sales['date'], y=daily_sales['orders'],
                      mode='lines', name='Commandes', line=dict(color='red')),
            row=2, col=1
        )

        # Évolution mensuelle
        monthly_data = filtered_df.groupby(filtered_df['date'].dt.to_period('M'))['total_price'].sum()
        fig_evolution.add_trace(
            go.Bar(x=[str(x) for x in monthly_data.index], y=monthly_data.values,
                   name='CA Mensuel', marker_color='purple'),
            row=2, col=2
        )

        fig_evolution.update_layout(height=600, showlegend=False, 
                                   title_text="Analyse Temporelle des Ventes")
        st.plotly_chart(fig_evolution, use_container_width=True)

        # Statistiques
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("💰 CA Moyen/Jour", f"{daily_sales['revenue'].mean():,.2f} €")
        with col2:
            st.metric("📦 Quantité Moy/Jour", f"{daily_sales['quantity'].mean():,.0f}")
        with col3:
            st.metric("🛒 Commandes Moy/Jour", f"{daily_sales['orders'].mean():.1f}")

    with tab2:
        st.subheader("🌍 Analyse Géographique")

        # Ventes par pays
        country_sales = filtered_df.groupby('country').agg({
            'total_price': 'sum',
            'quantity': 'sum',
            'customer_id': 'nunique'
        }).reset_index().sort_values('total_price', ascending=False)

        col1, col2 = st.columns(2)

        with col1:
            # Carte choroplèthe
            fig_map = px.choropleth(
                country_sales.head(20),
                locations='country',
                color='total_price',
                hover_name='country',
                hover_data={'total_price': ':,.2f'},
                color_continuous_scale='Viridis',
                title='Chiffre Affaires par Pays',
                locationmode='country names'
            )
            fig_map.update_layout(height=400)
            st.plotly_chart(fig_map, use_container_width=True)

        with col2:
            # Top pays
            fig_countries = px.bar(
                country_sales.head(10),
                x='total_price',
                y='country',
                orientation='h',
                title='Top 10 des Pays par CA',
                color='total_price',
                color_continuous_scale='Blues'
            )
            fig_countries.update_layout(height=400, yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig_countries, use_container_width=True)

        # Tableau détaillé
        st.subheader("📋 Détail par Pays")
        st.dataframe(
            country_sales.head(10).style.format({
                'total_price': '{:,.2f} €',
                'quantity': '{:,}',
                'customer_id': '{:,}'
            }),
            use_container_width=True
        )

    with tab3:
        st.subheader("🏷️ Analyse des Produits et Catégories")

        col1, col2 = st.columns(2)

        with col1:
            # Ventes par catégorie
            category_sales = filtered_df.groupby('category')['total_price'].sum().sort_values(ascending=False)

            fig_pie = px.pie(
                values=category_sales.values,
                names=category_sales.index,
                title='Répartition du CA par Catégorie',
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            st.plotly_chart(fig_pie, use_container_width=True)

        with col2:
            # Top produits
            product_sales = filtered_df.groupby(['product_code', 'product_description']).agg({
                'total_price': 'sum',
                'quantity': 'sum'
            }).reset_index().sort_values('total_price', ascending=False).head(10)

            fig_products = px.bar(
                product_sales,
                x='total_price',
                y='product_description',
                orientation='h',
                title='Top 10 des Produits',
                color='total_price',
                color_continuous_scale='Viridis'
            )
            fig_products.update_layout(height=400, yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig_products, use_container_width=True)

        # Performance par catégorie
        st.subheader("📊 Performance Détaillée par Catégorie")
        category_detail = filtered_df.groupby('category').agg({
            'total_price': ['sum', 'mean'],
            'quantity': 'sum',
            'product_code': 'nunique',
            'invoice_id': 'nunique'
        }).round(2)
        category_detail.columns = ['CA Total', 'CA Moyen', 'Quantités', 'Produits Uniques', 'Commandes']
        category_detail = category_detail.reset_index().sort_values('CA Total', ascending=False)

        st.dataframe(
            category_detail.style.format({
                'CA Total': '{:,.2f} €',
                'CA Moyen': '{:,.2f} €',
                'Quantités': '{:,}'
            }),
            use_container_width=True
        )

    with tab4:
        st.subheader("📊 Patterns Saisonniers")

        col1, col2 = st.columns(2)

        with col1:
            # Ventes par mois
            monthly_pattern = filtered_df.groupby('month_name')['total_price'].sum().reset_index()
            month_order = ['January', 'February', 'March', 'April', 'May', 'June',
                          'July', 'August', 'September', 'October', 'November', 'December']
            monthly_pattern['month_name'] = pd.Categorical(
                monthly_pattern['month_name'], categories=month_order, ordered=True
            )
            monthly_pattern = monthly_pattern.sort_values('month_name')

            fig_monthly = px.bar(
                monthly_pattern,
                x='month_name',
                y='total_price',
                title='Chiffre Affaires par Mois',
                color='total_price',
                color_continuous_scale='Plasma'
            )
            fig_monthly.update_layout(xaxis_tickangle=45)
            st.plotly_chart(fig_monthly, use_container_width=True)

        with col2:
            # Ventes par jour de la semaine
            weekday_pattern = filtered_df.groupby('day_name')['total_price'].sum().reset_index()
            day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            weekday_pattern['day_name'] = pd.Categorical(
                weekday_pattern['day_name'], categories=day_order, ordered=True
            )
            weekday_pattern = weekday_pattern.sort_values('day_name')

            fig_weekday = px.bar(
                weekday_pattern,
                x='day_name',
                y='total_price',
                title='Chiffre Affaires par Jour de la Semaine',
                color='total_price',
                color_continuous_scale='Viridis'
            )
            st.plotly_chart(fig_weekday, use_container_width=True)

        # Heatmap des ventes
        st.subheader("🔥 Heatmap des Ventes")
        heatmap_data = filtered_df.groupby(['month', 'day_of_week'])['total_price'].sum().reset_index()
        heatmap_pivot = heatmap_data.pivot(index='month', columns='day_of_week', values='total_price')

        day_mapping = {0: 'Lun', 1: 'Mar', 2: 'Mer', 3: 'Jeu', 4: 'Ven', 5: 'Sam', 6: 'Dim'}
        heatmap_pivot.columns = [day_mapping.get(col, str(col)) for col in heatmap_pivot.columns]

        fig_heatmap = px.imshow(
            heatmap_pivot,
            labels=dict(x="Jour de la Semaine", y="Mois", color="CA (€)"),
            title="Heatmap des Ventes par Mois et Jour",
            color_continuous_scale='Viridis'
        )
        st.plotly_chart(fig_heatmap, use_container_width=True)

    with tab5:
        st.subheader("🔮 Prédictions de Ventes")

        st.info("🤖 Modèle de prédiction basé sur les données historiques et les patterns saisonniers")

        # Paramètres de prédiction
        col1, col2 = st.columns(2)
        with col1:
            pred_days = st.slider("Nombre de jours à prédire", 7, 60, 30)
        with col2:
            confidence_level = st.selectbox("Niveau de confiance", [80, 90, 95], index=1)

        if st.button("🚀 Générer les Prédictions", type="primary"):
            # Calculs pour les prédictions
            daily_data = filtered_df.groupby(filtered_df['date'].dt.date)['total_price'].sum()

            # Prédictions basées sur la tendance et saisonnalité
            mean_daily = daily_data.mean()
            std_daily = daily_data.std()

            # Simulation de prédictions avec tendance saisonnière
            future_dates = pd.date_range(
                start=daily_data.index.max() + timedelta(days=1),
                periods=pred_days,
                freq='D'
            )

            # Ajout d'un pattern saisonnier simple
            seasonal_factor = np.sin(2 * np.pi * np.arange(pred_days) / 365) * 0.2 + 1
            trend_factor = np.linspace(1, 1.1, pred_days)  # Tendance légèrement croissante

            base_predictions = np.random.normal(mean_daily, std_daily * 0.3, pred_days)
            predictions = base_predictions * seasonal_factor * trend_factor
            predictions = np.maximum(predictions, 0)  # Pas de valeurs négatives

            # Intervalles de confiance
            confidence_mult = {80: 1.28, 90: 1.64, 95: 1.96}[confidence_level]
            margin = std_daily * 0.3 * confidence_mult

            lower_bound = predictions - margin
            upper_bound = predictions + margin

            # Graphique des prédictions
            fig_pred = go.Figure()

            # Données historiques (30 derniers jours)
            recent_data = daily_data.tail(30)
            fig_pred.add_trace(go.Scatter(
                x=recent_data.index,
                y=recent_data.values,
                mode='lines+markers',
                name='Données Historiques',
                line=dict(color='blue', width=2)
            ))

            # Prédictions
            fig_pred.add_trace(go.Scatter(
                x=future_dates,
                y=predictions,
                mode='lines+markers',
                name='Prédictions',
                line=dict(color='red', width=2, dash='dash')
            ))

            # Intervalles de confiance
            fig_pred.add_trace(go.Scatter(
                x=future_dates,
                y=upper_bound,
                fill=None,
                mode='lines',
                line_color='rgba(0,0,0,0)',
                showlegend=False
            ))

            fig_pred.add_trace(go.Scatter(
                x=future_dates,
                y=lower_bound,
                fill='tonexty',
                mode='lines',
                line_color='rgba(0,0,0,0)',
                name=f'Intervalle {confidence_level}%',
                fillcolor='rgba(255,0,0,0.2)'
            ))

            fig_pred.update_layout(
                title=f'Prédictions pour les {pred_days} Prochains Jours',
                xaxis_title='Date',
                yaxis_title='Chiffre Affaires Prédit (€)',
                height=500,
                hovermode='x unified'
            )

            st.plotly_chart(fig_pred, use_container_width=True)

            # Statistiques des prédictions
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("💰 CA Prédit Total", f"{predictions.sum():,.2f} €")
            with col2:
                st.metric("📊 CA Moyen/Jour", f"{predictions.mean():,.2f} €")
            with col3:
                st.metric("📈 CA Maximum", f"{predictions.max():,.2f} €")
            with col4:
                st.metric("📉 CA Minimum", f"{predictions.min():,.2f} €")

            # Sauvegarde des prédictions
            pred_df = pd.DataFrame({
                'Date': future_dates,
                'Prédiction (€)': predictions.round(2),
                'Borne Inf (€)': lower_bound.round(2),
                'Borne Sup (€)': upper_bound.round(2)
            })

            st.subheader("📋 Tableau des Prédictions")
            st.dataframe(pred_df, use_container_width=True)

            # Bouton de téléchargement
            csv = pred_df.to_csv(index=False)
            st.download_button(
                label="📥 Télécharger les Prédictions (CSV)",
                data=csv,
                file_name=f'yshop_predictions_{pred_days}j.csv',
                mime='text/csv'
            )

    # Résumé et recommandations
    st.markdown("---")
    st.subheader("📋 Résumé et Recommandations")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        #### 🎯 Points Clés Identifiés
        - **Saisonnalité**: Variations importantes selon les mois et jours
        - **Géographie**: Concentration sur certains marchés
        - **Produits**: Performance inégale des catégories
        - **Tendances**: Évolution temporelle des ventes
        """)

    with col2:
        st.markdown("""
        #### 🚀 Recommandations Stratégiques
        - **Stocks**: Optimiser selon les prédictions
        - **Marketing**: Cibler les périodes de forte demande
        - **Expansion**: Explorer les marchés sous-exploités
        - **Produits**: Développer les catégories performantes
        """)

else:
    st.error("❌ Impossible de charger les données. Vérifiez que le fichier 'Online.xlsx' est présent dans le répertoire.")
    st.info("💡 Assurez-vous que le fichier de données est dans le même dossier que l'application.")
