# KOSMONAUDID — Rahvusvahelise Kosmosejaama (ISS) nähtavuse prognoosimine Eesti kohal

## Äriküsimus
Projekt lahendab probleemi, kuidas tuvastada ja prognoosida Rahvusvahelise Kosmosejaama (ISS) füüsilist nähtavust Eesti eri asukohtades, kombineerides jaama trajektoori reaalsete ilmaandmetega (pilvisus). Kasu saavad astronoomiahuvilised ja fotograafid, kes soovivad jaama palja silmaga kosmoses märgata või pildistada.

## Mõõdikud
1. **ISS-i ülelennu nähtavuse indeks** — Arvutuslik indeks (KÕRGE / KESKMINE / MADAL / PUUDUB), mis põhineb jaama asukohal ja konkreetse Eesti asukoha hetke pilvisusel.
2. **Pilvisuse protsent (%)** — Open-Meteo API-st pärinev pilvisuse näitaja Eesti koordinaatidel ülelennu hetkel.
3. **Kaugus vaatluspunktist (km)** — ISS-i ja Eesti vaatluspunkti vaheline matemaatiline kaugus maapinnal.

## Stack 
- **Sissevõtt & Transformatsioon:** Python (Requests, Pandas)
- **Andmehoidla:** PostgreSQL
- **Visualiseerimine:** Streamlit
- **Keskkond:** Docker Compose

## Esimesed katsed andmeallikatega
Oleme edukalt testinud ühendust järgmiste API-dega ja veendunud andmete kättesaadavuses:
1. **OpenNotify ISS API** (Annab jaama jooksvad koordinaadid)
2. **Open-Meteo API** (Annab reaalajas ilma- ja pilvisuse andmed)

Täpsem arhitektuuri ja andmevoo kirjeldus asub failis: [`docs/arhitektuur.md`](docs/arhitektuur.md)

## Meeskond
- Natalja Pilipenko — 
- Liisa Rikanson — 
