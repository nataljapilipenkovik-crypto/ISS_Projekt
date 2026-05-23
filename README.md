Kosmonaudid — Rahvusvahelise Kosmosejaama (ISS) nähtavuse prognoosimine Eesti kohal

## Äriküsimus

Projekt lahendab probleemi, kuidas reaalajas tuvastada ja prognoosida Rahvusvahelise Kosmosejaama (ISS) füüsilist nähtavust Eesti eri asukohtades, kombineerides jaama trajektoori reaalsete ilmaandmetega (pilvisus). Kasu saavad astronoomiahuvilised ja fotograafid, kes soovivad jaama palja silmaga kosmoses märgata või pildistada.

**Mõõdikud:**

1. **ISS-i ülelennu nähtavuse indeks** — Süsteemi arvutatud indeks (KÕRGE / KESKMINE / MADAL / PUUDUB), mis põhineb jaama asukohal ja konkreetse Eesti asukoha hetke pilvisusel.
2. **Pilvisuse protsent (%)** — Open-Meteo API-st pärinev reaalajas pilvisuse näitaja Eesti koordinaatidel ülelennu hetkel.
3. **Haversine distants (km)** — ISS-i ja Eesti vaatluspunkti vaheline matemaatiline kaugus maapinnal.

## Arhitektuur

```mermaid
flowchart LR
    api_iss[OpenNotify ISS API] --> ingest[Python sissevõtu skript]
    api_weather[Open-Meteo API] --> ingest
    geo_csv[Eesti asukohtade CSV] --> ingest
    
    ingest --> staging[(staging: raw_iss & raw_weather)]
    staging --> transform[Transformatsioon & Haversine arvutus]
    transform --> mart[(mart: fct_iss_passes & dim_weather)]
    
    mart --> dashboard[Näidikulaud: Streamlit / kaardi visualiseering]
    mart --> quality[Andmekvaliteedi testid: koordinaatide vahemikud]
    scheduler[Cron / GitHub Actions] --> ingest

Täpsem kirjeldus: [`docs/arhitektuur.md`](docs/arhitektuur.md)

## Andmestik

|Allikas|Tüüp|Ajas muutuv?|Roll|
|-------|----|------------|----|
|OpenNotify ISS API | Jah, reaalajas (päring iga 60s)ISS-i jooksvate koordinaatide (laiuskraad, pikkuskraad) ja ajatempli saamine.|
|Open-Meteo API |Jah, tunni kaupaEesti asukohtade reaalajas ilmaandmete (pilvisus protsentides) pärimine.|
|Eesti asukohtade CSVFail (.csv)|Ei, staatiline|Spikker-tabel (seed), mis sisaldab Eesti suuremate linnade ametlikke geokoordinaate.|

## Stack
|Komponent|Tööriist|Sissevõtt|
|Python (requests raamistik)|
|Transformatsioon|Python (pandas andmetöötlus ja Haversine valem)|
|Andmehoidla|PostgreSQL (pgDuckDB) / Kohalikud organiseeritud CSV failid|
|Näidikulaud|Streamlit (koos interaktiivse kaardikomponendiga)|
|Orkestreerimine|Docker Compose taustaprotsess (tulevikus GitHub Actions / Cron)|

## Käivitamine

```bash
# 1. Klooni repo ja liigu kausta
git clone <teie-repo-url>
cd ISS_Projekt

# 2. Kopeeri keskkonnamuutujad (Vajalik vaid esimesel korral!)
cp .env.example .env

# 3. Käivita kogu süsteem ja näidikulaud taustal
docker compose up -d --build

# 4. Vaata töövoo (pipeline) elavaid logisid ja andmete liikumist
docker compose logs -f pipeline

```


Näidikulaud on brauseris koheselt kättesaadav aadressil: http://localhost:8501

## Saladused ja konfiguratsioon

Kõik projekti seaded ja andmebaasi paroolid on eraldatud koodist ja asuvad kohalikus .env failis. Turvakaalutlustel on .env lisatud .gitignore ja .dockerignore failidesse ning seda GitHubi ei fanta. Repos on kaasas mall .env.example.

**Vajalikud muutujad .env failis:**
|Muutuja|Tähendus|Näide|
|-------|--------|-----|


##on vaja lõpetada siin