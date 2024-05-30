import numpy as np
import pandas as pd


class SimulatedAnnealing():
    
    # self.x = initial_solution
    # self.current_neighbor = self.solution_to_neighbor(initial_solution)
    
        
    def solution_to_neighbor(self, solution, D_sorted):
        neighbor = {}
        for j in D_sorted:
            for i in range(solution.shape[0]):
                if solution[i, j] == 1:
                    neighbor[j] = i
        return neighbor

    def neighbor_to_solution(self, neighbor):
        solution = np.zeros((len(neighbor), len(neighbor)), dtype=int)
        for room, discipline in neighbor.items():
            solution[discipline, room] = 1
        return solution
    
    
    # def objective_function(self):
    #     # Compute the first part of the objective function
    #     f = np.sum(x * D * N[:, np.newaxis])
        
    #     # Compute the penalty term
    #     penalty = 0
    #     for i in range(d):
    #         for j in range(s):
    #             g_ij = N[i] * x[i, j] - C[j]
    #             penalty += max(0, g_ij) ** 2
        
    #     # Add the penalty term to the objective function
    #     f += u * penalty
        
    #     return f
    
    def get_neighbor(self, d):
        # Converter o dicionário para uma lista de tuplas (chave, valor)
        keys = list(d.keys())

        # Escolher uma posição aleatória que não seja a primeira (pois não há elemento anterior para trocar)
        pos = np.random.randint(1, len(keys) - 1)
        print(pos)
        print(keys[pos])
        
        # Pegar as chaves na posição escolhida e na anterior
        # Trocar os valores dessas chaves
        d[keys[pos - 1]], d[keys[pos]] = d[keys[pos]], d[keys[pos - 1]]
        
        return d
            
    
    # def get_neighbor(self):
    #     neighbor = self.current_solution.copy()
    #     # Choose a random cell
    #     i = np.random.randint(0, 100)
    #     # Swap cells i and (i-1)
    #     aux = neighbor[i]
    #     neighbor[i] = neighbor[i-1]
    #     neighbor[i-1] = aux
    #     return neighbor
    
    # def optimize():
              
    #     # begin optimizing
    #     self.step, self.accept = 1, 0
    #     while self.step < self.step_max and self.t >= self.t_min:

    #     # get neighbor
    #     proposed_neighbor = self.get_neighbor()

    #     # check energy level of neighbor
    #     E_n = self.cost_func(proposed_neighbor)
    #     dE = E_n - self.current_energy
        
    #     # determine if we should accept the current neighbor
    #     if np.random.random() < self.safe_exp(-dE / self.t):
    #         self.current_energy = E_n
    #         self.current_state = proposed_neighbor[:]
    #         self.accept += 1
            
    #     # check if the current neighbor is best solution so far
    #     if E_n < self.best_energy:
    #         self.best_energy = E_n
    #         self.best_state = proposed_neighbor[:]
        
    #     # update temparature t
    #     self.t = self.update_t(self.step)
    #     # update step k
    #     self.step += 1
        
        