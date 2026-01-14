import requests

# --- CONFIGURAZIONE ---
# 1. Vai su https://github.com/settings/tokens
# 2. Genera un nuovo token (Classic) con permessi 'repo'
# 3. Incolla il token qui sotto
GITHUB_TOKEN = "INCOLLA_QUI_IL_TUO_TOKEN"

# Inserisci il tuo username e il nome del repo
REPO_OWNER = "NinNonNan" 
REPO_NAME = "biometric" 
# ----------------------

BASE_URL = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/labels"
HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

# Lista delle etichette da creare
LABELS = [
    # Tipi di attività (Cosa?)
    {"name": "bug", "color": "d73a4a", "description": "Qualcosa non funziona come dovrebbe."},
    {"name": "feature", "color": "a2eeef", "description": "Una nuova funzionalità o una richiesta utente."},
    {"name": "documentation", "color": "0075ca", "description": "Miglioramenti o aggiunte alla documentazione."},
    {"name": "chore", "color": "cfd3d7", "description": "Attività di manutenzione (refactoring, aggiornamento dipendenze)."},
    {"name": "testing", "color": "f9d0c4", "description": "Aggiunta o miglioramento dei test."},

    # Aree del progetto (Dove?)
    {"name": "api", "color": "5319e7", "description": "Riguarda gli endpoint dell'API (/update, /data)."},
    {"name": "backend", "color": "1d76db", "description": "Logica del server Flask, calcoli, gestione dati."},
    {"name": "core", "color": "fbca04", "description": "Logica di business principale (calcolo biometrico)."},
    {"name": "frontend", "color": "00cc00", "description": "Interfaccia utente (HTML, CSS, JS, stile Pip-Boy)."},
    {"name": "deploy", "color": "d4c5f9", "description": "Configurazione del deploy, webhook, PythonAnywhere."},
]

def setup_github_labels():
    print(f"--- Configurazione Label per {REPO_OWNER}/{REPO_NAME} ---")
    
    for label in LABELS:
        # Tentativo di creazione
        response = requests.post(BASE_URL, json=label, headers=HEADERS)
        
        if response.status_code == 201:
            print(f"[CREATA] {label['name']}")
        elif response.status_code == 422:
            # Se esiste già (422 Validation Failed), proviamo ad aggiornarla per fissare colore/descrizione
            print(f"[ESISTE] {label['name']} -> Aggiorno dettagli...")
            requests.patch(f"{BASE_URL}/{requests.utils.quote(label['name'])}", json=label, headers=HEADERS)
        else:
            print(f"[ERRORE] {label['name']}: {response.status_code} - {response.text}")

if __name__ == "__main__":
    setup_github_labels()
