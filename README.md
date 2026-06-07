# KOSMONAUDID — Rahvusvahelise Kosmosejaama (ISS) nähtavuse prognoosimine Eesti kohal

## Äriküsimus
Projekt lahendab probleemi, kuidas tuvastada ja prognoosida Rahvusvahelise Kosmosejaama (ISS) füüsilist nähtavust Eestist, kombineerides jaama trajektoori reaalsete ilmaandmetega (pilvisus). Kasu saavad astronoomiahuvilised ja fotograafid, kes soovivad jaama palja silmaga kosmoses märgata või pildistada.

## Mõõdikud
1. **Nähtavuse indeks** — hinnang ISS-i nähtavusele (KÕRGE, MADAL või EI OLE NÄHTAV), mis põhineb elevatsiooninurgal ja pilvisusel.
2. **Pilvisuse protsent (%)** — Open-Meteo API-st pärinev pilvisuse näitaja Eesti koordinaatidel ülelennu hetkel.
3. **Kaugus vaatluspunktist (km)** — ISS-i ja Eesti vaatluspunkti vaheline matemaatiline kaugus maapinnal.

## Stack 
- **Sissevõtt & Transformatsioon:** Python (Requests, Pandas)
- **Andmehoidla:** CSV failid
- **Visualiseerimine:** Streamlit
- **Keskkond:** Docker Compose

## Esimesed katsed andmeallikatega
Oleme edukalt testinud ühendust järgmiste API-dega ja veendunud andmete kättesaadavuses:
1. **OpenNotify ISS API** (Annab jaama jooksvad koordinaadid)
2. **Open-Meteo API** (Annab reaalajas ilma- ja pilvisuse andmed)

Täpsem arhitektuuri ja andmevoo kirjeldus asub failis: [`docs/arhitektuur.md`](docs/arhitektuur.md)

## Andmekvaliteedi testid

Projekt sisaldab järgmisi andmekvaliteedi kontrolle:

1. NOT NULL kontroll – olulised väljad ei tohi olla tühjad.
2. Väärtuste vahemiku kontroll – koordinaadid, pilvisus ja elevatsioon peavad jääma lubatud piiridesse.
3. Unikaalsuse kontroll – sama ajatempliga kirjed ei tohi korduda.

Testide käivitamine:

python tests/run_tests.py

## Käivitamine
```bash
1. Paigalda sõltuvused

pip install -r requirements.txt

2. Käivita andmete kogumine

python scripts/ingest.py

3. Käivita testid

python tests/run_tests.py

4. Käivita näidikulaud

streamlit run app/app.py
```

## Tulemused

Projekt võimaldab koguda reaalajas ISS-i asukohaandmeid, kombineerida neid Eesti pilvisusandmetega ning hinnata automaatselt ISS-i nähtavust Eesti piirkonnas.

## Refleksioon

Projekti käigus õppisime reaalajas API-de kasutamist, andmete transformeerimist, andmekvaliteedi kontrollide loomist ning Streamlit näidikulaua arendamist. Hästi õnnestus erinevate andmeallikate ühendamine ühtseks andmevooks ning äriküsimusele vastava nähtavusindeksi loomine.


## Puudused

- Kasutame ainult Eesti keskpunkti, mitte konkreetseid vaatluskohti.
- Hämarikuaega ei arvutata.
- Andmed salvestatakse CSV faili, mitte andmebaasi.
- Nähtavuse mudel on lihtsustatud.

## Meeskond
- Natalja Pilipenko — arhitektuur, andmeallikad, andmetorustiku ja transformatsioonide arendus, andmekvaliteedi testid
- Liisa Rikanson — näidikulaud, dokumentatsioon, koodi testimine ja projekti video
