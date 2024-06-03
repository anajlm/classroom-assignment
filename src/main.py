import relax_and_fix
import simulated_annealing
import pandas as pd
import numpy as np
import csv



# # Read data from CSV files
# alunos_por_disciplina_df = pd.read_csv('..\data\disciplina.csv', index_col='Disciplina')
# # salas_df = pd.read_csv('..\data\salas.csv', header=0)

# alunos_por_disciplina_array = alunos_por_disciplina_df.values.flatten()
# print(alunos_por_disciplina_array)


# Read data from the CSV file and pad the arrays to handle one-based indexing
# Ler dados do arquivo de capacidades das salas
C = {}
with open('..\data\capacidade_salas.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar=';')
    next(reader)  # Skip the header
    for row in reader:
        room = int(row[0])
        C[room] = int(row[1])

# Ler dados do arquivo de número de alunos das disciplinas
N = {}
with open('..\data\disciplinas.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar=';')
    next(reader)
    for row in reader:
        discipline = int(row[0])
        N[discipline] = int(row[1])
        
# Ler dados do arquivo de distancia das salas
D = {}
with open('..\data\distancia_salas.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar=';')
    next(reader)
    for row in reader:
        room = int(row[0])  # Room number (first column)
        distances = list(map(int, row[1:]))  # Distances (remaining columns)
        # Create a dictionary for the distances with discipline numbers as keys
        D[room] = {i + 1: distances[i] for i in range(len(distances))}

# print(C)
# print(D[1])
# print(N)
# Display the first few entries to verify
# print("First few entries in the dictionary D:")
# for key in list(D.keys())[:5]:
#     print(f"Sala {key}: {D[key]}")

# N = disciplinas_df['N'].values
# C = salas_df['C'].values
# D = salas_df['D'].values

# sa = simulated_annealing.SimulatedAnnealing()
raf = relax_and_fix.RelaxAndFix(N, C, D, 100, 100)
initial_solution = raf.compute_solution()

print(initial_solution)

# neighbor = sa.solution_to_neighbor(initial_solution, D_sorted)
# print(neighbor)

# solution = sa.neighbor_to_solution(neighbor)
# print(np.array_equal(solution,initial_solution))

# swaped = sa.get_neighbor(neighbor)
# print(swaped)

# Ensure each classroom is ocupied by a class
# for i in range(len(N)):
#     j = np.random.randint(0, len(C))
#     initial_solution[i, j] = 1
    
#optimal_solution = simulated_annealing.optimize(N, C, initial_solution)

# Dumps solution on CSV file


   
# # Exemplo de uso
# N = np.random.randint(20, 60, size=100)  # Número de estudantes por disciplina
# C = np.random.randint(30, 70, size=100)  # Capacidade das salas

# raf = RelaxAndFix(N, C)
# initial_solution = raf.fix()
# optimized_solution = raf.optimize(initial_solution)

# print("Solução inicial:", initial_solution)
# print("Solução otimizad
