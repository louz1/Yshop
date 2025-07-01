
@echo off
echo Lancement du Dashboard Yshop...
echo.
echo Vérification de Streamlit...
pip install streamlit plotly pandas openpyxl --quiet
echo.
echo Ouverture du dashboard dans le navigateur...
streamlit run yshop_dashboard.py
pause
