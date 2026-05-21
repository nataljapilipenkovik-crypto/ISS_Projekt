##Projekti progress ja struktuuri ülevaade
Kuupäev: 21. mai 2025

Tegevus: Projekti repositooriumi loomine, baasarhitektuuri seadistamine ja failide rollide kaardistamine.

Projekti hoidla nimega ISS_Projekt on loodud avalikuna (Public) ning on jagatud loogilisteks kaustadeks ja konfiguratsioonifailideks. Pärast saame iga gruppiosalejale anda luba muudatuste tegemiseks. Allpool on toodud iga komponendi täpne kirjeldus ja eesmärk.
Kataloogide struktuur (Kaustad)
1. app/
Sisaldab kasutusliidese koodi.

Siin asub fail app.py, mis käivitab Streamlit veebirakenduse (näidikutelaua). See loeb puhastatud andmeid kaustast data/ ning kuvab kasutajale interaktiivse kaardi ISS-i asukohaga, reaalajas ilmainfo ja nähtavuse hinnangu Eesti kontekstis.
2. data/
Andmehoidla

Siia tekivad automaatselt programmi töö käigus kaks CSV-faili:

raw_iss_weather.csv – töötlemata (toored) andmed otse API-dest.

clean_iss_weather.csv – puhastatud andmed, mis on läbinud transformatsiooni ja kontrolli.
3. docs/
Projekti dokumentatsioon.

Siin asub arhitektuur.md, mis on koostatud vastavalt õpetaja antud mudelile. See kirjeldab äriküsimust, mõõdikuid ja andmevoogu. Märkus meeskonnale: seda faili saab ja tuleb jooksvalt täiendada, kui projekt areneb.
4. scripts/
Siin asub projekti "mootor" ehk andmetöötluse ahel (Data Pipeline). 
Skriptid on omavahel tihedalt seotud ja töötavad järgmises jadas:
ingest.py (Sissevõtt) – teeb päringu ISS API-sse (koordinaadid) ja Open-Meteo API-sse (Tallinna pilvisus) ning liidab need toorandmeteks.
transform.py (Transformatsioon) – võtab toorandmed, kontrollib geograafiliste piiride (Bounding Box) abil, kas ISS on Eesti kohal, ning arvutab pilvisuse põhjal nähtavuse kvaliteedi (100% miinus pilvisus).
run_pipeline.py (Orkestreerija) – Peamine juhtskript. See seob kogu ahela kokku. Dockeris käivitades töötab see deemonina (lõputus tsüklis), käivitades automaatselt iga 60 sekundi järel failid ingest.py $\rightarrow$ transform.py $\rightarrow$ andmekvaliteedi testid.
5. tests/
Andmete kvaliteedi tagamine (Data Quality Gateway).

Fail test_data_quality.py. 
See testib automaatselt puhastatud andmefaili enne, kui Streamlit seda kuvada lubab. Testitakse kolme kriitilist reeglit:

1. Ega ISS-i koordinaadid pole tühjad (NaN).
2. Kas laius- ja pikkuskraadid on reaalses vahemikus ($-90$ kuni $+90$ / $-180$ kuni $+180$).
3. Ega ajatempel (timestamp) ei näita tulevikku.

Konfiguratsioonifailid ja nende eesmärk

Dockerfile Retsept Docker-kujutise (image) ehitamiseks. See määrab, et konteineris peab olema Python 3.11, paigaldab vajalikud teegid ja seadistab käsu Streamlit-i käivitamiseks pordil 8501.

docker-compose.yml Orkestreerimisfail, mis seob kokku kaks teenust: dashboard (Streamlit veebileht) ja pipeline (andmekoguja). See loob nende vahele ühise virtuaalse andmruumi (Docker Volume), et mõlemad konteinerid näeksid sama kausta data/ reaalajas.

.gitignore ja .dockerignore – Miks on vaja kahte erinevat ignoreerimise faili?

.gitignore suhtleb Git-iga (GitHubiga). See tagab, et me ei laeks internetti üles kohalikku prügi (näiteks Maci .DS_Store faile, Pythoni vahemälu __pycache__ või salajasi paroole failist .env).

.dockerignore suhtleb Dockeriga. Kui me ehitame konteinerit, siis me ei taha, its konteineri sisse kopeeritaks rasket Giti ajalugu (.git kaust) või kohapeal arvutis testitud vanu CSV-faile. Konteiner peab alustama puhtalt lehelt ja koguma oma andmeid ise. Seetõttu hoiab see fail Docker-kujutise kerge ja kiirena.

.env.example Näidisfail keskkonnamuutujate jaoks. Siia ei kirjutata päris paroole, vaid ainult struktuur (näiteks DB_PASSWORD=kirjuta_siia_oma_parool). Päris paroolid kirjutab iga meeskonnaliige oma privaatsesse .env faili, mida GitHubi ei lasta.

requirements.txt Nimekiri kõikidest Pythoni teekidest (pandas, requests, streamlit), mida projekt vajab. Docker kasutab seda faili teekide automaatseks paigalduseks.

LICENCE Kuna repositoorium on avalik (Public), lisati vaikimisi litsents, mis määrab, kuidas teised inimesed tohivad meie koodi kasutada ja jagada.

README.md Projekti esileht GitHubis. Hetkel on olemas baasstruktuur, kuid seda täiendame ja lihvime koos meeskonnaga projekti edasises faasis.

Juhend meeskonnale: Kuidas projekti VS Code-is avada ja käivitada
Selleks, et projekt sinu arvutis tööle hakkaks, tee läbi järgmised sammud terminalis (veendu, et Docker Desktop on taustal käivitatud):

## 1. Klooni repositoorium oma arvutisse
git clone <meie-repo-url>
cd ISS_Projekt

## 2. Loo näidise põhjal oma privaatne seadete fail (kui vajalik)
cp .env.example .env

## 3. Käivita kogu süsteem (nii andmekoguja kui ka veebileht) Dockeris
docker compose up -d --build

Pärast seda avaneb Streamlit näidikutelaud sinu veebibrauseris aadressil: http://localhost:8501

Järgmised sammud meeskonnale:

Vaadata üle docs/arhitektuur.md ja arutada läbi mõõdikute täpsused.

Täita ühiselt README.md faili kirjeldused.

Oluline märkus: Kuna repositoorium asub minu kontol, on see hetkel vaikimisi seadistatud nii, et teised saavad koodi ainult lugeda (Read-only). Selleks, et te saaksite koodi muuta ja oma uuendusi otse GitHubi üles laadida (git push), pean ma teid lisama projekti kaasautoriteks (Collaborators).
Palun saatke mulle oma GitHubi kasutajanimi (username) või e-maili aadress, mis on seotud teie GitHubi kontoga.
Mina lisan teid GitHubi seadetest (Settings $\rightarrow$ Collaborators $\rightarrow$ Add people).
Te saate oma e-mailile või GitHubi teavitustesse kutse – see tuleb kindlasti vastu võtta, muidu Git blokeerib teie üleslaadimise katsed!
Kuni te pole kutset vastu võtnud, saate koodi oma arvutis jooksutada, kuid ei saa muudatusi ühisesse hoidlasse saata.

Kuidas failid nüüd kiiresti GitHubis värskendada?
Kuna muutsid faili docs/progress.md, kasuta meie kiiret liitkäsku terminalis, et kõik korraga GitHubi saata:

Bash
git add . && git commit -m "docs: täiendatud meeskonna õiguste juhend progress.md-s" && git push origin main

Mina kasutasin VS ja Dockeri.
