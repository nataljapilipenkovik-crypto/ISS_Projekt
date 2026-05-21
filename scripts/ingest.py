import requests
import pandas as pd
from datetime import datetime
from pathlib import Path

# ISS API
ISS_URL = "http://api.open-notify.org/iss-now.json"

# Me loome andmekaust, kui pole veel
Path("data").mkdir(exist_ok=True)

# API-i päring
response = requests.get(ISS_URL)

# Kontrollime
if response.status_code != 200:
    raise Exception(f"API request failed: {response.status_code}")

# Saame JSON-i
data = response.json()

# Saame vajalikke andmeid
timestamp = data["timestamp"]

latitude = data["iss_position"]["latitude"]
longitude = data["iss_position"]["longitude"]

# Ajatempli teisendamine kuupäevaks
from datetime import datetime, timezone
datetime_utc = datetime.fromtimestamp(timestamp, tz=timezone.utc)

# Loome DataFrame-i
df = pd.DataFrame([{
    "timestamp": timestamp,
    "datetime_utc": datetime_utc,
    "latitude": latitude,
    "longitude": longitude
}])

# CSV fail
csv_path = "data/iss_locations.csv"

# Kui fail on juba olemas → append
try:
    existing_df = pd.read_csv(csv_path)
    df = pd.concat([existing_df, df], ignore_index=True)
except FileNotFoundError:
    pass

# Salvestame
df.to_csv(csv_path, index=False)

print("ISS data saved successfully!")
print(df.tail())