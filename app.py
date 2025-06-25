import streamlit as st
import pandas as pd
from conversion_rules import convert_coverflex, convert_doubleyou, load_causal_map

st.set_page_config(page_title="Convertitore Welfare", layout="wide")

st.title("🧾 Convertitore File Welfare - Coverflex / DoubleYou")

uploaded_file = st.file_uploader("📤 Carica il file CSV da convertire", type=["csv"])

if uploaded_file is not None:
    try:
        content = uploaded_file.getvalue().decode("utf-8", errors="ignore")
        st.text("Contenuto file (prime 500 caratteri):")
        st.code(content[:500])

        uploaded_file.seek(0)

        mapping = load_causal_map()

        df = pd.read_csv(uploaded_file, sep=None, engine="python")

        st.markdown("**✅ Colonne file caricato:**")
        st.write(df.columns.tolist())

        if "Codice fiscale dipendente" in df.columns:
            result = convert_coverflex(df, mapping)
            filename = "coverflex_converted.csv"
        elif "CodFisc" in df.columns:
            result = convert_doubleyou(df, mapping)
            filename = "doubleyou_converted.csv"
        else:
            st.error("❌ Formato file non riconosciuto.")
            st.stop()

        st.success("✅ Conversione completata. Scarica il file:")
        st.download_button("📥 Scarica CSV convertito", data=result.to_csv(index=False), file_name=filename, mime="text/csv")
        st.dataframe(result.head(50))

    except Exception as e:
        st.error(f"❌ Errore durante la conversione: {e}")
