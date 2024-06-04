import relax_and_fix
import simulated_annealing
import pandas as pd
import numpy as np
import csv

# Read data from the CSV files and store them in dictionaries
# Reading room capacity data
C = {}
with open('..\data\capacidade_salas.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar=';')
    next(reader)  # Skip the header
    for row in reader:
        room = int(row[0])
        C[room] = int(row[1])

# Reading number of students per discipline data
N = {}
with open('..\data\disciplinas.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar=';')
    next(reader)
    for row in reader:
        discipline = int(row[0])
        N[discipline] = int(row[1])
        
# Reading distance of each classroom from the building of each discipline data
D = {}
with open('..\data\distancia_salas.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar=';')
    next(reader)
    for row in reader:
        room = int(row[0])
        distances = list(map(int, row[1:]))
        # Create a dictionary for the distances with discipline numbers as keys
        D[room] = {i + 1: distances[i] for i in range(len(distances))}


# Get a initial solution by appling Relax-and-Fix
raf = relax_and_fix.RelaxAndFix(N, C, D, 100, 100)
initial_solution = raf.compute_solution()
print(initial_solution)

# Use the initial solution to obtain the optimized solution with Simulated Annealing
# sa = simulated_annealing.SimulatedAnnealing()
#optimized_solution = sa.compute_solutuion()

# neighbor = sa.solution_to_neighbor(initial_solution, D_sorted)
# print(neighbor)

# solution = sa.neighbor_to_solution(neighbor)
# print(np.array_equal(solution,initial_solution))
