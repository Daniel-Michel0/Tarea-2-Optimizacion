import pulp
import matplotlib.pyplot as plt
import random

path='wi29.tsp'
file=[[float(j) for j in i.split(' ')] for i in open(path,'r').read().split('\n')[7:-1]]
file=random.sample(file, 10) #Reduzco el tamaño por tiempos de computo

x_coord=[i[1] for i in file]
y_coord=[i[2] for i in file]

plt.figure(figsize=(7,8))
plt.xlabel("X")
plt.ylabel("Y")
plt.title("Problema TSP")

plt.scatter(x=x_coord,y=y_coord, color='blue',zorder=1)