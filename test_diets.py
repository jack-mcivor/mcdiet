from pprint import pprint
from mcdiet import DietProblem, InfeasibleError
import pytest


def test_no_purchase():
    menu = {'Big Mac': {'price': 5, 'foods': {'big-mac': 1}}}
    nutr = {'big-mac': {'cals': 100, 'protein': 25, 'carbs': 50, 'fat': 10, 'sat': 5, 'sugar': 0, 'sodium': 0}}
    diet = DietProblem(menu=menu, nutr=nutr)

    # Single big mac
    diet.solve(nutrition={'protein': (None, None)})
    result = diet.history[-1]
    expected = {'cost': 0.0, 'purchase': []}
    assert result == expected


def test_infeasible():
    menu = {'Big Mac': {'price': 5, 'foods': {'big-mac': 1}}}
    nutr = {'big-mac': {'cals': 100, 'protein': 25, 'carbs': 50, 'fat': 10, 'sat': 5, 'sugar': 0, 'sodium': 0}}
    diet = DietProblem(menu=menu, nutr=nutr)

    with pytest.raises(InfeasibleError):
        diet.solve(nutrition={'protein': (2, 1)})
    with pytest.raises(InfeasibleError):
        diet.solve(nutrition={'protein': (None, 30), 'cals': (200, None)})


def test_single_meal_single_food():
    menu = {'Big Mac': {'price': 5, 'foods': {'big-mac': 1}}}
    nutr = {'big-mac': {'cals': 100, 'protein': 25, 'carbs': 50, 'fat': 10, 'sat': 5, 'sugar': 0, 'sodium': 0}}
    diet = DietProblem(menu=menu, nutr=nutr)

    # Single big mac
    diet.solve(nutrition={'protein': (20, None)})
    result = diet.history[-1]
    expected = {'cost': 5.0, 'purchase': [{'meal': 'Big Mac', 'bought': 1, 'foods': [{'food': 'big-mac', 'available': 1, 'eat': 1}]}]}
    assert result == expected

    # Two big macs
    diet.solve(nutrition={'protein': (40, None)})
    result = diet.history[-1]
    expected = {'cost': 10.0, 'purchase': [{'meal': 'Big Mac', 'bought': 2, 'foods': [{'food': 'big-mac', 'available': 2, 'eat': 2}]}]}
    assert result == expected


def test_single_meal_combo():
    menu = {'Big Mac Combo': {'price': 5, 'foods': {'big-mac': 1, 'coke': 1}}}
    nutr = {'big-mac': {'cals': 100, 'protein': 25, 'carbs': 50, 'fat': 10, 'sat': 5, 'sugar': 0, 'sodium': 0},
            'coke': {'cals': 100, 'protein': 0, 'carbs': 30, 'fat': 0, 'sat': 0, 'sugar': 30, 'sodium': 0}}
    diet = DietProblem(menu=menu, nutr=nutr)

    # Single big mac- don't drink coke
    diet.solve(nutrition={'protein': (20, None), 'sugar': (None, 10)})
    result = diet.history[-1]
    expected = {'cost': 5.0, 'purchase': [{'meal': 'Big Mac Combo', 'bought': 1, 
                                           'foods': [{'food': 'big-mac', 'available': 1, 'eat': 1}, 
                                                     {'food': 'coke', 'available': 1, 'eat': 0}]}]}
    assert result == expected

    # Two big macs, one coke
    diet.solve(nutrition={'protein': (40, None), 'sugar': (30, 40)})
    result = diet.history[-1]
    expected = {'cost': 10.0, 'purchase': [{'meal': 'Big Mac Combo', 'bought': 2, 
                                           'foods': [{'food': 'big-mac', 'available': 2, 'eat': 2}, 
                                                     {'food': 'coke', 'available': 2, 'eat': 1}]}]}
    assert result == expected

def test_two_meal_combo():
    menu = {'Big Mac Coke': {'price': 5, 'foods': {'big-mac': 1, 'coke': 1}},
            'Double Big Mac Fries': {'price': 8, 'foods': {'big-mac': 2, 'fries': 1}}}

    nutr = {'big-mac': {'cals': 100, 'protein': 25, 'carbs': 50, 'fat': 10, 'sat': 5, 'sugar': 0, 'sodium': 0},
            'coke': {'cals': 100, 'protein': 0, 'carbs': 30, 'fat': 0, 'sat': 0, 'sugar': 30, 'sodium': 0},
            'fries': {'cals': 100, 'protein': 0, 'carbs': 20, 'fat': 10, 'sat': 5, 'sugar': 0, 'sodium': 200},}
    diet = DietProblem(menu=menu, nutr=nutr)

    # Two big macs, one coke, one fries
    # WARNING- there are 2 equivalent solutions here- eat both big macs from the Double Big Mac Fries meal, or one from each
    diet.solve(nutrition={'protein': (40, 60), 'sugar': (30, 40), 'sodium': (200, 300)})
    result = diet.history[-1]
    expected = {'cost': 13.0, 
                'purchase': [{'meal': 'Big Mac Coke', 'bought': 1, 
                              'foods': [{'food': 'big-mac', 'available': 1, 'eat': 1}, 
                                        {'food': 'coke', 'available': 1, 'eat': 1}]},
                             {'meal': 'Double Big Mac Fries', 'bought': 1, 
                              'foods': [{'food': 'big-mac', 'available': 2, 'eat': 1}, 
                                        {'food': 'fries', 'available': 1, 'eat': 1}]}]}
    assert result == expected
