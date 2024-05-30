#import fix_and_optimize
import simulated_annealing
import pandas as pd
import numpy as np

sa = simulated_annealing.SimulatedAnnealing()

# Read data from CSV files
disciplinas_df = pd.read_csv('..\data\disciplinas.csv', header=0)
salas_df = pd.read_csv('..\data\salas.csv', header=0)

N = disciplinas_df['N'].values
C = salas_df['C'].values
D = salas_df['D'].values

#initial_solution = fix_and_optimize.run()
# temporary random initial solution

def order_ascending(array):
    # Crie uma lista de tuplas (índice, elemento)
    indexed_array = [(index, array[index]) for index, element in enumerate(array)]

    # Ordene a lista de tuplas com base no valor do elemento em ordem crescente
    sorted_indexed_array = sorted(indexed_array, key=lambda x: x[1])

    # Extraia os índices da lista de tuplas ordenadas
    sorted_indexes = [index for index, element in sorted_indexed_array]
    
    return sorted_indexes

def order_descending(array):
    # Create a list of tuples (index, element)
    indexed_array = [(index, array[index]) for index, element in enumerate(array)]

    # Sort the list of tuples based on element value in descending order
    sorted_indexed_array = sorted(indexed_array, key=lambda x: x[1], reverse=True)

    # Extract the indexes from the sorted list of tuples
    sorted_indexes = [index for index, element in sorted_indexed_array]
    
    return sorted_indexes

# Ordenar as disciplinas e salas pela quantidade de alunos e capacidade
N_sorted = order_descending(N)
print(N_sorted)
D_sorted = order_ascending(D)
print(D_sorted)

# Initialize the solution (x) matrix
initial_solution = np.zeros((len(N), len(D)), dtype=int)
for i in range(len(N)):
    initial_solution[N_sorted[i], D_sorted[i]] = 1
    # as a vector
    #initial_solution[D_sorted[i]] = N_sorted[i]
    
# print(initial_solution)

neighbor = sa.solution_to_neighbor(initial_solution, D_sorted)
print(neighbor)

solution = sa.neighbor_to_solution(neighbor)
print(np.array_equal(solution,initial_solution))

swaped = sa.get_neighbor(neighbor)
print(swaped)

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
