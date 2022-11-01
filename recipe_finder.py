import re
import json
import warnings
from glom import glom, T, Merge, Iter, SKIP

import constants
warnings.simplefilter(action='ignore')
from itertools import combinations
from cookpot import recipe_out_str, ingredient_attr

known_recipe = json.load( open( "known_recipe.json" ) )
mods_list = constants.MODIFIERS_SHORT

def find(message):
    try:
        filter_values, filter_modifiers, hpe_mode = get_filters(message)
    except:
        return 'Invalid filters, command syntax `? find m:amzQ v:120` '

    spec = {'f1': (T.items(), Iter({T[0]: lambda t: t[1] if (t[1]['mods'] in filter_modifiers and (t[1]['crit'] in filter_values or t[1]['no_crit'] in filter_values)) else SKIP}), Merge())}
    f1 = glom(known_recipe, spec)
    
    if hpe_mode == 'only':
        spec = {'f1': (T.items(), Iter({T[0]: lambda t: t[1] if t[1]['hpe'] == 'False' else SKIP}), Merge())}
        f1 = glom(f1['f1'], spec)
    elif hpe_mode == 'exclude':
        spec = {'f1': (T.items(), Iter({T[0]: lambda t: t[1] if t[1]['hpe'] == 'True' else SKIP}), Merge())}
        f1 = glom(f1['f1'], spec)

    spec = {
        'fix': (T.items(), Iter({T[0]: lambda t: t[1] if t[1]['crit'] == t[1]['no_crit'] else SKIP}), Merge()),
        'no_crit': (T.items(), Iter({T[0]: lambda t: t[1] if t[1]['no_crit'] in filter_values else SKIP}), Merge()),
        'crit': (T.items(), Iter({T[0]: lambda t: t[1] if t[1]['crit'] in filter_values else SKIP}), Merge()),
        }

    f2 = glom(f1['f1'], spec)
    fix = f2['fix']
    no_crit = f2['no_crit']
    crit = f2['crit']

    if len(fix.keys()) > 0:
        r = fix.get(list(fix.keys())[0])
    elif len(no_crit.keys()) >0:
        r = no_crit.get(list(no_crit.keys())[0])
    elif len(crit.keys()) >0:
        r = crit.get(list(crit.keys())[0])
    else:
        return 'No Match'

    ingredients = eval(r['ings'])
    matched_out = [ingredient_attr(str(ing), 'NameOut') for ing in ingredients]
    matched_out = ', '.join(sorted(matched_out))
    out_str = f'Ingredients: {matched_out}\n'
    out_str += recipe_out_str(ingredients)
    print(out_str)
    return out_str

def check_hpe(hpe_mode, recipe):
    if hpe_mode=='exclude':
        if no_hpe(eval(recipe['ings'])):
            print('Found no crit recipe without HPE')
            return recipe
    elif hpe_mode=='only':
        if no_hpe(eval(recipe['ings'])) == False:
            print('Found no crit recipe with HPE')
            return recipe
    else:
        print('Found crit recipe')
        return recipe
    return None

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

    value_range, strict_modifier_mode, hpe_mode = False, False, None

    if 'M:' in message:
        message = message.replace('M:', 'm:')
        strict_modifier_mode = True
    
    if 'v:' in message:
        value_range = True
    
    message = message.replace('V:', 'v:')
    if 'v:' in message:
        x1, x2 = re.search('v:', message).span()
    if 'm:' in message:
        y1, y2 = re.search('m:', message).span()

    xv, yv, xm, ym = None, None, None, None
    if y1 > x1:
        xv, yv, xm = x2, y1, y2
    if x1 > y1:
        xv, xm, ym = x2, y2, x1
    
    if '+' in message[xv:yv]:
        filter_value=int(message[xv:yv].replace('+', ''))
    else:
        filter_value=int(message[xv:yv])
    filter_modifiers=message[xm:ym].replace(',', '')

    if 'h' in filter_modifiers:
        hpe_mode = 'only'
    if 'H' in filter_modifiers:
        hpe_mode = 'exclude'

    to_exclude = [char.upper() for char in filter_modifiers if char.isupper()]
    to_include= [char.upper() for char in filter_modifiers if char.islower()]

    other_mods = [m for m in mods_list if m not in to_exclude and m not in to_include]
    base = order_modifiers(''.join(to_include))
    feasible_mods = [base]

    if strict_modifier_mode == False:
        for num in range(1 ,len( other_mods)+1):
            for i in combinations(other_mods, num):
                feasible_mods.append(order_modifiers(base+''.join(list(i))))

    filter_values = [filter_value]
    if value_range == True:
        filter_values = [filter_value + o for o in range(121-filter_value)]

    return filter_values, feasible_mods, hpe_mode

def order_modifiers(mod_str):
    filter_modifiers_ordered = ''
    for m in mods_list:
        if str(m) in str(mod_str):
            filter_modifiers_ordered += f'{m},'
    filter_modifiers_ordered = filter_modifiers_ordered.rstrip(' ').rstrip(',')
    return filter_modifiers_ordered

