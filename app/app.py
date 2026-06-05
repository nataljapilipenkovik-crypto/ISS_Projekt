import os
import pandas as pd
import streamlit as st

st.set_page_config(page_title="ISS Kosmoserakendus", layout="wide")

st.title("ISS-i reaalaja andmetorustik ja nähtavuse prognoos")
st.markdown(
    "Rakendus vastab küsimusele: *Millal ja milliste tingimustega on "
    "Rahvusvaheline Kosmosejaam (ISS) Eesti kohal nähtav?*"
)

failitee = "data/clean_iss_data.csv"

if not os.path.exists(failitee):
    st.warning("Andmefaili veel pole! Käivita esmalt: `python scripts/ingest.py`")
else:
    df = pd.read_csv(failitee)

    if df.empty:
        st.info("Andmefail on tühi.")
    else:
        df = df.sort_values(by="timestamp", ascending=False)
        viimane_kirje = df.iloc[0]

        st.subheader("Hetkeseis ja põhimõõdikud")
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)

        with kpi1:
            st.metric("Viimane mõõtmisaeg", str(viimane_kirje["timestamp"]))
        with kpi2:
            st.metric("Kaugus Eesti keskpunktist", f"{viimane_kirje['distance_km']} km")
        with kpi3:
            st.metric(
                "Elevatsiooni nurk",
                f"{viimane_kirje['elevation_deg']}°",
                help="ISS on horisondist kõrgemal, kui nurk on üle 10°."
            )
        with kpi4:
            st.metric("Pilvisus Eestis", f"{int(viimane_kirje['cloud_cover_percent'])}%")

        st.markdown("### Otsus ja nähtavus")
        indeks = str(viimane_kirje["visibility_index"])

        if "KÕRGE" in indeks:
            st.success(indeks)
        elif "MADAL" in indeks:
            st.info(indeks)
        else:
            st.error(indeks)

        st.divider()

        tab1, tab2, tab3 = st.tabs(
            ["ISS trajektoori kaart", "Distantsi dünaamika", "Andmetabel"]
        )

        with tab1:
            st.subheader("ISS-i viimased asukohad kaardil")
            map_df = df[["iss_latitude", "iss_longitude"]].rename(
                columns={"iss_latitude": "latitude", "iss_longitude": "longitude"}
            )
            st.map(map_df)
            st.caption("Kaardil on kuvatud kõik kogutud ISS-i asukohapunktid.")

        with tab2:
            st.subheader("ISS-i kaugus Eestist ajas")
            st.line_chart(df.set_index("timestamp")["distance_km"])
            st.caption("Graafik näitab, kas ISS liigub Eesti suhtes lähemale või kaugemale.")

        with tab3:
            st.subheader("Kogutud andmete ajalugu")
            st.dataframe(df, use_container_width=True)