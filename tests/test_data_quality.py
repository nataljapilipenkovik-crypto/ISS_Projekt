import pandas as pd
import time
from pathlib import Path

def run_data_quality_tests():
    """Käivitab andmekvaliteedi kontrollid puhastatud andmetele"""
    clean_path = "data/clean_iss_weather.csv"
    
    print("=" * 50)
    print("ANDMEKVALITEEDI TESTIDE KÄIVITAMINE")
    print("=" * 50)
    
    if not Path(clean_path).exists():
        print(f"Viga: Faili {clean_path} ei leitud. Teste ei saa käivitada.")
        return False
        
    df = pd.read_csv(clean_path)
    
    if df.empty:
        print("Hoiatus: Andmefail on tühi, teste pole millegi peal jooksu lasta.")
        return False
        
    errors = 0
    current_time = int(time.time())
    
    # TEST 1: ISS koordinaadid ei ole tühjad (Not Null)
    null_lat = df['iss_latitude'].isnull().sum()
    null_lon = df['iss_longitude'].isnull().sum()
    if null_lat == 0 and null_lon == 0:
        print("[PASSED] Test 1: ISS koordinaadid ei sisalda tühje väärtusi.")
    else:
        print(f"[FAILED] Test 1: Leiti tühje väärtusi! Laiuskraad: {null_lat}, Pikkuskraad: {null_lon}")
        errors += 1
        
    # TEST 2: Laius- ja pikkuskraadid jäävad lubatud vahemikku
    invalid_lat = df[(df['iss_latitude'] < -90) | (df['iss_latitude'] > 90)]
    invalid_lon = df[(df['iss_longitude'] < -180) | (df['iss_longitude'] > 180)]
    
    if invalid_lat.empty and invalid_lon.empty:
        print("[PASSED] Test 2: Laius- ja pikkuskraadid on lubatud vahemikus.")
    else:
        print(f"[FAILED] Test 2: Koordinaadid on vigased väljaspool piire (-90/90 või -180/180)!")
        errors += 1
        
    # TEST 3: Ajatempli väärtused ei ole tulevikus
    future_timestamps = df[df['timestamp'] > current_time]
    if future_timestamps.empty:
        print("[PASSED] Test 3: Ajatemplid on korrektsed ega asu tulevikus.")
    else:
        print(f"[FAILED] Test 3: Leiti {len(future_timestamps)} rida ajatempliga tulevikus!")
        errors += 1

    # Kokkuvõte
    print("-" * 50)
    if errors == 0:
        print("KÕIK TESTID LÄBITUD EDUKALT! Andmed on puhtad.")
        print("-" * 50)
        return True
    else:
        print(f"TESTID EBAÕNNESTUSID! Leiti {errors} kriitilist viga.")
        print("-" * 50)
        return False

if __name__ == "__main__":
    run_data_quality_tests()