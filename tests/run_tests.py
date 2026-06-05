import pandas as pd
import os

def test_andmekvaliteet():
    failitee = "data/clean_iss_data.csv"
    
    assert os.path.exists(failitee), "TEST EBAÕNNESTUS: Andmefaili ei eksisteeri!"
    df = pd.read_csv(failitee)
    assert len(df) > 0, "TEST EBAÕNNESTUS: Fail on tühi!"
    
    # TEST 1: NOT NULL kontroll (väärtused peavad olemas olema)
    assert df['iss_latitude'].notnull().all(), "TEST 1 VIGA: Laiuskraadides on tühje lahtreid!"
    assert df['elevation_deg'].notnull().all(), "TEST 1 VIGA: Elevatsiooni nurk on puudu!"
    
    # TEST 2: VÄÄRTUSTE VAHEMIK (Geograafia ja astronoomia piirid)
    assert df['iss_latitude'].between(-90, 90).all(), "TEST 2 VIGA: Laiuskraad on vigane!"
    assert df['elevation_deg'].between(-90, 90).all(), "TEST 2 VIGA: Elevatsiooninurk peab jääma -90 ja 90 kraadi vahele!"
    assert df['cloud_cover_percent'].between(0, 100).all(), "TEST 2 VIGA: Pilvisus peab olema 0-100%!"
    
    # TEST 3: ÄRILOGIKA KONTROLL (Unikaalsus ja seosed)
    # Kontrollime, et sama ajatempliga ridu ei oleks topelt (Unikaalsuse test)
    assert df['timestamp'].is_unique, "TEST 3 VIGA: Andmetes on dubleerivad ajatemplid!"
    
    print(f"KÕIK ANDMEKVALITEEDI TESTID LÄBITUD! (Edukalt kontrollitud {len(df)} rida)")

if __name__ == "__main__":
    test_andmekvaliteet()