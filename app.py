import streamlit as st
import pandas as pd
from conversion_rules import convert_coverflex, convert_doubleyou

# Carica la mappatura delle causali solo una volta grazie alla cache
@st.cache_data
def load_mappa_causali():
    return pd.read_csv('mappa_causali.csv')

# Funzione per tentare conversione automatica: prima Coverflex, poi DoubleYou se fallisce
def tenta_conversione_auto(df, codice_azienda, mappa):
    try:
        return convert_coverflex(df, codice_azienda, mappa), "coverflex"
    except Exception:
        try:
            return convert_doubleyou(df, codice_azienda, mappa), "doubleyou"
        except Exception:
            return None, "non riconosciuto"

# Main dell'app
def main():
    st.title("Convertitore Welfare CSV")

    codice_azienda = st.text_input("Codice azienda:")

    uploaded_files = st.file_uploader(
        "📤 Carica uno o più file CSV (max 24)",
        type=['csv'],
        accept_multiple_files=True
    )

    # Mostra una tabella con selettori tipo file (Auto/Coverflex/DoubleYou)
    file_tipi = {}
    if uploaded_files:
        st.markdown("### 📂 Seleziona tipologia per ciascun file:")
        cols = st.columns(2)  # Colonne per impaginare affiancati
        for i, file in enumerate(uploaded_files):
            col = cols[i % 2]  # Alterna tra colonna 0 e 1
            with col:
                tipo = st.selectbox(
                    f"{file.name}",
                    options=["Auto", "coverflex", "doubleyou"],
                    key=f"select_{i}"
                )
                file_tipi[file.name] = tipo.lower()

    # Pulsante principale di conversione
    if st.button("🚀 Converti"):
        if not codice_azienda:
            st.error("⚠️ Inserisci il codice azienda.")
            return
        if not uploaded_files:
            st.error("⚠️ Carica almeno un file.")
            return

        mappa_causali_df = load_mappa_causali()
        converted_results = {}

        for file in uploaded_files:
            tipo = file_tipi.get(file.name, "auto")

            try:
                # Prova parsing CSV con vari metodi in base al tipo
                if tipo == "coverflex":
                    df = pd.read_csv(file, sep=None, engine='python', skiprows=3)
                    result = convert_coverflex(df, codice_azienda, mappa_causali_df)
                    metodo_usato = "coverflex"

                elif tipo == "doubleyou":
                    df = pd.read_csv(file, sep=';', engine='python')
                    result = convert_doubleyou(df, codice_azienda, mappa_causali_df)
                    metodo_usato = "doubleyou"

                else:  # modalità Auto
                    try:
                        df = pd.read_csv(file, sep=None, engine='python', skiprows=3)
                    except Exception:
                        df = pd.read_csv(file, sep=';', engine='python')  # fallback

                    result, metodo_usato = tenta_conversione_auto(df, codice_azienda, mappa_causali_df)

                # ✅ Salva il risultato solo se valido
                if isinstance(result, pd.DataFrame) and not result.empty:
                    converted_results[file.name] = {
                        "data": result,
                        "type": metodo_usato
                    }
                    st.success(f"✅ {file.name} convertito come {metodo_usato.capitalize()} ({len(result)} record)")
                else:
                    st.warning(f"⚠️ Il file '{file.name}' non ha prodotto dati validi per la conversione.")

            except Exception as e:
                st.error(f"❌ Errore nel file '{file.name}': {e}")

        # 🔽 Se ci sono risultati, mostra i download
        if converted_results:
            st.markdown("### 📥 Scarica i file convertiti:")
            for file_name, data in converted_results.items():
                result_df = data["data"]
                tipo = data["type"]
                st.download_button(
                    label=f"⬇️ {file_name} ({tipo})",
                    data=result_df.to_csv(index=False).encode('utf-8'),
                    file_name=f"{file_name.replace('.csv', '')}_convertito_{tipo}.csv",
                    mime='text/csv',
                    key=f"download_{file_name}"
                )

# Avvio app
if __name__ == '__main__':
    main()
