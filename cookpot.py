import numpy as np
import difflib

import constants

all_ingredients = constants.ALL_INGREDIENTS

def cook(input_str):
    ingredients = input_str.replace('?', '').replace('cook', '')
    out_str = f"Ingredients input:{ingredients}\n"

    ingredients = get_ingredient_list(ingredients)
    matching_flag = need_matching(ingredients)
    ingredients = handle_dragon_part(ingredients)

    if matching_flag:
        ingredients, matched_out = fuzzy_matching(ingredients)
        matched_out = ', '.join(sorted(matched_out))
        out_str += f'Predicted ingredients: {matched_out}\n'

    out_str += recipe_out_str(ingredients)
    return out_str

def recipe_out_str(ingredients):
    price, hp_no_crit, hp_crit = recipe_attr(ingredients)

    out_str = f'''Sell price: {price}\n'''

    if hp_no_crit == hp_crit:
        out_str += f'''HP value: {hp_no_crit}\n'''
    else:
        out_str += f'''HP value: {hp_no_crit} (w/o HP crit), {hp_crit} (w/ HP crit)\n'''
    out_str += f'''Modifiers: {price_to_mods(price)}'''

    return out_str

def recipe_price_hp(input_str):
    ingredients = input_str.replace('cook', '')

    ingredients = get_ingredient_list(ingredients)
    matching_flag = need_matching(ingredients)
    ingredients = handle_dragon_part(ingredients)

    if matching_flag:
        ingredients, _ = fuzzy_matching(ingredients)

    price, hp_no_crit, hp_crit = recipe_attr(ingredients)

    return price, hp_no_crit, hp_crit

def get_ingredient_list(input_str):
    ingredients = input_str.lower().replace(' ', '').split(',')

    for idx, item in enumerate(ingredients):
        if item[-2:] in ['x1', 'x2', 'x3', 'x4', 'x5']:
            ingredients[idx] = item[:-2]

            iter = eval(item[-1])-1
            for _ in range(iter):
                ingredients.append(item[:-2])
        if item[0] == "'":
            item = item[1:]
        if item[-1] == "'":
            item = item[:-2]

    return ingredients

def handle_dragon_part(ingredients):
    def format_dragon_part(item, d_name):
        d_part = ''
        if 'claw' in item:
            d_part = f"{d_name}'sclaw"
        elif 'scale' in item:
            d_part = f"{d_name}'sscale"
        elif 'horn' in item:
            d_part = f"shardof{d_name}'shorn"
        elif 'fang' in item:
            d_part = f"shardof{d_name}'sfang"
        return d_part

    def update_ingredients(ingredients):
        for idx, ing in enumerate(ingredients):
            for d_name in ['naydra', 'farosh', 'dinraal']:
                if d_name in ing:
                    ingredients[idx] = format_dragon_part(ing, d_name)

            if ('electricdrag' in ing) or ('drag' in ing):
                ingredients[idx] = format_dragon_part(ing, 'farosh')
            if 'icedrag' in ing:
                ingredients[idx] = format_dragon_part(ing, 'naydra')
            if 'firedrag' in ing:
                ingredients[idx] = format_dragon_part(ing, 'dinraal')

    def append_ingredients(ingredients, count=1):
        the_part = 'horn'
        the_idx = 0
        for idx, item in enumerate(ingredients):
            for part in ['claw', 'horn', 'fang', 'scale']:
                if part in item:
                    the_part = part
                    the_idx = idx
        ingredients[the_idx] = format_dragon_part(the_part, 'farosh')
        if count >= 2:
            ingredients.append(format_dragon_part(the_part, 'naydra'))
        if count >= 3:
            ingredients.append(format_dragon_part(the_part, 'dinraal'))

        return ingredients

    if '2distinct' in str(ingredients):
        ingredients = append_ingredients(ingredients, count=2)
    if '3distinct' in str(ingredients):
        ingredients = append_ingredients(ingredients, count=3)
    else:
        update_ingredients(ingredients)

    return ingredients

def need_matching(ingredients):
    for ing in ingredients:
        if ing not in ingredient_attr_list('Name'):
            return True

def fuzzy_matching(ingredients):
    matched = []
    matched_out = []

    def find_match(original_name, ingredients):
        for idx, name in enumerate(original_name):
            matched = difflib.get_close_matches(name, ingredients)
            if len(matched) > 0:
                return idx

    original_name = ingredient_attr_list('Name')
    print_name = ingredient_attr_list('NameOut')

    for ing in ingredients:
        if ing in original_name:
            index = original_name.index(ing)
        else:
            contain_list = list(filter(lambda i: ing in i, original_name))
            if len(contain_list) > 0:
                index = original_name.index(contain_list[0])
            else:
                index =find_match(original_name, [ing])

        matched.append(original_name[index])
        matched_out.append(print_name[index])

    return matched, matched_out

def ingredient_attr(name, attr):
    return all_ingredients[name][attr]

