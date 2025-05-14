import random
import csv
from collections import Counter

# Definición de roles y personas
roles = {
    'DG': ['JVG'],
    'DR': ['HYV'],
    'DM': ['PGR'],
    'DE': ['MFE'],
    'TR': ['GTR', 'LPG', 'RGB', 'HYV', 'BJC'],
    'TC': ['RGB', 'MDS', 'LPG'],
    'PS': ['HJR', 'PTS', 'IHP']
}

# Tareas y roles asignables
asignacion_tarea_rol = {
    'T1': ['DR'],
    'T2.1': ['TR'],
    'T2.2': ['TC'],
    'T3': ['DM'],
    'T4': ['DE', 'PS']
}

# Restricciones
# R1: T2.1 y T2.2 usuarios diferentes
# R2: T3 y T4 usuarios diferentes
# R3: Si GTR hace T2.1, MDS debe hacer T2.2
# R4: JVG solo puede hacer T1
# R5: Fairness (balanceo)

# Personas por rol
personas_rol = {
    'DR': ['HYV'],
    'TR': ['GTR', 'LPG', 'RGB', 'HYV', 'BJC'],
    'TC': ['RGB', 'MDS', 'LPG'],
    'DM': ['PGR'],
    'DE': ['MFE'],
    'PS': ['HJR', 'PTS', 'IHP']
}

# Generar todas las combinaciones posibles que cumplen las restricciones
instancias = []
max_instancias = 20
contador = Counter()

while len(instancias) < max_instancias:
    instancia = {}
    # T1
    t1 = random.choice(personas_rol['DR'])
    instancia['T1'] = t1
    # R4: JVG solo puede hacer T1
    if t1 == 'JVG':
        t1_excluidos = ['JVG']
    else:
        t1_excluidos = []
    # T2.1
    posibles_t21 = [p for p in personas_rol['TR'] if p not in t1_excluidos]
    t21 = random.choice(posibles_t21)
    instancia['T2.1'] = t21
    # T2.2
    # R1: T2.1 y T2.2 diferentes
    posibles_t22 = [p for p in personas_rol['TC'] if p != t21]
    # R3: Si GTR hace T2.1, MDS debe hacer T2.2
    if t21 == 'GTR' and 'MDS' in posibles_t22:
        t22 = 'MDS'
    else:
        t22 = random.choice(posibles_t22)
    instancia['T2.2'] = t22
    # T3
    posibles_t3 = [p for p in personas_rol['DM'] if p not in [t21, t22]]
    t3 = random.choice(posibles_t3)
    instancia['T3'] = t3
    # T4
    posibles_t4 = [p for p in personas_rol['DE'] + personas_rol['PS'] if p != t3]
    # R2: T3 y T4 diferentes
    t4 = random.sample(posibles_t4, 2) if len(posibles_t4) >= 2 else posibles_t4
    instancia['T4'] = t4
    # Fairness: no más de 2 instancias seguidas por persona en la misma tarea
    valido = True
    for tarea, persona in instancia.items():
        if isinstance(persona, list):
            for p in persona:
                if contador[(tarea, p)] >= max_instancias // len(personas_rol.get(asignacion_tarea_rol[tarea][0], [])):
                    valido = False
        else:
            if contador[(tarea, persona)] >= max_instancias // len(personas_rol.get(asignacion_tarea_rol[tarea][0], [])):
                valido = False
    if not valido:
        continue
    # No repetir instancia exacta
    if instancia in instancias:
        continue
    instancias.append(instancia)
    for tarea, persona in instancia.items():
        if isinstance(persona, list):
            for p in persona:
                contador[(tarea, p)] += 1
        else:
            contador[(tarea, persona)] += 1

# Guardar en CSV
with open('asignaciones_20instancias.csv', 'w', newline='') as csvfile:
    fieldnames = ['INSTANCIA', 'T1', 'T2.1', 'T2.2', 'T3', 'T4']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for idx, inst in enumerate(instancias, 1):
        fila = {
            'INSTANCIA': idx,
            'T1': inst['T1'],
            'T2.1': inst['T2.1'],
            'T2.2': inst['T2.2'],
            'T3': inst['T3'],
            'T4': ' y '.join(inst['T4']) if isinstance(inst['T4'], list) else inst['T4']
        }
        writer.writerow(fila)
print("Asignaciones generadas en asignaciones_20instancias.csv")