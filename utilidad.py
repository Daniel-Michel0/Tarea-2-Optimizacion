import random

def generarMatriz(n):
    matriz = []
    for i in range(0,n):
        fila = []
        for j in range(0,n):
            if(i==j): 
                fila.append(1000)
            else:
                fila.append(random.randint(20,100))  
        matriz.append(fila)  

    for fila in matriz:
        print(fila) 

    return matriz

def read_atsp(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    edge_weight_section_start = lines.index("EDGE_WEIGHT_SECTION\n") + 1
    edge_weight_section_end = len(lines)

    edge_weights = [list(map(int, line.split())) for line in lines[edge_weight_section_start:edge_weight_section_end] if line.strip() != 'EOF']

    return edge_weights