import requests
import pandas as pd
from datetime import datetime, timezone
from pathlib import Path

# API URL-id
ISS_URL = "http://api.open-notify.org/iss-now.json"
# Küsime jooksvat pilvisust (cloud_cover) Eesti kohta (Tallinn)
WEATHER_URL = "https://api.open-meteo.com/v1/forecast?latitude=59.437&longitude=24.753&current=cloud_cover&timezone=auto"

def fetch_iss_data():
    """ISS-i koordinaatide pärimine API-st"""
    response = requests.get(ISS_URL)
    if response.status_code != 200:
        raise Exception(f"ISS API päring ebaõnnestus: {response.status_code}")
    data = response.json()
    return {
        "timestamp": data["timestamp"],
        "iss_latitude": float(data["iss_position"]["latitude"]),
        "iss_longitude": float(data["iss_position"]["longitude"])
    }

def fetch_weather_data():
    """Ilmaandmete (pilvisuse) pärimine Eesti kohta"""
    response = requests.get(WEATHER_URL)
    if response.status_code != 200:
        raise Exception(f"Ilma API päring ebaõnnestus: {response.status_code}")
    data = response.json()
    return {
        "estonia_cloud_cover": data["current"]["cloud_cover"]  # Pilvisus protsentides
    }

def main():
    # Loome andmete kausta (data), kui seda veel pole
    Path("data").mkdir(exist_ok=True)
    
    try:
        # Kogume andmed mõlemast allikast
        iss = fetch_iss_data()
        weather = fetch_weather_data()
        
        # Ühendame andmed üheks sõnastikuks
        combined_data = {
            "timestamp": iss["timestamp"],
            "datetime_utc": datetime.fromtimestamp(iss["timestamp"], tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S'),
            "iss_latitude": iss["iss_latitude"],
            "iss_longitude": iss["iss_longitude"],
            "estonia_cloud_cover": weather["estonia_cloud_cover"]
        }
        
        # Loome DataFrame'i
        df = pd.DataFrame([combined_data])
        csv_path = "data/raw_iss_weather.csv"
        
        # Kui fail on olemas -> lisame rea juurde (append), kui mitte -> loome uue faili
        if Path(csv_path).exists():
            df.to_csv(csv_path, mode='a', header=False, index=False)
        else:
            df.to_csv(csv_path, index=False)
            
        print("ISS-i ja ilmaandmed edukalt salvestatud!")
        print(df.to_string(index=False))
        
    except Exception as e:
        print(f"Viga andmevoo käivitamisel: {e}")

if __name__ == "__main__":
    main()