import pandas as pd

def convert_coverflex(df, codice_azienda, mappa_causali_df):
    df = df.copy()

    # Conversione della data: dayfirst=True, errore convertito in NaT
    df['Data'] = pd.to_datetime(df['Data'], dayfirst=True, errors='coerce')

    output = pd.DataFrame()
    output['Codice dipendente'] = df['Codice fiscale dipendente']
    output['Codice voce'] = range(1, len(df) + 1)
    output['Codice causale'] = df['Tratt. Fiscale'].map(mappa_causali_df.set_index('Trattamento')['Codice']).fillna('')

    output['Descrizione'] = ''
    output['Quantità'] = ''
    output['Base'] = ''
    # Moltiplica per 100 e arrotonda importo
    output['Importo'] = (df['Importo'].str.replace(',', '.').astype(float) * 100).round().astype('Int64')
    output['Periodo'] = df['Data'].dt.strftime('%d%m%y').fillna('')
    output['Tipo elaborazione'] = ''

    return output

def convert_doubleyou(df, codice_azienda, mappa_causali_df):
    df = df.copy()

    df['Data Ordine'] = pd.to_datetime(df['Data Ordine'], dayfirst=True, errors='coerce')

    output = pd.DataFrame()
    output['Codice dipendente'] = df['CodFisc']
    output['Codice voce'] = range(1, len(df) + 1)
    output['Codice causale'] = df['Tratt. Fiscale'].map(mappa_causali_df.set_index('Trattamento')['Codice']).fillna('')

    output['Descrizione'] = ''
    output['Quantità'] = ''
    output['Base'] = ''
    output['Importo'] = (df['Totale'].astype(float) * 100).round().astype('Int64')
    output['Periodo'] = df['Data Ordine'].dt.strftime('%d%m%y').fillna('')
    output['Tipo elaborazione'] = ''

    return output
