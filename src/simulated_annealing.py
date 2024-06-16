import numpy as np
import pandas as pd


class SimulatedAnnealing:
    def __init__(self, N, C, D, initial_solution, num_disciplines, num_rooms, verbose=True):
        self.N = N  # Number of students per class
        self.C = C  # Capacity for each room
        self.D = D  # Distance from each room to the building of each discipline 
        self.initial_solution = initial_solution
        self.num_disciplines = num_disciplines # Number of disciplines
        self.num_rooms = num_rooms # Number of classrooms
        
        self.u = 1000

        self.verbose = verbose
    
    def solution_to_neighbor(self, solution):
        neighbor = {}
        for j in range(1, self.num_rooms + 1):
            for i in range(1, self.num_disciplines + 1):
                if solution[(i, j)] == 1:
                    neighbor[j] = i

        return neighbor

    def neighbor_to_solution(self, neighbor):
        solution = {}
        for i in range(1, self.num_disciplines + 1):
            for j in range(1, self.num_rooms + 1):
                solution[(i, j)] = 0
        
        for j, i in neighbor.items():
            solution[(i, j)] = 1
            
        return solution
    
    def objective_function(self, x):
        f = 0
        for i in range(1, self.num_disciplines + 1):
            for j in range(1, self.num_rooms + 1):
                f += x[(i, j)] * self.D[i][j] * self.N[i]

        penalty = 0
        for i in range(1, self.num_disciplines + 1):
            for j in range(1, self.num_rooms + 1):
                g_ij = self.N[i] * x[(i, j)] - self.C[j]
                penalty += max(0, g_ij) ** 2

        f += self.u * penalty
        
        return f        
    
    def get_next_neighbor(self, neighbor):
        # Choose a random cell
        i = np.random.randint(2, self.num_rooms + 1)
        
        # Swap cells i and (i-1)
        aux = neighbor[i]
        neighbor[i] = neighbor[i-1]
        neighbor[i-1] = aux
        
        return neighbor
    
    def _update_temperature(self, t):
        return 0.9 * t
    
    def _get_initial_temperature(self):
        dE = []
        initial_neighbor = self.solution_to_neighbor(self.initial_solution)
        initial_energy = self.objective_function(self.initial_solution)
        
        for _ in range(100):
            proposed_neighbor = self.get_next_neighbor(initial_neighbor)
            proposed_solution = self.neighbor_to_solution(proposed_neighbor)
            proposed_energy = self.objective_function(proposed_solution)
            dE.append(abs(proposed_energy - initial_energy))
            
        avg_dE = np.mean(dE)
        t0 = -avg_dE / np.log(0.5)
        
        return t0
    
    def compute_solution(self):
        
        # Define the initial temperature t_k >= 0
        t_k = self._get_initial_temperature()
        # Define the number of iterations at each temperature
        M_k = 100 * self.num_rooms
        
        # Select a initial solution
        current_solution = self.initial_solution
        current_neighbor = self.solution_to_neighbor(self.initial_solution)
        current_energy = self.objective_function(self.initial_solution)
        
        best_solution, best_energy = current_solution, current_energy

        no_improvement_stages = 0
        k = 0
        # The stop criteria is defined as 3 consecutive steps without improvement
        while no_improvement_stages < 3:

            m = 0
            while m <= M_k:

                # Generate a new solution by shaking the neighborhood
                proposed_neighbor = self.get_next_neighbor(current_neighbor)
                proposed_solution = self.neighbor_to_solution(proposed_neighbor)

                # Compute the energy level of the new solution
                E_n = self.objective_function(proposed_solution)
                dE = E_n - current_energy
                    
                # Determine if we should accept the new solution
                if dE <= 0:
                    current_neighbor = proposed_neighbor
                    current_solution = proposed_solution
                    current_energy = E_n
                else:     
                    if np.random.random() < np.exp(-dE/t_k):
                        current_neighbor = proposed_neighbor
                        current_solution = proposed_solution
                        current_energy = E_n
                
                m += 1
                
            # Check if there was improvement of the solution on this step
            if current_energy < best_energy:
                best_solution, best_energy = current_solution, current_energy
                no_improvement_stages = 0
            else:
                no_improvement_stages += 1
                    
            # Update temparature t_k
            t_k = self._update_temperature(t_k)
            # Update step k
            k += 1
            
            if self.verbose:
                print(f"Iteration {k}: Temperature = {t_k:.4f}, Current Energy = {current_energy:.4f}, Best Energy = {best_energy:.4f}")

        return best_solution
        