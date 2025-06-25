import pandas as pd

def load_causal_map():
    return pd.read_csv("mappa_causali.csv", encoding="utf-8")

def convert_coverflex(df, company_code, causal_map):
    df.columns = df.columns.str.strip()

    # Trova la riga di intestazione corretta
    header_row = df[df.iloc[:, 0].str.contains("Codice fiscale dipendente", na=False)].index[0]
    df = pd.read_csv("coverflex.csv", skiprows=header_row)

    df["Importo"] = df["Importo"].astype(str).str.replace(".", "", regex=False).str.replace(",", ".", regex=False)
    df["Importo"] = df["Importo"].astype(float)

    df["Codice dipendente"] = df["Codice fiscale dipendente"]
    df["Codice voce"] = df["Tratt. Fiscale"].map(dict(zip(causal_map["Trattamento"], causal_map["Codice"])))
    df["Descrizione"] = ""
    df["Quantità"] = ""
    df["Base"] = ""
    df["Importo"] = (df["Importo"] * 100).round().astype(int)
    df["Periodo"] = pd.to_datetime(df["Data"], dayfirst=True).dt.strftime("%d%m%y")
    df["Tipo elaborazione"] = ""

    return df[["Codice dipendente", "Codice voce", "Descrizione", "Quantità", "Base", "Importo", "Periodo", "Tipo elaborazione"]]

def convert_doubleyou(df, company_code, causal_map):
    df.columns = df.columns.str.strip()

    df["Importo"] = df["Totale"].astype(str).str.replace(".", "", regex=False).str.replace(",", ".", regex=False)
    df["Importo"] = df["Importo"].astype(float)

    df["Codice dipendente"] = df["CodFisc"]
    df["Codice voce"] = df["Tratt. Fiscale"].map(dict(zip(causal_map["Trattamento"], causal_map["Codice"])))
    df["Descrizione"] = ""
    df["Quantità"] = ""
    df["Base"] = ""
    df["Importo"] = (df["Importo"] * 100).round().astype(int)
    df["Periodo"] = pd.to_datetime(df["Data Ordine"], dayfirst=True).dt.strftime("%d%m%y")
    df["Tipo elaborazione"] = ""

    return df[["Codice dipendente", "Codice voce", "Descrizione", "Quantità", "Base", "Importo", "Periodo", "Tipo elaborazione"]]
