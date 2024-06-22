from cookpot import recipe_price_hp


def test_good():
    recipes = {
        'fairy, palm fruit, dragonhornx3': (29, 75, 75),
        'fairy, palm fruit, dragon fangx3': (29, 70, 70),
        'fairy, palm fruit, 3 distinct dragonhorn': (29, 105, 105),
        'Endura Carrot, Roasted Endura Carrot, 2x Roasted Bird Thigh, Roasted Whole Bird': (411, 112, 120),
        'Hearty Durian, Courser Bee Honey, Roasted Endura Carrot 3': (385, 112, 120),
        'Courser Bee Honey, Dragon Horn, Hearty 2 Salmon, Roasted Bird Thigh': (149, 120, 120),
        'Hearty Truffle, Dragon Horn, Hearty Salmon, Fairy, Frozen Bird Thigh': (135, 120, 120),
        'Hyrule Herb, 1x Fairy x2, Dragon Fang, Roasted Bird Thigh': (61, 120, 120),
        'Big Hearty Radish x2, Courser Bee Honey, Dragon Horn, Roasted Bird Thigh': (189, 120, 120),
        'Big Hearty Radish, Courser Bee Honey, Dragon Horn, Hearty Salmon, Roasted Bird Thigh': (169, 120, 120),
        'Hearty Truffle, Silent Princess, 3 distinct Dragon Horn': (57, 81, 81),
        'Spicy Pepper, Hearty Truffle, 3 distinct Dragon Horn': (39, 77, 77),
        'Silent Princess, 3 distinct Dragon Horn, Fairy': (43, 93, 105),
        'Hyrule Herb, 3 distinct Dragon Horn': (15, 65, 65),
        'Hightail Lizard, Molduga Fin, Hinox Tooth, Hinox Guts x2': (640, 0, 12),
        'Raw Gourmet Meat x4, Fairy': (400, 120, 120),
        'Energetic Rhino Beetle, Chuchu Jellyx4': (140, 0, 12)
    }
    for recipe in recipes.keys():
        assert recipe_price_hp(recipe) == recipes.get(recipe)



def test_ultimate():
    recipes = {
        'roasted endura carrotx3, endura carrot, frozen hearty salmon': (445, 120, 120),
        'roasted endura carrotx3, icy prime meat, hearty blueshell snail' : (405, 108, 120),
        'roasted endura carrotx3, icy prime meat, hearty durian': (405, 108, 120)
    }
    for recipe in recipes.keys():
        assert recipe_price_hp(recipe) == recipes.get(recipe)

def test_fairy():
    recipes = {
        'fairy': (2, 28, 40),
        'fairyx2': (2, 68, 80),
        'fairyx3': (2, 108, 120),
        'fairyx4': (2, 120, 120),
        'fairyx5': (2, 120, 120),
        'fairyx6': (2, 120, 120), # test: more than 5 ingredients
        'fairyx10': (2, 120, 120), # test: more than 5 ingredients
        'fairyx0': (2, 28, 40) # test: x0 = 0 ignored, 1 used
    }
    for recipe in recipes.keys():
        assert recipe_price_hp(recipe) == recipes.get(recipe)



def test_nuts():
    recipes = {
        'acorn': (8, 2, 14),
        'acornx2': (10, 4, 16),
        'acornx3': (20, 6, 18),
        'acornx4': (20, 8, 20),
        'acornx5': (30, 10, 22),
        'chickalootreenut': (10, 2, 14),
        'chickalootreenutx2': (10, 4, 16),
        'chickalootreenutx3': (20, 6, 18),
        'chickalootreenutx4': (30, 8, 20),
        'chickalootreenutx5': (50, 10, 22),
        'chickalootreenut, acorn': (10, 8, 20),
        'chickalootreenutx2, acornx2': (30, 12, 24),
        'acorn, hyrulebass': (20, 12, 24),
        'acornx2, hyrulebass': (30, 14, 26),
        'acorn, chickalootreenut, hyrulebass': (30, 16, 28),
        'acorn, roasted endura carrot': (2, 13, 13) # todo test in game
    }
    for recipe in recipes.keys():
        assert recipe_price_hp(recipe) == recipes.get(recipe)

def test_fairy_nuts():
    recipes = {
        'fairy, acorn': (2, 32, 44),
        'fairy, acornx2': (2, 34, 46),
        'fairy, acornx3': (2, 36, 48),
        'fairy, acornx4': (2, 38, 50),
        'fairy, acornx5': (2, 38, 50), # test: more than 5 ingredients
        'fairyx2, acorn': (2, 72, 84)
    }
    for recipe in recipes.keys():
        assert recipe_price_hp(recipe) == recipes.get(recipe)


