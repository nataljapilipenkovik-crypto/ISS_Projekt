import streamlit as st
import pandas as pd
from pathlib import Path

# Seadistame lehe pealkirja ja ikooni
st.set_page_config(page_title="ISS Eesti Jälgija", layout="wide")

st.title("ISS-i trajektoor ja nähtavus Eesti kontekstis")
st.markdown("See näidikutelaud kuvab Rahvusvahelise Kosmosejaama (ISS) asukohta ja hindab selle nähtavust Eestis.")

clean_path = "data/clean_iss_weather.csv"

# Kontrollime, kas andmefail on olemas
if not Path(clean_path).exists():
    st.error(f"Andmefaili ({clean_path}) ei leitud! Palun käivitage esmalt andmevoog (pipeline).")
else:
    # Loeme puhastatud andmed
    df = pd.read_csv(clean_path)
    
    if df.empty:
        st.warning("Andmefail on tühi. Oodake uute andmete saabumist.")
    else:
        # Võtame viimase punkti andmed (reaalajas seis)
        latest_data = df.iloc[-1]
        
        # --- METRIKATUUR (KPI-d) ---
        st.subheader(" Viimased andmed reaalajas")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(label="Aeg (UTC)", value=latest_data["datetime_utc"])
        with col2:
            st.metric(label="ISS Laiuskraad", value=f"{latest_data['iss_latitude']:.4f}°")
        with col3:
            st.metric(label="ISS Pikkuskraad", value=f"{latest_data['iss_longitude']:.4f}°")
        with col4:
            st.metric(label="Pilvisus Eestis (Tallinn)", value=f"{latest_data['estonia_cloud_cover']}%")

        st.divider()

        # --- ÄRILOOGIKA JA HOIATUSED ---
        st.subheader("Nähtavuse staatus Eestis")
        
        # Kontrollime, kas viimases punktis on ISS Eesti kohal
        if latest_data["is_over_estonia"]:
            st.success("TÄHELEPANU! ISS lendab praegu EESTI KOHAL!")
            
            # Hindame nähtavuse kvaliteeti
            vis_quality = latest_data["visibility_quality"]
            st.metric(label="Nähtavuse kvaliteet", value=f"{vis_quality}%")
            
            if vis_quality > 70:
                st.info(" Taevas on selge! ISS peaks olema silmaga hästi nähtav (kui on pime aeg).")
            elif vis_quality > 30:
                st.warning("⛅ Taevas on vahelduv pilvisus. Nähtavus on piiratud.")
            else:
                st.error("🌧 Taevas on täielikult pilves. ISS-i ei ole võimalik näha.")
        else:
            st.info(" ISS ei ole praegu Eesti kohal. Jaam tiirleb mujal maailmas.")

        st.divider()

        # --- KAART ---
        st.subheader("ISS-i asukoha kaart")
        st.markdown("Kaart näitab viimast teadaolevat ISS-i asukohta maailmas.")
        
        # Streamlit vajab kaardi jaoks DataFrame'i, kus on veerud 'latitude' ja 'longitude'
        map_data = pd.DataFrame([{
            'latitude': latest_data['iss_latitude'],
            'longitude': latest_data['iss_longitude']
        }])
        
        # Kuvame kaardi (zoomituna globaalseks vaateks)
        st.map(map_data, size=20, zoom=1)

        st.divider()

        # --- ANDMETABEL ---
        st.subheader("Viimased salvestatud logid (Ajalugu)")
        # Kuvame tabelina viimased 10 rida, sorteerituna uuemad eespool
        st.dataframe(df.tail(10).sort_index(ascending=False), use_container_width=True)