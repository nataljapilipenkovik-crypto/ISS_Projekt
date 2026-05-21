import time
import sys
from pathlib import Path

# Lisame projektikausta süsteemi teekonda, et moodulid korrektselt importida
sys.path.append(str(Path(__file__).parent.parent))

# Impordime meie sammud
try:
    from scripts.ingest import main as run_ingest
    from scripts.transform import main as run_transform
except ImportError as e:
    print(f"Viga moodulite importimisel: {e}")
    print("Veenduge, et käivitate skripti projekti juurkaustast: python3 scripts/run_pipeline.py")
    sys.exit(1)

def run_pipeline():
    """Käivitab kogu andmetöötluse ahela (Pipeline)"""
    print("=" * 50)
    print(f"Andmevoo käivitamine: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    # 1. SAMM: Andmete sissevõtt (Ingest)
    start_time = time.time()
    print("\n[SAMM 1/2] ISS-i ja ilmaandmete pärimine (Ingest)...")
    try:
        run_ingest()
        print(f"-> Samm 1 edukalt lõpetatud! Aeg: {time.time() - start_time:.2f} sekundit.")
    except Exception as e:
        print(f"!!! Viga 1. sammus (Ingest) ebaõnnestus: {e}")
        return False

    # 2. SAMM: Andmete transformatsioon (Transform)
    start_time = time.time()
    print("\n[SAMM 2/2] Andmete puhastamine ja töötlemine (Transform)...")
    try:
        run_transform()
        print(f"-> Samm 2 edukalt lõpetatud! Aeg: {time.time() - start_time:.2f} sekundit.")
    except Exception as e:
        print(f"!!! Viga 2. sammus (Transform) ebaõnnestus: {e}")
        return False

    print("\n" + "=" * 50)
    print("Kogu andmevoog (Pipeline) on edukalt läbitud!")
    print("=" * 50)
    return True

if __name__ == "__main__":
    # Kontrollime käsurea argumente (vastavalt dokis olevale `run-all` nõudele)
    if len(sys.argv) > 1 and sys.argv[1] == "run-all":
        run_pipeline()
    else:
        # Kui argumenti ei antud, käivitame vaikeväärtusena ikkagi kogu ahela
        run_pipeline()