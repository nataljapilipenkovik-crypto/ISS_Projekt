import streamlit as st
import pandas as pd
import os

st.title("ISS-i kosmoserakenduse minimaalne töövoog")

failitee = "data/raw_iss.csv"

if not os.path.exists(failitee):
    st.info("Andmefaili veel pole. Käivita esmalt terminalis sissevõtu skript!")
else:
    # 1. Transformatsioon: Loeme toorandmed sisse
    df = pd.read_csv(failitee)
    
    # Teeme tüübiteisendused (igaks juhuks, et Streamlit ei kurdaks)
    df['latitude'] = pd.to_numeric(df['latitude'])
    df['longitude'] = pd.to_numeric(df['longitude'])
    
    # Kuvame lihtsa KPI (Mitu punkti meil andmebaasis on)
    st.metric(label="Kogutud asukohapunkte kokku", value=len(df))
    
    st.subheader("ISS-i viimased teadaolevad asukohad kaardil")
    
    # 2. Visuaal: Streamliti sisseehitatud kaart, mis ootab 'latitude' ja 'longitude' tulpasid
    st.map(df[['latitude', 'longitude']])
    
    # Kuvame ka tabeli, et näha toorandmeid
    st.subheader("Andmete eelvaade (Toorkiht)")
    st.dataframe(df.tail(5))
