import streamlit as st
import pandas as pd
from conversion_rules import convert_coverflex, convert_doubleyou

@st.cache_data
def load_mappa_causali():
    return pd.read_csv('mappa_causali.csv')

def rileva_tipologia(nome_file):
    nome = nome_file.lower()
    if 'coverflex' in nome:
        return 'Coverflex'
    elif 'doubleyou' in nome or 'double_you' in nome:
        return 'DoubleYou'
    return None  # Non riconosciuto

def main():
    st.title("🧰 Convertitore file welfare multipli")

    codice_azienda = st.text_input("Codice azienda:")
    uploaded_files = st.file_uploader(
        "Carica fino a 24 file CSV",
        type=['csv'],
        accept_multiple_files=True
    )

    mappa_causali_df = load_mappa_causali()

    # Interfaccia di selezione manuale della tipologia per ciascun file
    file_tipologie = {}
    if uploaded_files:
        if len(uploaded_files) > 24:
            st.error("❗ Puoi caricare al massimo 24 file")
            return

        st.markdown("### Seleziona la tipologia per ogni file:")
        for i, file in enumerate(uploaded_files):
            with st.container():
                col1, col2 = st.columns([3, 2])
                with col1:
                    st.markdown(f"**📄 {file.name}**")
                with col2:
                    scelta = st.selectbox(
                        f"Tipologia per {file.name}",
                        ['Auto', 'Coverflex', 'DoubleYou'],
                        key=f"tipologia_{i}"
                    )
                    file_tipologie[file.name] = scelta

    if st.button("Converti"):
        if not codice_azienda:
            st.error("❗ Inserisci il codice azienda")
            return
        if not uploaded_files:
            st.error("❗ Carica almeno un file")
            return

        for i, file in enumerate(uploaded_files):
            nome_file = file.name
            try:
                scelta = file_tipologie.get(nome_file, 'Auto')
                if scelta == 'Auto':
                    tipologia = rileva_tipologia(nome_file)
                    if not tipologia:
                        st.warning(f"⚠️ Tipologia non riconosciuta per il file: {nome_file}")
                        continue
                else:
                    tipologia = scelta

                # Lettura e conversione
                if tipologia == 'Coverflex':
                    df = pd.read_csv(file, sep=None, engine='python', skiprows=3)
                    result = convert_coverflex(df, codice_azienda, mappa_causali_df)
                    nome_output = nome_file.replace('.csv', '_converted_coverflex.csv')
                elif tipologia == 'DoubleYou':
                    df = pd.read_csv(file, sep=';', engine='python')
                    result = convert_doubleyou(df, codice_azienda, mappa_causali_df)
                    nome_output = nome_file.replace('.csv', '_converted_doubleyou.csv')
                else:
                    st.warning(f"⚠️ Tipologia non riconosciuta per il file: {nome_file}")
                    continue

                st.success(f"✅ File '{nome_file}' convertito come {tipologia}.")

                st.download_button(
                    label=f"⬇️ Scarica {nome_output}",
                    data=result.to_csv(index=False).encode('utf-8'),
                    file_name=nome_output,
                    mime='text/csv'
                )

            except Exception as e:
                st.error(f"❌ Errore durante la conversione di {nome_file}: {e}")

# Avvio app
if __name__ == '__main__':
    main()
