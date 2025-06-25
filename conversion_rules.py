import pandas as pd

def mappa_causali(trattamento_series, mappa_df):
    """
    Mappa la colonna 'Trattamento Fiscale' usando la mappa causali fornita.
    Se la voce non è presente nella mappa, restituisce 'WF01' come default.
    """
    mapping = dict(zip(
        mappa_df["Trattamento Fiscale"].astype(str),
        mappa_df["Codice Causale"].astype(str)
    ))
    return trattamento_series.map(mapping).fillna("WF01")


def convert_coverflex(df, codice_azienda, mappa_causali_df):
    """
    Conversione del file Coverflex nel formato standard interno.
    """
    df_out = pd.DataFrame()
    df_out["Codice dipendente"] = df["Employee ID"]
    df_out["Codice voce"] = "WELF01"
    df_out["Descrizione"] = df["Spesa"]
    df_out["Quantità"] = 1
    df_out["Base"] = ""
    df_out["Importo"] = df["Importo"].astype(float) * 100
    df_out["Periodo"] = pd.to_datetime(df["Data"], dayfirst=True).dt.strftime("%Y%m")
    df_out["Tipo elaborazione"] = "W"
    df_out["Codice progressivo"] = range(1, len(df) + 1)
    df_out["Codice Causale"] = mappa_causali(df["Tratt. Fiscale"], mappa_causali_df)
    df_out["Colonna 11"] = ""
    df_out["Colonna 12"] = ""
    df_out["Colonna 13"] = ""
    df_out["Importo x100"] = df_out["Importo"]
    df_out["Data ddmmyy"] = pd.to_datetime(df["Data"], dayfirst=True).dt.strftime("%d%m%y")
    df_out["Colonna 16"] = ""

    return df_out


def convert_doubleyou(df, codice_azienda, mappa_causali_df):
    """
    Conversione del file DoubleYou nel formato standard interno.
    """
    df_out = pd.DataFrame()
    df_out["Codice dipendente"] = df["ID Dipendente"]
    df_out["Codice voce"] = "WELF01"
    df_out["Descrizione"] = df["Descrizione Voce"]
    df_out["Quantità"] = 1
    df_out["Base"] = ""
    df_out["Importo"] = df["Importo"].astype(float) * 100
    df_out["Periodo"] = pd.to_datetime(df["Data"], dayfirst=True).dt.strftime("%Y%m")
    df_out["Tipo elaborazione"] = "W"
    df_out["Codice progressivo"] = range(1, len(df) + 1)
    df_out["Codice Causale"] = mappa_causali(df["Tratt. Fiscale"], mappa_causali_df)
    df_out["Colonna 11"] = ""
    df_out["Colonna 12"] = ""
    df_out["Colonna 13"] = ""
    df_out["Importo x100"] = df_out["Importo"]
    df_out["Data ddmmyy"] = pd.to_datetime(df["Data"], dayfirst=True).dt.strftime("%d%m%y")
    df_out["Colonna 16"] = ""

    return df_out
