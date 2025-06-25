import streamlit as st
import pandas as pd
from io import BytesIO
from conversion_rules import convert_coverflex, convert_doubleyou
import os

# Carica la mappa causali fissa (assicurati che il file sia nella stessa cartella o correggi il path)
MAPPAC_PATH = os.path.join(os.path.dirname(__file__), "mappa_causali.csv")
mappa_causali_df = pd.read_csv(MAPPAC_PATH)

st.title("📄 Convertitore file provider Welfare")

with st.form("conversione_form"):
    codice_azienda = st.text_input("Codice azienda")
    provider = st.radio("Seleziona provider", ["Coverflex", "DoubleYou"])
    uploaded_file = st.file_uploader("Carica file CSV da convertire", type=["csv"])
    submitted = st.form_submit_button("Converti")

if submitted:
    if not codice_azienda:
        st.error("Inserisci il Codice azienda.")
    elif uploaded_file is None:
        st.error("Carica un file CSV da convertire.")
    else:
        try:
            df = pd.read_csv(uploaded_file)

            if provider == "Coverflex":
                df_out = convert_coverflex(df, codice_azienda, mappa_causali_df)
            elif provider == "DoubleYou":
                df_out = convert_doubleyou(df, codice_azienda, mappa_causali_df)

            st.success("✅ Conversione completata.")

            # Preparazione per il download
            buffer = BytesIO()
            df_out.to_csv(buffer, index=False)
            buffer.seek(0)

            st.download_button(
                label="📥 Scarica file convertito",
                data=buffer,
                file_name="file_convertito.csv",
                mime="text/csv"
            )

        except Exception as e:
            st.error(f"❌ Errore durante la conversione: {e}")
