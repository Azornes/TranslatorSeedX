@echo off
echo Creating GitHub repository via API...
echo.

REM You need to replace YOUR_GITHUB_TOKEN with your actual token
REM Get token from: https://github.com/settings/tokens
REM Required scopes: repo, public_repo

set GITHUB_TOKEN=YOUR_GITHUB_TOKEN
set REPO_NAME=TranslatorSeedX
set REPO_DESCRIPTION=Seed-X Translation Application - PyQt6 GUI for multilingual translation using Seed-X-PPO-7B model

if "%GITHUB_TOKEN%"=="YOUR_GITHUB_TOKEN" (
    echo ERROR: Please edit this file and replace YOUR_GITHUB_TOKEN with your actual GitHub token
    echo.
    echo Steps to get token:
    echo 1. Go to https://github.com/settings/tokens
    echo 2. Click "Generate new token" ^(classic^)
    echo 3. Select scopes: repo, public_repo
    echo 4. Copy the token and replace YOUR_GITHUB_TOKEN in this file
    echo.
    pause
    exit /b 1
)

echo Creating repository: %REPO_NAME%
echo Description: %REPO_DESCRIPTION%
echo.

curl -X POST ^
  -H "Authorization: token %GITHUB_TOKEN%" ^
  -H "Accept: application/vnd.github.v3+json" ^
  https://api.github.com/user/repos ^
  -d "{\"name\":\"%REPO_NAME%\",\"description\":\"%REPO_DESCRIPTION%\",\"private\":false,\"auto_init\":false}"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo Repository created successfully!
    echo.
    echo Now pushing code to GitHub...
    git push -u origin master
    
    if %ERRORLEVEL% EQU 0 (
        echo.
        echo SUCCESS! Repository is now available at:
        echo https://github.com/Azornes/%REPO_NAME%
    ) else (
        echo.
        echo Repository created but push failed. Try manually:
        echo git push -u origin master
    )
) else (
    echo.
    echo Failed to create repository. Check your token and try again.
)

echo.
pause
