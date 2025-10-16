# Script de commit automatique pour KOF Ultimate Online
# Exécuté toutes les heures par le planificateur de tâches Windows

$RepoPath = "D:\KOF Ultimate Online"
$LogFile = "$RepoPath\auto_git_commit.log"

# Fonction de log
function Write-Log {
    param($Message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "$timestamp - $Message" | Out-File -FilePath $LogFile -Append
}

Write-Log "========== Début de la vérification automatique =========="

# Se placer dans le répertoire du dépôt
Set-Location $RepoPath

# Vérifier s'il y a des changements
$changes = git status --porcelain

if ($changes) {
    Write-Log "Changements détectés, début du commit..."

    # Ajouter tous les fichiers
    git add -A
    Write-Log "Fichiers ajoutés au staging"

    # Créer un commit avec timestamp
    $commitMessage = @"
Auto-commit: Sauvegarde automatique $(Get-Date -Format "yyyy-MM-dd HH:mm")

Modifications automatiquement committées par le système de sauvegarde horaire.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
"@

    git commit -m $commitMessage 2>&1 | Out-File -FilePath $LogFile -Append

    if ($LASTEXITCODE -eq 0) {
        Write-Log "Commit créé avec succès"

        # Pusher vers le remote
        git push 2>&1 | Out-File -FilePath $LogFile -Append

        if ($LASTEXITCODE -eq 0) {
            Write-Log "Push réussi vers le dépôt distant"
        } else {
            Write-Log "ERREUR: Échec du push"
        }
    } else {
        Write-Log "ERREUR: Échec du commit"
    }
} else {
    Write-Log "Aucun changement détecté, rien à committer"
}

Write-Log "========== Fin de la vérification automatique =========="
