import os
import requests
import json

# --- CONFIGURAZIONE ---
# Assicurati che questo corrisponda al tuo repository GitHub
REPO_OWNER_AND_NAME = "NinNonNan/biometric"
GITHUB_API_URL = f"https://api.github.com/repos/{REPO_OWNER_AND_NAME}/labels"

# Legge il token da una variabile d'ambiente per sicurezza.
# MAI scrivere il token direttamente qui!
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# Definisci le etichette che vuoi creare nel tuo repository
LABELS_TO_CREATE = [
    {"name": "api", "color": "fbca04", "description": "Interfacce API e comunicazione server"},
    {"name": "bug", "color": "d73a4a", "description": "Qualcosa non funziona"},
    {"name": "chore", "color": "f9d0c4", "description": "Manutenzione ordinaria e dipendenze"},
    {"name": "core", "color": "5319e7", "description": "Funzionalità principali del backend"},
    {"name": "documentation", "color": "0075ca", "description": "Miglioramenti o aggiunte alla documentazione"},
    {"name": "duplicate", "color": "cfd3d7", "description": "Problema o PR già esistente"},
    {"name": "enhancement", "color": "a2eeef", "description": "Miglioramento di funzionalità esistenti"},
    {"name": "feature", "color": "2cbe4e", "description": "Nuova funzionalità"},
    {"name": "frontend", "color": "1d76db", "description": "Interfaccia utente, HTML/CSS/JS"},
    {"name": "good first issue", "color": "7057ff", "description": "Buono per i nuovi arrivati"},
    {"name": "help wanted", "color": "008672", "description": "È richiesta attenzione extra"},
    {"name": "invalid", "color": "e4e669", "description": "Non sembra essere un problema valido"},
    {"name": "question", "color": "d876e3", "description": "Sono richieste maggiori informazioni"},
    {"name": "simulation", "color": "d4c5f9", "description": "Logica di simulazione dati (bot)"},
    {"name": "wontfix", "color": "ffffff", "description": "Non verrà risolto"},
]
# --- FINE CONFIGURAZIONE ---

def setup_labels():
    """
    Si connette all'API di GitHub per creare etichette predefinite nel repository.
    Legge il GITHUB_TOKEN necessario da una variabile d'ambiente.
    """
    if not GITHUB_TOKEN:
        print("❌ ERRORE: La variabile d'ambiente GITHUB_TOKEN non è impostata.")
        print("Impostala prima di eseguire lo script:")
        print("  (In PowerShell) > $env:GITHUB_TOKEN='ghp_tuo_token_qui'")
        return

    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    print(f"🔗 Connessione al repository: {REPO_OWNER_AND_NAME}")
    print("🔎 Controllo le etichette esistenti e creo quelle mancanti...")

    try:
        # Ottieni le etichette esistenti per evitare di creare duplicati
        response = requests.get(GITHUB_API_URL, headers=headers)
        response.raise_for_status() # Ferma lo script se c'è un errore (es. token sbagliato)
        existing_labels = {label['name'] for label in response.json()}
        print(f"ℹ️  Trovate {len(existing_labels)} etichette esistenti.")

        # Itera sulle etichette da creare
        for label in LABELS_TO_CREATE:
            if label["name"] in existing_labels:
                print(f"  - Ignoro '{label['name']}', esiste già.")
            else:
                print(f"  + Creo '{label['name']}'...")
                create_response = requests.post(GITHUB_API_URL, headers=headers, data=json.dumps(label))
                if create_response.status_code == 201:
                    print(f"    ✅ Successo!")
                else:
                    print(f"    ❌ Fallito! Status: {create_response.status_code}, Risposta: {create_response.text}")

    except requests.exceptions.RequestException as e:
        print(f"\nSi è verificato un errore durante la comunicazione con l'API di GitHub: {e}")

if __name__ == "__main__":
    setup_labels()