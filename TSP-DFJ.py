import pulp
import sys
import itertools
from utilidad import read_atsp

# Obtener el archivo como parámetro en la terminal
if len(sys.argv) < 2:
    print("Por favor, ingresa el nombre del archivo .atsp")
    sys.exit(1)

path = sys.argv[1]
graph = read_atsp(path)

n = len(graph)

def solve_dfj_problem(cost_matrix):
    n = len(cost_matrix)

    # Crear un problema de minimización
    problema_dfj = pulp.LpProblem("Problema_DFJ", pulp.LpMinimize)

    # Crear variables binarias x_ij
    x = pulp.LpVariable.dicts("x", ((i, j) for i in range(n) for j in range(n)), 0, 1, pulp.LpBinary)

    # Función objetivo: Minimizar la distancia total
    problema_dfj += pulp.lpSum(cost_matrix[i][j] * x[(i, j)] for i in range(n) for j in range(n))

    # Restricciones
    for j in range(n):
        problema_dfj += pulp.lpSum(x[(i, j)] for i in range(n)) == 1  # Restricción (2)

    for i in range(n):
        problema_dfj += pulp.lpSum(x[(i, j)] for j in range(n)) == 1  # Restricción (3)

    for s in range(2, n):
        for S in itertools.combinations(range(n), s):
            problema_dfj += pulp.lpSum(x[(i, j)] for i in S for j in S) <= len(S) - 1  # Restricción (4)

    # Resolver el problema
    problema_dfj.solve()

    # Imprimir la solución
    print("Estado:", pulp.LpStatus[problema_dfj.status])
    for (i, j) in x:
        if(x[(i, j)].varValue == 1):
            print(f"x({i},{j}) = {x[(i, j)].varValue}")
    print("Valor óptimo =", pulp.value(problema_dfj.objective))

solucion = solve_dfj_problem(graph)
