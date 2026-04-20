import requests
import json
import time

url = "http://localhost:5678/webhook/minutas"
payload = {"meeting_text": "Reunión de prueba corta. Hablamos de nada. Fin."}

print("Enviando request a n8n (webhook: minutas)...")
start_time = time.time()
try:
    response = requests.post(url, json=payload, timeout=600)
    print(f"Status: {response.status_code}")
    print(f"Time: {time.time() - start_time:.2f}s")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
except Exception as e:
    print(f"Excepcion: {e}")
