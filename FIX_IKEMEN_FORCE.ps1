# Force fix Ikemen GO folders
$ikemenDir = "D:\KOF Ultimate Online\Ikemen_GO"
$baseDir = "D:\KOF Ultimate Online"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host " RÉPARATION FORCÉE IKEMEN GO" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$folders = @('data', 'font', 'chars', 'stages', 'sound')

foreach ($folder in $folders) {
    $target = Join-Path $ikemenDir $folder
    $source = Join-Path $baseDir $folder

    Write-Host "Processing: $folder" -ForegroundColor Yellow

    # Force remove if exists (even if it's a broken junction)
    if (Test-Path $target) {
        Write-Host "  Removing existing..." -NoNewline
        try {
            # Try to remove junction/symlink
            (Get-Item $target).Delete()
        } catch {
            # If that fails, use cmd to remove
            cmd /c "rd /S /Q `"$target`" 2>nul"
        }

        # Double check it's gone
        if (-not (Test-Path $target)) {
            Write-Host " OK" -ForegroundColor Green
        } else {
            Write-Host " FAILED" -ForegroundColor Red
            continue
        }
    }

    # Create junction
    Write-Host "  Creating junction..." -NoNewline
    $result = cmd /c "mklink /J `"$target`" `"$source`" 2>&1"

    if ($LASTEXITCODE -eq 0) {
        Write-Host " OK" -ForegroundColor Green
    } else {
        Write-Host " FAILED - Copying instead" -ForegroundColor Yellow
        try {
            Copy-Item -Path $source -Destination $target -Recurse -Force -ErrorAction Stop
            Write-Host "  Copy complete" -ForegroundColor Green
        } catch {
            Write-Host "  Copy FAILED: $_" -ForegroundColor Red
        }
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host " TERMINÉ!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

# Test if data/system.def exists
$systemDef = Join-Path $ikemenDir "data\system.def"
if (Test-Path $systemDef) {
    Write-Host "[OK] data/system.def found!" -ForegroundColor Green
} else {
    Write-Host "[ERROR] data/system.def MISSING!" -ForegroundColor Red
}

Write-Host ""

# Only pause if run manually (not from another script)
if (-not $env:AUTOMATED_RUN) {
    Write-Host "Press any key to continue..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
}
