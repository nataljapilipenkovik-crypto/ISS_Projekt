import os
import requests
import pandas as pd
import numpy as np
from datetime import datetime

os.makedirs('data', exist_ok=True)

# Eesti keskpunkti koordinaadid
EE_LAT = 58.6260
EE_LON = 25.5547
ISS_ALTITUDE_KM = 420.0  # ISS-i keskmine kõrgus maapinnast

def arvuta_mõõdikud(iss_lat, iss_lon):
    # 1. Hetkeline kaugus (Haversine valem)
    R = 6371.0  # Maa raadius
    rad_lat1, rad_lon1, rad_lat2, rad_lon2 = map(np.radians, [EE_LAT, EE_LON, iss_lat, iss_lon])
    
    dlat = rad_lat2 - rad_lat1
    dlon = rad_lon2 - rad_lon1
    
    a = np.sin(dlat/2)**2 + np.cos(rad_lat1) * np.cos(rad_lat2) * np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    distants = R * c
    
    # Elevatsiooni nurk (Kõrgus horisondist kraadides)
    # Kasutame nurkkaugust (tsentraalnurk)
    alpha = distants / R
    # Trigonomeetriline lähendus elevatsiooni leidmiseks vaatleja suhtes
    nimetaja = np.sqrt(R**2 + (R + ISS_ALTITUDE_KM)**2 - 2 * R * (R + ISS_ALTITUDE_KM) * np.cos(alpha))
    if nimetaja == 0:
        elevatsioon = 90.0
    else:
        sin_elev = ((R + ISS_ALTITUDE_KM) * np.cos(alpha) - R) / nimetaja
        # Piirame vahemikku, et vältida ümardusvigu
        sin_elev = max(-1.0, min(1.0, sin_elev))
        elevatsioon = np.degrees(np.arcsin(sin_elev))
        
    # Asimuut (Suund kraadides: 0 = Põhi, 90 = Ida, 180 = Lõuna, 270 = Lääs)
    x = np.sin(dlon) * np.cos(rad_lat2)
    y = np.cos(rad_lat1) * np.sin(rad_lat2) - np.sin(rad_lat1) * np.cos(rad_lat2) * np.cos(dlon)
    asimuut = (np.degrees(np.arctan2(x, y)) + 360) % 360

    return round(distants, 2), round(elevatsioon, 1), round(asimuut, 1)

print(f"[{datetime.now().strftime('%H:%M:%S')}] Päritakse API andmeid...")

try:
    # Küsime ISS asukoha
    iss_res = requests.get("http://api.open-notify.org/iss-now.json", timeout=10).json()
    iss_lat = float(iss_res["iss_position"]["latitude"])
    iss_lon = float(iss_res["iss_position"]["longitude"])
    
    # Küsime pilvisuse Eesti keskpunktis
    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={EE_LAT}&longitude={EE_LON}&current=cloud_cover"
    weather_res = requests.get(weather_url, timeout=10).json()
    pilvisus = float(weather_res["current"]["cloud_cover"])
    
    # Arvutame astronoomilised mõõdikud
    distants, elevatsioon, asimuut = arvuta_mõõdikud(iss_lat, iss_lon)
    
    # Ärilogika: Nähtavuse akna hindamine
    if elevatsioon > 10 and pilvisus <= 50:
        indeks = "KÕRGE (ISS on nähtav!)"
    elif elevatsioon > 0 and pilvisus <= 50:
        indeks = "MADAL (Horisondi taga / madalal)"
    else:
        indeks = "EI OLE NÄHTAV (Pilves või liiga kaugel)"
        
    uus_rida = {
        "timestamp": datetime.fromtimestamp(iss_res["timestamp"]).strftime('%Y-%m-%d %H:%M:%S'),
        "iss_latitude": iss_lat,
        "iss_longitude": iss_lon,
        "distance_km": distants,
        "elevation_deg": elevatsioon,
        "azimuth_deg": asimuut,
        "cloud_cover_percent": pilvisus,
        "visibility_index": indeks
    }
    
    df_uus = pd.DataFrame([uus_rida])
    failitee = "data/clean_iss_data.csv"
    
    if os.path.exists(failitee):
        df_uus.to_csv(failitee, mode='a', header=False, index=False)
    else:
        df_uus.to_csv(failitee, mode='w', header=True, index=False)
        
    print(f"Andmed salvestatud! Distants: {distants} km, Elevatsioon: {elevatsioon}°, Pilvisus: {pilvisus}%, Otsus: {indeks}")

except Exception as e:
    print(f"Viga andmevoos: {e}")