import json
import random
from itertools import product

# Configuración de tareas, roles y reglas
ROLE_PERSONS = {
    'DG': ['JVG'],
    'DR': ['HYV'],
    'DM': ['PGR'],
    'DE': ['MFE'],
    'TR': ['GTR', 'LPG', 'RGB', 'HYV', 'BJC'],
    'TC': ['RGB', 'MDS', 'LPG'],
    'PS': ['HJR', 'PTS', 'IHP']
}
TASKS = ['T1', 'T2', 'T3', 'T4', 'T5']
ROLES = list(ROLE_PERSONS.keys())
SOD = [('T1','T2'), ('T2','T3'), ('T3','T4')]
BIND = [('T4','T1'), ('T5','T2')]

# Comprobar validez de asignación de roles
def valid_roles(assign):
    for a,b in SOD:
        if assign[a] == assign[b]: return False
    for bind_t, base in BIND:
        if assign[bind_t] != assign[base]: return False
    return True

# Generar y mapear a personas todas las asignaciones válidas

def main():
    solutions = []
    for combo in product(ROLES, repeat=len(TASKS)):
        role_assign = dict(zip(TASKS, combo))
        if valid_roles(role_assign):
            # mapear roles a personas (elige una al azar)
            person_assign = {
                t: random.choice(ROLE_PERSONS[role_assign[t]])
                for t in TASKS
            }
            solutions.append(person_assign)
    # Guardar como JSON de personas
    with open('assignments_persons.json', 'w') as f:
        json.dump(solutions, f, indent=2)
    print(f"Precomputed {len(solutions)} person assignments")


if __name__ == '__main__':
    main()