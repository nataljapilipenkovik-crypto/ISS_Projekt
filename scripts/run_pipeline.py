import time
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

try:
    from scripts.ingest import main as run_ingest
    from scripts.transform import main as run_transform
    from tests.test_data_quality import run_data_quality_tests  # UUS IMPORT
except ImportError as e:
    print(f"Viga moodulite importimisel: {e}")
    sys.exit(1)

def run_pipeline():
    print("=" * 50)
    print(f"Andmevoo käivitamine: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    # 1. SAMM: Ingest
    try:
        run_ingest()
    except Exception as e:
        print(f"!!! Viga Ingest sammus: {e}")
        return False

    # 2. SAMM: Transform
    try:
        run_transform()
    except Exception as e:
        print(f"!!! Viga Transform sammus: {e}")
        return False

    # 3. SAMM: Data Quality Tests (UUS SAMM)
    print("\n[SAMM 3/3] Andmekvaliteedi kontroll (Data Quality Tests)...")
    tests_passed = run_data_quality_tests()
    
    if not tests_passed:
        print("!!! Torujuhe katkestati: Andmed ei läbinud kvaliteedikontrolli!")
        return False

    print("\n" + "=" * 50)
    print("Kogu andmevoog koos testidega on edukalt läbitud!")
    print("=" * 50)
    return True

if __name__ == "__main__":
    run_pipeline()