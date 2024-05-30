import pandas as pd
import numpy as np

# Configurações
num_disciplinas = 100
num_salas = 100

# Geração de dados para disciplinas
disciplinas = {
    'N': np.random.randint(20, 60, size=num_disciplinas)
}

disciplinas_df = pd.DataFrame(disciplinas)
disciplinas_df.to_csv('disciplinas.csv', index=False)

# Geração de dados para salas
salas = {
    'C': np.random.randint(30, 70, size=num_salas),
    'D': np.random.randint(50, 200, size=num_disciplinas)
}

salas_df = pd.DataFrame(salas)
salas_df.to_csv('salas.csv', index=False)

disciplinas_df.head(), salas_df.head()
