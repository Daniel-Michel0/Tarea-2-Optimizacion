import pulp
import sys
from utilidad import read_atsp

def agregar_corte_gg(problema, solucion_no_entera):
    # Agrega un corte GG al problema
    problema += pulp.lpSum(x[(i, j)] for (i, j) in solucion_no_entera) <= len(solucion_no_entera) - 1

# Crear un problema de minimización
problema = pulp.LpProblem("Problema_de_Rutas_Mínimas", pulp.LpMinimize)

# Obtener el archivo como parámetro en la terminal
if len(sys.argv) < 2:
    print("Por favor, ingresa el nombre del archivo .atsp")
    sys.exit(1)

path = sys.argv[1]
graph = read_atsp(path)

n = len(graph)

# Conjuntos de nodos y aristas
V = range(n)
A = [(i, j) for i in V for j in V if i != j]

# Variables binarias x_ij
x = pulp.LpVariable.dicts("x", A, 0, 1, pulp.LpBinary)

# Variables de flujo y_i
y = pulp.LpVariable.dicts("y", V, 0, n - 1, pulp.LpInteger)

# Función objetivo: Minimizar la distancia total
problema += pulp.lpSum(graph[i][j] * x[(i, j)] for (i, j) in A)

# Restricciones
for i in V:
    problema += pulp.lpSum(x[(i, j)] for j in V if i != j) == 1

for j in V:
    problema += pulp.lpSum(x[(i, j)] for i in V if i != j) == 1

for i in V[1:]:
    for j in V:
        if i != j:
            problema += y[i] - y[j] + n * x[(i, j)] <= n - 1

# Resolver el problema con GG
while True:
    # Resolver el problema
    problema.solve()

    # Imprimir la solución
    print("Status:", pulp.LpStatus[problema.status])
    for (i, j) in A:
        if x[(i, j)].varValue == 1:
            print(f"x({i},{j}) = 1")
    print("Optimal value =", pulp.value(problema.objective))

    # Verificar si la solución es entera
    if all(var.varValue.is_integer() for var in problema.variables()):
        print("Solución entera encontrada.")
        break
    else:
        # Identificar una solución no entera
        solucion_no_entera = [(i, j) for (i, j) in A if x[(i, j)].varValue % 1 != 0]

        # Agregar corte de GG al problema
        agregar_corte_gg(problema, solucion_no_entera)
