import streamlit as st  # Libreria per creare interfacce web
import pandas as pd     # Libreria per gestire i CSV e DataFrame
from conversion_rules import convert_coverflex, convert_doubleyou  # Funzioni di conversione

# ✅ Funzione per caricare la mappa delle causali (con caching)
@st.cache_data
def load_mappa_causali():
    return pd.read_csv('mappa_causali.csv')

# ✅ Rileva la tipologia (Coverflex/DoubleYou) in base al nome del file
def rileva_tipologia(nome_file):
    nome_file_lower = nome_file.lower()
    if 'coverflex' in nome_file_lower:
        return 'Coverflex'
    elif 'doubleyou' in nome_file_lower or 'double_you' in nome_file_lower:
        return 'DoubleYou'
    return None  # Se non riconosciuto

# ✅ Funzione principale dell'applicazione
def main():
    st.title("🧾 Convertitore file welfare multipli")

    # Campo per inserire il codice azienda (obbligatorio)
    codice_azienda = st.text_input("Codice azienda:")

    # Upload multiplo dei file CSV (max 24)
    uploaded_files = st.file_uploader(
        "Carica fino a 24 file CSV di origine (Coverflex e/o DoubleYou)",
        type=['csv'],
        accept_multiple_files=True,
        help="Puoi caricare fino a 24 file"
    )

    # Carica la mappatura delle causali da file
    mappa_causali_df = load_mappa_causali()

    # Dizionario per memorizzare le tipologie selezionate per ogni file
    file_tipologie = {}

    # ✅ Se sono stati caricati dei file, mostra i menu a tendina per ciascun file
    if uploaded_files:
        st.markdown("### 📂 Seleziona tipologia per ciascun file:")
        for file in uploaded_files:
            # Imposta il valore di default del menu a partire dal nome file
            default_tipologia = rileva_tipologia(file.name) or "Auto"

            # Layout a due colonne: nome file a sinistra, menu tendina a destra
            col1, col2 = st.columns([3, 2])
            with col1:
                st.markdown(f"📄 **{file.name}**")
            with col2:
                file_tipologie[file.name] = st.selectbox(
                    label="",  # Nessuna etichetta per compattezza
                    options=['Auto', 'Coverflex', 'DoubleYou'],
                    index=['Auto', 'Coverflex', 'DoubleYou'].index(default_tipologia),
                    key=f"select_{file.name}"  # Chiave univoca per ciascun file
                )

    # ✅ Quando l'utente preme il bottone "Converti"
    if st.button("🔄 Converti"):
        # Controllo presenza codice azienda e file caricati
        if not codice_azienda:
            st.error("❗ Inserisci il codice azienda")
            return
        if not uploaded_files:
            st.error("❗ Carica almeno un file")
            return

        # Inizializza o svuota la lista dei file convertiti nello stato di sessione
        st.session_state.converted_files = []

        # ✅ Itera su ciascun file caricato
        for i, file in enumerate(uploaded_files):
            nome_file = file.name
            try:
                # Recupera la tipologia selezionata dal menu a tendina
                scelta = file_tipologie.get(nome_file, 'Auto')

                # Se la scelta è "Auto", cerca di rilevarla dal nome file
                if scelta == 'Auto':
                    tipologia = rileva_tipologia(nome_file)
                    if not tipologia:
                        st.warning(f"⚠️ Tipologia non riconosciuta per il file: {nome_file}")
                        continue  # Salta alla prossima iterazione
                else:
                    tipologia = scelta  # Usa la selezione manuale

                # ✅ Conversione basata sulla tipologia rilevata o forzata
                if tipologia == 'Coverflex':
                    # Coverflex → ignora le prime 3 righe del CSV
                    df = pd.read_csv(file, sep=None, engine='python', skiprows=3)
                    result = convert_coverflex(df, codice_azienda, mappa_causali_df)
                    nome_output = nome_file.replace('.csv', '_converted_coverflex.csv')

                elif tipologia == 'DoubleYou':
                    # DoubleYou → separatore forzato a punto e virgola
                    df = pd.read_csv(file, sep=';', engine='python')
                    result = convert_doubleyou(df, codice_azienda, mappa_causali_df)
                    nome_output = nome_file.replace('.csv', '_converted_doubleyou.csv')

                else:
                    st.warning(f"⚠️ Tipologia non riconosciuta per il file: {nome_file}")
                    continue

                # ✅ Salva il file convertito in session_state per download successivo
                st.session_state.converted_files.append({
                    'nome_output': nome_output,
                    'data': result.to_csv(index=False).encode('utf-8')
                })

                # Messaggio di successo per ogni file
                st.success(f"✅ File '{nome_file}' convertito correttamente.")

            except Exception as e:
                # Mostra errore se la conversione fallisce
                st.error(f"❌ Errore nella conversione di {nome_file}: {e}")

    # ✅ Se ci sono file convertiti, mostra i bottoni per il download
    if 'converted_files' in st.session_state and st.session_state.converted_files:
        st.markdown("### 📥 File convertiti disponibili per il download:")
        for i, file_info in enumerate(st.session_state.converted_files):
            st.download_button(
                label=f"⬇️ Scarica {file_info['nome_output']}",
                data=file_info['data'],
                file_name=file_info['nome_output'],
                mime='text/csv',
                key=f"download_{i}"  # Chiave unica per evitare conflitti
            )

# ✅ Avvia l'app se il file viene eseguito come script principale
if __name__ == '__main__':
    main()
