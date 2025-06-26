import streamlit as st  # Libreria per creare interfacce web interattive
import pandas as pd  # Per la manipolazione di file CSV e DataFrame
import csv  # Per rilevamento automatico del delimitatore CSV
import io  # Per gestire file in memoria come stream di testo

from conversion_rules import convert_coverflex, convert_doubleyou  # Funzioni di conversione specifiche


@st.cache_data  # Cache per caricare una sola volta la mappa causali
def load_mappa_causali():
    return pd.read_csv('mappa_causali.csv')  # File con la mappatura causali


def detect_delimiter(file) -> str:
    """
    Rileva automaticamente il delimitatore CSV del file.
    Se non riesce, ritorna una virgola come default.
    """
    try:
        # Legge tutto il contenuto del file in memoria come stringa
        content = file.getvalue().decode('utf-8')
        # Usa csv.Sniffer per trovare il delimitatore
        sniffer = csv.Sniffer()
        delimiter = sniffer.sniff(content).delimiter
        return delimiter
    except Exception:
        # Se il rilevamento fallisce, ritorna la virgola di default
        return ','


def main():
    st.title("Convertitore file welfare")  # Titolo dell'applicazione

    codice_azienda = st.text_input("Codice azienda:")  # Input codice azienda

    # Caricamento multiplo file (max 24)
    files = st.file_uploader(
        "Carica fino a 24 file CSV (Coverflex e/o DoubleYou)", 
        type=['csv'], 
        accept_multiple_files=True,
        key='multi_files'
    )

    mappa_causali_df = load_mappa_causali()  # Carica mappa causali

    # Se sono stati caricati file, mostra l'interfaccia di selezione tipo per ciascun file
    if files:
        st.markdown("### 📂 Seleziona tipologia per ciascun file")
        tipi_file = []
        for i, f in enumerate(files):
            # Riga con nome file e selectbox per tipo (auto, coverflex, doubleyou)
            tipo = st.selectbox(
                f"{f.name}", 
                options=['Auto', 'Coverflex', 'DoubleYou'], 
                key=f"tipo_{i}"
            )
            tipi_file.append(tipo)

        # Bottone per iniziare la conversione
        if st.button("Converti tutti i file"):
            if not codice_azienda:
                st.error("Inserisci il codice azienda")
                return

            risultati = []  # Lista per risultati conversione di ogni file
            messaggi_errori = []  # Lista per messaggi di errori o scarti

            # Ciclo su ogni file e tipo selezionato
            for f, tipo_file in zip(files, tipi_file):
                try:
                    # Rileva o forza il delimitatore in base al tipo e modalità 'Auto'
                    if tipo_file == 'Coverflex':
                        delimiter = detect_delimiter(f)
                        content = f.getvalue().decode('utf-8')
                        df = pd.read_csv(io.StringIO(content), sep=delimiter, engine='python', skiprows=3)
                        output, scarti = convert_coverflex(df, codice_azienda, mappa_causali_df)

                    elif tipo_file == 'DoubleYou':
                        delimiter = detect_delimiter(f)
                        content = f.getvalue().decode('utf-8')
                        df = pd.read_csv(io.StringIO(content), sep=delimiter, engine='python')
                        output, scarti = convert_doubleyou(df, codice_azienda, mappa_causali_df)

                    else:  # Auto detection
                        # Prima prova come Coverflex
                        try:
                            delimiter = detect_delimiter(f)
                            content = f.getvalue().decode('utf-8')
                            df = pd.read_csv(io.StringIO(content), sep=delimiter, engine='python', skiprows=3)
                            output, scarti = convert_coverflex(df, codice_azienda, mappa_causali_df)
                        except Exception:
                            # Se fallisce Coverflex prova DoubleYou
                            delimiter = detect_delimiter(f)
                            content = f.getvalue().decode('utf-8')
                            df = pd.read_csv(io.StringIO(content), sep=delimiter, engine='python')
                            output, scarti = convert_doubleyou(df, codice_azienda, mappa_causali_df)

                    # Mostra successo e bottone per download per ogni file
                    st.success(f"✅ Conversione completata per file: {f.name}")

                    # Se ci sono record scartati mostra messaggio sintetico
                    if len(scarti) > 0:
                        st.warning(f"⚠️ {len(scarti)} record scartati in {f.name}. Controlla il file di scarti.")

                    # Bottone di download per il file convertito
                    st.download_button(
                        label=f"📥 Scarica file convertito: {f.name}",
                        data=output.to_csv(index=False).encode('utf-8'),
                        file_name=f"converted_{f.name}",
                        mime='text/csv',
                        key=f"download_{f.name}"
                    )

                    # Se ci sono record scartati, aggiungi il file di scarti con download
                    if len(scarti) > 0:
                        st.download_button(
                            label=f"📂 Scarica file scarti: {f.name}",
                            data=scarti.to_csv(index=False).encode('utf-8'),
                            file_name=f"scarti_{f.name}",
                            mime='text/csv',
                            key=f"scarti_{f.name}"
                        )

                except Exception as e:
                    st.error(f"❌ Errore nel file '{f.name}': {str(e)}")


if __name__ == '__main__':
    main()
