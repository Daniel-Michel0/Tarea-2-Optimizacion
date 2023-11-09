import numpy as np
import pulp
import matplotlib.pyplot as plt
from utilidad import read_atsp
import sys

# Obtener el archivo como parametro en la terminal
if len(sys.argv) < 2:
    print("Por favor, ingresa el nombre del archivo .atsp")
    sys.exit(1)

path = sys.argv[1]
graph = read_atsp(path)
# Imprimir la matriz
for line in graph:
    print(line)


def dfj(cost_matrix):
    n = len(cost_matrix)

    # Crear un problema de minimización
    problema = pulp.LpProblem("Problema_ATSP", pulp.LpMinimize)

    # Crear variables binarias x_ij
    x = pulp.LpVariable.dicts("x", ((i, j) for i in range(n) for j in range(n) if i != j), 0, 1, pulp.LpBinary)

    # Crear variables u_i para eliminar subciclos
    u = pulp.LpVariable.dicts("u", (i for i in range(n)), 0, n-1, pulp.LpInteger)

    # Función objetivo: Minimizar la distancia total
    problema += pulp.lpSum(cost_matrix[i][j] * x[(i, j)] for i in range(n) for j in range(n) if i != j)

    # Restricciones de entrada y salida para cada nodo
    for i in range(n):
        problema += pulp.lpSum(x[(i, j)] for j in range(n) if i != j) == 1
        problema += pulp.lpSum(x[(j, i)] for j in range(n) if i != j) == 1

    # Eliminación de subciclos
    for i in range(1, n):
        for j in range(1, n):
            if i != j:
                problema += u[i] - u[j] + n * x[(i, j)] <= n - 1

    # Resolver el problema
    problema.solve()

    # Obtener la solución
    if pulp.LpStatus[problema.status] == "Optimal":
        optimal_path = [i for i in range(n) if x[(i, j)].varValue == 1 for j in range(n) if i != j][0]
        optimal_cost = pulp.value(problema.objective)
        return optimal_path, optimal_cost
    else:
        return None

result = dfj(graph)
if result:
    path, cost = result
    print("Ciclo Hamiltoniano óptimo:", path)
    print("Costo mínimo:", cost)
else:
    print("No se encontró una solución óptima.")