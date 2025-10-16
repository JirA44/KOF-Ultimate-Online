# Script de configuration de la tâche planifiée pour commits automatiques
# Exécuter ce script une seule fois pour mettre en place le système

# Définir l'action : exécuter le script de commit automatique
$action = New-ScheduledTaskAction -Execute 'powershell.exe' `
    -Argument '-ExecutionPolicy Bypass -File "D:\KOF Ultimate Online\auto_git_commit.ps1"'

# Définir le déclencheur : toutes les heures, commençant maintenant
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Hours 1)

# Enregistrer la tâche planifiée
Register-ScheduledTask `
    -TaskName 'KOF_Ultimate_AutoCommit' `
    -Action $action `
    -Trigger $trigger `
    -Description 'Commit automatique horaire pour KOF Ultimate Online - Vérifie et committe les changements toutes les heures' `
    -Force

Write-Host "Tâche planifiée 'KOF_Ultimate_AutoCommit' créée avec succès !" -ForegroundColor Green
Write-Host "Le script s'exécutera toutes les heures et committera automatiquement les changements s'il y en a." -ForegroundColor Green
Write-Host ""
Write-Host "Pour vérifier la tâche : Get-ScheduledTask -TaskName 'KOF_Ultimate_AutoCommit'" -ForegroundColor Cyan
Write-Host "Pour désactiver : Disable-ScheduledTask -TaskName 'KOF_Ultimate_AutoCommit'" -ForegroundColor Cyan
Write-Host "Pour supprimer : Unregister-ScheduledTask -TaskName 'KOF_Ultimate_AutoCommit' -Confirm:$false" -ForegroundColor Cyan
