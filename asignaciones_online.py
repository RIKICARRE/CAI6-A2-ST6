from ortools.sat.python import cp_model

# Definición de tareas y roles
tasks = ['T1', 'T2', 'T3', 'T4', 'T5']
roles = ['PPV','MDF','JEP','DIP','OFA','DLT']

# Reglas de separación y binding
sod = [('T1','T2'), ('T2','T3'), ('T3','T4')]     # DSoD/DBoD
binding = [('T4','T1'), ('T5','T2')]              # binding-of-duty

# Crear modelo
model = cp_model.CpModel()

# Variables: x[(t,r)] = 1 si tarea t la ejecuta rol r
x = {}
for t in tasks:
    for r in roles:
        x[(t,r)] = model.NewBoolVar(f"x_{t}_{r}")

# Cada tarea debe asignarse a exactamente un rol
for t in tasks:
    model.Add(sum(x[(t,r)] for r in roles) == 1)

# Reglas DSoD/DBoD: tareas t1 y t2 no pueden compartir rol
for t1, t2 in sod:
    for r in roles:
        model.Add(x[(t1,r)] + x[(t2,r)] <= 1)

# Reglas binding: t_bind debe asignarse al mismo rol que t_base
for t_bind, t_base in binding:
    for r in roles:
        model.Add(x[(t_bind,r)] == x[(t_base,r)])

# (Opcional) Fairness u otros objetivos: Ejemplo minimizar la carga
# Si tuvieras datos de carga, podrías modelar un objetivo aquí.

# Resolver
solver = cp_model.CpSolver()
solver.parameters.max_time_in_seconds = 10
status = solver.Solve(model)

if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
    print("Asignación encontrada:")
    for t in tasks:
        for r in roles:
            if solver.Value(x[(t,r)]) == 1:
                print(f"  - {t} → {r}")
else:
    print("No se encontró ninguna solución válida.")
