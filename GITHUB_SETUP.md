# Instrukcje dodania projektu do GitHub

## Metoda 1: Automatyczne utworzenie przez skrypty (ZALECANE)

### Opcja A: PowerShell (zalecane)
1. Uzyskaj Personal Access Token:
   - Idź na https://github.com/settings/tokens
   - Kliknij "Generate new token (classic)"
   - Wybierz scopes: `repo`, `public_repo`
   - Skopiuj token

2. Uruchom skrypt:
```powershell
.\create_github_repo.ps1 -Token YOUR_ACTUAL_TOKEN
```

### Opcja B: Batch file
1. Edytuj plik `create_github_repo.bat`
2. Zamień `YOUR_GITHUB_TOKEN` na swój rzeczywisty token
3. Uruchom: `create_github_repo.bat`

## Metoda 2: Ręczne utworzenie na GitHub

### Krok 1: Utwórz repozytorium na GitHub

1. Przejdź do https://github.com/Azornes/
2. Kliknij przycisk "New" lub "+" w prawym górnym rogu
3. Wybierz "New repository"
4. Wypełnij formularz:
   - **Repository name**: `TranslatorSeedX`
   - **Description**: `Seed-X Translation Application - PyQt6 GUI for multilingual translation using Seed-X-PPO-7B model`
   - **Visibility**: Public (zaznacz "Public")
   - **NIE zaznaczaj**: "Add a README file", "Add .gitignore", "Choose a license" (mamy już te pliki)
5. Kliknij "Create repository"

### Krok 2: Wypchnij kod na GitHub

Po utworzeniu repozytorium uruchom te komendy w terminalu:

```bash
git push -u origin master
```

Lub jeśli GitHub używa `main` jako domyślnej gałęzi:

```bash
git branch -M main
git push -u origin main
```

## Krok 3: Sprawdź repozytorium

Po udanym push'u, Twoje repozytorium będzie dostępne pod adresem:
https://github.com/Azornes/TranslatorSeedX

## Struktura repozytorium

Repozytorium będzie zawierać:
- ✅ Kod źródłowy w modularnej strukturze (`src/`)
- ✅ Dokumentację (`README.md`, `PROJECT_STRUCTURE.md`)
- ✅ Skrypty instalacyjne (`install.bat`, `install.ps1`)
- ✅ Plik uruchamiający (`main.py`, `run.bat`)
- ✅ Konfigurację (`requirements.txt`, `.gitignore`)
- ❌ Pliki modeli (wykluczone przez `.gitignore` - za duże dla GitHub)

## Uwagi

- Pliki modeli są wykluczone z repozytorium (za duże)
- Użytkownicy będą mogli pobrać modele automatycznie przez aplikację
- Repozytorium zawiera tylko kod źródłowy i dokumentację
- Rozmiar repozytorium: ~100KB (bez modeli)

## Po utworzeniu repozytorium

Możesz dodać:
- GitHub Actions dla CI/CD
- Issues templates
- Pull request templates
- Wiki z dodatkową dokumentacją
- Releases z skompilowanymi wersjami
