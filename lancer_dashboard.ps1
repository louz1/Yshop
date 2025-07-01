# Script PowerShell pour lancer le Dashboard Yshop
Write-Host "🚀 Lancement du Dashboard Yshop..." -ForegroundColor Green
Write-Host ""

# Vérifier si le fichier de données existe
if (Test-Path "Online.xlsx") {
    Write-Host "✅ Fichier de données trouvé: Online.xlsx" -ForegroundColor Green
} else {
    Write-Host "❌ Fichier Online.xlsx non trouvé !" -ForegroundColor Red
    Write-Host "Vérifiez que le fichier est dans le dossier courant." -ForegroundColor Yellow
    pause
    exit
}

# Vérifier si l'application existe
if (Test-Path "yshop_dashboard.py") {
    Write-Host "✅ Application dashboard trouvée: yshop_dashboard.py" -ForegroundColor Green
} else {
    Write-Host "❌ Fichier yshop_dashboard.py non trouvé !" -ForegroundColor Red
    pause
    exit
}

Write-Host ""
Write-Host "📦 Installation/Vérification des packages..." -ForegroundColor Cyan
& "C:/Users/kadem/AppData/Local/Programs/Python/Python313/python.exe" -m pip install streamlit plotly openpyxl --quiet --upgrade

Write-Host ""
Write-Host "🌐 Ouverture du dashboard dans votre navigateur..." -ForegroundColor Cyan
Write-Host "📍 Adresse: http://localhost:8501" -ForegroundColor Yellow
Write-Host ""
Write-Host "💡 Pour arrêter l'application, appuyez sur Ctrl+C dans cette fenêtre" -ForegroundColor Yellow
Write-Host ""

# Lancer Streamlit
& "C:/Users/kadem/AppData/Local/Programs/Python/Python313/python.exe" -m streamlit run yshop_dashboard.py

Write-Host ""
Write-Host "Dashboard fermé. Appuyez sur une touche pour continuer..." -ForegroundColor Green
pause
