# PIP-BOY Biometric Overlay

Un server Python leggero basato su Flask che funge da backend per un'interfaccia biometrica a tema "Pip-Boy" (Fallout). Il sistema riceve dati sulla frequenza cardiaca, calcola i livelli di stress e visualizza le informazioni in una dashboard web in stile retrò.

## Funzionalità

*   **Monitoraggio in Tempo Reale**: Riceve aggiornamenti della frequenza cardiaca tramite API REST.
*   **Analisi Dati**: Calcola automaticamente:
    *   Media HR (ultimi 60 valori).
    *   Delta HR (differenza dalla media).
    *   Indice di Stress.
    *   Stato dell'utente (CALM, TENSE, CRITICAL).
*   **Interfaccia Pip-Boy**: Dashboard HTML/CSS integrata con animazioni e stile fosforo verde.
*   **Data Logging**: Salva tutti i dati ricevuti in un file `biometrics_log.csv` per analisi successive.

## Prerequisiti

*   Python 3.x
*   Flask

## Installazione

1.  Clona questo repository o scarica i file.
2.  Installa le dipendenze necessarie:

```bash
pip install flask
```

## Utilizzo

1.  Avvia il server:

```bash
python server.py
```

2.  Apri il browser e vai all'indirizzo: `http://localhost:8000` (o l'IP della macchina se in rete locale).

## API Endpoints

### Aggiornamento Dati

*   **URL**: `/update`
*   **Metodo**: `POST`
*   **Content-Type**: `application/json`

**Parametri Body:**

| Parametro | Tipo | Descrizione |
| :--- | :--- | :--- |
| `hr` | `int` | Frequenza cardiaca corrente (BPM). Obbligatorio. |
| `ts` | `float` | Timestamp (opzionale). Se omesso, usa l'ora del server. |

**Esempio di richiesta (Python):**

```python
import requests

url = "http://localhost:8000/update"
data = {"hr": 75}

response = requests.post(url, json=data)
print(response.json())
```

**Esempio di richiesta (cURL):**

```bash
curl -X POST http://localhost:8000/update -H "Content-Type: application/json" -d '{"hr": 80}'
```

## Log Dati

Il file `biometrics_log.csv` viene creato automaticamente nella stessa directory dello script e contiene lo storico delle sessioni.