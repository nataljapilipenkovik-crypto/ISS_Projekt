## [21. mai 2025] - Projekti hoidla seadistamine ja koostöö planeerimine

**Tehtud tööd:**
- Loodud avalik repositoorium `ISS_Projekt` ja selle baasstruktuur (`app/`, `data/`, `docs/`, `scripts/`, `tests/`).
- Lisatud andmete kogumise, transformatsiooni ja testide skriptid (`ingest.py`, `transform.py`, `run_pipeline.py`, `test_data_quality.py`).
- Seadistatud interaktiivne Streamlit veebirakendus (`app.py`).
- Projekt pakendatud Dockerisse (`Dockerfile`, `.dockerignore`, `docker-compose.yml`).

**Oluline info meeskonnale:**
- **Koodi muutmiseks (git push):** Saada mulle oma **GitHubi kasutajanimi (username)**. Lisand sind kaasautoriks (*Collaborator*), misjärel pead oma e-mailil või GitHubis kutse vastu võtma.
- **Käivitamine:** Salvesta kood, ava terminal projekti kaustas ja käivita: `docker compose up -d --build`. Rakendus avaneb aadressil `http://localhost:8501`.
- **Töö lõpetamine:** Enne VS Code sulgemist salvesta failid (`Cmd+S` / `Ctrl+S`), peata terminalis protsessid (`Ctrl+C`) ja saada muudatused GitHubi käsuga:
  `git add . && git commit -m "update" && git push origin main`