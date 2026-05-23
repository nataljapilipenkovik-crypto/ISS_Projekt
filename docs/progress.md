# Edenemisraport

## Mis on valmis

- [x] Docker Compose käivitab kõik teenused
- [x] Andmeid saadakse allikast kätte
- [x] Andmed laetakse `staging` kihti
- [x] Vähemalt üks transformatsioon toimib
- [x] Vähemalt üks näidikulaud on nähtav
- [x] Vähemalt üks andmekvaliteedi test läbib

**Täpsustus:**
Projekti hoidla `ISS_Projekt` on loodud ja baasarhitektuur on paigas. Seadistatud on automaatne andmetorustik (`run_pipeline.py`), mis teeb iga 60 sekundi järel päringuid ISS API ja Open-Meteo API suunas. Toorandmed salvestatakse CSV-kujul `staging` kihti (`raw_iss_weather.csv`). Transformatsiooni käigus (`transform.py`) kontrollitakse geograafiliste piiride  abil ISS-i asukohta Eesti kohal ja arvutatakse pilvisuse põhjal nähtavuse indeks, mis salvestatakse faili `clean_iss_weather.csv`. Streamlit veebirakendus (`app.py`) kuvab puhastatud andmeid interaktiivsel kaardil.

## Järgmised sammud

- [ ] Skripti loogika optimeerimine: intervalli tihendamine (nt iga 10-30 sekundi järel), kui ISS jõuab Eesti lähedale ehk Euroopa koordinaatide aknasse.
- [ ] Streamliti näidikuakna täiendamine ajalooliste ülelendude graafikutega ja visuaalsete märguannete lisamine ("Nähtav praegu" / "Ei ole nähtav").
- [ ] Andmekvaliteedi testide integreerimine otse põhitorustikku enne andmete kirjutamist puhastatud faili, et vältida vigaste andmete sattumist näidikulauale.

## Mis takistab

- [Praegu pole blokeerivaid probleeme. Süsteemi põhikomponendid ja Dockeriseeritud keskkond töötavad plaanipäraselt.]

## Kontrollpunkt

Käsk, millega saab kontrollida, et töövoog töötab:

```bash
# Käivitab andmetorustiku ja kontrollib andmete liikumist allikatest kuni puhastatud CSV-ni
docker compose exec pipeline python scripts/run_pipeline.py