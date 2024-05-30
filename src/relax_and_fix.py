import numpy as np
import random
from gurobipy import *

# Set the environment variable to point to your license file
#os.environ["GRB_LICENSE_FILE"] =  "C:\Users\LP2G\gurobi.lic"

class RelaxAndFix:
    def __init__(self, N, C, D):
        self.N = N  # Número de estudantes por disciplina
        self.C = C  # Capacidade das salas
        self.D = D  # Distancia das salas
        self.d = 100 # Number of disciplines
        self.n = 100 # Number of classrooms
        
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

    def get_initial_solution(self, N, D):
        # Ordenar as disciplinas e salas pela quantidade de alunos e distancia das salas
        # As salas com menor distancia sao atribuidas as turmas com maior numero de alunos,
        # de modo a minimizar a funcao objetivo
        N_sorted = self.order_descending(N)
        #print(N_sorted)
        D_sorted = self.order_ascending(D)
        #print(D_sorted)

        # Initialize the solution (x) matrix
        initial_solution = np.zeros((len(N), len(D)), dtype=int)
        for i in range(len(N)):
            initial_solution[N_sorted[i], D_sorted[i]] = 1
            
        return initial_solution

    def add_input_variables(self):
        self.model = Model(name='Room Allocation Problem')
        self.model.setParam('TimeLimit', 10)
        
        x = {}
        for i in range(1, 100 + 1):
            x[i] = {}
            for j in range(1, 100 + 1):
                x[i][j] = self.model.addVar(vtype=GRB.BINARY, name=f'x_{i}_{j}')
        
        return x
    
    def add_constraints(self, x, C, d, s):
        # Constraint 1: Each room is assigned to exactly one discipline
        for j in range(1, s + 1):
            self.model.addConstr(quicksum(x[i][j] for i in range(1, d + 1)) == 1)
        
        # Constraint 2: Each discipline is assigned to exactly one room
        for i in range(1, d + 1):
            self.model.addConstr(quicksum(x[i][j] for j in range(1, s + 1)) == 1)

        # Constraint 3: The number of students in each room does not exceed the room capacity
        for i in range(1, d + 1):
            for j in range(1, s + 1):
                self.model.addConstr(N[i] * x[i][j] <= C[j])

    def define_objective_function(self, x, D, N, d, s):
        self.model.setObjective(
            quicksum(x[i][j] * D[i][j] * N[i]
                 for i in range(1, d + 1)
                 for j in range(1, s + 1)),
            sense=GRB.MINIMIZE
        )
        
    def _fix_variable(self, var, value):
        var.lb = value
        var.ub = value
        return var
    
    def _unfix_variable(self, var, lb=0):
        var.lb = lb
        var.ub = float('inf')
        return var
    
    def _unrelax_variable(self, var, vtype, lower_default=0):
        var.vtype = vtype
        var.lb = lower_default  # Reset lower bound to default (0)
        var.ub = float('inf')  # Reset upper bound to default (unconstrained)
        return var
    
    def _relax_variable(self, var):
        var.vtype = GRB.CONTINUOUS
        var.ub = float('inf')
        var.lb = 0
        return var


    def relax_and_fix(self, J, num_tasks):
        #if self.verbose:
        print ("First iteration of relax and fix...")
        for i in range(0, num_tasks):
            task_id = i + 1
            for j in range(0, num_tasks):
                order = j +1
                if i < round(0.3 * num_tasks):
                    self._unfix_variable(J[task_id][order])
                else:
                    self._relax_variable(J[task_id][order])
        
        self.model.optimize()
        self._found_a_valid_solution()

        if self.verbose:
            print ("Second iteration of relax and fix...")
        for i in range(0, num_tasks):
            task_id = i + 1
            for j in range(0, num_tasks):
                order = j +1
                if i < round(0.3 * num_tasks):
                    self._fix_variable(J[task_id][order], J[task_id][order].X)
                elif i < round(0.6 * num_tasks) :
                    self._unrelax_variable(J[task_id][order], GRB.INTEGER)
                else:
                    self._relax_variable(J[task_id][order])
        
        self.model.optimize()
        self._found_a_valid_solution()

        if self.verbose:
            print ("Third iteration of relax and fix...")
        for i in range(0, num_tasks):
            task_id = i + 1
            for j in range(0, num_tasks):
                order = j +1
                if i < round(0.6 * num_tasks) :
                    self._fix_variable(J[task_id][order], J[task_id][order].X)
                else:
                    self._unrelax_variable(J[task_id][order], GRB.INTEGER)
        
        self.model.optimize()
        self._found_a_valid_solution()
        


    def optimize(self, initial_solution, iterations=1000):
        # Copiar a solução inicial
        best_solution = initial_solution.copy()
        best_cost = self.objective_function(best_solution)
        
        for _ in range(iterations):
            # Realizar um swap randômico
            new_solution, _ = self.swap_random_values(best_solution.copy())
            new_cost = self.objective_function(new_solution)
            
            # Verificar se a nova solução é melhor
            if new_cost < best_cost:
                best_solution = new_solution
                best_cost = new_cost
        
        return best_solution

