import streamlit as st
import pandas as pd
from io import BytesIO
from conversion_rules import convert_coverflex, convert_doubleyou
import os
import re

MAPPAC_PATH = os.path.join(os.path.dirname(__file__), "mappa_causali.csv")
mappa_causali_df = pd.read_csv(MAPPAC_PATH)

def normalize_importo(df, col='Importo'):
    def fix_val(x):
        if pd.isna(x):
            return 0.0
        s = str(x).strip()
        # Rimuove tutto ciò che non è numero, virgola o punto
        s_clean = re.sub(r'[^0-9,\.]', '', s)
        # Gestione punti e virgole
        if '.' in s_clean and ',' in s_clean:
            s_clean = s_clean.replace('.', '')
            s_clean = s_clean.replace(',', '.')
        elif ',' in s_clean and '.' not in s_clean:
            s_clean = s_clean.replace(',', '.')
        try:
            return float(s_clean)
        except Exception as e:
            print(f"Valore non convertibile: '{x}' → '{s_clean}' - errore: {e}")
            return 0.0
    df[col] = df[col].apply(fix_val)
    return df

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
            uploaded_file.seek(0)
            raw_text = uploaded_file.read().decode('latin1')
            st.text_area("Contenuto file (prime 500 caratteri):", raw_text[:500])
            uploaded_file.seek(0)

            if provider == "Coverflex":
                df = pd.read_csv(
                    uploaded_file,
                    skiprows=3,
                    sep=',',
                    quotechar='"',
                    decimal=',',
                    encoding='latin1',
                    engine='python'
                )
                df = normalize_importo(df, 'Importo')
            else:
                df = pd.read_csv(uploaded_file)
                df = normalize_importo(df, 'Totale')

            df.columns = df.columns.str.strip()
            st.write("Colonne file caricato:", df.columns.tolist())
            st.write("Prime righe del file:", df.head())

            # Stampa debug valori importo
            if provider == "Coverflex":
                st.write("Valori normalizzati Importo (Coverflex):", df['Importo'].head(10))
                df_out = convert_coverflex(df, codice_azienda, mappa_causali_df)
            else:
                st.write("Valori normalizzati Totale (DoubleYou):", df['Totale'].head(10))
                df_out = convert_doubleyou(df, codice_azienda, mappa_causali_df)

            st.success("✅ Conversione completata.")

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
