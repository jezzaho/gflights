# GFLIGHTS - GOOGLE FLIGHTS PARSER

## Instrukcja 

## Opcja 1 - Codespaces, klon repozytorium, instalacja pakietów

## Opcja 2 - Środowisko lokalne

main.py - główny program wykonawczy
utils.py - funkcje pomocniczne
scraper.py - scraper strony internetowej

## KONFIGURACJA

1. ```console
foo@bar:~$ pip install playwright
```
2. ```console
foo@bar:~$ playwright install chromium 
foo
```

3. ```console
foo@bar:~$ pip install pandas selectolax openpyxl
foo
```

4. URUCHOMIENIE
```console
foo@bar:~$ python run main.py
foo
```

### WEJŚCIA

Pierwsze wejście podajemy lotnisko wylotu w kodzie IATA - podajemy tylko jedno, które jest bazowe, dla niego stworzone zostaną przyloty i odloty
Drugie wejścia to lotniska docelowe - jedno lub wiele oddzielone spacją również kodem iata przykład. FRA lub FRA MUC lub LTN LHR STN 

!! W kodzie main.py linia 13 jest hardcoded koniec przedziału, skrócony celem testowania i szybkiego sprawdzania wyników ustawiony jest na "4-10-2024", ta data może być dowolnie zmieniana pod warunkiem, że większa od "3-31-2024"
