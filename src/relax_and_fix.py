import numpy as np
import random
from gurobipy import *

class RelaxAndFix:
    def __init__(self, N, C, D, num_disciplines, num_rooms, verbose=False):
        self.N = N  # Number of students per class
        self.C = C  # Capacity for each room
        self.D = D  # Distance from each room to the building of each discipline 
        self.num_disciplines = num_disciplines # Number of disciplines
        self.num_rooms = num_rooms # Number of classrooms
        self.verbose = verbose
    
    def _add_input_variables(self, d, s):
        self.model = Model(name='Classroom Assignment Problem')
        self.model.setParam('TimeLimit', 10)
        
        x = {}
        for i in range(1, d + 1):
            x[i] = {}
            for j in range(1, s + 1):
                x[i][j] = self.model.addVar(vtype=GRB.BINARY, name=f'x_{i}_{j}')
        
        return x
    
    def _add_constraints(self, C, N, x, d, s):
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

    def _define_objective_function(self, x, D, N, d, s):
        self.model.setObjective(
            quicksum(x[i][j] * D[i][j] * N[i]
                 for i in range(1, d + 1)
                 for j in range(1, s + 1)),
            sense=GRB.MINIMIZE
        )
        
    def _relax_and_fix(self, x, num_disciplines, num_rooms):
        # Stage 1: Unfix the first third of variables
        if self.verbose:
            print("First iteration of relax and fix...")
        for i in range(1, num_disciplines + 1):
            for j in range(1, num_rooms + 1):
                if i <= round(0.3 * num_disciplines):
                    self._unfix_variable(x[i][j])
                else:
                    self._relax_variable(x[i][j])
        
        self.model.optimize()
        self._found_a_valid_solution()

        # Stage 2: Fix the first third and unrelax the second third of the variables
        if self.verbose:
            print("Second iteration of relax and fix...")
        for i in range(1, num_disciplines + 1):
            for j in range(1, num_rooms + 1):
                if i <= round(0.3 * num_disciplines):
                    self._fix_variable(x[i][j], x[i][j].X)
                elif i <= round(0.6 * num_disciplines):
                    self._unrelax_variable(x[i][j], GRB.INTEGER)
                else:
                    self._relax_variable(x[i][j])
        
        self.model.optimize()
        self._found_a_valid_solution()

        # Stage 3: Fix the first two thirds and unrelax the last third of the variables
        if self.verbose:
            print("Third iteration of relax and fix...")
        for i in range(1, num_disciplines + 1):
            for j in range(1, num_rooms + 1):
                if i <= round(0.6 * num_disciplines):
                    self._fix_variable(x[i][j], x[i][j].X)
                else:
                    self._unrelax_variable(x[i][j], GRB.INTEGER)
        
        self.model.optimize()
        self._found_a_valid_solution()

    def _fix_variable(self, var, value):
        var.lb = value
        var.ub = value
        return var

    def _unfix_variable(self, var, lb=0):
        var.lb = lb
        var.ub = float('inf')
        return var

    def _relax_variable(self, var):
        var.vtype = GRB.CONTINUOUS
        var.lb = 0
        var.ub = 1
        return var
    
    def _unrelax_variable(self, var, vtype, lower_default=0):
        var.vtype = vtype
        var.lb = lower_default  # Reset lower bound to default (0)
        var.ub = float('inf')  # Reset upper bound to default (unconstrained)
        return var

    def _found_a_valid_solution(self):
        if self.model.SolCount > 0:
            if self.verbose:
                print("Best solution found:")
                for v in self.model.getVars():
                    print(f"{v.VarName} {v.X:g}")
            return True
        else:
            print("Error: it was not able to find a valid solution")
            exit(1)

    def compute_solution(self):
        x = self._add_input_variables(self.num_disciplines, self.num_rooms)
        self._add_constraints(self.C, self.N, x, self.num_disciplines, self.num_rooms)
        self._define_objective_function(x, self.D, self.N, self.num_disciplines, self.num_rooms)
        self._relax_and_fix(x, self.num_disciplines, self.num_rooms)
        
        if self.verbose:
            for v in self.model.getVars():
                print(f"{v.VarName} {v.X:g}")

            print(f"Obj: {self.model.ObjVal:g}")
        
        solution = {}
        for i in range(1, self.num_disciplines + 1):
            for j in range(1, self.num_rooms + 1):
                solution[(i, j)] = x[i][j].X

        self.model.dispose()
        
        return solution
