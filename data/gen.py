## Script for generating random data for the problems's input variables ##

import pandas as pd
import numpy as np

# Define the number of disciplines and rooms
num_disciplinas = 500
num_salas = 500

# Generating data for room capacity
capacidade_salas = {
    'Capacidade': np.random.randint(30, 70, size=num_salas)  # Capacity for each room
}
capacidade_salas_df = pd.DataFrame(capacidade_salas)
capacidade_salas_df.index = np.arange(1, len(capacidade_salas_df) + 1)  # Starting index from 1
capacidade_salas_df.to_csv('capacidade_salas_2.csv', index_label='Sala')

# Generating data for number of students per class
alunos_por_disciplina = {
    'Alunos': np.random.randint(20, 60, size=num_disciplinas)  # Number of students per class
}
alunos_por_disciplina_df = pd.DataFrame(alunos_por_disciplina)
alunos_por_disciplina_df.index = np.arange(1, len(alunos_por_disciplina_df) + 1)  # Starting index from 1
alunos_por_disciplina_df.to_csv('disciplinas_2.csv', index_label='Disciplina')

# # Generating data for distance from each room to the building
# distancia_salas = {
#     f'Disciplina_{i}': np.random.randint(50, 200, size=num_salas) for i in range(1, num_disciplinas + 1)  # Distance from each room to the building of each discipline
# }
# distancia_salas_df = pd.DataFrame(distancia_salas)
# distancia_salas_df.index = np.arange(1, len(distancia_salas_df) + 1)  # Starting index from 1
# distancia_salas_df.to_csv('distancia_salas.csv', index_label='Sala')


# Generate data for distance from each room to the building of each discipline
np.random.seed(42)  # Set seed for reproducibility

# Create a base distance for each discipline
base_distances = np.random.randint(50, 100, size=num_disciplinas)

# Create the distance matrix with increasing values for each subsequent room
distancia_salas = {}
for i in range(1, num_disciplinas + 1):
    base_distance = 10 #base_distances[i-1]
    distances = [base_distance + 10 * (j - 1) for j in range(num_salas)]
    distancia_salas[f'Disciplina_{i}'] = distances

# Convert to DataFrame
distancia_salas_df = pd.DataFrame(distancia_salas)
distancia_salas_df.index = np.arange(1, len(distancia_salas_df) + 1)  # Starting index from 1

# Save to CSV
distancia_salas_df.to_csv('distancia_salas_2.csv', index_label='Sala')

# Display the DataFrame
print(distancia_salas_df)
