from ortools.sat.python import cp_model
import uuid
from math import floor

# Settings
LISTINGS_START = 0
LISTINGS_STOP = 4
# LISTINGS_STOP = 2
MAX_TIME = 10.0


class SolutionsContainer(cp_model.CpSolverSolutionCallback):
    """ Container to store solutions """

    def __init__(self, variables):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__variables = variables
        self.__solution_count = 0
        self.__solutions = []

    def on_solution_callback(self):
        """ Callback that runs after each solution found """
        self.__solution_count += 1
        solution = {}
        for variable in self.__variables:
            solution[variable.Name()] = self.Value(variable)
        self.__solutions.append(solution)

    def solution_count(self):
        """ Returns the total numbr of solutions """
        return self.__solution_count

    def solutions(self):
        """ Return the soutions """
        return self.__solutions


def SearchForAllSolutions(*args, start):
    """ Searches for all solutions to the linear equations """
    MAX_WHISPERS = 3 if len(args) < 3 else 5
    model = cp_model.CpModel()
    vals = []
    constraints = []
    constraints_dict = {}
    uuid_ref = {}

    # Add variable constraints to the model
    for index in range(len(args)):
        new_constraints = _get_constraint(model, args[index], index)
        constraints_dict.update(new_constraints[0])
        constraints.append(new_constraints[0])
        uuid_ref.update(new_constraints[1])

    # Add Constraints to keep track of variable usage
    used_vars = [model.NewBoolVar("{}".format(i)) for i in range(len(constraints_dict))]

    # Adds conditional constraints based on variable usage to the model
    for uniq_id, index in zip(constraints_dict, range(len(constraints_dict))):
        model.Add(constraints_dict[uniq_id]["val"] == 0).OnlyEnforceIf(
            used_vars[index].Not()
        )
        model.Add(constraints_dict[uniq_id]["val"] > 0).OnlyEnforceIf(used_vars[index])

    # Adds constraint to limit the number of non-zero variables
    model.Add(sum(used_vars) <= MAX_WHISPERS)

    # Adds the equations to the model
    for index in range(len(constraints) - 1):
        eqn1 = []
        eqn2 = []
        # Equations are added with an alternating pattern
        # Equation 1 depends on both have/want amt when its not the first equation
        for constraint in constraints[index]:
            constraint = constraints[index][constraint]
            coeff = (
                constraint["coefficients"][0]
                if index == 0
                else constraint["coefficients"][1]
            )
            eqn1.append(coeff * constraint["val"])
            vals.append(constraint["val"])
        # print(f'eqn1: {eqn1}')
        for constraint in constraints[index + 1]:
            constraint = constraints[index + 1][constraint]
            eqn2.append(constraint["coefficients"][0] * constraint["val"])
            vals.append(constraint["val"])
        # print(f'eqn2: {eqn2}')

        model.Add(sum(eqn1) == sum(eqn2))

    # Creates Solver and Initializes CP-Sat Solver
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = MAX_TIME
    container = SolutionsContainer(vals)

    # solver.parameters.log_search_progress = True

    status = solver.SearchForAllSolutions(model, container)

    ###
    # print(solver.StatusName(status))
    # print(container.solution_count())
    # print(container.solutions())
    ###

    trades = []
    trades.append(start)
    for arg in args:
        trades.append(arg[0]["has_curr"])

    return {
        # "trades": ",".join([i[0]["has_curr"] for i in args]),
        "trades": ",".join(trades),
        "solutions_num": container.solution_count(),
        "solutions": container.solutions(),
        "uuid_ref": uuid_ref,
        "time": solver.WallTime(),
        "status": solver.StatusName(),
    }


def _get_constraint(model, listings, index):
    constraint = {}
    ref = {}
    for listing in listings[LISTINGS_START:LISTINGS_STOP]:
        uuid1 = uuid.uuid1()
        max_val = floor(listing["has_stock"] / listing["has_rate"])
        coefficient_p1 = listing["want_rate"] if index != 0 else listing["has_rate"]
        # coefficient_p1 = listing["want_rate"] if index == 0 else listing["has_rate"]
        coefficient_p2 = listing["want_rate"] * listing["has_rate"]
        conversion = coefficient_p2 if index % 2 == 0 else listing["has_rate"]
        constraint[str(uuid1)] = {
            "val": model.NewIntVar(0, max_val, str(uuid1)),
            "listing": listing,
            "coefficients": [coefficient_p1, coefficient_p2],
            "conversion": conversion,
        }
        ref[str(uuid1)] = {
            "listing": listing,
            "conversion": conversion,
        }
    return (constraint, ref)


# arr2 = [
#     [
#         {"has_curr": "curr", "want_rate": 100, "has_rate": 1, "has_stock": 24},
#     ],
#     [
#         {"has_curr": "curr", "want_rate": 1, "has_rate": 10, "has_stock": 24},
#         {"has_curr": "curr", "want_rate": 1, "has_rate": 25, "has_stock": 25},
#     ],
#     [
#         {"has_curr": "curr", "want_rate": 5, "has_rate": 20, "has_stock": 60},
#         {"has_curr": "curr", "want_rate": 1, "has_rate": 5, "has_stock": 30},
#     ],
# ]
# arr3 = [
#     [
#         {"has_curr": "curr", "want_rate": 50, "has_rate": 110, "has_stock": 851},
#     ],
#     [
#         {"has_curr": "curr", "want_rate": 60, "has_rate": 1, "has_stock": 15},
#     ],
#     [
#         {"has_curr": "curr", "want_rate": 5, "has_rate": 76, "has_stock": 9861},
#         {"has_curr": "curr", "want_rate": 5, "has_rate": 76, "has_stock": 249},
#     ],
# ]
# SearchForAllSolutions(*arr2, start="curr")