# PowerShell script to create GitHub repository via API
param(
    [string]$Token = "YOUR_GITHUB_TOKEN"
)

Write-Host "Creating GitHub repository via API..." -ForegroundColor Green
Write-Host ""

$repoName = "TranslatorSeedX"
$repoDescription = "Seed-X Translation Application - PyQt6 GUI for multilingual translation using Seed-X-PPO-7B model"

if ($Token -eq "YOUR_GITHUB_TOKEN") {
    Write-Host "ERROR: Please provide your GitHub token" -ForegroundColor Red
    Write-Host ""
    Write-Host "Usage: .\create_github_repo.ps1 -Token YOUR_ACTUAL_TOKEN"
    Write-Host ""
    Write-Host "Steps to get token:"
    Write-Host "1. Go to https://github.com/settings/tokens"
    Write-Host "2. Click 'Generate new token (classic)'"
    Write-Host "3. Select scopes: repo, public_repo"
    Write-Host "4. Copy the token and use it with this script"
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "Creating repository: $repoName" -ForegroundColor Yellow
Write-Host "Description: $repoDescription" -ForegroundColor Yellow
Write-Host ""

# Prepare the JSON payload
$body = @{
    name = $repoName
    description = $repoDescription
    private = $false
    auto_init = $false
} | ConvertTo-Json

# Set headers
$headers = @{
    "Authorization" = "token $Token"
    "Accept" = "application/vnd.github.v3+json"
    "User-Agent" = "PowerShell-Script"
}

try {
    # Create repository
    $response = Invoke-RestMethod -Uri "https://api.github.com/user/repos" -Method Post -Headers $headers -Body $body -ContentType "application/json"
    
    Write-Host "Repository created successfully!" -ForegroundColor Green
    Write-Host "Repository URL: $($response.html_url)" -ForegroundColor Cyan
    Write-Host ""
    
    # Push code to GitHub
    Write-Host "Pushing code to GitHub..." -ForegroundColor Yellow
    $pushResult = git push -u origin master 2>&1
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "SUCCESS! Repository is now available at:" -ForegroundColor Green
        Write-Host "https://github.com/Azornes/$repoName" -ForegroundColor Cyan
    } else {
        Write-Host ""
        Write-Host "Repository created but push failed:" -ForegroundColor Yellow
        Write-Host $pushResult -ForegroundColor Red
        Write-Host ""
        Write-Host "Try manually: git push -u origin master" -ForegroundColor Yellow
    }
    
} catch {
    Write-Host "Failed to create repository:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    
    if ($_.Exception.Response.StatusCode -eq 401) {
        Write-Host ""
        Write-Host "Authentication failed. Please check your token." -ForegroundColor Yellow
    } elseif ($_.Exception.Response.StatusCode -eq 422) {
        Write-Host ""
        Write-Host "Repository might already exist or name is invalid." -ForegroundColor Yellow
    }
}

Write-Host ""
Read-Host "Press Enter to exit"
