import streamlit as st
import pandas as pd
from conversion_rules import convert_coverflex, convert_doubleyou

@st.cache_data
def load_mappa_causali():
    return pd.read_csv('mappa_causali.csv')

def main():
    st.title("Convertitore file welfare")

    codice_azienda = st.text_input("Codice azienda:")
    provider = st.radio("Provider:", ('Coverflex', 'DoubleYou'))
    file = st.file_uploader("Carica il file CSV di origine", type=['csv'])

    mappa_causali_df = load_mappa_causali()

    if st.button("Converti"):
        if not codice_azienda:
            st.error("Inserisci il codice azienda")
            return
        if not file:
            st.error("Carica un file CSV")
            return

        try:
            # Per Coverflex: carica con sep='\t' o sep=';' o prova sep=',', se serve
            if provider == 'Coverflex':
                df = pd.read_csv(file, sep=None, engine='python')
                result = convert_coverflex(df, codice_azienda, mappa_causali_df)
            else:
                df = pd.read_csv(file, sep=None, engine='python')
                result = convert_doubleyou(df, codice_azienda, mappa_causali_df)

            st.success("Conversione completata!")
            st.download_button(
                label="Scarica file convertito",
                data=result.to_csv(index=False).encode('utf-8'),
                file_name=f'output_{provider}_{codice_azienda}.csv',
                mime='text/csv'
            )
        except Exception as e:
            st.error(f"❌ Errore durante la conversione: {e}")

if __name__ == '__main__':
    main()
