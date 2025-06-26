import streamlit as st
import pandas as pd
from conversion_rules import convert_coverflex, convert_doubleyou

# ✅ Carica la mappa delle causali una sola volta (con caching per performance)
@st.cache_data
def load_mappa_causali():
    return pd.read_csv('mappa_causali.csv')

# ✅ Funzione per cercare di capire automaticamente il tipo di file dal nome
def rileva_tipologia(nome_file):
    nome_file_lower = nome_file.lower()
    if 'coverflex' in nome_file_lower:
        return 'Coverflex'
    elif 'doubleyou' in nome_file_lower or 'double_you' in nome_file_lower:
        return 'DoubleYou'
    return None  # Nessun match: da chiedere all’utente

# ✅ Funzione principale Streamlit
def main():
    st.title("🧾 Convertitore file welfare multipli")

    # 👉 Campo per il codice azienda richiesto per ogni conversione
    codice_azienda = st.text_input("Codice azienda:")

    # 👉 Uploader multiplo: permette di caricare fino a 24 file CSV
    uploaded_files = st.file_uploader(
        "Carica fino a 24 file CSV di origine (Coverflex e/o DoubleYou)",
        type=['csv'],
        accept_multiple_files=True,
        help="Puoi caricare fino a 24 file"
    )

    # ✅ Carica il file delle mappature delle causali (una sola volta grazie alla cache)
    mappa_causali_df = load_mappa_causali()

    # 👉 Dizionario che associa il nome file alla tipologia selezionata (manuale o auto)
    file_tipologie = {}

    # ✅ Per ogni file caricato, chiedi all’utente la tipologia (o lascia su Auto)
    if uploaded_files:
        st.markdown("### 📂 Seleziona tipologia per ciascun file:")
        for file in uploaded_files:
            default_tipologia = rileva_tipologia(file.name) or "Auto"
            file_tipologie[file.name] = st.selectbox(
                f"Tipo per '{file.name}'",
                options=['Auto', 'Coverflex', 'DoubleYou'],
                index=['Auto', 'Coverflex', 'DoubleYou'].index(default_tipologia),
                key=f"select_{file.name}"  # Evita conflitti nel frontend Streamlit
            )

    # ✅ Conversione al clic del bottone
    if st.button("🔄 Converti"):
        # ⚠️ Validazione campi obbligatori
        if not codice_azienda:
            st.error("❗ Inserisci il codice azienda")
            return
        if not uploaded_files:
            st.error("❗ Carica almeno un file")
            return

        # ✅ Pulizia della sessione per evitare conflitti tra upload precedenti
        st.session_state.converted_files = []

        # ✅ Loop sui file caricati
        for i, file in enumerate(uploaded_files):
            nome_file = file.name
            try:
                # Determina la tipologia dal nome o dalla scelta dell’utente
                scelta = file_tipologie.get(nome_file, 'Auto')
                if scelta == 'Auto':
                    tipologia = rileva_tipologia(nome_file)
                    if not tipologia:
                        st.warning(f"⚠️ Tipologia non riconosciuta per il file: {nome_file}")
                        continue
                else:
                    tipologia = scelta

                # ✅ Conversione specifica per tipo file
                if tipologia == 'Coverflex':
                    # Coverflex: salta intestazione/report
                    df = pd.read_csv(file, sep=None, engine='python', skiprows=3)
                    result = convert_coverflex(df, codice_azienda, mappa_causali_df)
                    nome_output = nome_file.replace('.csv', '_converted_coverflex.csv')

                elif tipologia == 'DoubleYou':
                    # DoubleYou: usa separatore a punto e virgola
                    df = pd.read_csv(file, sep=';', engine='python')
                    result = convert_doubleyou(df, codice_azienda, mappa_causali_df)
                    nome_output = nome_file.replace('.csv', '_converted_doubleyou.csv')

                else:
                    # ⚠️ Fallback: tipo non gestito
                    st.warning(f"⚠️ Tipologia non riconosciuta per il file: {nome_file}")
                    continue

                # ✅ Salva il file convertito in sessione per mostrare il bottone di download
                st.session_state.converted_files.append({
                    'nome_output': nome_output,
                    'data': result.to_csv(index=False).encode('utf-8')
                })

                st.success(f"✅ File '{nome_file}' convertito correttamente.")

            except Exception as e:
                st.error(f"❌ Errore nella conversione di {nome_file}: {e}")

    # ✅ Mostra i bottoni di download anche dopo che l’utente li ha cliccati
    if 'converted_files' in st.session_state and st.session_state.converted_files:
        st.markdown("### 📥 File convertiti disponibili per il download:")
        for i, file_info in enumerate(st.session_state.converted_files):
            st.download_button(
                label=f"⬇️ Scarica {file_info['nome_output']}",
                data=file_info['data'],
                file_name=file_info['nome_output'],
                mime='text/csv',
                key=f"download_{i}"  # Unico per ogni file
            )

# ✅ Punto di ingresso dell’applicazione Streamlit
if __name__ == '__main__':
    main()
