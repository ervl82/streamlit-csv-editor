import streamlit as st
import pandas as pd
from conversion_rules import convert_coverflex, convert_doubleyou
import os

# Carica la mappa causali già presente in locale
MAPPACOL_PATH = "mappa_causali.csv"

@st.cache_data
def load_mappa_causali():
    try:
        df = pd.read_csv(MAPPACOL_PATH)
        return df
    except Exception as e:
        st.error(f"Errore nel caricamento della mappa causali: {e}")
        return None

def main():
    st.title("Convertitore File Welfare Aziendale")

    codice_azienda = st.text_input("Codice azienda")
    provider = st.radio("Provider", ("Coverflex", "DoubleYou"))
    uploaded_file = st.file_uploader("Carica file CSV da convertire", type=['csv'])

    if uploaded_file and codice_azienda:
        mappa_causali_df = load_mappa_causali()
        if mappa_causali_df is None:
            st.stop()

        try:
            if provider == 'Coverflex':
                # Auto detect separator, uso engine python per flessibilità
                df = pd.read_csv(uploaded_file, sep=None, engine='python', encoding='utf-8')
                result = convert_coverflex(df, codice_azienda, mappa_causali_df)
            else:
                # DoubleYou usa separatore punto e virgola
                df = pd.read_csv(uploaded_file, sep=';', engine='python', encoding='utf-8')
                result = convert_doubleyou(df, codice_azienda, mappa_causali_df)

            st.success("Conversione completata!")

            csv = result.to_csv(index=False, sep=';', encoding='utf-8')
            st.download_button(
                label="Scarica file convertito",
                data=csv,
                file_name=f"{provider}_convertito_{codice_azienda}.csv",
                mime='text/csv'
            )
        except Exception as e:
            st.error(f"❌ Errore durante la conversione: {e}")

if __name__ == "__main__":
    main()
