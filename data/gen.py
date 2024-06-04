## Script for generating random data for the problems's input variables ##

import pandas as pd
import numpy as np

# Defining the size of the problem
num_disciplinas = 100
num_salas = 100

# Generating data for room capacity
capacidade_salas = {
    'Capacidade': np.random.randint(30, 70, size=num_salas)  # Capacity for each room
}
capacidade_salas_df = pd.DataFrame(capacidade_salas)
capacidade_salas_df.index = np.arange(1, len(capacidade_salas_df) + 1)  # Starting index from 1
capacidade_salas_df.to_csv('capacidade_salas.csv', index_label='Sala')

# Generating data for number of students per class
alunos_por_disciplina = {
    'Alunos': np.random.randint(20, 60, size=num_disciplinas)  # Number of students per class
}
alunos_por_disciplina_df = pd.DataFrame(alunos_por_disciplina)
alunos_por_disciplina_df.index = np.arange(1, len(alunos_por_disciplina_df) + 1)  # Starting index from 1
alunos_por_disciplina_df.to_csv('disciplinas.csv', index_label='Disciplina')

# Generating data for distance from each room to the building
distancia_salas = {
    f'Disciplina_{i}': np.random.randint(50, 200, size=num_salas) for i in range(1, num_disciplinas + 1)  # Distance from each room to the building of each discipline
}
distancia_salas_df = pd.DataFrame(distancia_salas)
distancia_salas_df.index = np.arange(1, len(distancia_salas_df) + 1)  # Starting index from 1
distancia_salas_df.to_csv('distancia_salas.csv', index_label='Sala')