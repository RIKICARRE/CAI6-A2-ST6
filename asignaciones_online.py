import sys
import json
import random
from ortools.sat.python import cp_model

# Configuración de tareas, roles y reglas
TASKS = ['T1', 'T2', 'T3', 'T4', 'T5']
ROLES = ['DG', 'DR', 'DM', 'DE', 'TR', 'TC', 'PS']
SOD = [('T1','T2'), ('T2','T3'), ('T3','T4')]
BIND = [('T4','T1'), ('T5','T2')]
ROLE_PERSONS = {
    'DG': ['JVG'],
    'DR': ['HYV'],
    'DM': ['PGR'],
    'DE': ['MFE'],
    'TR': ['GTR', 'LPG', 'RGB', 'HYV', 'BJC'],
    'TC': ['RGB', 'MDS', 'LPG'],
    'PS': ['HJR', 'PTS', 'IHP']
}


def solve_for_initiator(initiator_role):
    model = cp_model.CpModel()
    x = {(t,r): model.NewBoolVar(f"x_{t}_{r}") for t in TASKS for r in ROLES}

    # Cada tarea exactamente un rol
    for t in TASKS:
        model.Add(sum(x[(t,r)] for r in ROLES) == 1)

    # DSoD/DBoD
    for t1,t2 in SOD:
        for r in ROLES:
            model.Add(x[(t1,r)] + x[(t2,r)] <= 1)

    # Binding of Duty
    for tb,base in BIND:
        for r in ROLES:
            model.Add(x[(tb,r)] == x[(base,r)])

    # asignar iniciador a T1 si su rol es válido
    if initiator_role in ROLES:
        model.Add(x[('T1', initiator_role)] == 1)

    # Resolver
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 5
    solver.parameters.random_seed = 12345
    status = solver.Solve(model)
    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        raise RuntimeError("No se encontró solución de asignación de roles")

    # Asignación de roles
    assignment_roles = {t: r for t in TASKS for r in ROLES if solver.Value(x[(t,r)])}

    # Mapear a personas
    assignment_persons = {t: random.choice(ROLE_PERSONS[role])
                          for t, role in assignment_roles.items()}
    return assignment_persons


def main():
    if len(sys.argv) != 2:
        print(f"Uso: {sys.argv[0]} <rol_iniciador>")
        sys.exit(1)
    initiator = sys.argv[1]
    result = solve_for_initiator(initiator)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()