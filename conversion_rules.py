import pandas as pd  # Libreria per la manipolazione dei dati

def convert_coverflex(df, codice_azienda, mappa_causali_df):
    df = df.copy()  # Crea una copia del DataFrame per evitare modifiche all’originale

    # Converte la colonna 'Data' in formato datetime, assumendo giorno prima del mese
    df['Data'] = pd.to_datetime(df['Data'], dayfirst=True, errors='coerce')

    output = pd.DataFrame()  # Crea un nuovo DataFrame vuoto per l’output
    output['Codice dipendente'] = range(1, len(df) + 1)  # Assegna numeri progressivi

    # Mappa la causale usando la tabella "mappa_causali_df"
    output['Codice voce'] = df['Tratt. Fiscale'].map(
        mappa_causali_df.set_index('Trattamento')['Codice']
    ).fillna('')  # Se non trovata, lascia vuoto

    # Colonne fisse o vuote nel file di destinazione
    output['Descrizione'] = ''
    output['Quantità'] = ''
    output['Base'] = ''

    # Converte 'Importo' da stringa con virgola a float, moltiplica per 100 e arrotonda
    output['Importo'] = (
        df['Importo']
        .astype(str)
        .str.replace('.', '', regex=False)       # Rimuove punti (es. 2.590.00 → 259000)
        .str.replace(',', '.', regex=False)      # Converte la virgola in punto
        .astype(float) * 100
    ).round().astype('Int64')


    # Estrae la data nel formato richiesto ddmmyy
    output['Periodo'] = df['Data'].dt.strftime('%d%m%y').fillna('')
    output['Tipo elaborazione'] = ''  # Colonna vuota

    return output  # Restituisce il DataFrame convertito


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
