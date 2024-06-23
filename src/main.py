import relax_and_fix
import simulated_annealing
import pandas as pd
import numpy as np
import csv

num_disciplines = 500
num_rooms = 500

# Read data from the CSV files and store them in dictionaries
# Reading room capacity data
C = {}
with open('..\data\capacidade_salas_2.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar=';')
    next(reader)  # Skip the header
    for row in reader:
        room = int(row[0])
        C[room] = int(row[1])

# Reading number of students per discipline data
N = {}
with open('..\data\disciplinas_2.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar=';')
    next(reader)
    for row in reader:
        discipline = int(row[0])
        N[discipline] = int(row[1])
        
# Reading distance of each classroom to the building of each discipline data
D = {}
with open('..\data\distancia_salas_2.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar=';')
    next(reader)
    for row in reader:
        room = int(row[0])
        distances = list(map(int, row[1:]))
        D[room] = {i + 1: distances[i] for i in range(len(distances))}

# Get a initial solution by appling Relax-and-Fix
rf = relax_and_fix.RelaxAndFix(N, C, D, num_disciplines, num_rooms, True)
initial_solution = rf.compute_solution()
#print(initial_solution)

# Use the initial solution to obtain the optimal solution with Simulated Annealing
sa = simulated_annealing.SimulatedAnnealing(N, C, D, initial_solution, num_disciplines, num_rooms, True)
#neighbor = sa.solution_to_neighbor(initial_solution)
#print(neighbor)
optimal_solution = sa.compute_solution()
print(optimal_solution)
