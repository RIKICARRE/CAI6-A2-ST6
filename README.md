# PoC ZTNA – Estructura y Uso

---

## 📁 Estructura de archivos

```
ztna_poc/
├── policy.json                # Definición de política de acceso
├── backend.py                 # Recursos protegidos (varios endpoints)
├── broker.py                  # Broker ZTNA (reverse proxy)
├── client.py                  # Cliente ZTNA
├── asignaciones_online.py     # Solver online: asigna personas en tiempo real
├── asignaciones_offline.py    # Precomputa asignaciones de roles
├── assignments.json           # Soluciones precalculadas (generado por asignaciones_offline.py)
└── protected_resources/
    ├── historial.py           # Lógica de /historial
    ├── recetas.py             # Lógica de /recetas
    ├── citas.py               # Lógica de /citas
    └── informes.py            # Lógica de /informes
```

---

## 🚀 Instrucciones de uso

1. **Crear y activar el entorno virtual**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Instalar dependencias**

   ```bash
   pip install -r requirements.txt
   ```

3. **Generar par de claves para el cliente ZTNA**

   ```bash
   openssl genrsa -out client.key 2048
   openssl req -new -x509 -key client.key \
       -out client.crt -subj "/CN=Client1"
   ```

---

### 🔐 PoC ZTNA (Zero Trust)

4. **Arrancar el backend**

   ```bash
   python3 backend.py
   ```

5. **Arrancar el broker**

   ```bash
   python3 broker.py
   ```

6. **Ejecutar el cliente**

   ```bash
   python3 client.py
   ```

#### Endpoints disponibles

* `/historial` → Historial médico
* `/recetas`   → Recetas
* `/citas`     → Citas
* `/informes`  → Informes

> El broker ZTNA valida **firma**, **certificado** y **contexto** según `policy.json`. Cada recurso puede tener reglas y roles distintos.

---

## 🔄 Flujo de selección de recursos

1. Al iniciar `client.py`, se muestra un menú con los endpoints.
2. El cliente solicita un **nonce**, lo **firma** y envía junto a su **certificado** y **contexto**.
3. El **broker** verifica:

   * Noce autenticidad,
   * Cadena de confianza del certificado,
   * Atributos de contexto (e.g. `devicePosture`, `location`).
4. Si pasa todas las comprobaciones, se reenvía al **backend**.

> De lo contrario, devuelve **403 Access denied**.

---

## 📋 Ejemplo de uso

```text
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

```text
Status: 403
Access denied: You don't have permission to access this resource
```

---

## ⚙️ Uso de los scripts de asignaciones

Además de la funcionalidad ZTNA, el repositorio incluye dos utilidades para asignar **personas** a las tareas de un proceso de compras, cumpliendo las reglas de separación y binding-of-duty:

### 1. asignaciones\_online.py

Resuelve en tiempo real la asignación basándose en un rol iniciador.

```bash
# Ejecutar directamente indicando el rol del iniciador (por ejemplo DR)
python3 bpms_models/asignaciones_online.py DR
```

* **Entrada:** rol del usuario que inicia (`DR`, `DG`, `DM`, etc.)
* **Salida:** JSON con pares `T1 -> siglas`, ..., `T5 -> siglas`.

### 2. asignaciones\_offline.py

Precalcula todas las combinaciones válidas de roles y almacena en `assignments.json`.

```bash
# Generar o regenerar assignments.json
python3 bpms_models/asignaciones_offline.py
```

Posteriormente, para consultar una asignación para un iniciador, usar:

```bash
python3 bpms_models/lookup_assignments.py
# Se solicitará el rol del iniciador y devolverá una asignación de personas.
```

> Ambas soluciones emplean el mapeo de `ROLE_PERSONS` definido en el código, asegurando que cada rol se asigne a una persona actual del servicio.
