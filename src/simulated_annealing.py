import numpy as np
import pandas as pd


class SimulatedAnnealing:
    def __init__(self, N, C, D, initial_solution, num_disciplines, num_rooms, verbose=False):
        self.N = N  # Number of students per class
        self.C = C  # Capacity for each room
        self.D = D  # Distance from each room to the building of each discipline 
        self.initial_solution = initial_solution
        self.num_disciplines = num_disciplines # Number of disciplines
        self.num_rooms = num_rooms # Number of classrooms
        
        self.u = 1000  # Penalty coefficient

        self.verbose = verbose
    
    def _solution_to_neighbor(self, solution):
        """Converts the solution dictionary to a neighbor representation."""
        neighbor = {}
        for j in range(1, self.num_rooms + 1):
            for i in range(1, self.num_disciplines + 1):
                if solution[(i, j)] == 1:
                    neighbor[j] = i

        return neighbor

    def _neighbor_to_solution(self, neighbor):
        """Converts the neighbor representation back to a solution dictionary."""
        solution = {}
        for i in range(1, self.num_disciplines + 1):
            for j in range(1, self.num_rooms + 1):
                solution[(i, j)] = 0
        
        for j, i in neighbor.items():
            solution[(i, j)] = 1
            
        return solution
    
    def _objective_function(self, x):
        # Compute objective function
        f = 0
        for i in range(1, self.num_disciplines + 1):
            for j in range(1, self.num_rooms + 1):
                f += x[(i, j)] * self.D[j][i] * self.N[i]
        
        # Compute the penalty
        # We are only considering restriction 3 to compute the penalty,
        # since the restrictions 1 and 2 are automatically satisfied by the neighborhood 
        penalty = 0
        for i in range(1, self.num_disciplines + 1):
            for j in range(1, self.num_rooms + 1):
                g_ij = self.N[i] * x[(i, j)] - self.C[j]
                penalty += max(0, g_ij) ** 2

        f += self.u * penalty
        
        return f        
    
    def _shake_up_neighborhood(self, neighbor):
        # Choose a random cell
        i = np.random.randint(2, self.num_rooms + 1)
        
        num_desciplines = len(neighbor)
        for index in range(1, num_desciplines + 1):
            target_index = (i - index) % num_desciplines
            # Skip index 0, as it start indexing from 1
            if target_index != 0:
                if (self.C[target_index] >= self.N[neighbor[i]]) and (self.C[i] >= self.N[neighbor[target_index]]):
                    # Swap cells i and (i-1)
                    aux = neighbor[i]
                    neighbor[i] = neighbor[target_index]
                    neighbor[target_index] = aux
                    return neighbor
        # Return current neighbor if it could not identify a valid neighbor for the random selected index
        return neighbor
    
    def _update_temperature(self, t):
        return 0.7 * t
    
    def _get_initial_temperature(self):
        dE = []
        initial_neighbor = self._solution_to_neighbor(self.initial_solution)
        initial_energy = self._objective_function(self.initial_solution)
        
        # Perform 100 pertubations and get the average dE
        for _ in range(100):
            proposed_neighbor = self._shake_up_neighborhood(initial_neighbor.copy())
            proposed_solution = self._neighbor_to_solution(proposed_neighbor)
            proposed_energy = self._objective_function(proposed_solution)
            dE.append(proposed_energy - initial_energy)
        avg_dE = np.mean(dE)
        
        # Deduce t_0 from the equation exp(−∆E/t_0) = τ_0.
        # Here we choose initial acceptance rate as 𝜏_0 = 0.2
        t_0 = -avg_dE / np.log(0.2)
        
        if self.verbose:
            print(f"Temperatura inicial: {t_0}")
        
        return t_0
    
    def compute_solution(self):
        
        # Define the initial temperature t_k >= 0
        t_k = self._get_initial_temperature()
        # Define the number of iterations at each temperature
        M_k = 10 * self.num_rooms if self.num_rooms < 10 else 100
        
        # Select a initial solution
        self.current_solution = self.initial_solution
        self.current_neighbor = self._solution_to_neighbor(self.initial_solution)
        self.current_energy = self._objective_function(self.initial_solution)
        
        best_solution, best_energy = self.current_solution, self.current_energy

        no_improvement_stages = 0
        k = 0
        # The stop criteria is defined as 3 consecutive steps without improvement
        while no_improvement_stages < 3:

            m = 0
            while m <= M_k:

                # Generate a new solution by shaking the neighborhood
                proposed_neighbor = self._shake_up_neighborhood(self.current_neighbor.copy())
                proposed_solution = self._neighbor_to_solution(proposed_neighbor)

                # Compute the energy level of the new solution
                E_n = self._objective_function(proposed_solution)
                dE = E_n - self.current_energy
                    
                # Determine if we should accept the new solution
                if dE <= 0:
                    #print('aaaa')
                    self.current_neighbor = proposed_neighbor
                    self.current_solution = proposed_solution
                    self.current_energy = E_n
                else:     
                    #print(np.exp(-dE/t_k))
                    if np.random.random() < np.exp(-dE/t_k):
                        self.current_neighbor = proposed_neighbor
                        self.current_solution = proposed_solution
                        self.current_energy = E_n
                
                m += 1
                
            # Check if there was improvement of the solution on this step
            if self.current_energy < best_energy:
                best_solution, best_energy = self.current_solution, self.current_energy
                no_improvement_stages = 0
            else:
                no_improvement_stages += 1
                    
            # Update temparature t_k
            t_k = self._update_temperature(t_k)
            # Update step k
            k += 1
            
            if self.verbose:
                print(f"Iteration {k}: Temperature = {t_k:.4f}, Current Energy = {self.current_energy:.4f}, Best Energy = {best_energy:.4f}")

        return best_solution
        