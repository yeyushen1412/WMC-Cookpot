import json
import time
import warnings
warnings.simplefilter(action='ignore')

from itertools import combinations_with_replacement

import constants
from cookpot import price_to_mods, recipe_attr, ingredient_attr


ingredient_list = [i[0] for i in constants.UNIQUE_INGREDIENTS]

def iterate_recipes(num_ing):
    start= time.time()

    known_recipe = json.load( open( "known_recipe.json" ) )
    for choice in combinations_with_replacement(ingredient_list, num_ing):
        known_recipe = check_known_recipe(choice, known_recipe)

    json.dump(known_recipe, open( "known_recipe.json", 'w' ) )

    end = time.time()
    print(end-start)

def check_known_recipe(choice, known_recipe):
    ingredients = list(choice)
    price, no_crit, crit = recipe_attr(ingredients)
    mods = price_to_mods(price, mode='short')
    ings = str(ingredients)
    unique_key = f'{mods}_{no_crit}_{crit}'

    if unique_key not in known_recipe.keys():
        known_recipe.update({unique_key: {
            'mods': mods,
            'ings': ings,
            'price': price,
            'no_crit': no_crit,
            'crit': crit}
        })
    elif is_easier(ingredients, eval(known_recipe[unique_key]['ings'])):
        known_recipe.update({unique_key: {
            'mods': mods,
            'ings': ings,
            'price': price,
            'no_crit': no_crit,
            'crit': crit}
        })

    return known_recipe

def is_easier(new, old):
    new_types = list(set([ingredient_attr(ing, 'Type') for ing in new]))
    old_types = list(set([ingredient_attr(ing, 'Type') for ing in old]))

    if ('Cooked' in old_types) and ('Cooked' not in new_types):
        return True
    elif ('Cooked' not in old_types) and ('Cooked' in new_types):
        return False
    elif len(list(set(new))) < len(list(set(old))):
        return True
    return False
