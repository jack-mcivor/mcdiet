import json
from collections import defaultdict
from pprint import pprint

from pkg_resources import resource_filename
from pulp import LpMinimize, LpProblem, LpStatus, LpVariable, lpSum, value

# https://en.wikibooks.org/wiki/Fundamentals_of_Human_Nutrition/Average_Macronutrient_Distribution_Range
# https://nutritionfoundation.org.nz/nutrition-facts/minerals/sodium
C = 2500
DEFAULT_NUTR_REQS = {
    'cals': (C, None),
    # default macros are based on percentage of calories
    'carbs': (C/4*0.45, C/4*0.65),
    'protein': (C/4*0.1, C/4*0.35),
    'fat': (C/9*0.2, C/9*0.35),
    'sat': (None, None),
    'sugar': (None, C/4*0.25),
    'sodium': (920, 2300),
}

def read_json(filename):
    with open(resource_filename(__name__, f'assets/{filename}'), 'r') as f:
        return json.load(f)

class InfeasibleError(ValueError):
    pass

class UnboundedError(ValueError):
    pass


class DietProblem:
    """
    TODO: fractional foods? eg. buy big mac combo and eat 1/2 of fries
    TODO: error introspection? eg. why is infeasible?
    TODO: input validation?
    """
    def __init__(self, menu=None, nutr=None):
        self.history = []
        # Assets
        self.menu = menu or read_json('menu.json')
        self.nutr = nutr or read_json('foods_and_nutrition.json')

        # Indices with deterministic order
        self.meals = list(sorted(self.menu.keys()))
        self.foods = list(sorted(self.nutr.keys()))

    def solve(self, max_menu_item=None, max_food_item=3, nutrition=DEFAULT_NUTR_REQS, exclude=None, include=None):
        """Create, formulate and solve the diet problem for given constraints
        """
        self.prob = prob = LpProblem(__class__, LpMinimize)

        # Variables
        self.xm = xm = LpVariable.dicts('meals', self.meals, 0, max_menu_item, cat='Integer')
        self.xf = xf = LpVariable.dicts('foods', self.foods, 0, max_food_item, cat='Integer')

        # Objective
        prob += lpSum(self.menu[i]['price']*xm[i] for i in self.meals)

        # Ensure that foods eaten are available under meals bought
        for j in self.foods:
            prob += lpSum([self.menu[i]['foods'].get(j, 0)*xm[i] for i in self.meals]) >= xf[j]

        # Must meet nutrition
        for r, (lower, upper) in nutrition.items():
            if lower:
                prob += lpSum([xf[i]*self.nutr[i][r] for i in self.foods]) >= lower
            if upper:
                prob += lpSum([xf[i]*self.nutr[i][r] for i in self.foods]) <= upper

        if include:
            for food in include:
                prob += xf[food] >= 1

        if exclude:
            for food in exclude:
                prob += xf[food] == 0

        # Solve and save
        status = LpStatus[prob.solve()]
        if status == 'Optimal':
            pass
        elif status == 'Infeasible':
            raise InfeasibleError()
        elif status == 'Unbounded':
            raise UnboundedError
        else:
            raise ValueError(status)

        solution = self.parse_solution()
        self.history.append(solution)
        return solution

    def parse_solution(self):
        cost = round(value(self.prob.objective), 2)
        purchases = {i: int(value(self.xm[i])) for i in self.meals}
        eats = {i: int(value(self.xf[i])) for i in self.foods}

        solution = {'cost': cost, 'purchase': []}
        for meal, n_bought in purchases.items():
            if n_bought:
                foods = []
                for food, n_available in self.menu[meal]['foods'].items():
                    n_available = n_available * n_bought
                    n_eaten = eats[food]
                    # Eat as much as possible (greedy)- in reality there are lots of straight swaps that do not change the structure of the solution-
                    # eg. drink the coke from my Big Mac combo or drink the coke from my Hunger Buster Combo
                    # This methodolgy requires (arbitrarily) assigning foods to meals
                    n_reported = min(n_eaten, n_available)
                    eats[food] -= n_reported
                    foods.append({'food': food, 'available': n_available, 'eat': n_reported})

                solution['purchase'].append({'meal': meal,
                                             'bought': n_bought,
                                             'foods': foods})

        # Optional: check there are no remaining foods to eat
        for i, n_eaten in eats.items():
            assert n_eaten == 0, i

        return solution


    def print_last_solution(self):
        """Simple way of printing the solution
        """
        pprint(self.history[-1])
