import requests
import json

print("Teeme esimese katse ISS API-ga...")
iss_response = requests.get("http://api.open-notify.org/iss-now.json")

if iss_response.status_code == 200:
    data = iss_response.json()
    print("API ühendus toimib! ISS asukoht praegu:")
    print(f"Laiuskraad: {data['iss_position']['latitude']}")
    print(f"Pikkuskraad: {data['iss_position']['longitude']}")
else:
    print("Viga ISS API-st andmete saamisel.")