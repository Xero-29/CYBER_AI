import requests
import json

TARGET_URL = "http://127.0.0.1:5000/api/v1/status"

print("=== SALIDA ===")
print(f"Lanzando auditoría empírica contra: {TARGET_URL}\n")

try:
    response = requests.get(TARGET_URL, timeout=5)
    print(f"Código de Estado HTTP: {response.status_code}")
    
    print("\nCabeceras HTTP detectadas (Metadatos expuestos):")
    for header, value in response.headers.items():
        print(f"  - {header}: {value}")
        
    print("\nCuerpo de la respuesta (JSON):")
    print(json.dumps(response.json(), indent=2))

except Exception as e:
    print(f"Error al conectar con la API local: {e}")

print("\n=== FIN DE LA AUDITORÍA ===")
