import pandas as pd

def mappa_causali(tratt_fiscale_series, mappa_df):
    """
    Mappa i valori di 'Tratt. Fiscale' con i codici causali dalla mappa.
    Se non trova corrispondenza, restituisce stringa vuota.
    """
    mappa_dict = dict(zip(mappa_df['Trattamento Fiscale'], mappa_df['Codice Causale']))
    return tratt_fiscale_series.map(mappa_dict).fillna("")

def convert_coverflex(df, codice_azienda, mappa_causali_df):
    df_out = pd.DataFrame()
    df_out["Codice dipendente"] = df["Codice fiscale dipendente"]
    df_out["Codice voce"] = "WELF01"  # esempio codice voce fisso
    df_out["Descrizione"] = ""
    df_out["Quantità"] = ""
    df_out["Base"] = ""
    # Converti importo da stringa a float e moltiplica per 100
    df_out["Importo"] = df["Importo"].astype(str).str.replace(",", ".").astype(float) * 100
    # Data nel formato ddmmyy
    df_out["Periodo"] = pd.to_datetime(df["Data"], dayfirst=True).dt.strftime("%d%m%y")
    df_out["Tipo elaborazione"] = ""
    df_out["Codice progressivo"] = range(1, len(df) + 1)
    df_out["Codice Causale"] = mappa_causali(df["Tratt. Fiscale"], mappa_causali_df)

    # Colonne extra vuote se serve (adatta in base ai tuoi requisiti)
    df_out["Colonna 11"] = ""
    df_out["Colonna 12"] = ""
    df_out["Colonna 13"] = ""

    return df_out

def convert_doubleyou(df, codice_azienda, mappa_causali_df):
    df_out = pd.DataFrame()
    df_out["Codice dipendente"] = df["CodFisc"]
    df_out["Codice voce"] = "WELF02"  # esempio codice voce fisso
    df_out["Descrizione"] = ""
    df_out["Quantità"] = ""
    df_out["Base"] = ""
    df_out["Importo"] = df["Totale"].astype(str).str.replace(",", ".").astype(float) * 100
    df_out["Periodo"] = pd.to_datetime(df["Data Ordine"], dayfirst=True).dt.strftime("%d%m%y")
    df_out["Tipo elaborazione"] = ""
    df_out["Codice progressivo"] = range(1, len(df) + 1)
    df_out["Codice Causale"] = mappa_causali(df["Tratt. Fiscale"], mappa_causali_df)

    df_out["Colonna 11"] = ""
    df_out["Colonna 12"] = ""
    df_out["Colonna 13"] = ""

    return df_out
