# Tønnesjakk

En Python-implementasjon av det strategiske brettspillet Tønnesjakk.

## Om Spillet
Tønnesjakk er et strategisk brettspill hvor spillere konkurrerer om å flytte sine tønner over brettet. 
Spillet kombinerer elementer av sjakk og dam, med unike regler som gjør det både utfordrende og 
underholdende.

## Funksjoner
- Komplett implementasjon av Tønnesjakk-regler
- Konsollbasert brukergrensesnitt
- Omfattende testsuite
- AI-agent funksjonalitet (under utvikling)

## Prosjektstruktur
```
tonnesjakk/
├── src/
│   └── game/
│       ├── model.py      # Spillogikk og datastrukturer
│       ├── controller.py # Spillkontroll
│       ├── view.py      # Brukergrensesnitt
│       └── main.py      # Hovedapplikasjon
├── tests/
│   └── game/
│       ├── test_model.py # Enhetstester
│       └── test_rules.py # Spillregeltester
└── requirements.txt
```

## Installasjon
1. Klon repositoriet:
```bash
git clone git@github.com:emilgarden/tonnesjakk.git
cd tonnesjakk
```

2. Opprett og aktiver virtuelt miljø:
```bash
python -m venv venv
source venv/bin/activate  # På Windows: venv\Scripts\activate
```

3. Installer avhengigheter:
```bash
pip install -r requirements.txt
```

## Kjøre Spillet
```bash
python -m src.game.main
```

## Kjøre Tester
```bash
python -m unittest discover -v
```

## Utvikling
- Følg eksisterende kodestruktur og konvensjoner
- Skriv tester for ny funksjonalitet
- Hold dokumentasjonen oppdatert

## Kommende Funksjoner
- AI-agent med maskinlæring
- Grafisk brukergrensesnitt
- Nettverksbasert multiplayer
- Replay-system for spillanalyse

## Bidrag
Bidrag er velkomne! Vennligst les gjennom kodestil og prosjektstruktur før du sender inn pull requests.

## Lisens
[Velg en passende lisens]