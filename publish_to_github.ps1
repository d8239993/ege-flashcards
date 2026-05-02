# Один раз: вход в GitHub в браузере, создание репозитория и push (ветка main).
# Запуск: правый клик → «Выполнить с помощью PowerShell» или: pwsh -File .\publish_to_github.ps1
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

$gh = Join-Path ${env:ProgramFiles} "GitHub CLI\gh.exe"
if (-not (Test-Path $gh)) {
    Write-Host "Установите GitHub CLI: winget install GitHub.cli"
    exit 1
}

& $gh auth status 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "Нужен вход в GitHub — откроется браузер."
    & $gh auth login -h github.com -p https -w
}

$repoName = "vk-cards-flashcards"
$hasRemote = git remote get-url origin 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "Remote уже задан, отправляю в GitHub..."
    git push -u origin main
    Write-Host "Готово. Включите Pages: репозиторий на GitHub → Settings → Pages → Source: GitHub Actions."
    exit 0
}

Write-Host "Создаю репозиторий $repoName и отправляю код..."
& $gh repo create $repoName --public --source . --remote origin --push
Write-Host "Готово. Откройте: https://github.com/$( & $gh api user -q .login )/$repoName"
Write-Host "Затем: Settings → Pages → Build and deployment → Source: GitHub Actions."
