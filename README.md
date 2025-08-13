# Seed-X Translation GUI

Profesjonalna aplikacja GUI w Pythonie do korzystania z modelu tłumaczeniowego Seed-X-PPO-7B.

## Funkcje

- Obsługa tłumaczeń między 28 językami
- Nowoczesny interfejs GUI z PyQt6
- Wielowątkowe ładowanie modelu i tłumaczenie (nieblokujący UI)
- Tryb Chain-of-Thought (CoT) z szczegółowymi wyjaśnieniami
- Regulowane parametry generowania (temperatura, top-p, top-k, itp.)
- Historia tłumaczeń z funkcją eksportu/importu
- Dokowane panele dla ustawień i historii
- Trwałe ustawienia aplikacji
- Skróty klawiszowe dla częstych akcji
- Automatyczne pobieranie modeli z Hugging Face
- Obsługa GPU (CUDA) dla szybkich tłumaczeń

## Backends

Aplikacja obsługuje dwa backendy:

1. **GGUF (llama.cpp)** - Zalecany dla większości użytkowników
   - Używa skwantyzowanych modeli GGUF
   - Niższe zużycie pamięci
   - Dobra wydajność na CPU i GPU
   - Działa na Windows

2. **Transformers** - Dla oryginalnych modeli
   - Używa modeli pełnej precyzji
   - Wyższe zużycie pamięci
   - Najlepsza jakość
   - Działa na Windows z CUDA

## Wymagania

- Python 3.8+
- GPU z obsługą CUDA (zalecane) lub CPU (wolniejsze)
- Co najmniej 8GB RAM (16GB zalecane)
- Około 5GB miejsca na dysku dla modelu Q4_K_M

## Instalacja

### Opcja 1: Automatyczna instalacja (Zalecana)

**Dla Windows Command Prompt:**
```cmd
install.bat
```

**Dla PowerShell:**
```powershell
.\install.ps1
```

### Opcja 2: Instalacja ręczna

1. Utwórz środowisko wirtualne:
```bash
python -m venv venv
```

2. Aktywuj środowisko wirtualne:
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. Zainstaluj wymagane pakiety:
```bash
pip install -r requirements.txt
```

## Użycie

### Szybki start
```cmd
run.bat
```

### Start ręczny
```bash
# Najpierw aktywuj środowisko wirtualne
venv\Scripts\activate

# Uruchom aplikację
python translator_app.py
```

## Pobieranie modeli

Aplikacja automatycznie wykryje i załaduje dostępne modele. Jeśli nie masz żadnego modelu:

1. Uruchom aplikację
2. Kliknij "Download Model"
3. Wybierz model (zalecany: Q4_K_M - 4.6GB)
4. Poczekaj na zakończenie pobierania
5. Model zostanie automatycznie załadowany

### Dostępne modele GGUF:

- **Q4_K_M (4.6GB)** - Zalecany balans jakości/szybkości
- **Q5_K_M (5.4GB)** - Lepsza jakość, wolniejszy
- **Q8_0 (8.0GB)** - Najlepsza jakość, wymaga więcej RAM

### Model oryginalny (dla Transformers):

- **Original Seed-X-PPO-7B (15GB)** - Pełna precyzja, wymaga więcej VRAM

## Obsługiwane języki

- Arabski (ar), Czeski (cs), Duński (da), Niemiecki (de)
- Angielski (en), Hiszpański (es), Fiński (fi), Francuski (fr)
- Chorwacki (hr), Węgierski (hu), Indonezyjski (id), Włoski (it)
- Japoński (ja), Koreański (ko), Malajski (ms), Norweski Bokmål (nb)
- Holenderski (nl), Norweski (no), Polski (pl), Portugalski (pt)
- Rumuński (ro), Rosyjski (ru), Szwedzki (sv), Tajski (th)
- Turecki (tr), Ukraiński (uk), Wietnamski (vi), Chiński (zh)

## Struktura projektu

```
TranslatorSeedX/
├── translator_app.py           # Główna aplikacja GUI
├── model_handler.py            # Handler dla GGUF (llama.cpp)
├── model_handler_transformers.py # Handler dla Transformers
├── config.py                   # Konfiguracja aplikacji
├── download_missing_files.py   # Skrypt pobierania plików modelu
├── requirements.txt            # Zależności Python
├── install.bat                 # Instalator Windows (CMD)
├── install.ps1                 # Instalator Windows (PowerShell)
├── run.bat                     # Uruchamianie aplikacji
├── README.md                   # Ten plik
├── models/                     # Katalog modeli
│   └── README.md               # Informacje o modelach
└── venv/                       # Środowisko wirtualne (po instalacji)
```

## Rozwiązywanie problemów

### Model się nie ładuje
- Sprawdź czy masz wystarczająco RAM/VRAM
- Spróbuj mniejszego modelu (Q4_K_M zamiast Q8_0)
- Sprawdź logi w konsoli dla szczegółów błędu
- Dla modeli Transformers: upewnij się, że masz zainstalowane CUDA

### Wolne tłumaczenie
- Użyj GPU zamiast CPU (sprawdź czy CUDA jest dostępne)
- Zmniejsz parametr "Max Tokens" w ustawieniach
- Użyj mniejszego modelu
- Przełącz na backend Transformers dla lepszej wydajności GPU

### Błędy CUDA
- Upewnij się, że masz zainstalowany PyTorch z obsługą CUDA
- Sprawdź czy sterowniki GPU są aktualne
- Spróbuj reinstalacji PyTorch: `pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121`

## Licencja

Ten projekt używa modelu Seed-X-PPO-7B na licencji OpenMDW.

## Autorzy

Aplikacja GUI stworzona dla modelu Seed-X-PPO-7B od ByteDance.
Model GGUF skwantyzowany przez Mungert na Hugging Face.
