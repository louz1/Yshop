@echo off
echo 🚀 Push du Projet Yshop vers GitHub...
echo.

git add .
set /p message="💬 Message de commit (ou Entrée pour message auto): "
if "%message%"=="" set message=🔄 Update: %date% %time%

echo 📦 Commit en cours...
git commit -m "%message%"

echo 🌐 Push vers GitHub...
git push origin main

echo.
echo ✅ Push terminé avec succès!
echo 🔗 Repository: https://github.com/VOTRE_USERNAME/Yshop-Sales-Prediction
echo.
pause
