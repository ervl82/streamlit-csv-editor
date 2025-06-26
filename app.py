import streamlit as st
import pandas as pd
from conversion_rules import convert_coverflex, convert_doubleyou

# Carica la mappa causali una sola volta (caching)
@st.cache_data
def load_mappa_causali():
    return pd.read_csv('mappa_causali.csv')

# Funzione per tentare conversione "intelligente" se l'utente ha selezionato 'Auto'
def try_auto_conversion(df, codice_azienda, mappa_causali_df):
    try:
        return convert_coverflex(df, codice_azienda, mappa_causali_df), "coverflex"
    except Exception:
        pass  # Ignora il primo tentativo e prova DoubleYou
    try:
        return convert_doubleyou(df, codice_azienda, mappa_causali_df), "doubleyou"
    except Exception:
        raise ValueError("Il file non è compatibile con nessuna delle due modalità.")

# Funzione principale dell’app
def main():
    st.set_page_config(page_title="Convertitore Welfare", layout="centered")
    st.title("🧾 Convertitore file Welfare")

    # Sezione input utente
    codice_azienda = st.text_input("Codice azienda")
    uploaded_files = st.file_uploader("📤 Carica uno o più file CSV", type=['csv'], accept_multiple_files=True)

    # Caricamento mappa causali
    mappa_causali_df = load_mappa_causali()

    # Dizionario per salvare i file convertiti
    converted_results = {}

    # Se l’utente ha caricato almeno un file
    if uploaded_files:
        st.subheader("📂 Seleziona tipologia per ciascun file")

        # Layout a griglia per visualizzare il nome file e menu tendina sulla stessa riga
        file_options = {}
        for i, file in enumerate(uploaded_files):
            cols = st.columns([2, 1])
            with cols[0]:
                st.markdown(f"**{file.name}**")  # Nome file
            with cols[1]:
                file_type = st.selectbox(
                    "Tipo",
                    ["Auto", "Coverflex", "DoubleYou"],
                    key=f"select_{i}"
                )
                file_options[file.name] = file_type

    # Bottone per avviare la conversione
    if st.button("🚀 Converti"):
        if not codice_azienda:
            st.error("❌ Inserisci il codice azienda prima di procedere.")
            return

        if not uploaded_files:
            st.error("❌ Carica almeno un file CSV.")
            return

        for file in uploaded_files:
            file_name = file.name
            tipo = file_options[file_name]

            try:
                # Legge il contenuto del file
                content = file.read()
                # Reset del puntatore per rileggerlo in seguito
                file.seek(0)

                df = None
                result = None
                metodo_usato = tipo.lower()

                # Tentativo di lettura con o senza header a seconda del tipo
                if metodo_usato == "coverflex":
                    df = pd.read_csv(file, sep=None, engine="python", skiprows=3)
                    result = convert_coverflex(df, codice_azienda, mappa_causali_df)
                elif metodo_usato == "doubleyou":
                    df = pd.read_csv(file, sep=';', engine="python")
                    result = convert_doubleyou(df, codice_azienda, mappa_causali_df)
                elif metodo_usato == "auto":
                    # Tenta prima Coverflex, poi DoubleYou
                    try:
                        df = pd.read_csv(file, sep=None, engine="python", skiprows=3)
                        result = convert_coverflex(df, codice_azienda, mappa_causali_df)
                        metodo_usato = "coverflex"
                    except Exception:
                        file.seek(0)  # Reset file pointer
                        df = pd.read_csv(file, sep=';', engine="python")
                        result = convert_doubleyou(df, codice_azienda, mappa_causali_df)
                        metodo_usato = "doubleyou"

                # Salva il risultato se la conversione ha avuto successo
                if result is not None:
                    converted_results[file_name] = {
                        "data": result,
                        "type": metodo_usato
                    }
                    st.success(f"✅ {file_name} convertito come {metodo_usato.capitalize()} ({len(result)} record)")
                else:
                    st.warning(f"⚠️ Nessun dato convertito per {file_name}")

            except Exception as e:
                st.error(f"❌ Errore nel file '{file_name}': {str(e)}")

        # Se sono presenti risultati, offri i pulsanti per il download
        if converted_results:
            st.subheader("📥 Scarica i file convertiti")
            for name, info in converted_results.items():
                tipo = info["type"]
                result_df = info["data"]
                output_name = f"{name.replace('.csv', '')}_{tipo}_converted.csv"
                st.download_button(
                    label=f"⬇️ Scarica {output_name}",
                    data=result_df.to_csv(index=False).encode('utf-8'),
                    file_name=output_name,
                    mime="text/csv",
                    key=f"download_{output_name}"
                )

# Avvio dell'applicazione
if __name__ == '__main__':
    main()
