import pandas as pd

def convert_coverflex(df, codice_azienda, mappa_causali_df):
    df = df.copy()  # Evita modifiche all'originale

    # ✅ Conversione sicura della data in formato italiano dd/mm/yyyy
    df['Data'] = pd.to_datetime(df['Data'], dayfirst=True, errors='coerce')

    output = pd.DataFrame()

    # Numero progressivo come codice dipendente
    output['Codice dipendente'] = range(1, len(df) + 1)

    # Mappatura del codice causale
    output['Codice voce'] = df['Tratt. Fiscale'].map(
        mappa_causali_df.set_index('Trattamento')['Codice']
    ).fillna('')

    # Colonne placeholder vuote
    output['Descrizione'] = ''
    output['Quantità'] = ''
    output['Base'] = ''

    # ✅ Conversione sicura dell'importo da formato italiano a centesimi interi
    output['Importo'] = (
        df['Importo']
        .astype(str)
        .str.replace('.', '', regex=False)       # Rimuove il separatore delle migliaia
        .str.replace(',', '.', regex=False)      # Converte la virgola in punto decimale
        .astype(float) * 100                     # Moltiplica per 100 per ottenere i centesimi
    ).round().astype('Int64')

    # ✅ Formatta la data come stringa nel formato richiesto ddmmyy
    output['Periodo'] = df['Data'].dt.strftime('%d%m%y')

    # Colonna vuota richiesta
    output['Tipo elaborazione'] = ''

    return output


def convert_doubleyou(df, codice_azienda, mappa_causali_df):
    df = df.copy()  # Crea una copia del DataFrame

    # Converte 'Data Ordine' in formato datetime
    df['Data Ordine'] = pd.to_datetime(df['Data Ordine'], dayfirst=True, errors='coerce')

    output = pd.DataFrame()
    output['Codice dipendente'] = df['CodFisc']  # Colonna codice fiscale
    output['Codice voce'] = range(1, len(df) + 1)  # Numerazione sequenziale

    # Mappa la causale
    output['Codice causale'] = df['Tratt. Fiscale'].map(
        mappa_causali_df.set_index('Trattamento')['Codice']
    ).fillna('')  # Se non trovata, lascia vuoto

    output['Descrizione'] = ''
    output['Quantità'] = ''
    output['Base'] = ''

    # Gestione dei decimali con virgola → punto → float → centesimi → int
    output['Importo'] = (
        df['Totale']
        .astype(str)
        .str.replace('.', '', regex=False)       # Rimuove punti (es. 2.590.00 → 259000)
        .str.replace(',', '.', regex=False)      # Converte la virgola in punto
        .astype(float) * 100
    ).round().astype('Int64')


    # Estrazione del periodo in formato ddmmyy
    output['Periodo'] = df['Data Ordine'].dt.strftime('%d%m%y').fillna('')
    output['Tipo elaborazione'] = ''

    return output  # Restituisce il risultato finale
