# Edenemisraport

## Mis on valmis

- [x] Docker Compose käivitab kõik teenused (`db`, `pipeline`, `dashboard`)
- [x] Andmeid saadakse allikatest (OpenNotify ja Open-Meteo) kätte
- [x] Andmed laetakse `staging` kihti töötlemata kujul
- [x] Vähemalt üks transformatsioon (asukoha ja nähtavuse arvutus) toimib
- [x] Vähemalt üks näidikulaud (Streamlit kaart) on nähtav ja töötab
- [x] Vähemalt üks andmekvaliteedi test (koordinaatide vahemikud) läbib

**Täpsustus:**
Projekti hoidla `ISS_Projekt` on loodud ja baasarhitektuur on paigas. Seadistatud on automaatne andmetorustik (`run_pipeline.py`), mis teeb taustaprotsessina iga 60 sekundi järel päringuid ISS API ja Open-Meteo API suunas. Toorandmed salvestatakse CSV-kujul `staging` kihti (`data/raw_iss_weather.csv`). 

Transformatsiooni käigus kontrollitakse geograafiliste piiride (bounding box) abil ISS-i asukohta Eesti läheduses ja arvutatakse ilma pilvisuse põhjal jaama reaalne nähtavuse indeks, mis salvestatakse `mart` kihi faili `data/clean_iss_weather.csv`. Streamlit veebirakendus (`app/app.py`) kuvab puhastatud andmeid interaktiivsel kaardil.

## Järgmised sammud

- [ ] **Skripti loogika optimeerimine:** Intervalli dünaamiline tihendamine (nt iga 10–30 sekundi järel), kui ISS jõuab Eesti lähedale ehk Euroopa koordinaatide aknasse, et ülelende mitte maha magada.
- [ ] **Näidikulaua täiendamine:** Streamliti akna täiendamine ajalooliste ülelendude graafikutega ja visuaalsete märguannete lisamine ("Nähtav praegu" / "Ei ole nähtav").
- [ ] **Testide integreerimine:** Andmekvaliteedi kontrollide viimine otse põhitorustiku sisse vahetult enne andmete kirjutamist puhtasse faili, et vältida vigaste andmete sattumist näidikulauale.

## Mis takistab

- Praegu blokeerivaid probleeme ei ole. Süsteemi põhikomponendid, andmete liikumine ja Dockeriseeritud keskkond töötavad plaanipäraselt.

## Kontrollpunkt

Käsk, millega saab reaalajas veenduda, et andmetorustik töötab, teeb päringuid ja salvestab andmeid:

```bash
docker compose logs -f pipeline