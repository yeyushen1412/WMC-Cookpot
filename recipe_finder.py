import re
import json
import warnings

import constants
warnings.simplefilter(action='ignore')
from itertools import combinations
from cookpot import recipe_out_str, ingredient_attr

known_recipe = json.load( open( "known_recipe.json" ) )
mods_list = constants.MODIFIERS_SHORT

def find(message):
    if ('m:' not in message) or ('v:' not in message):
        return 'Invalid filters, command syntax `? find m:amzQ v:120[+]` '
    try:
        filter_value, filter_modifiers, value_range = get_filters(message)
    except:
        return 'Invalid filters, command syntax `? find m:amzQ v:120[+]` '

    filter_values = [filter_value]
    if value_range == True:
        filter_values = [filter_value + o for o in range(120-filter_value)]

    for filter_modifier in filter_modifiers:
       for filter_value in filter_values:
            r = get_recipe(filter_value, filter_modifier)

            if r != 'No Match':
                ingredients = eval(r)
                matched_out = [ingredient_attr(str(ing), 'NameOut') for ing in ingredients]
                matched_out = ', '.join(sorted(matched_out))
                out_str = f'Ingredients: {matched_out}\n'
                out_str += recipe_out_str(ingredients)
                print(out_str)
                return out_str

    return 'No Match'


def get_recipe(filter_value, filter_modifiers):
    for i in known_recipe.keys():
        recipe = known_recipe.get(i)
        if recipe['mods'] == filter_modifiers:
            if (recipe['no_crit'] == int(filter_value)) and (recipe['crit'] == int(filter_value)):
                print('Found certain recipe')
                return recipe['ings']

    for i in known_recipe.keys():
        recipe = known_recipe.get(i)
        if recipe['mods'] == filter_modifiers:
            if (recipe['no_crit'] == int(filter_value)):
                print('Found no crit recipe')
                return recipe['ings']

    for i in known_recipe.keys():
        recipe = known_recipe.get(i)
        if recipe['mods'] == filter_modifiers:
            if (recipe['crit'] == int(filter_value)):
                print('Found crit recipe')
                return recipe['ings']

    return 'No Match'


def no_hpe(ingredients):
    types = list(set([ingredient_attr(ing, 'Type') for ing in ingredients]))

    if 'Cooked' not in types:
        return True
    return False

def modifer_name(m):
    return constants.MODIFIERS_LOOKUP.get(m, '')


def get_filters(message):
    message = message.replace(' ', '')
    x1, y1 = 0, 0
    x2, y2 = len(message), len(message)

    if 'v:' in message:
        x1, x2 = re.search('v:', message).span()
    if 'm:' in message:
        y1, y2 = re.search('m:', message).span()

    xv, yv, xm, ym = None, None, None, None
    if y1 > x1:
        xv, yv, xm = x2, y1, y2
    if x1 > y1:
        xv, xm, ym = x2, y2, x1
    value_range = False
    if '+' in message[xv:yv]:
        filter_value=int(message[xv:yv].replace('+', ''))
        value_range = True
    else:
        filter_value=int(message[xv:yv])
    filter_modifiers=message[xm:ym].replace(',', '')

    to_exclude = [char.upper() for char in filter_modifiers if char.isupper()]
    to_include= [char.upper() for char in filter_modifiers if char.islower()]

    other_mods = [m for m in mods_list if m not in to_exclude and m not in to_include]
    base = order_modifiers(''.join(to_include))
    feasible_mods = [base]

    for num in range(1 ,len( other_mods)+1):
        for i in combinations(other_mods, num):
            feasible_mods.append(order_modifiers(base+''.join(list(i))))
    return filter_value, feasible_mods, value_range

def order_modifiers(mod_str):
    filter_modifiers_ordered = ''
    for m in mods_list:
        if str(m) in str(mod_str):
            filter_modifiers_ordered += f'{m}, '
    filter_modifiers_ordered = filter_modifiers_ordered.rstrip(' ').rstrip(',')
    return filter_modifiers_ordered

