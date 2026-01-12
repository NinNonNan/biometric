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

from flask import Flask, request, jsonify
from datetime import datetime
import csv
import os

app = Flask(__name__)

# Dati correnti
hr_data = {
    "ts": None,
    "hr": None,
    "hr_avg": None,
    "delta_hr": None,
    "stress": None,
    "state": None
}
hr_list = []

# File CSV per log
LOG_FILE = "biometrics_log.csv"
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

    hr = int(data['hr'])
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
    if len(hr_list) > 60:
        hr_list.pop(0)

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

# Route principale: mostra pagina HTML Pip-Boy con dati attuali
@app.route('/')
def index():
    critical_class = "critical" if hr_data["state"] == "CRITICAL" else ""
    return f"""
<!DOCTYPE html>
<html>
<head>
    <title>PIP-BOY BIOMETRICS</title>
    <meta http-equiv="refresh" content="1">
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='0.9em' font-size='90'>♥</text></svg>">
    <style>
        body {{
            background-color:#000;
            margin:0;
            padding:0;
            display:flex;
            justify-content:center;
            align-items:center;
            height:100vh;
            font-family:'Fira Mono', monospace;
        }}
        .screen {{
            position: relative;
            width: 400px;
            background-color: #013d1a;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 0 20px rgba(0,255,0,0.4) inset;
            color: #0c0;
            overflow: hidden;
        }}
        .screen:after {{
            background-image: linear-gradient(transparent, transparent 3px, #022);
            background-size: 4px 4px;
            position: absolute;
            top:0; left:0; right:0; bottom:0;
            content:"";
            pointer-events:none;
            z-index:1;
        }}
        @keyframes pulse {{
            from{{transform:scale(1)}} to{{transform:scale(1.3)}}
        }}
        .heart {{
            display:inline-block;
            animation:pulse 1s ease-in-out infinite alternate;
            font-size:54px;
            line-height:1;
            vertical-align:middle;
            margin-right:10px;
        }}
        .hr-box {{
            display:flex;
            justify-content:center;
            align-items:center;
            font-size:54px;
            margin-bottom:20px;
        }}
        .state {{
            text-align:center;
            font-size:1.5em;
            margin-bottom:20px;
        }}
        .critical {{ color:#ff5555; }}
        .details {{
            font-size:16px;
            text-align:left;
            line-height:1.5;
        }}
        .label {{ opacity:0.7; margin-right:5px; }}
    </style>
</head>
<body>
    <div class="screen">
        <div class="hr-box">
            <span class="heart">♥</span><span>{hr_data["hr"]} BPM</span>
        </div>
        <div class="state {critical_class}">{hr_data["state"]}</div>
        <div class="details">
            <div><span class="label">AVG HR:</span>{hr_data["hr_avg"]}</div>
            <div><span class="label">Δ HR:</span>{hr_data["delta_hr"]}</div>
            <div><span class="label">STRESS IDX:</span>{hr_data["stress"]}</div>
            <div><span class="label">TIME:</span>{hr_data["ts"]}</div>
        </div>
    </div>
</body>
</html>
"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
