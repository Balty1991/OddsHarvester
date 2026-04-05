# OddsHarvester Prediction Overlay

Acest pachet adaugă peste repo-ul `OddsHarvester` un calculator de predicții și un modul de calibrare/backtest pentru datele exportate de scraper.

## Ce conține

- comandă nouă CLI: `oddsharvester predict`
- motor de predicții bazat pe consensul cotelor și reguli statistice simple, dar robuste
- calibrare opțională din fișiere istorice exportate de `historic`
- export rezultate în JSON sau CSV
- scor de încredere, edge estimat și miză Kelly fracționată

## Cum se folosește

### Varianta recomandată

1. Descarci repo-ul original `OddsHarvester`.
2. Copiezi peste el fișierele din acest overlay, păstrând structura directoarelor.
3. Rulezi din repo-ul rezultat:

```bash
pip install -e .
oddsharvester predict --input upcoming.json --markets 1x2,over_2_5,btts
```

### Fără calibrare istorică

```bash
oddsharvester predict \
  --input upcoming.json \
  --markets 1x2,double_chance,over_1_5,over_2_5,under_3_5,btts \
  --top 20 \
  --min-confidence 60 \
  --output predictions.json
```

### Cu calibrare din fișier istoric

```bash
oddsharvester predict \
  --input upcoming.json \
  --calibration-input historic.json \
  --markets 1x2,over_2_5,btts \
  --top 30 \
  --output predictions.csv \
  --output-format csv
```

## Ce face calculatorul

- citește cote 1X2 / BTTS / O-U / Double Chance din exporturi OddsHarvester
- normalizează probabilitățile implicite (scoate marja de overround)
- construiește consens pe piață
- estimează piețe derivate precum `over_1_5`, `under_3_5`, `1X`, `X2`
- aplică ajustări dacă există calibrare din rezultate istorice
- generează selecții ordonate după încredere și edge

## Câmpuri rezultate

- `predicted_market`
- `selection`
- `probability`
- `confidence`
- `edge`
- `fair_odds`
- `best_odds`
- `recommended_stake`
- `explanation`

## Observații

- Overlay-ul nu rescrie motorul original de scraping; îl completează.
- Schema exactă a exporturilor poate varia, așa că parserul inclus este tolerant și caută câmpuri echivalente.
- Dacă inputul nu conține anumite piețe, motorul sare elegant peste ele.

## Fișiere de copiat în repo-ul original

- `src/oddsharvester/cli/cli.py`
- `src/oddsharvester/cli/commands/__init__.py`
- `src/oddsharvester/cli/commands/predict.py`
- tot directorul `src/oddsharvester/predict/`

