"""
Server Python per PIP-BOY Biometric Overlay
-------------------------------------------

Funzionalità principali:
1. Riceve aggiornamenti di frequenza cardiaca tramite POST /update
2. Calcola:
   - HR corrente
   - HR media (ultimi 60 valori)
   - Delta HR (HR corrente - media)
   - Stress index (derivato dal delta HR)
   - Stato: CALM, TENSE, CRITICAL
3. Scrive un file di log CSV "biometrics_log.csv" con tutte le informazioni
4. Espone:
   - GET / → mostra pagina HTML stile Pip-Boy con cuore pulsante
   - Aggiornamento dati tramite refresh automatico della pagina
"""

from flask import Flask, request, jsonify, render_template
from datetime import datetime
from collections import deque
import csv
import os

app = Flask(__name__)

# Dati correnti
hr_data = {
    "ts": "--",
    "hr": "--",
    "hr_avg": "--",
    "delta_hr": "--",
    "stress": "--",
    "state": "WAITING"
}
hr_list = deque(maxlen=60)

# File CSV per log
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(BASE_DIR, "biometrics_log.csv")
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp","hr","hr_avg","delta_hr","stress","state"])

# Funzione per limitare i valori tra min e max
def clamp(value, min_val=0, max_val=100):
    return max(min_val, min(value, max_val))

# Route per aggiornare i dati HR tramite POST
@app.route('/update', methods=['POST'])
def update_hr():
    global hr_data, hr_list
    data = request.json
    if not data or 'hr' not in data:
        return jsonify({"error": "HR mancante"}), 400

    try:
        hr = int(data['hr'])
    except (ValueError, TypeError):
        return jsonify({"error": "HR deve essere un numero intero"}), 400

    raw_ts = data.get('ts')
    if raw_ts:
        try:
            ts_int = int(float(raw_ts))
            ts = datetime.fromtimestamp(ts_int).strftime("%Y-%m-%d %H:%M:%S")
        except:
            ts = f"INVALID_TS:{raw_ts}"
    else:
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    hr_list.append(hr)

    hr_avg = sum(hr_list) / len(hr_list)
    delta_hr = hr - hr_avg
    stress = clamp(abs(delta_hr) * 5)

    if stress < 30:
        state = "CALM"
    elif stress < 60:
        state = "TENSE"
    else:
        state = "CRITICAL"

    hr_data.update({
        "ts": ts,
        "hr": hr,
        "hr_avg": round(hr_avg,1),
        "delta_hr": round(delta_hr,1),
        "stress": round(stress,1),
        "state": state
    })

    # Scrivi log CSV
    with open(LOG_FILE, mode='a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([ts, hr, round(hr_avg,1), round(delta_hr,1), round(stress,1), state])

    return jsonify({"status": "ok"}), 200

# Route per ottenere i dati correnti (AJAX)
@app.route('/data')
def get_data():
    return jsonify(hr_data)

# Route principale: mostra pagina HTML Pip-Boy con dati attuali
@app.route('/')
def index():
    return render_template('index.html', hr_data=hr_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False)
