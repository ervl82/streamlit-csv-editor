Convertitore di file per provider di welfare aziendale
Scenario
La nostra azienda gestisce piani di welfare per clienti che utilizzano diversi provider esterni (ad es. Coverflex, DoubleYou). Ogni provider permette di scaricare un file di estrazione (CSV) con i movimenti di spesa dei dipendenti, ma il formato varia per struttura e nomenclatura delle colonne. Dobbiamo quindi normalizzare questi file in un formato interno standard per poterli caricare nei nostri sistemi.
Obiettivo del progetto
Realizzare un piccolo servizio (“convertitore di file”) che:
riceve in input:
Codice azienda (Il numero della ditta)
Provider (Coverflex o DoubleYou)
File di origine (il file da convertire, in formato CSV )
applica le regole di conversione specifiche del provider scelto
restituisce un file nel Formato Standard Interno (CSV) pronto per l’import
Requisiti funzionali
Autodeterminazione della logica di conversione: in base al provider selezionato, carica un set di regole per la conversione specifiche di quel provider
Gestione errori: messaggi chiari in caso di record scartati o formati non riconosciuti.
Performance: gestire file fino a 1000 righe in < 30 s.
Requisiti tecnici
Puoi sviluppare lo strumento in qualsiasi ambiente tu voglia: con coding, con degli strumenti no-code, con google sheet. L’importante è che:
funzioni
sia disponibile online e tutti ci possano accedere
prende un file come input (clicchi un pulsante e ti fa selezionare il file) e restituisce un file di export (clicchi un pulsante e lo scarica oppure un link da cui posso scaricare il file)
Bonus: se riesce a supportare conversioni simulanee ancora meglio
Interfaccia utente minima
+----------------------------------+
| Codice azienda: [___________]    |
| Provider:   (•) Coverflex        |
|             ( ) DoubleYou        |
| File input:  [ Scegli file ]     |
|                                  |
|      [   Converti   ]            |
+----------------------------------+
​
Tutto ciò che aggiungi rispetto a quanto richiesto è a tua discrezione.
File di output
Il file di output deve avere le seguenti colonne, con le seguenti regole di formato.
Codice dipendente
Codice voce
Descrizione
Quantità
Base
Importo
Periodo
Tipo elaborazione
Un codice progressivo che inizia da 1
Codice Causale corrispondentemappato secondo le “Voci Welfare”
Lasciare vuoto
Lasciare vuoto
Lasciare vuoto
Importo della rimborso moltiplicato per 100 (1€ --> 100)
Data riga nel formato ddmmyy (2025-03-01 --> 010325)
Lasciare vuoto
Esempio
⬅️ Input
ID Dipendente
Tratt. Fiscale
Tipologia
Tratt. Busta
Importo
Data
Tipologia welfare
Dipendente 1
Rimb. art. 51 comma 2 lett. f-ter
15 - Spese per assistenza domiciliare
Figurativo
0,17
1/3/2025
Welfare On Top
Dipendente 2
Rimb. art. 51 comma 2 lett. f-bis
Spese testi scolastici
Figurativo
274,62
1/3/2025
Welfare On Top
Dipendente 3
Rimb. art. 51 comma 2 lett. f-bis
12 - Spese ludoteche
Figurativo
14,99
2/3/2025
Welfare On Top
➡️ Output
Codice dipendente
Codice voce
Descrizione
Quantità
Base
Importo
Periodo
Tipo elaborazione
1
376
17
010325
2
375
27462
010325
3
375
1499
020325
