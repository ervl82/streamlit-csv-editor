import pandas as pd

def load_causal_map():
    return pd.read_csv("mappa_causali.csv", sep=",", encoding="utf-8")

def convert_coverflex(df, company_code, causal_map):
    df.columns = df.columns.str.strip()
    
    df = df[df.columns[df.columns.str.contains("Codice fiscale dipendente|Importo|Data|Tratt. Fiscale", case=False, na=False)]]
    df.columns = ["Codice fiscale dipendente", "Importo", "Data", "Tratt. Fiscale"]

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
    df["Progressivo"] = range(1, len(df) + 1)

    final = df[["Codice dipendente", "Codice voce", "Descrizione", "Quantità", "Base", "Importo", "Periodo", "Tipo elaborazione"]]
    return final

def convert_doubleyou(df, company_code, causal_map):
    df.columns = df.columns.str.strip()
    
    df = df[df.columns[df.columns.str.contains("CodFisc|Totale|Data Ordine|Tratt. Fiscale", case=False, na=False)]]
    df.columns = ["Codice fiscale dipendente", "Importo", "Data", "Tratt. Fiscale"]

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
    df["Progressivo"] = range(1, len(df) + 1)

    final = df[["Codice dipendente", "Codice voce", "Descrizione", "Quantità", "Base", "Importo", "Periodo", "Tipo elaborazione"]]
    return final
