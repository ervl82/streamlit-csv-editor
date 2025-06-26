import pandas as pd

def convert_coverflex(df, codice_azienda, mappa_causali_df):
    """
    Converte il DataFrame di Coverflex nel formato di output richiesto.

    Args:
        df (pd.DataFrame): DataFrame in input con i dati originali.
        codice_azienda (str): Codice azienda (non usato direttamente qui).
        mappa_causali_df (pd.DataFrame): Mappa causali per conversione.

    Returns:
        output (pd.DataFrame): DataFrame convertito.
        scarti (list): Lista di messaggi riguardanti record scartati.
    """
    df = df.copy()  # Evita modifiche all'originale

    # Colonne essenziali da verificare
    required_columns = ['Data', 'Tratt. Fiscale', 'Importo']
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        raise ValueError(f"Colonne mancanti nel file Coverflex: {', '.join(missing)}")

    scarti = []

    # Conversione sicura della data in formato datetime (auto-detect)
    df['Data'] = pd.to_datetime(df['Data'], errors='coerce')

    # Controlla quali righe hanno data non valida
    mask_data_valida = df['Data'].notna()
    scarti.extend([
        f"Riga {i+2}: data non valida → '{val}'"
        for i, val in df.loc[~mask_data_valida, 'Data'].items()
    ])

    # Conversione Importo: da stringa con formato italiano a float centesimi
    importi_raw = (
        df['Importo']
        .astype(str)
        .str.replace('.', '', regex=False)  # Rimuove punti migliaia
        .str.replace(',', '.', regex=False) # Cambia virgola in punto
    )
    importi_float = pd.to_numeric(importi_raw, errors='coerce')
    mask_importo_valido = importi_float.notna()
    scarti.extend([
        f"Riga {i+2}: importo non valido → '{val}'"
        for i, val in importi_raw[~mask_importo_valido].items()
    ])

    # Maschera combinata per righe valide
    mask_ok = mask_data_valida & mask_importo_valido
    df_valid = df[mask_ok].copy()

    # Costruzione output
    output = pd.DataFrame()
    output['Codice dipendente'] = range(1, len(df_valid) + 1)  # Progressivo
    output['Codice voce'] = df_valid['Tratt. Fiscale'].map(
        mappa_causali_df.set_index('Trattamento')['Codice']
    ).fillna('')  # Codice causale mappato o vuoto
    output['Descrizione'] = ''
    output['Quantità'] = ''
    output['Base'] = ''
    output['Importo'] = (importi_float[mask_ok] * 100).round().astype('Int64')  # Cent.
    output['Periodo'] = df_valid['Data'].dt.strftime('%d%m%y').fillna('')
    output['Tipo elaborazione'] = ''

    return output, scarti


def convert_doubleyou(df, codice_azienda, mappa_causali_df):
    """
    Converte il DataFrame di DoubleYou nel formato di output richiesto.

    Args:
        df (pd.DataFrame): DataFrame input.
        codice_azienda (str): Codice azienda (non usato direttamente qui).
        mappa_causali_df (pd.DataFrame): Mappa causali per conversione.

    Returns:
        output (pd.DataFrame): DataFrame convertito.
        scarti (list): Lista di messaggi riguardanti record scartati.
    """
    df = df.copy()

    # Colonne essenziali da verificare
    required_columns = ['CodFisc', 'Tratt. Fiscale', 'Totale', 'Data Ordine']
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        raise ValueError(f"Colonne mancanti nel file DoubleYou: {', '.join(missing)}")

    scarti = []

    # Conversione data con formato italiano dd/mm/yyyy
    df['Data Ordine'] = pd.to_datetime(df['Data Ordine'], format='%d/%m/%Y', errors='coerce')
    mask_data_valida = df['Data Ordine'].notna()
    scarti.extend([
        f"Riga {i+2}: data non valida → '{val}'"
        for i, val in df.loc[~mask_data_valida, 'Data Ordine'].items()
    ])

    # Conversione importi da stringa (virgola->punto) a float
    importi_raw = df['Totale'].astype(str).str.replace(',', '.', regex=False)
    importi_float = pd.to_numeric(importi_raw, errors='coerce')
    mask_importo_valido = importi_float.notna()
    scarti.extend([
        f"Riga {i+2}: importo non valido → '{val}'"
        for i, val in importi_raw[~mask_importo_valido].items()
    ])

    # Maschera righe valide
    mask_ok = mask_data_valida & mask_importo_valido
    df_valid = df[mask_ok].copy()

    # Costruzione output
    output = pd.DataFrame()
    output['Codice dipendente'] = range(1, len(df_valid) + 1)
    output['Codice voce'] = df_valid['Tratt. Fiscale'].map(
        mappa_causali_df.set_index('Trattamento')['Codice']
    ).fillna('')
    output['Descrizione'] = ''
    output['Quantità'] = ''
    output['Base'] = ''
    output['Importo'] = (importi_float[mask_ok] * 100).round().astype('Int64')
    output['Periodo'] = df_valid['Data Ordine'].dt.strftime('%d%m%y').fillna('')
    output['Tipo elaborazione'] = ''

    return output, scarti
