import streamlit as st
import pandas as pd
from io import StringIO
from conversion_rules import convert_coverflex, convert_doubleyou, load_causal_map

st.title("Convertitore file welfare")

uploaded_file = st.file_uploader("Carica file CSV", type=["csv"])
provider = st.selectbox("Seleziona provider", ["Coverflex", "DoubleYou"])
company_code = st.text_input("Codice azienda")

if uploaded_file and provider and company_code:
    content = uploaded_file.read().decode("utf-8")

    st.write("Contenuto file (prime 500 caratteri):")
    st.text(content[:500])

    # Carica dataframe
    df = pd.read_csv(StringIO(content), sep=None, engine="python", header=None)
    df.columns = df.iloc[0]
    df = df[1:].reset_index(drop=True)

    try:
        causal_map = load_causal_map()

        if provider == "Coverflex":
            converted_df = convert_coverflex(df, company_code, causal_map)
            filename = "coverflex_converted.csv"
        else:
            converted_df = convert_doubleyou(df, company_code, causal_map)
            filename = "doubleyou_converted.csv"

        st.dataframe(converted_df)

        csv = converted_df.to_csv(index=False).encode("utf-8")
        st.download_button("Scarica file convertito", data=csv, file_name=filename, mime="text/csv")

    except Exception as e:
        st.error(f"❌ Errore durante la conversione: {e}")
