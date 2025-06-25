import pandas as pd
import re

# Funzione per pulire e convertire importi con virgole e punti
def clean_importo(val):
    if pd.isna(val):
        return 0
    val_str = str(val).strip()
    val_str = val_str.replace(' ', '')
    if '.' in val_str and ',' in val_str:
        val_str = val_str.replace('.', '').replace(',', '.')
    elif ',' in val_str:
        val_str = val_str.replace(',', '.')
    val_str = re.sub(r'[^0-9.]', '', val_str)
    try:
        return float(val_str)
    except:
        return 0

# Carico mappa causali da file CSV
mappa_causali = pd.read_csv('mappa_causali.csv', encoding='utf-8')
causali_dict = dict(zip(mappa_causali['Trattamento'].str.strip(), mappa_causali['Codice']))

def convert_coverflex(df, codice_azienda):
    output_rows = []
    progressivo = 1
    for _, row in df.iterrows():
        # Mapping colonne input
        codice_dipendente = row.get('Codice fiscale dipendente', '').strip()
        trattamento = row.get('Tratt. Fiscale', '').strip()
        importo_raw = row.get('Importo', 0)
        data_raw = row.get('Data', '')
        
        importo = clean_importo(importo_raw)
        importo = int(importo * 100)  # moltiplico per 100
        
        # Parsing data dd/mm/yyyy o yyyy-mm-dd
        data_str = ''
        for fmt in ('%d/%m/%Y', '%Y-%m-%d', '%d-%m-%Y'):
            try:
                data_str = pd.to_datetime(data_raw, format=fmt).strftime('%d%m%y')
                break
            except:
                pass
        if data_str == '':
            try:
                # Provo parser generico
                data_str = pd.to_datetime(data_raw, dayfirst=True).strftime('%d%m%y')
            except:
                data_str = '000000'  # fallback

        codice_causale = causali_dict.get(trattamento, '')
        
        output_rows.append({
            'Codice dipendente': codice_dipendente,
            'Codice voce': progressivo,
            'Descrizione': '',
            'Quantità': '',
            'Base': '',
            'Importo': importo,
            'Periodo': data_str,
            'Tipo elaborazione': '',
            'Codice causale': codice_causale
        })
        progressivo += 1
    return pd.DataFrame(output_rows)

def convert_doubleyou(df, codice_azienda):
    output_rows = []
    progressivo = 1
    for _, row in df.iterrows():
        codice_dipendente = row.get('CodFisc', '').strip()
        trattamento = row.get('Tratt. Fiscale', '').strip()
        importo_raw = row.get('Totale', 0)
        data_raw = row.get('Data Ordine', '')
        
        importo = clean_importo(importo_raw)
        importo = int(importo * 100)
        
        data_str = ''
        for fmt in ('%d/%m/%Y', '%Y-%m-%d', '%d-%m-%Y'):
            try:
                data_str = pd.to_datetime(data_raw, format=fmt).strftime('%d%m%y')
                break
            except:
                pass
        if data_str == '':
            try:
                data_str = pd.to_datetime(data_raw, dayfirst=True).strftime('%d%m%y')
            except:
                data_str = '000000'

        codice_causale = causali_dict.get(trattamento, '')
        
        output_rows.append({
            'Codice dipendente': codice_dipendente,
            'Codice voce': progressivo,
            'Descrizione': '',
            'Quantità': '',
            'Base': '',
            'Importo': importo,
            'Periodo': data_str,
            'Tipo elaborazione': '',
            'Codice causale': codice_causale
        })
        progressivo += 1
    return pd.DataFrame(output_rows)

def convert_file(df, codice_azienda, provider):
    if provider == 'Coverflex':
        return convert_coverflex(df, codice_azienda)
    elif provider == 'DoubleYou':
        return convert_doubleyou(df, codice_azienda)
    else:
        raise ValueError('Provider non supportato')
