import requests
import json
import time

url = "http://localhost:5678/webhook/minutas-chunking"
payload = {"meeting_text": "Este es un texto largo " * 4000}  # ~96k characters, forces chunking

print("Enviando request a n8n...")
start_time = time.time()
try:
    response = requests.post(url, json=payload)
    print(f"Status: {response.status_code}")
    print(f"Time: {time.time() - start_time:.2f}s")
    print(f"Response Body (primeros 500 chars): {response.text[:500]}")
except Exception as e:
    print(f"Excepcion durante post: {e}")
