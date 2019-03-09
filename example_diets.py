from mcdiet import DietProblem

diet = DietProblem()

# I don't care where my calories come from
# $6.90, 23x mayonnaise
diet.solve(nutrition={'cals': (2000, None)}, max_food_item=None)
diet.print_last_solution()

# Don't I need protein?
# $11.20, 10pc mcnugs, 8x mayonnaise
diet.solve(nutrition={'cals': (2000, None), 'protein': (50, None)}, max_food_item=None)
diet.print_last_solution()

# Ok, no sauce please. And I really want a big mac
diet.solve(nutrition={'cals': (2000, None), 'protein': (50, None)}, max_food_item=None, 
           exclude=['mayonnaise', 'sweet-n-sour-sauce', 'barbeque-sauce'], include=['big-mac'])
diet.print_last_solution()

# I should probably watch my saturated fat and sugar. And make sure I don't eat more than 3 of the same thing
diet.solve(nutrition={'cals': (2000, None), 'protein': (50, None), 'sat': (None, 20), 'sugar': (None, 50)}, max_food_item=3)
diet.print_last_solution()

# What about recommended requirements?
diet.solve()
diet.print_last_solution()
