# 1. Kasutame ametlikku kergat Pythoni baaskujutist
FROM python:3.11-slim

# 2. Paigaldame süsteemsed tööriistad, mida võib vaja minna teekide ehitamiseks
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

# 3. Määrame töökataloogi konteineri sees
WORKDIR /app

# 4. Kopeerime sõltuvuste faili töökataloogi
COPY requirements.txt .

# 5. Uuendame pip-i ja paigaldame kõik vajalikud Pythoni teegid
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 6. Kopeerime kogu ülejäänud projekti koodi konteinerisse
COPY . .

# 7. Avaneme pordi 8501, mida Streamlit vaikimisi kasutab
EXPOSE 8501

# 8. Seadistame konteineri tervisekontrolli (Healthcheck)
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# 9. Käsk Streamlit rakenduse käivitamiseks
# Lipud keelavad CORS-i tõrked, üleliigsed teavitused ja seovad rakenduse pordiga
CMD ["streamlit", "run", "app/app.py", "--server.port=8501", "--server.address=0.0.0.0"]