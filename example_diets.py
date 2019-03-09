from pprint import pprint

from mcdiet import DietProblem

diet = DietProblem()

# I don't care where my calories come from
# $6.90, 23x mayonnaise
result = diet.solve(nutrition={'cals': (2000, None)}, max_food_item=None)
pprint(result)

# Don't I need protein?
# $11.20, 10pc mcnugs, 8x mayonnaise
result = diet.solve(nutrition={'cals': (2000, None), 'protein': (50, None)}, max_food_item=None)
pprint(result)

# Ok, no sauce please. And I really want a big mac
result = diet.solve(nutrition={'cals': (2000, None), 'protein': (50, None)}, max_food_item=None,
                     exclude=['mayonnaise', 'sweet-n-sour-sauce', 'barbeque-sauce'], include=['big-mac'])
pprint(result)

# I should probably watch my saturated fat and sugar. And make sure I don't eat more than 3 of the same thing
result = diet.solve(nutrition={'cals': (2000, None), 'protein': (50, None), 'sat': (None, 20), 'sugar': (None, 50)}, max_food_item=3)
pprint(result)

# What about recommended requirements?
result = diet.solve()
pprint(result)
