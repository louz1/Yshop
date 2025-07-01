# Script PowerShell pour pousser les modifications sur GitHub
Write-Host "🚀 Push du Projet Yshop vers GitHub..." -ForegroundColor Green

# Vérifier s'il y a des modifications
$status = git status --porcelain
if ($status) {
    Write-Host "📝 Modifications détectées, ajout des fichiers..." -ForegroundColor Yellow
    git add .
    
    # Demander un message de commit
    $message = Read-Host "💬 Message de commit (ou Entrée pour message auto)"
    if ([string]::IsNullOrWhiteSpace($message)) {
        $date = Get-Date -Format "yyyy-MM-dd HH:mm"
        $message = "🔄 Update: $date"
    }
    
    Write-Host "📦 Commit en cours..." -ForegroundColor Cyan
    git commit -m $message
    
    Write-Host "🌐 Push vers GitHub..." -ForegroundColor Cyan
    git push origin main
    
    Write-Host "✅ Push terminé avec succès!" -ForegroundColor Green
} else {
    Write-Host "ℹ️  Aucune modification à pousser" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🔗 Votre repository: https://github.com/VOTRE_USERNAME/Yshop-Sales-Prediction" -ForegroundColor Blue
Write-Host ""
pause
