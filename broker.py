import json
import base64
from flask import Flask, request, jsonify, abort
import requests
from cryptography import x509
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
import os
import threading
import time

app = Flask(__name__)

# Cargar política (inicialmente)
def load_policy():
    with open('policy.json') as f:
        return json.load(f)

POLICY = load_policy()
POLICY_MTIME = os.path.getmtime('policy.json')

# Monitorización de cambios en policy.json
def policy_watcher():
    global POLICY, POLICY_MTIME
    while True:
        try:
            mtime = os.path.getmtime('policy.json')
            if mtime != POLICY_MTIME:
                POLICY = load_policy()
                POLICY_MTIME = mtime
                print("[ZTNA] Política recargada automáticamente.")
        except Exception as e:
            print(f"[ZTNA] Error al recargar política: {e}")
        time.sleep(2)

threading.Thread(target=policy_watcher, daemon=True).start()

# Nonce temporal en memoria
NONCES = {}

@app.route('/nonce', methods=['GET'])
def get_nonce():
    client_id = request.remote_addr
    nonce = os.urandom(16)
    b64 = base64.b64encode(nonce).decode()
    NONCES[client_id] = nonce
    return jsonify({"nonce": b64})

@app.route('/resource', methods=['POST'])
def proxy_resource():
    client_id = request.remote_addr
    body = request.get_json()
    if not body:
        abort(400, "JSON esperado")

    # Extraer parámetros
    b64nonce = body.get('nonce')
    signature = base64.b64decode(body.get('signature', ''))
    cert_pem = body.get('certificate', '').encode()
    context = body.get('context', {})
    endpoint = body.get('endpoint', '/resource')
    
    # Asegurar que el endpoint comienza con /
    if endpoint and not endpoint.startswith('/'):
        endpoint = '/' + endpoint

    # Verificar nonce conocido
    raw_nonce = NONCES.get(client_id)
    if not raw_nonce or base64.b64encode(raw_nonce).decode() != b64nonce:
        abort(403, "Nonce inválido")

    # Cargar certificado X.509
    try:
        cert = x509.load_pem_x509_certificate(cert_pem)
        pubkey = cert.public_key()
    except Exception:
        abort(400, "Certificado no válido")

    # Verificar firma del nonce
    try:
        pubkey.verify(
            signature,
            raw_nonce,
            padding.PKCS1v15(),
            hashes.SHA256()
        )
    except Exception:
        abort(403, "Firma inválida")

    # Extraer CN del cert
    cn = cert.subject.get_attributes_for_oid(x509.NameOID.COMMON_NAME)[0].value

    # Verificar política
    match = next((c for c in POLICY['allowed_clients'] if c['cn'] == cn), None)
    if not match:
        abort(403, "Cliente no autorizado")

    # Verificar contexto
    for attr, val in match.items():
        if attr in ['cn', 'roles']:
            continue
        if context.get(attr) != val:
            abort(403, f"Contexto inválido ({attr})")

    # Forward al backend
    backend_url = f'http://localhost:5001{endpoint}'
    print(f"[ZTNA] Reenviando petición a: {backend_url}")
    try:
        resp = requests.get(backend_url)
        return jsonify(resp.json()), resp.status_code
    except Exception as e:
        print(f"[ZTNA] Error al acceder a {backend_url}: {str(e)}")
        return jsonify({"error": f"Error al acceder al recurso: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(port=5000)