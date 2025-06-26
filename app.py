import streamlit as st  # Libreria per creare interfacce web
import pandas as pd  # Manipolazione file CSV
from conversion_rules import convert_coverflex, convert_doubleyou  # Importa le funzioni di conversione

@st.cache_data  # Cache per evitare di ricaricare ogni volta il file
def load_mappa_causali():
    return pd.read_csv('mappa_causali.csv')  # Carica il file delle mappature

def main():
    st.title("Convertitore file welfare")  # Titolo applicazione

    # Inserimento dati da parte dell’utente
    codice_azienda = st.text_input("Codice azienda:")
    provider = st.radio("Provider:", ('Coverflex', 'DoubleYou'))  # Scelta del provider
    file = st.file_uploader("Carica il file CSV di origine", type=['csv'])  # Upload file

    mappa_causali_df = load_mappa_causali()  # Caricamento mappature causali

    if st.button("Converti"):  # Quando si preme il bottone "Converti"
        if not codice_azienda:
            st.error("Inserisci il codice azienda")  # Errore se campo vuoto
            return
        if not file:
            st.error("Carica un file CSV")  # Errore se file mancante
            return

        try:
            if provider == 'Coverflex':
                # Coverflex: salta le prime 3 righe inutili (titoli/report)
                df = pd.read_csv(file, sep=None, engine='python', skiprows=3)
                result = convert_coverflex(df, codice_azienda, mappa_causali_df)
                file_name = 'coverflex_converted.csv'
            else:
                # DoubleYou: forza separatore a punto e virgola
                df = pd.read_csv(file, sep=';', engine='python')
                result = convert_doubleyou(df, codice_azienda, mappa_causali_df)
                file_name = 'doubleyou_converted.csv'

            # Messaggio di successo
            st.success("✅ Conversione completata!")

            # Bottone per scaricare il file risultante
            st.download_button(
                label="📥 Scarica file convertito",
                data=result.to_csv(index=False).encode('utf-8'),
                file_name=file_name,  # Nome file coerente con il provider
                mime='text/csv'
            )
        except Exception as e:
            # Mostra eventuali errori durante la conversione
            st.error(f"❌ Errore durante la conversione: {e}")

# Avvio dell’app
if __name__ == '__main__':
    main()
