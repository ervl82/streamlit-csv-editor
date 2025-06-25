import pandas as pd

def load_causal_map():
    df = pd.read_csv("mappa_causali.csv", sep=",")
    mapping = dict(zip(df["Trattamento"], df["Codice"]))
    return mapping

def convert_coverflex(df, mapping):
    df.columns = df.columns.str.strip()

    # Elimina righe non dati (es. intestazioni extra)
    df = df[df["Codice fiscale dipendente"].notna()]
    df = df[df["Codice fiscale dipendente"].str.contains(r"\w+", na=False)]

    output = []
    for idx, row in df.iterrows():
        codice_dip = row["Codice fiscale dipendente"]
        codice_voce = ""
        descrizione = row["Tratt. Fiscale"]
        quantita = "1"
        base = ""
        try:
            importo_float = float(str(row["Importo"]).replace(",", "."))
        except:
            importo_float = 0.0
        importo = f"{importo_float:.2f}"
        periodo = ""
        tipo_elab = ""
        progressivo = idx + 1
        codice_causale = mapping.get(str(row["Tratt. Fiscale"]).strip(), "")
        vuoto1 = ""
        vuoto2 = ""
        vuoto3 = ""
        importo_cent = int(round(importo_float * 100))
        try:
            data_riga = pd.to_datetime(row["Data"], dayfirst=True)
        except:
            data_riga = pd.to_datetime("1900-01-01")
        data_riga_str = data_riga.strftime("%d%m%y")
        vuoto4 = ""

        output.append([
            codice_dip, codice_voce, descrizione, quantita, base, importo,
            periodo, tipo_elab, progressivo, codice_causale,
            vuoto1, vuoto2, vuoto3,
            importo_cent, data_riga_str, vuoto4
        ])

    columns = [
        "Codice dipendente", "Codice voce", "Descrizione", "Quantità", "Base", "Importo",
        "Periodo", "Tipo elaborazione", "Progressivo", "Codice Causale",
        "Vuoto1", "Vuoto2", "Vuoto3",
        "Importo cent", "Data riga", "Vuoto4"
    ]

    return pd.DataFrame(output, columns=columns)

def convert_doubleyou(df, mapping):
    df.columns = df.columns.str.strip()

    df = df[df["CodFisc"].notna()]
    df = df[df["CodFisc"].str.contains(r"\w+", na=False)]

    output = []
    for idx, row in df.iterrows():
        codice_dip = row["CodFisc"]
        codice_voce = ""
        descrizione = row["Tratt. Fiscale"]
        quantita = "1"
        base = ""
        try:
            importo_float = float(str(row["Totale"]).replace(",", "."))
        except:
            importo_float = 0.0
        importo = f"{importo_float:.2f}"
        periodo = ""
        tipo_elab = ""
        progressivo = idx + 1
        codice_causale = mapping.get(str(row["Tratt. Fiscale"]).strip(), "")
        vuoto1 = ""
        vuoto2 = ""
        vuoto3 = ""
        importo_cent = int(round(importo_float * 100))
        try:
            data_riga = pd.to_datetime(row["Data Ordine"], dayfirst=True)
        except:
            data_riga = pd.to_datetime("1900-01-01")
        data_riga_str = data_riga.strftime("%d%m%y")
        vuoto4 = ""

        output.append([
            codice_dip, codice_voce, descrizione, quantita, base, importo,
            periodo, tipo_elab, progressivo, codice_causale,
            vuoto1, vuoto2, vuoto3,
            importo_cent, data_riga_str, vuoto4
        ])

    columns = [
        "Codice dipendente", "Codice voce", "Descrizione", "Quantità", "Base", "Importo",
        "Periodo", "Tipo elaborazione", "Progressivo", "Codice Causale",
        "Vuoto1", "Vuoto2", "Vuoto3",
        "Importo cent", "Data riga", "Vuoto4"
    ]

    return pd.DataFrame(output, columns=columns)
