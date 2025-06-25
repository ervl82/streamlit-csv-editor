import pandas as pd

# Carica la mappa causali una volta sola 
causali_df = pd.read_csv('mappa_causali.csv')

def get_codice_causale(trattamento):
    # Cerca nella mappa causali, restituisce codice o None se non trovato
    row = causali_df[causali_df['Trattamento'] == trattamento]
    if not row.empty:
        return row['Codice'].values[0]
    return None

def convert_coverflex(df, codice_azienda):
    df = df.copy()

    # Pulizia colonne: rimuovi righe vuote o intestazioni duplicate
    df = df.loc[df['Codice fiscale dipendente'].notnull()]

    # Correggi i tipi numerici e formati
    df['Importo'] = df['Importo'].astype(str).str.replace(',', '.').astype(float)

    # Costruisci il dataframe risultato
    result = pd.DataFrame()
    result['Codice dipendente'] = df['Codice fiscale dipendente']
    # Codice voce: mappato da 'Tratt. Fiscale'
    result['Codice voce'] = df['Tratt. Fiscale'].apply(get_codice_causale)
    result['Descrizione'] = ''
    result['Quantità'] = ''
    result['Base'] = ''
    # Importo moltiplicato per 100 e convertito in int
    result['Importo'] = (df['Importo'] * 100).round().astype(int)
    # Periodo: formato ddmmyy (giorno, mese, anno due cifre)
    result['Periodo'] = pd.to_datetime(df['Data'], dayfirst=True).dt.strftime('%d%m%y')
    result['Tipo elaborazione'] = ''
    # Codice progressivo
    result.insert(0, 'Progressivo', range(1, len(result) + 1))
    return result

def convert_doubleyou(df, codice_azienda):
    df = df.copy()

    # Pulizia colonne: rimuovi righe vuote o intestazioni duplicate
    df = df.loc[df['CodFisc'].notnull()]

    # Correggi importi
    df['Totale'] = df['Totale'].astype(str).str.replace(',', '.').astype(float)

    result = pd.DataFrame()
    result['Codice dipendente'] = df['CodFisc']
    # Codice voce: mappato da 'Tratt. Fiscale'
    result['Codice voce'] = df['Tratt. Fiscale'].apply(get_codice_causale)
    result['Descrizione'] = ''
    result['Quantità'] = ''
    result['Base'] = ''
    result['Importo'] = (df['Totale'] * 100).round().astype(int)
    # Per periodo: se c'è colonna 'Periodo' prova a convertire in ddmmyy, altrimenti usa 'Data Ordine'
    if 'Periodo' in df.columns:
        # Prova a convertire da testo tipo "aprile - 2025" a formato ddmmyy: lo mettiamo a '' perché non è una data precisa
        result['Periodo'] = ''
    else:
        result['Periodo'] = pd.to_datetime(df['Data Ordine'], dayfirst=True).dt.strftime('%d%m%y')

    result['Tipo elaborazione'] = ''
    result.insert(0, 'Progressivo', range(1, len(result) + 1))
    return result

def convert_file(df, codice_azienda, provider):
    if provider == 'Coverflex':
        return convert_coverflex(df, codice_azienda)
    elif provider == 'DoubleYou':
        return convert_doubleyou(df, codice_azienda)
    else:
        raise ValueError('Provider non supportato')