def test_dubious():
    recipes = {
        'roasted endura carrot': (2, 12, 12),
        'roasted big radish': (2, 24, 24),
        'roasted big radish, roasted endura carrot': (2, 36, 36),
        'lynel guts': (2, 4, 4),
        'ancient core': (2, 4, 4),
        'lynel guts, applex3': (2, 6, 6),
        'hightaillizard': (2, 4, 4),
        'hightaillizard, starx2': (2, 4, 4),
        'starx2': (2, 4, 4),
        'dragon horn': (2, 4, 4),
        'salt': (2, 4, 4),
        'tabanthawheatx5': (2, 20, 20),
        'salt, starx2': (2, 4, 4),
        'salt, dragon horn': (2, 4, 4),
        'courserbeehoney, dragonhorn': (2, 8, 8),
    }
    for recipe in recipes.keys():
        assert recipe_price_hp(recipe) == recipes.get(recipe)

    recipes = {
        'courserbeehoney, salt': (2, 8, 8),
        'courserbeehoney, acorn': (2, 9, 9)
    }
    for recipe in recipes.keys():
        assert recipe_price_hp(recipe) == recipes.get(recipe)


def test_material_only():
    recipes = {
        'rocksalt, tabanthawheat': (10, 8, 20),
        'rocksalt, tabanthawheat, star': (20, 20, 20),
        'rocksaltx2, tabanthawheat': (20, 8, 20),
        'rocksalt, tabanthawheatx2': (20, 16, 28),
        'canesugar, freshmilk, goatbutter, monsterextract, tabanthawheat': (50, 12, 24)
    }

    for recipe in recipes.keys():
        assert recipe_price_hp(recipe) == recipes.get(recipe)

def test_hp_boost():
    recipes = {
        'apple, voltfruit, tabanthawheat, canesugar': (40, 20, 32),
        'apple, voltfruit, tabanthawheat, canesugar, star': (40, 32, 32),
        'applex2, voltfruit, tabanthawheat, canesugar': (50, 24, 36),
        'apple, wildberry, tabanthawheat, canesugar': (30, 20, 32),
        'tabanthawheat, freshmilk, birdegg, canesugar, wildberry': (50, 40, 52),
        'apple, goatbutter, acorn': (20, 12, 24),
        'apple, goatbutter': (10, 8, 20),
        'apple, goatbutter, star': (20, 20, 20),
        'courserbeehoney': (20, 8, 20),
        'courserbeehoney, star': (2, 8, 8),
        'freshmilk': (10, 6, 18),
        'freshmilk, dragon horn': (10, 33, 33),
        'freshmilk, star': (10, 16, 16),
    }

    for recipe in recipes.keys():
        assert recipe_price_hp(recipe) == recipes.get(recipe)

    recipes = {
        'apple, tabanthawheat, canesugar': (20, 12, 24),
        'tabanthawheat, freshmilk, birdegg, canesugar': (30, 20, 32)
    } # no recipe hp boost

    for recipe in recipes.keys():
        assert recipe_price_hp(recipe) == recipes.get(recipe)


def test_rockhard():
    recipes = {
        'wood': (2, 1, 1),
        'wood, acron': (2, 1, 1),
        'wood, hylian shroom': (2, 1, 1)
    }
    for recipe in recipes.keys():
        assert recipe_price_hp(recipe) == recipes.get(recipe)

    recipe = {
        'wood, fairy': (2, 28, 40)
    }
    for recipe in recipes.keys():
        assert recipe_price_hp(recipe) == recipes.get(recipe)

def test_yellow_heart():
    recipes = {
        'hearty durian': (30, 16, 20),
        'hearty durianx2': (60, 32, 36)
    }
    for recipe in recipes.keys():
        assert recipe_price_hp(recipe) == recipes.get(recipe)


def test_star():
    recipes = {
        'hylian shroom, star': (10, 16, 16),
        'hylian shroom, starx2': (10, 16, 16)
    }

    for recipe in recipes.keys():
        assert recipe_price_hp(recipe) == recipes.get(recipe)

def test_monster_extract():
    recipes = {
        'monster extract, apple': (10, 1, 16),
        'monster extract, dragon horn, apple': (20, 16, 31)
    }

    for recipe in recipes.keys():
        assert recipe_price_hp(recipe) == recipes.get(recipe)