def ingredient_attr_list(attr):
    return [all_ingredients[ing][attr] for ing in all_ingredients.keys()]

def ingredients_price(ingredients, mode):
    return [ingredient_attr(ing, mode) for ing in ingredients]

def recipe_cureType(ingredients):
    effects = [ingredient_attr(ing, 'EffectType') for ing in ingredients]
    effects = list(set(effects))

    if len(effects) == 1:
        return effects[0]
    elif len(effects) == 2:
        if 'None' in effects:
            effects.remove('None')
            return effects[0]
    else:
        return 'None'

def recipe_cureTempHP(ingredients):
    tempHP = 0
    for ing in ingredients:
        if ingredient_attr(ing, 'EffectType') == 'LifeMaxUp':
            tempHP += ingredient_attr(ing, 'HitPointRecover') + 4

    return tempHP

def recipe_cureHP(ingredients, crit=False, fact=2, ignoreRecipeHP=False):
    if 'monsterextract' not in ingredients:
        boost_rates = [ingredient_attr(ing, 'BoostSuccessRate') for ing in ingredients]
        if sum(boost_rates) >= 100:
            if recipe_cureType(ingredients) == 'None':
                crit = True
            if 'starfragment' in ingredients:
                crit = True

    if recipe_cureType(ingredients) == 'LifeMaxUp':
        cureHP = recipe_cureTempHP(ingredients)

        if crit:
            cureHP += 4
        return min([cureHP, 120])

    cureHP = sum([ingredient_attr(ing, 'HitPointRecover') * fact for ing in ingredients])
    if ('monsterextract' in ingredients) and (recipe_cureType(ingredients) == 'None') and not is_material_only_recipe(ingredients) and not crit:
        cureHP = 1
    if not ignoreRecipeHP:
        cureHP += sum([ingredient_attr(ing, 'BoostHitPointRecover') for ing in set(ingredients)])
    if not ignoreRecipeHP:
        cureHP += recipe_HPBoost(ingredients)

    if crit:
        cureHP += 12
    return min([cureHP, 120])

def recipe_HPBoost(ingredients):
    recipes_ingredients = constants.HP_BOOST_INGREDIENTS
    if len(set(recipes_ingredients).intersection(ingredients)) == 0:
        return 0

    recipes = constants.HP_BOOST_RECIPES

    for recipe_name in recipes.keys():
        recipe_ingredients = recipes.get(recipe_name)['Ingredients']
        if is_hpboost_recipe(ingredients, recipe_ingredients):
            return recipes.get(recipe_name)['HP_Boost']

    ingredients = list(set(remove_ingredient(ingredients, ['Dragon', 'Cooked'], attr='Type')))
    if ingredients == ['freshmilk']:
        return 2
    if ingredients == ['courserbeehoney']:
        return -8

    if 'goatbutter' in ingredients:
        ingredients = list(set(remove_ingredient(ingredients, ['Material'], attr='Type')))
        ingredients = sorted(list(set(remove_ingredient(ingredients, ['starfragment', 'acorn', 'courserbeehoney', 'chickalootreenut'], attr='Name'))))
        if ingredients == ['apple']:
            return 4
    return 0

def recipe_price(ingredients):
    sell = sum(ingredients_price(ingredients, 'SellingPrice'))
    buy = sum(ingredients_price(ingredients, 'BuyingPrice'))
    sell = sell * constants.SELL_FACTOR[len(ingredients)-1]
    sell = int((np.floor(sell / 10) + np.ceil(int(sell % 10)/10)) * 10)
    sell = min([buy, sell])
    return max([sell, 2])

def recipe_attr(ingredients):
    food_type = recipe_type(ingredients)
    if food_type == 'Rock-Hard':
        price = 2
        hp_no_crit, hp_crit = 1, 1
    elif food_type == 'Dubious Food':
        price = 2
        non_boost_ingredients = remove_ingredient(ingredients, ['Dragon', 'Star'], attr='Type')
        hp_no_crit = max([4, recipe_cureHP(non_boost_ingredients, False, fact=1, ignoreRecipeHP=True)])
        hp_crit = hp_no_crit

    elif food_type == 'Fairy Tonic':
        price = 2
        hp_no_crit = fairy_tonic_hp(ingredients)
        hp_crit = hp_no_crit + 12

        non_fairy_ingredients = list(filter(lambda i: i != 'fairy', ingredients))
        if len(non_fairy_ingredients) > 0:
            hp_crit = recipe_cureHP(non_fairy_ingredients, True, fact=2) + hp_no_crit
            hp_no_crit += recipe_cureHP(non_fairy_ingredients, False, fact=2)

    else:
        price = recipe_price(ingredients)
        hp_no_crit = recipe_cureHP(ingredients, False)
        hp_crit = recipe_cureHP(ingredients, True)

        if food_type == 'Nuts':
            hp_crit -= 2
            hp_no_crit -= 2

    hp_no_crit = min([120, hp_no_crit])
    hp_crit = min([120, hp_crit])

    return price, hp_no_crit, hp_crit

