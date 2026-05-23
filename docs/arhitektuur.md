# KOSMONAUDID : ISS-i trajektoor ja nähtavus Eesti kontekstis

## Äriküsimus

Millal, kus ja milliste tingimuste korral on Rahvusvaheline Kosmosejaam (ISS) Eesti territooriumilt palja silmaga nähtav ning milline on selle reaalajaline trajektoor võrreldes Eesti koordinaatidega?

Rahvusvaheline Kosmosejaam (ISS) tiirleb ümber Maa kiirusega umbes 28 000 km/h ning selle koordinaadid muutuvad pidevalt. See on ideaalne andmeallikas dünaamilise andmetorustiku (data pipeline) loomiseks.

## Mõõdikud

1. Nähtavuse aken (Visibility window): Aeg, mil ISS on horisondist kõrgemal kui 10 kraadi Eesti kohal (arvutatakse ISS-i asukoha asimuudi ja elektsiooni nurga põhjal Tallinna/Tartu koordinaatide suhtes).
2. Pilvisuse indeks (Cloud cover index): Ilmaprognoosi pilvisuse protsentuaalne näitaja (0-100%) ISS-i ülelennu hetkel (kui pilvisus on > 50%, siis nähtavus on madal).
3. Reaalajaline kaugus (Current distance): Hetkeline distants (kilomeetrites) ISS-i suborbitaalse punkti ja Eesti keskpunkti vahel (arvutatakse Haversine'i valemi abil).

## Andmeallikad

| Allikas | Tüüp | Ajas muutuv? | Roll |
|---------|------|--------------|------|
| [Open Notify API](http://api.open-notify.org/iss-now.json) | ISS asukoha API | Uueneb iga 1-2 sekundi tagant (reaalajas). Meie loeme näiteks iga 10-15 minuti tagant (või tihedamalt ülelennu ajal) | Põhiandmevoog |
| [Open-Meteo API](https://api.open-meteo.com) | Ilmaandmete API | Jah, Uueneb kord tunnis (prognoos ja hetkeseis).| Täiendav andmeallikas |

## Andmevoog

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

## Andmebaasi kihid 

| Kiht | Roll |
|------|------|
| `staging` | Hoiab allika andmeid töötlemata kujul. |
| `mart` | Hoiab transformeeritud ja ärilogikat sisaldavaid tabeleid. |


## Tööjaotus
| Roll | Vastutus | Täitja |
|------|----------|--------|
| Andmeallika omanik | Kirjutab sissevõtu loogika, hoiab API-t töös | Natalja Pilipenko |
| Transformatsioonide omanik | Kirjutab mart kihi mudelid ja mõõdikute arvutuse | Natalja Pilipenko |
| Kvaliteedi omanik | Kirjutab testid ja vaatab läbi ebaõnnestunud kontrollid | Liisa Rikanson |
| Näidikulaua omanik | Ehitab näidikulaua ja seob selle äriküsimusega | Liisa Rikanson |

## Riskid

| Risk | Mõju | Maandus |
|------|------|---------|
| ISS-i kiirus | ISS lendab Eestist üle väga kiiresti (mõne minutiga) ning 15-minutise intervalliga andmete korjamisel magame ülelennu maha | Muudame skripti loogikat: tavapäraselt küsime andmeid kord tunnis, aga kui ISS jõuab Euroopa koordinaatidele, tihendame päringuid iga 10 sekundi tagant |
| Usaldusväärsus | Tasuta kosmose-API-del on päringute limiit (Rate limit) või nad on tihti maas. | Lisame koodi try-catch ploki ja salvestame viimase teadaoleva trajektoori kiiruse, et vajadusel asukohta ajutiselt interpoleerida (ennustada). |


## Privaatsus ja turve 

- Projektis kasutatakse eranditult avalikke astronoomilisi ja meteoroloogilisi andmeid. Isikuandmeid (GDPR) ei koguta ega töödelda.
- Kõik tundlikud andmed (andmebaasi paroolid, API võtmed) hoitakse kohalikus `.env` failis, mis on lisatud `.gitignore` faili ja mida GitHubi ei fanta.
- Projekti juurkaustas on loodud `.dockerignore` fail. See tagab, et `docker compose build` käsu ajal ei kopeerita kohalikku `.env` faili ega lokaalseid arendusfaile (nt `.venv`, `__pycache__`) Docker konteineri kujutise (image) sisse. See välistab tundlike andmete lekkimise konteinerist.




