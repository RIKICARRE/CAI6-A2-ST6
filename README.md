# Estructura de archivos:

```
ztna_poc/
├── policy.json         # Definición de política de acceso
├── backend.py          # Recursos protegidos (varios endpoints)
├── broker.py           # Broker ZTNA (reverse proxy)
├── client.py           # Cliente ZTNA
└── protected_resources/
    ├── historial.py    # Lógica de /historial
    ├── recetas.py      # Lógica de /recetas
    ├── citas.py        # Lógica de /citas
    └── informes.py     # Lógica de /informes
```

# Instrucciones de uso:
1. Generar un par cliente:
   ```bash
   openssl genrsa -out client.key 2048
   openssl req -new -x509 -key client.key -out client.crt -subj "/CN=Client1"
   ```
2. Arrancar el backend:
   ```bash
   python3 backend.py
   ```
3. Arrancar el broker:
   ```bash
   python3 broker.py
   ```
4. Ejecutar el cliente:
   ```bash
   python3 client.py
   ```

# Endpoints disponibles
- `/historial`   → Historial médico
- `/recetas`     → Recetas
- `/citas`       → Citas
- `/informes`    → Informes

Cada endpoint está protegido por el broker ZTNA, que valida la firma, el certificado y el contexto del dispositivo según la política definida en `policy.json`. El acceso es granular: cada recurso puede tener reglas y roles distintos.

# Flujo de selección de recursos
Al ejecutar el cliente, se muestra un menú para seleccionar el recurso a consultar. Tras autenticarse y firmar el nonce, el cliente envía la petición al broker, que aplica la política y reenvía la solicitud al backend solo si se cumplen todos los requisitos.

# Ejemplo de uso
```
Recursos disponibles:
1. Historial médico (/historial)
2. Recetas (/recetas)
3. Citas (/citas)
4. Informes (/informes)
Seleccione el recurso a consultar: 2
Status: 200
{"recetas": [ ... ]}
```
Si el acceso es denegado:
```
Status: 403
Access denied: You don't have permission to access this resource
```

Este PoC implementa un acceso Zero Trust contextual: el broker valida posesión de clave (firma), identidad (CN) y contexto contra una política dinámica; solo entonces reenvía la petición al recurso protegido.