import streamlit as st
import pandas as pd
from io import StringIO
from conversion_rules import convert_coverflex, convert_doubleyou, load_causal_map

st.set_page_config(page_title="Convertitore Welfare", layout="centered")
st.title("🔄 Convertitore file Welfare Aziendale")

company_code = st.text_input("Codice azienda")
provider = st.radio("Seleziona provider", ["Coverflex", "DoubleYou"])
uploaded_file = st.file_uploader("Carica file CSV", type=["csv"])

if uploaded_file and provider and company_code:
    try:
        content = uploaded_file.getvalue().decode("utf-8")

        # Rimozione righe di intestazione extra (Coverflex ha header dopo 3 righe)
        if provider.lower() == "coverflex":
            skip = 3
        else:
            skip = 0

        df = pd.read_csv(StringIO(content), sep=None, engine="python", skiprows=skip)

        st.write("✅ File caricato:")
        st.dataframe(df.head())

        causal_map = load_causal_map()

        if provider == "Coverflex":
            result_df = convert_coverflex(df, company_code, causal_map)
            filename = "coverflex_converted.csv"
        else:
            result_df = convert_doubleyou(df, company_code, causal_map)
            filename = "doubleyou_converted.csv"

        csv_output = result_df.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Scarica file convertito", data=csv_output, file_name=filename, mime="text/csv")

    except Exception as e:
        st.error(f"❌ Errore durante la conversione: {e}")
