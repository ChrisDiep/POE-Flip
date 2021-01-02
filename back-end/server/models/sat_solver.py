from ortools.sat.python import cp_model
import uuid
from math import floor

LISTINGS_START = 0
LISTINGS_STOP = 5
MAX_TIME = 10.0 #seconds
MAX_WHISPERS = 4
class SolutionsContainer(cp_model.CpSolverSolutionCallback):
    def __init__(self, variables):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__variables = variables
        self.__solution_count = 0
        self.__solutions = []

    def on_solution_callback(self):
        self.__solution_count += 1
        solution = {}
        for variable in self.__variables:
            solution[variable.Name()] = self.Value(variable)
        self.__solutions.append(solution)

    def solution_count(self):
        return self.__solution_count

    def solutions(self):
        return self.__solutions


def SearchForAllSolutions(*args):
    model = cp_model.CpModel()
    vals = []
    constraints = []
    constraints_dict = {}
    # print(f"Length: {len(args) - 1}")
    for index in range(len(args)):
        new_constraints = _get_constraint(model, args[index], index)
        constraints_dict.update(new_constraints)
        # constraints_dict.update(new_constraints[1])
        constraints.append(new_constraints)
    print(len(constraints_dict))

    used_vars = [model.NewBoolVar('{}'.format(i)) for i in range(len(constraints_dict))]
    for uuid, index in zip(constraints_dict, range(len(constraints_dict))):
        model.Add(constraints_dict[uuid]["val"] == 0).OnlyEnforceIf(used_vars[index].Not())
        model.Add(constraints_dict[uuid]["val"] > 0).OnlyEnforceIf(used_vars[index])
    model.Add(sum(used_vars) <= MAX_WHISPERS)

    for index in range(len(constraints) - 1):
        eqn1 = []
        eqn2 = []
        for constraint in constraints[index]:
            constraint = constraints[index][constraint]
            # print(constraint)
            coeff = constraint["coefficients"][0] if index == 0 else constraint["coefficients"][1]
            eqn1.append(
                coeff
                * constraint["val"]
            )
            vals.append(constraint["val"])
        print(f"equation 1: {eqn1}")
        for constraint in constraints[index + 1]:
            constraint = constraints[index + 1][constraint]
            # print(constraint)
            eqn2.append(constraint["coefficients"][0] * constraint["val"])
            vals.append(constraint["val"])

        print(f"equation 2: {eqn2}")
        model.Add(sum(eqn1) == sum(eqn2))
    solver = cp_model.CpSolver()
    # solver.parameters.log_search_progress = True
    solver.parameters.max_time_in_seconds = MAX_TIME
    container = SolutionsContainer(vals)
    # print(model)
    status = solver.SearchForAllSolutions(model, container)
    # print(f"Status = {solver.StatusName(status)}")
    print(f"Number of Solutions Found: {container.solution_count()}")
    # print(container.solutions())
    # print(constraints_dict)
    # return {
    #     "solutions": container.solutions(),
    #     "reference": constraints_dict,
    # }
    return {
        "trades": " ".join([i[0]["has_curr"] for i in args]),
        "solutions_num": container.solution_count(),
        "time": solver.WallTime(),
        "status": solver.StatusName(),
    }


def _get_constraint(model, listings, index):
    constraint = {}
    for listing in listings[LISTINGS_START:LISTINGS_STOP]:
        uuid1 = uuid.uuid1()
        max_val = floor(listing["has_stock"] / listing["has_rate"])
        coefficient_p1 = listing["want_rate"] if index != 0 else listing["has_rate"]
        coefficient_p2 = listing["want_rate"] * listing["has_rate"]
        conversion = coefficient_p2 if index % 2 == 0 else listing["has_rate"]
        constraint[str(uuid1)] = {
            "val": model.NewIntVar(0, max_val, str(uuid1)),
            "listing": listing,
            "coefficients": [coefficient_p1, coefficient_p2],
            "conversion": conversion,
        }
    return constraint


# arr = [
#     [
#         {"has_curr": "curr", "want_rate": 100, "has_rate": 1, "has_stock": 24},
#     ],
#     [
#         {"has_curr": "curr","want_rate": 5, "has_rate": 550, "has_stock": 2002},
#         {"has_curr": "curr", "want_rate": 5, "has_rate": 550, "has_stock": 1700},
#         {"has_curr": "curr", "want_rate": 5, "has_rate": 550, "has_stock": 675},
#     ],
# ]
# arr2 = [
#     [
#         {"want_rate": 100, "has_rate": 1, "has_stock": 24},
#     ],
#     [
#         {"want_rate": 1, "has_rate": 10, "has_stock": 24},
#         {"want_rate": 1, "has_rate": 25, "has_stock": 25},
#     ],
#     [
#         {"want_rate": 5, "has_rate": 20, "has_stock": 60},
#         {"want_rate": 1, "has_rate": 5, "has_stock": 30},
#     ],
# ]
# SearchForAllSolutions(*arr)
