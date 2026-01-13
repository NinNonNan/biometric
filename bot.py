import requests
import time
import random

# !!! IMPORTANTE !!!
# Sostituisci questo URL con l'URL della tua applicazione su PythonAnywhere.
URL = "https://NinNonNan.pythonanywhere.com/update"

print("--- Starting John Doe Biometric Bot ---")
print(f"Targeting: {URL}")

# Frequenza cardiaca di partenza
current_hr = 75

while True:
    try:
        # Simula una piccola fluttuazione casuale.
        # C'è una piccola probabilità di un "salto" più grande per rendere i dati più vari.
        if random.random() < 0.9:
            change = random.randint(-2, 2)  # Fluttuazione normale
        else:
            change = random.randint(-15, 15) # Salto occasionale

        current_hr += change

        # Mantiene la frequenza cardiaca entro un range realistico per la demo.
        current_hr = max(55, min(140, current_hr))

        # Prepara i dati da inviare
        payload = {"hr": current_hr, "subject": "John Doe"}

        # Invia la richiesta POST al server
        response = requests.post(URL, json=payload, timeout=10)
        response.raise_for_status()  # Genera un errore se la risposta non è 2xx

        print(f"Sent HR: {current_hr} -> Status: {response.status_code} ({response.json().get('status', 'N/A')})")

    except requests.exceptions.RequestException as e:
        print(f"Error sending data: {e}")

    # Attende un intervallo casuale prima del prossimo invio
    sleep_time = random.uniform(2, 5)
    time.sleep(sleep_time)