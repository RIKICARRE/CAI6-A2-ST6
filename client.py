import requests
import base64
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography import x509

# Cargar clave privada y certificado del cliente
with open('client.key', 'rb') as f:
    private_key = serialization.load_pem_private_key(f.read(), password=None)
with open('client.crt', 'rb') as f:
    client_cert_pem = f.read()

# Obtener nonce del broker
r = requests.get('http://127.0.0.1:5000/nonce')
nonce_b64 = r.json()['nonce']
nonce_raw = base64.b64decode(nonce_b64)

# Firmar el nonce
signature = private_key.sign(
    nonce_raw,
    padding.PKCS1v15(),
    hashes.SHA256()
)
sign_b64 = base64.b64encode(signature).decode()

# Contexto del dispositivo
context = {
    "devicePosture": "compliant",
    "location": "hospital"
}

# Solicitar recurso protegido
recursos = [
    {"nombre": "Historial médico", "endpoint": "/historial"},
    {"nombre": "Recetas", "endpoint": "/recetas"},
    {"nombre": "Citas", "endpoint": "/citas"},
    {"nombre": "Informes", "endpoint": "/informes"}
]
print("Recursos disponibles:")
for idx, r in enumerate(recursos):
    print(f"{idx+1}. {r['nombre']} ({r['endpoint']})")
sel = int(input("Seleccione el recurso a consultar: ")) - 1
endpoint = recursos[sel]["endpoint"]

payload = {
    'nonce': nonce_b64,
    'signature': sign_b64,
    'certificate': client_cert_pem.decode(),
    'context': context,
    'endpoint': endpoint
}
r2 = requests.post('http://127.0.0.1:5000/resource', json=payload)
print(f"Status: {r2.status_code}")
if r2.status_code == 200:
    print(r2.json())
elif r2.status_code == 403:
    print("Access denied: You don't have permission to access this resource")
