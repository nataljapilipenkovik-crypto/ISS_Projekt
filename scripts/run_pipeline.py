import time
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

try:
    from scripts.ingest import main as run_ingest
    from scripts.transform import main as run_transform
    from tests.test_data_quality import run_data_quality_tests
except ImportError as e:
    print(f"Viga moodulite importimisel: {e}")
    sys.exit(1)

def run_pipeline():
    print("=" * 50)
    print(f"Andmevoo käivitamine: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    try:
        run_ingest()
    except Exception as e:
        print(f"!!! Viga Ingest sammus: {e}")
        return False

    try:
        run_transform()
    except Exception as e:
        print(f"!!! Viga Transform sammus: {e}")
        return False

    print("\n[SAMM 3/3] Andmekvaliteedi kontroll...")
    return run_data_quality_tests()

if __name__ == "__main__":
    # Kui käivitatakse parameetriga 'daemon', töötab skript lõputult iga 60 sekundi järel
    if len(sys.argv) > 1 and sys.argv[1] == "daemon":
        print("Andmevoog käivitatud deemonina (lõputu tsükkel)...")
        while True:
            run_pipeline()
            print("\nOotan 60 sekundit järgmise küsitluseni...\n")
            time.sleep(60)
    else:
        # Ühekordne käivitus
        run_pipeline()