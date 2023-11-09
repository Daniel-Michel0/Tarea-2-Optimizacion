import pulp
import random

# Matriz de distancias
c = [
    [0, 12, 29, 22, 13, 24],
    [12, 0, 19, 3, 25, 6],
    [29, 19, 0, 21, 23, 28],
    [22, 3, 21, 0, 4, 5],
    [13, 25, 23, 4, 0, 16],
    [24, 26, 28, 5, 16, 0]
]

n = len(c)

# Crear un problema de minimización
problema = pulp.LpProblem("Problema_de_Rutas_Mínimas", pulp.LpMinimize)

# Conjuntos de nodos y aristas
V = range(n)
A = [(i, j) for i in V for j in V if i != j]

# Variables binarias x_ij
x = pulp.LpVariable.dicts("x", A, 0, 1, pulp.LpBinary)

# Variables de distancia d_ij
d = pulp.LpVariable.dicts("d", A, 0, None, pulp.LpContinuous)

# Variables de flujo para la formulación MTZ
u = pulp.LpVariable.dicts("u", V, 0, n - 1, pulp.LpInteger)

# Función objetivo: Minimizar la distancia total
problema += pulp.lpSum(c[i][j] * x[(i, j)] for (i, j) in A)

# Restricciones
for i in V:
    problema += pulp.lpSum(x[(i, j)] for j in V if i != j) == 1

for j in V:
    problema += pulp.lpSum(x[(i, j)] for i in V if i != j) == 1

for i in V:
    for j in V:
        if i != j and i >= 1:
            problema += u[i] - u[j] + 1 <= n * (1 - x[(i, j)])

# Resolver el problema
problema.solve()

# Imprimir la solución
print("Status:", pulp.LpStatus[problema.status])
for (i, j) in A:
    if x[(i, j)].varValue == 1:
        print(f"x({i},{j}) = 1")
print("Optimal value =", pulp.value(problema.objective))
