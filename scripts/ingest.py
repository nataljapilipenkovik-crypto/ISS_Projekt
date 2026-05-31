import os
import requests
import pandas as pd
from datetime import datetime

# Loome andmete jaoks kausta, kui seda veel pole
os.makedirs('data', exist_ok=True)

url = "http://api.open-notify.org/iss-now.json"
print("Küsitakse andmeid ISS API-st...")

try:
    response = requests.get(url, timeout=10)
    if response.status_code == 200:
        data = response.json()
        
        # Kokkulepitud andmete struktuur!
        uus_rida = {
            "timestamp": datetime.fromtimestamp(data["timestamp"]).strftime('%Y-%m-%d %H:%M:%S'),
            "latitude": float(data["iss_position"]["latitude"]),
            "longitude": float(data["iss_position"]["longitude"])
        }
        
        df_uus = pd.DataFrame([uus_rida])
        failitee = "data/raw_iss.csv"
        
        # Idempotentne sissevõtt: lisab ridu juurde (append)
        if os.path.exists(failitee):
            df_uus.to_csv(failitee, mode='a', header=False, index=False)
        else:
            df_uus.to_csv(failitee, mode='w', header=True, index=False)
            
        print(f"Asukoht salvestatud faili {failitee}!")
    else:
        print(f"API viga, staatus: {response.status_code}")
except Exception as e:
    print(f"Viga sissevõtul: {e}")