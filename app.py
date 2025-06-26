import streamlit as st
import pandas as pd
from conversion_rules import convert_coverflex, convert_doubleyou

@st.cache_data
def load_mappa_causali():
    """
    Carica il file CSV con la mappatura delle causali da disco.
    Utilizza caching per evitare di ricaricare il file ogni volta che cambia qualcosa nella UI.
    """
    return pd.read_csv('mappa_causali.csv')

def main():
    st.title("Convertitore file welfare")  # Titolo principale dell'app

    # Input di testo per il codice azienda richiesto per la conversione
    codice_azienda = st.text_input("Codice azienda:")

    # Upload multiplo di file CSV (max 24 file)
    # L'utente può caricare sia file Coverflex che DoubleYou mischiati
    files = st.file_uploader(
        "Carica fino a 24 file CSV (mix Coverflex/DoubleYou possibile):",
        accept_multiple_files=True,
        type=['csv']
    )

    # Carica la tabella di mappatura delle causali una volta per tutte
    mappa_causali_df = load_mappa_causali()

    # Se ci sono file caricati, mostra la lista con un selettore a tendina accanto a ciascun file
    # per permettere la selezione manuale del tipo di file (Auto, Coverflex, DoubleYou)
    tipo_file_selezioni = []
    if files:
        st.markdown("### 📂 Seleziona tipologia per ciascun file:")
        for i, file in enumerate(files):
            # Layout a colonne: nome file a sinistra, selettore tipo a destra
            col1, col2 = st.columns([4, 2])
            with col1:
                st.write(file.name)  # Visualizza nome file caricato
            with col2:
                # Casella a tendina per scegliere manualmente il tipo di file
                # Default 'Auto' prova a riconoscere automaticamente il formato
                tipo = st.selectbox(
                    f"Tipo file {i}",
                    options=['Auto', 'Coverflex', 'DoubleYou'],
                    index=0,  # Imposta il valore di default su 'Auto'
                    key=f'tipo_file_{i}'  # Chiave unica per ogni selettore per mantenere stato
                )
                tipo_file_selezioni.append(tipo)

    # Bottone per avviare la conversione di tutti i file caricati e selezionati
    if st.button("Converti tutti i file"):
        # Controllo che il codice azienda sia stato inserito
        if not codice_azienda:
            st.error("Inserisci il codice azienda")
            return
        # Controllo che almeno un file sia stato caricato
        if not files:
            st.error("Carica almeno un file CSV")
            return

        # Lista per tenere traccia dei risultati convertiti (nome file e dataframe)
        risultati = []
        # Lista per collezionare eventuali messaggi di record scartati o errori di parsing
        messaggi_scarti_tot = []

        # Ciclo su tutti i file caricati per processarli singolarmente
        for i, file in enumerate(files):
            tipo_file = tipo_file_selezioni[i]  # Tipo file scelto per ciascun file

            try:
                # Se l’utente ha scelto esplicitamente Coverflex
                if tipo_file == 'Coverflex':
                    # Legge CSV con skiprows=3 (tipico di Coverflex), separatore automatico
                    df = pd.read_csv(file, sep=None, engine='python', skiprows=3)
                    output, scarti = convert_coverflex(df, codice_azienda, mappa_causali_df)

                # Se l’utente ha scelto esplicitamente DoubleYou
                elif tipo_file == 'DoubleYou':
                    # Legge CSV con separatore punto e virgola ';'
                    df = pd.read_csv(file, sep=';', engine='python')
                    output, scarti = convert_doubleyou(df, codice_azienda, mappa_causali_df)

                # Se tipo è Auto, prova prima DoubleYou, se fallisce passa a Coverflex
                elif tipo_file == 'Auto':
                    try:
                        # Prova a leggere come DoubleYou (separatore ';')
                        df = pd.read_csv(file, sep=';', engine='python')
                        output, scarti = convert_doubleyou(df, codice_azienda, mappa_causali_df)
                    except Exception:
                        # Se fallisce, prova come Coverflex (skiprows=3)
                        df = pd.read_csv(file, sep=None, engine='python', skiprows=3)
                        output, scarti = convert_coverflex(df, codice_azienda, mappa_causali_df)
                else:
                    st.warning(f"Tipo file non riconosciuto per '{file.name}', salto questo file.")
                    continue  # Salta il file

                # Salva il risultato e i messaggi di scarto
                risultati.append((file.name, output))
                messaggi_scarti_tot.extend([f"{file.name}: {msg}" for msg in scarti])

            except Exception as e:
                # Mostra errore specifico per file in caso di eccezioni generali
                st.error(f"Errore nel file '{file.name}': {e}")

        # Se ci sono risultati da mostrare
        if risultati:
            st.success("✅ Conversione completata!")

            # Se ci sono messaggi di scarto o warning, li mostra in modo semplice
            if messaggi_scarti_tot:
                st.warning("⚠️ Alcuni record sono stati scartati o contengono errori:")
                for msg in messaggi_scarti_tot:
                    st.write(msg)

            # Mostra un bottone di download per ogni file convertito, rimane visibile anche dopo il click
            for file_name, df_out in risultati:
                st.download_button(
                    label=f"📥 Scarica {file_name} convertito",
                    data=df_out.to_csv(index=False).encode('utf-8'),
                    file_name=f"converted_{file_name}",
                    mime='text/csv'
                )

if __name__ == '__main__':
    main()
