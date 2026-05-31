# Sprint 2 — Edenemisraport

## Mis on valmis
- [x] **Minimaalne andmevoog:** Üks allikas (ISS API) liigub läbi sissevõtu skripti faili ja sealt otse Streamlit visuaalini.
- [x] **Korratav sissevõtt:** Skript `scripts/ingest.py` on korratav (idempotentne) ja lisab iga käivitusega uue rea faili `data/raw_iss.csv`.
- [x] **Transformatsioon ja visuaal:** Failis `app/app.py` toimub andmete tüübituvastus ning kogutud punktid kuvatakse Streamliti kaardil ja KPI mõõdikuna.

## Järgmised sammud
- [ ] Teise andmeallika (Open-Meteo ilmaandmed) sissevõtt ja Haversine distantsi arvutamine eraldi transformatsiooni failis.
- [ ] Andmete salvestamise üleviimine CSV-failist PostgreSQL andmebaasi.
- [ ] Torustiku konteinerdamine Docker Compose abil.

## Mis takistab
- Blokeerivaid probleeme ei ole. Liigume graafikus ja minimaalne otsast-otsani töövoog toimib edukalt.

## Kontrollpunkt
1. Sissevõtu käivitamiseks ja andmete lisamiseks: `python scripts/ingest.py`
2. Veebirakenduse ja kaardi kuvamiseks: `streamlit run app/app.py`
