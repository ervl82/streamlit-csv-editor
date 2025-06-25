import pandas as pd

def clean_importo(val):
    if pd.isna(val):
        return 0
    # Rimuovo spazi, sostituisco virgola con punto e rimuovo punti come separatori migliaia
    val_str = str(val).strip().replace('.', '').replace(',', '.')
    try:
        return float(val_str)
    except:
        return 0

def format_data(data):
    # Provo a convertire la data con dayfirst=True e vari formati
    try:
        dt = pd.to_datetime(data, dayfirst=True, errors='coerce')
        if pd.isna(dt):
            # fallback: prova senza dayfirst
            dt = pd.to_datetime(data, errors='coerce')
        if pd.isna(dt):
            return ""
        return dt.strftime("%d%m%y")
    except:
        return ""

def mappa_causale(trattamento, mappa_causali_df):
    # Cerca la causale nella mappa e restituisce il codice corrispondente
    match = mappa_causali_df[mappa_causali_df['Trattamento'].str.strip().str.lower() == str(trattamento).strip().lower()]
    if not match.empty:
        return str(match.iloc[0]['Codice'])
    return ""

def convert_coverflex(df, codice_azienda, mappa_causali_df):
    output_rows = []
    progressivo = 1

    # Assicurati che le colonne chiave esistano
    expected_cols = ['Codice fiscale dipendente', 'Tratt. Fiscale', 'Importo', 'Data']
    for col in expected_cols:
        if col not in df.columns:
            raise ValueError(f"Colonna '{col}' non trovata nel file Coverflex")

    for _, row in df.iterrows():
        codice_dip = row['Codice fiscale dipendente']
        trattamento = row['Tratt. Fiscale']
        importo_raw = row['Importo']
        data_raw = row['Data']

        importo = clean_importo(importo_raw)
        if importo == 0:
            continue  # Skip righe senza importo

        causale = mappa_causale(trattamento, mappa_causali_df)
        periodo = format_data(data_raw)

        output_rows.append({
            "Codice dipendente": codice_dip,
            "Codice voce": causale,
            "Descrizione": "",
            "Quantità": "",
            "Base": "",
            "Importo": int(round(importo * 100)),
            "Periodo": periodo,
            "Tipo elaborazione": "",
            "Progressivo": progressivo
        })
        progressivo += 1

    output_df = pd.DataFrame(output_rows, columns=[
        "Codice dipendente", "Codice voce", "Descrizione", "Quantità", "Base",
        "Importo", "Periodo", "Tipo elaborazione", "Progressivo"
    ])
    return output_df

def convert_doubleyou(df, codice_azienda, mappa_causali_df):
    output_rows = []
    progressivo = 1

    # Controllo colonne necessarie
    expected_cols = ['CodFisc', 'Tratt. Fiscale', 'Totale', 'Data Ordine']
    for col in expected_cols:
        if col not in df.columns:
            raise ValueError(f"Colonna '{col}' non trovata nel file DoubleYou")

    for _, row in df.iterrows():
        codice_dip = row['CodFisc']
        trattamento = row['Tratt. Fiscale']
        importo_raw = row['Totale']
        data_raw = row['Data Ordine']

        importo = clean_importo(importo_raw)
        if importo == 0:
            continue

        causale = mappa_causale(trattamento, mappa_causali_df)
        periodo = format_data(data_raw)

        output_rows.append({
            "Codice dipendente": codice_dip,
            "Codice voce": causale,
            "Descrizione": "",
            "Quantità": "",
            "Base": "",
            "Importo": int(round(importo * 100)),
            "Periodo": periodo,
            "Tipo elaborazione": "",
            "Progressivo": progressivo
        })
        progressivo += 1

    output_df = pd.DataFrame(output_rows, columns=[
        "Codice dipendente", "Codice voce", "Descrizione", "Quantità", "Base",
        "Importo", "Periodo", "Tipo elaborazione", "Progressivo"
    ])
    return output_df
