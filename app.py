import streamlit as st
import pandas as pd
from conversion_rules import convert_coverflex, convert_doubleyou, load_causal_map

# Carica mappa causali (già presente nel repo)
causal_map = load_causal_map()

st.title("Convertitore file welfare")

codice_azienda = st.text_input("Codice azienda")
provider = st.radio("Provider", ("Coverflex", "DoubleYou"))
uploaded_file = st.file_uploader("Carica file CSV", type=["csv"])

if st.button("Converti"):
    if not codice_azienda:
        st.error("Inserisci il codice azienda")
    elif not uploaded_file:
        st.error("Carica un file CSV")
    else:
        try:
            # Leggi file CSV in base al provider, gestendo delimitatori e encoding
            if provider == "Coverflex":
                df_input = pd.read_csv(uploaded_file, sep=None, engine='python', encoding='utf-8')
                df_output = convert_coverflex(df_input, causal_map, codice_azienda)
            else:
                df_input = pd.read_csv(uploaded_file, sep=None, engine='python', encoding='utf-8')
                df_output = convert_doubleyou(df_input, causal_map, codice_azienda)

            # Converti DataFrame output in CSV
            csv_data = df_output.to_csv(index=False).encode('utf-8')

            # Nome file dinamico in base al provider
            file_name = f"{provider.lower()}_converted.csv"

            st.success("Conversione completata con successo!")
            st.download_button(
                label="Scarica file convertito",
                data=csv_data,
                file_name=file_name,
                mime="text/csv"
            )
        except Exception as e:
            st.error(f"❌ Errore durante la conversione: {str(e)}")
