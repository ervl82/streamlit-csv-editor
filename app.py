import streamlit as st
import pandas as pd
from conversion_rules import convert_coverflex, convert_doubleyou

@st.cache_data
def load_mappa_causali():
    """
    Carica il file CSV con la mappatura delle causali.
    Questa funzione è memorizzata in cache per evitare ricaricamenti inutili.
    """
    return pd.read_csv('mappa_causali.csv')

def main():
    st.title("Convertitore file welfare")

    # Input testo per codice azienda
    codice_azienda = st.text_input("Codice azienda:")

    # Radio button per forzare la conversione per tutti i file caricati
    provider_forzatura = st.radio(
        "Forza conversione per tutti i file (facoltativo):",
        options=['Nessuna', 'Coverflex', 'DoubleYou']
    )

    # Upload multiplo di file CSV (max 24)
    files = st.file_uploader(
        "Carica fino a 24 file CSV (mix Coverflex/DoubleYou possibile):",
        accept_multiple_files=True,
        type=['csv']
    )

    # Carica mappa causali da file esterno
    mappa_causali_df = load_mappa_causali()

    # Se sono caricati file, mostra la lista con selettori tipo per ogni file
    tipo_file_selezioni = []
    if files:
        st.markdown("### 📂 Seleziona tipologia per ciascun file:")
        for i, file in enumerate(files):
            # Uso colonne per affiancare nome file e menu a tendina
            col1, col2 = st.columns([4, 2])
            with col1:
                st.write(file.name)  # Mostra nome file
            with col2:
                # Imposta valore di default del menu a tendina
                default_val = 'Nessuna' if provider_forzatura == 'Nessuna' else provider_forzatura
                tipo = st.selectbox(
                    f"Tipo file {i}",
                    options=['Auto', 'Coverflex', 'DoubleYou'],
                    index=['Auto', 'Coverflex', 'DoubleYou'].index(default_val) if default_val in ['Coverflex','DoubleYou'] else 0,
                    key=f'tipo_file_{i}'  # Key unica per ogni selectbox
                )
                tipo_file_selezioni.append(tipo)

    # Pulsante per avviare la conversione
    if st.button("Converti tutti i file"):
        # Validazioni preliminari
        if not codice_azienda:
            st.error("Inserisci il codice azienda")
            return
        if not files:
            st.error("Carica almeno un file CSV")
            return

        risultati = []         # Lista per salvare i risultati di conversione (nome file + dataframe)
        messaggi_scarti_tot = []  # Lista per i messaggi di errori/scarti da tutti i file

        # Ciclo su ogni file caricato
        for i, file in enumerate(files):
            # Determina tipo file: forzatura globale > scelta utente > auto
            if provider_forzatura in ['Coverflex', 'DoubleYou']:
                tipo_file = provider_forzatura
            else:
                tipo_file = tipo_file_selezioni[i]

            try:
                # Legge il file con parametri diversi in base al tipo
                if tipo_file == 'Coverflex':
                    df = pd.read_csv(file, sep=None, engine='python', skiprows=3)
                    output, scarti = convert_coverflex(df, codice_azienda, mappa_causali_df)
                elif tipo_file == 'DoubleYou':
                    df = pd.read_csv(file, sep=';', engine='python')
                    output, scarti = convert_doubleyou(df, codice_azienda, mappa_causali_df)
                elif tipo_file == 'Auto':
                    # Tentativo automatico di conversione: prova Coverflex, poi DoubleYou se fallisce
                    try:
                        df = pd.read_csv(file, sep=None, engine='python', skiprows=3)
                        output, scarti = convert_coverflex(df, codice_azienda, mappa_causali_df)
                    except Exception:
                        df = pd.read_csv(file, sep=';', engine='python')
                        output, scarti = convert_doubleyou(df, codice_azienda, mappa_causali_df)
                else:
                    st.warning(f"Tipo file non riconosciuto per '{file.name}', saltato.")
                    continue

                # Salva risultati e messaggi di scarto
                risultati.append((file.name, output))
                messaggi_scarti_tot.extend([f"{file.name}: {msg}" for msg in scarti])

            except Exception as e:
                # Messaggio di errore in caso di problemi nel caricamento o conversione
                st.error(f"Errore nel file '{file.name}': {e}")

        # Se ci sono risultati da mostrare
        if risultati:
            st.success("✅ Conversione completata!")

            # Se ci sono messaggi di scarto, li mostra come warning
            if messaggi_scarti_tot:
                st.warning("⚠️ Alcuni record sono stati scartati o contengono errori:")
                for msg in messaggi_scarti_tot:
                    st.write(msg)

            # Mostra un bottone per scaricare ciascun file convertito
            for file_name, df_out in risultati:
                st.download_button(
                    label=f"📥 Scarica {file_name} convertito",
                    data=df_out.to_csv(index=False).encode('utf-8'),
                    file_name=f"converted_{file_name}",
                    mime='text/csv'
                )

if __name__ == '__main__':
    main()
