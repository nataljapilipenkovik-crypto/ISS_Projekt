import pandas as pd
from pathlib import Path

# Eesti geograafilised piirid (Bounding Box)
EST_LAT_MIN = 57.51
EST_LAT_MAX = 59.82
EST_LON_MIN = 21.77
EST_LON_MAX = 28.21

def is_over_estonia(lat, lon):
    """Kontrollib, kas ISS on Eesti kohal"""
    return EST_LAT_MIN <= lat <= EST_LAT_MAX and EST_LON_MIN <= lon <= EST_LON_MAX

def calculate_visibility_quality(cloud_cover):
    """Arvutab nähtavuse kvaliteedi protsentides (mida vähem pilvi, seda parem)"""
    return 100 - cloud_cover

def main():
    raw_path = "data/raw_iss_weather.csv"
    clean_path = "data/clean_iss_weather.csv"
    
    if not Path(raw_path).exists():
        print("Viga: Lähteandmete faili (raw_iss_weather.csv) ei leitud!")
        return
        
    # Loeme toorandmed
    df_raw = pd.read_csv(raw_path)
    
    # Kui fail on tühi, lõpetame töö
    if df_raw.empty:
        print("Hoiatus: Lähteandmete fail on tühi.")
        return
        
    # Teeme andmete transformatsiooni
    df_clean = df_raw.copy()
    
    # 1. Lisame filtri: kas on Eesti kohal (True/False)
    df_clean['is_over_estonia'] = df_clean.apply(
        lambda row: is_over_estonia(row['iss_latitude'], row['iss_longitude']), axis=1
    )
    
    # 2. Arvutame nähtavuse kvaliteedi
    df_clean['visibility_quality'] = df_clean['estonia_cloud_cover'].apply(calculate_visibility_quality)
    
    # Salvestame puhastatud andmed
    df_clean.to_csv(clean_path, index=False)
    
    print("Andmete transformatsioon edukalt lõpetatud!")
    print(f"Salvestatud faili: {clean_path}")
    print(df_clean.tail(2).to_string(index=False))

if __name__ == "__main__":
    main()