def recipe_type(ingredients):
    nuts_check_result = check_nuts_dubious(ingredients)
    if nuts_check_result in ['Food', 'Dubious Food']:
        return nuts_check_result

    ingredients = remove_ingredient(ingredients, ['Dragon', 'Star', 'Cooked'], attr='Type')
    if len(ingredients) == 0:
        return 'Dubious Food'

    ingredients = sorted(list(set(ingredients)))
    ingredient_types = list(set([ingredient_attr(ing, 'Type') for ing in ingredients]))

    if is_material_only_recipe(ingredients):
        return 'Food'

    if 'Fairy' in ingredient_types:
        if ('acorn' in ingredients) or ('chickalootreenut' in ingredients):
            ingredients_filtered = remove_ingredient(ingredients, ['acorn', 'chickalootreenut'], 'Name')
            ingredient_types = list(set([ingredient_attr(ing, 'Type') for ing in ingredients_filtered]))
        if is_fairy_tonic(ingredient_types):
            return 'Fairy Tonic'

    if 'Gem' in ingredient_types:
        return 'Rock-Hard'

    if ('Monster' in ingredient_types) and ('Insect' not in ingredient_types):
        return 'Dubious Food'
    if ('Monster' not in ingredient_types) and ('Insect' in ingredient_types):
        return 'Dubious Food'
    if (len(ingredient_types) == 1) and ('Material' in ingredient_types):
        return 'Dubious Food'

    if ingredients in [['acorn'], ['chickalootreenut']]:
        return 'Nuts'

    return 'Food'

def fairy_tonic_hp(ingredients):
    fairy_count = count_ingredients(ingredients, ['fairy'], 'Name')
    return min([40 * fairy_count - 12, 120])

def is_fairy_tonic(ingredient_types):
    if sorted(ingredient_types) in constants.FAIRY_TONIC:
        return True
    return False

def is_material_only_recipe(ingredients):
    if ingredients in constants.MATERIAL_ONLY_RECIPES:
        return True
    return False

def check_nuts_dubious(ingredients):
    ingredient_types = list(set([ingredient_attr(ing, 'Type') for ing in ingredients]))
    ingredients = remove_ingredient(ingredients, ['Dragon', 'Star', 'Cooked'], attr='Type')
    set_ingredients = sorted(list(set(ingredients)))
    if 'Dragon' in ingredient_types or 'Star' in ingredient_types or 'Cooked' in ingredient_types:
        if set_ingredients in constants.NUT_DUBIOUS_LOOKUP:
            return 'Dubious Food'
    if set_ingredients in constants.NUT_DUBIOUS_LOOKUP[-2:]:
        return 'Dubious Food'

    for special in constants.SPECIAL_INGREDIENTS:
        if special in set_ingredients:
            ingredients_filtered = remove_ingredient(set_ingredients, constants.SPECIAL_INGREDIENTS, 'Name')
            ingredient_types = list(set([ingredient_attr(ing, 'Type') for ing in ingredients_filtered]))
            if ingredient_types == ['Material']:
                if is_material_only_recipe(ingredients_filtered):
                    return 'Food'
                return 'Dubious Food'

def is_hpboost_recipe(ingredients, recipe_ingredients):
    ingredients = ingredients[:]
    recipe_min_len = len(recipe_ingredients)
    check = [False for _ in range(recipe_min_len)]

    if recipe_ingredients == constants.HP_BOOST_RECIPES['Fruitcake']['Ingredients']:
        if 'apple' in ingredients and 'wildberry' in ingredients:
            check[0] = True
            check[1] = True
        elif 'apple' in ingredients and 'wildberry' not in ingredients:
            check[0] = True
            ingredients.remove('apple')
        elif 'wildberry' in ingredients and 'apple' not in ingredients:
            check[0] = True
            ingredients.remove('wildberry')

    for ing in ingredients:
        for index in range(recipe_min_len):
            if (ing in recipe_ingredients[index]) and check[index]==False:
                check[index] = True
    return min(check)

def remove_ingredient(ingredients, to_remove, attr):
    ingredients = list(filter(lambda i: ingredient_attr(i, attr) not in to_remove, ingredients))
    return ingredients

def count_ingredients(ingredients, to_count, attr):
    without = remove_ingredient(ingredients, to_count, attr)
    return len(ingredients) - len(without)

def price_to_mods(price, mode='long'):
    mods_pool = constants.MODIFIERS
    if mode == 'short':
        mods_pool = constants.MODIFIERS_SHORT
    mods = []

    price_str = str(bin(price))
    for index, mod in enumerate(mods_pool):
        pos = index + 1
        if pos > len(price_str):
            break

        if price_str[-pos] == '1':
            mods.append(mod)

    return ', '.join(mods)

def need_crit(ingredients, value):
    _, hp_no_crit, _ = recipe_attr(ingredients)
    if hp_no_crit == value:
        return False
    return True
