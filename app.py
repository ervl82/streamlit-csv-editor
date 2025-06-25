import streamlit as st
import pandas as pd
from io import StringIO

st.title("Web app per caricare, modificare e scaricare CSV")

# Upload file CSV
uploaded_file = st.file_uploader("Carica un file CSV", type=["csv"])

if uploaded_file:
    # Leggi CSV in DataFrame pandas
    df = pd.read_csv(uploaded_file)
    st.write("### Dati caricati:")
    st.dataframe(df)

    # Modifica semplice: scegli colonna da modificare
    col_to_edit = st.selectbox("Scegli colonna da modificare", df.columns)

    # Input per nuovo valore da assegnare a tutta la colonna (esempio semplice)
    new_value = st.text_input(f"Inserisci nuovo valore per tutta la colonna '{col_to_edit}'")

    if st.button("Applica modifica"):
        if new_value:
            df[col_to_edit] = new_value
            st.success(f"Colonna '{col_to_edit}' aggiornata!")
            st.dataframe(df)
        else:
            st.error("Inserisci un valore valido.")

    # Download CSV modificato
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Scarica CSV modificato",
        data=csv,
        file_name='file_modificato.csv',
        mime='text/csv'
    )
else:
    st.info("Carica un file CSV per iniziare.")
