# GFLIGHTS - GOOGLE FLIGHTS PARSER

## Instrukcja 

## Opcja 1 - Codespaces, klon repozytorium, instalacja pakietów

## Opcja 2 - Środowisko lokalne

main.py - główny program wykonawczy
utils.py - funkcje pomocniczne
scraper.py - scraper strony internetowej

## KONFIGURACJA

WEBCRAWLER

```bash
foo@bar:~$ pip install playwright
```

PRZEGLĄDARKA WEBCRAWLERA

 ```bash
foo@bar:~$ playwright install chromium 
```

PANDAS I OPENPYXL DO EKSPORTU DO XLSX, SELECTOLAX DO PARSOWANIA STRONY DO JSON

 ```bash
foo@bar:~$ pip install pandas selectolax openpyxl
```

URUCHOMIENIE PROGRAMU

```bash
foo@bar:~$ python run main.py
```

### WEJŚCIA

Pierwsze wejście podajemy lotnisko wylotu w kodzie IATA - podajemy tylko jedno, które jest bazowe, dla niego stworzone zostaną przyloty i odloty
Drugie wejścia to lotniska docelowe - jedno lub wiele oddzielone spacją również kodem iata przykład. FRA lub FRA MUC lub LTN LHR STN 

!! W kodzie main.py linia 13 jest hardcoded koniec przedziału, skrócony celem testowania i szybkiego sprawdzania wyników ustawiony jest na "4-10-2024", ta data może być dowolnie zmieniana pod warunkiem, że większa od "3-31-2024"
