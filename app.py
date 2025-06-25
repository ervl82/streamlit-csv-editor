import streamlit as st
import pandas as pd
from conversion_rules import convert_file

st.title("Convertitore File Welfare")

codice_azienda = st.text_input("Codice azienda:")
provider = st.radio("Provider:", ('Coverflex', 'DoubleYou'))

uploaded_file = st.file_uploader("Carica il file CSV da convertire", type=["csv"])

if st.button("Converti"):
    if not codice_azienda:
        st.error("Inserisci il codice azienda.")
    elif not uploaded_file:
        st.error("Carica un file CSV.")
    else:
        try:
            # Leggo file con separatore corretto e gestione encoding
            if provider == 'Coverflex':
                df = pd.read_csv(uploaded_file, sep=None, engine='python', encoding='utf-8')
            elif provider == 'DoubleYou':
                # DoubleYou usa spesso punto e virgola come separatore
                df = pd.read_csv(uploaded_file, sep=';', encoding='utf-8')
            else:
                st.error("Provider non supportato")
                st.stop()

            converted_df = convert_file(df, codice_azienda, provider)
            
            # Mostra anteprima
            st.write("Anteprima file convertito:")
            st.dataframe(converted_df.head())

            # Prepara file per download
            csv = converted_df.to_csv(index=False, sep=';')
            st.download_button(
                label="Scarica file convertito",
                data=csv,
                file_name=f"welfare_convertito_{provider}.csv",
                mime='text/csv'
            )
        except Exception as e:
            st.error(f"❌ Errore durante la conversione: {str(e)}")
