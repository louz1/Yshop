@echo off
echo.
echo ============================================
echo       TEST DU DASHBOARD YSHOP
echo ============================================
echo.

echo [1/3] Verification de la syntaxe Python...
python -m py_compile yshop_dashboard.py
if %errorlevel% neq 0 (
    echo ❌ Erreur de syntaxe detectee !
    pause
    exit /b 1
)
echo ✅ Syntaxe Python valide

echo.
echo [2/3] Test des imports...
python -c "import pandas, plotly, streamlit; print('✅ Bibliotheques OK')"
if %errorlevel% neq 0 (
    echo ❌ Probleme avec les bibliotheques !
    echo ℹ️  Installez avec: pip install streamlit plotly pandas scikit-learn openpyxl
    pause
    exit /b 1
)

echo.
echo [3/3] Lancement du dashboard...
echo ℹ️  Le dashboard va s'ouvrir dans votre navigateur
echo ℹ️  Adresse: http://localhost:8501
echo ℹ️  Pour arreter: Ctrl+C dans cette fenetre
echo.
echo 🚀 Demarrage en cours...
timeout /t 2 >nul
streamlit run yshop_dashboard.py
