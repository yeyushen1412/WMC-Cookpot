import json

ALL_INGREDIENTS = json.load( open( "ingredients.json" ) )
SELL_FACTOR = [1.5, 1.8, 2.1, 2.4, 2.8]
MODIFIERS_SHORT = ['A', 'D', 'C', 'L', 'M', 'Z', 'Q', 'S', 'G']
MODIFIERS = ['Attack up', 'Durability up', 'Critical hit', 'Long throw', 'Multishot', 'Zoom', 'Quickshot', 'Surf up', 'Guard up']

MODIFIERS_LOOKUP = {
    'a': 'Attack up',
    'd': 'Durability up',
    'c': 'Critical hit',
    'c': 'Long throw',
    'm': 'Multishot',
    'z': 'Zoom',
    'q': 'Quickshot',
    's': 'Surf up',
    'g': 'Guard up'
}

HP_BOOST_RECIPES = {
    'Fruitcake': {
        'Ingredients':[
            ['apple', 'wildberry'],
            ['wildberry', 'voltfruit', 'hydromelon', 'mightybananas', 'heartydurian', 'palmfruit', 'apple'],
            ['tabanthawheat'],
            ['canesugar']
        ],
        'HP_Boost': 4
    },
    'Seafood Paella': {
        'Ingredients':[
            ['mightyporgy', 'armoredporgy'], ['heartyblueshellsnail'], ['hylianrice'], ['goatbutter'], ['rocksalt']
        ],
        'HP_Boost': 8
    },
    'Wildberry Crepe': {
        'Ingredients':[
            ['tabanthawheat'], ['freshmilk'], ['birdegg'], ['canesugar'], ['wildberry']
        ],
        'HP_Boost': 16
    },
    'Honey Crepe': {
        'Ingredients':[
            ['tabanthawheat'], ['freshmilk'], ['birdegg'], ['canesugar'], ['courserbeehoney']
        ],
        'HP_Boost': 4
    }
}

HP_BOOST_RECIPES2 = {
    'Milk': {
       'Ingredients':[
            ['freshmilk']
        ],
        'HP_Boost': 2
    },
    'Honey Candy': {
       'Ingredients':[
            ['courserbeehoney']
        ],
        'HP_Boost': -8
    },
}

HP_BOOST_INGREDIENTS = ['tabanthawheat', 'freshmilk', 'birdegg', 'canesugar','courserbeehoney', 'wildberry', 'mightyporgy', 'apple',  'voltfruit', 'hydromelon', 'mightybananas', 'heartydurian', 'palmfruit']

MATERIAL_ONLY_RECIPES = [
    ['rocksalt', 'tabanthawheat'],
    ['goronspice', 'hylianrice', 'monsterextract'],
    ['goronspice', 'hylianrice', 'monsterextract', 'rocksalt'],
    ['canesugar', 'goatbutter', 'monsterextract', 'tabanthawheat'],
    ['canesugar', 'freshmilk', 'goatbutter', 'monsterextract', 'tabanthawheat'],
    ['goatbutter', 'goronspice', 'hylianrice'],
    ['goronspice', 'hylianrice']
]

UNIQUE_INGREDIENTS =  [
    ['roastedacorn', 'roastedtreenut'],
    ['keesewing'],
    ['acorn'],
    ['bakedapple'],
    ['toastysilentshroom'],
    ['restlesscricket', 'winterwingbutterfly', 'summerwingbutterfly', 'sunsetfirefly', 'electricdarner', 'colddarner', 'hightaillizard', 'warmdarner', 'hot-footedfrog', 'thunderwingbutterfly', 'smotherwingbutterfly'],
    ['fairy'],
    ['monsterextract'],
    ['rocksalt'],
    ['wood'],
    ['bokoblinhorn'],
    ['tabanthawheat'],
    ['goatbutter'],
    ['canesugar'],
    ['hylianrice'],
    ['warmsafflina', 'coolsafflina', 'electricsafflina'],
    ['hyruleherb'],
    ['chickalootreenut'],
    ['hylianshroom', 'spicypepper', 'rushroom', 'silentshroom'],
    ['freshmilk'],
    ['birdegg'],
    ['apple'],
    ['wildberry'],
    ['toastyhylianshroom'],
    ['charredpepper', 'toastyendurashroom', 'toastystamellashroom', 'toastyironshroom', 'roastedwildberry', 'toastyrushroom', 'toastyrazorshroom'],
    ['roastedswiftcarrot', 'toastychillshroom', 'toastyzapshroom', 'toastysunshroom'],
    ['bakedpalmfruit'],
    ['goronspice'],
    ['bluenightshade'],
    ['swiftcarrot', 'sunshroom', 'zapshroom', 'chillshroom'],
    ['hydromelon', 'voltfruit'],
    ['bladedrhinobeetle', 'ruggedrhinobeetle'],
    ['palmfruit'],
    ['chuchujelly', 'moblinhorn', 'octoballoon'],
    ['mightythistle', 'armoranth'],
    ['ironshroom', 'fortifiedpumpkin', 'stamellashroom', 'mightybananas', 'razorshroom', 'fleet-lotusseeds'],
    ['campfireegg', 'hard-boiledegg'],
    ['roastedmightythistle', 'roastedarmoranth'],
    ['roastedmightybananas', 'roastedvoltfruit', 'roastedlotusseeds', 'bakedfortifiedpumpkin', 'roastedhydromelon'],
    ['toastedheartytruffle'],
    ['sneakyriverescargot'],
    ['roastedtrout', 'roastedbass'],
    ['electrickeesewing', 'icekeesewing', 'firekeesewing'],
    ['hyrulebass', 'sneakyriversnail', 'sizzlefintrout', 'voltfintrout', 'endurashroom', 'chillfintrout'],
    ['heartytruffle'],
    ['fireprooflizard'],
    ['frozentrout', 'frozenriversnail'],
    ['roastedbirdthigh'],
    ['silentprincess'],
    ['blackenedcrab'],
    ['searedsteak', 'roastedbirddrumstick'],
    ['roastedheartybass'],
    ['roastedradish'],
    ['roastedheartydurian'],
    ['bokoblinfang'],
    ['rawmeat', 'razorclawcrab', 'ironshellcrab', 'rawbirddrumstick'],
    ['frozenbass', 'frozenheartybass', 'frozencrab'],
    ['icymeat', 'frozenbirddrumstick'],
    ['blueshellescargot'],
    ['roastedheartysalmon'],
    ['roastedcarp', 'roastedporgy'],
    ['redchuchujelly', 'whitechuchujelly', 'lizalfoshorn', 'octoroktentacle', 'yellowchuchujelly'],
    ['swiftviolet'],
    ['mightyporgy', 'armoredporgy', 'bright-eyedcrab', 'armoredcarp', 'stealthfintrout', 'mightycarp'],
    ['courserbeehoney'],
    ['heartysalmon'],
    ['frozencarp', 'frozenporgy'],
    ['icyheartyblueshellsnail'],
    ['frozenheartysalmon'],
    ['moblinfang'],
    ['ancientscrew'],
    ['toastedbigheartytruffle'],
    ['roastedbigradish'],
    ['searedprimesteak'],
    ['ancientspring', 'lizalfostalon'],
    ['heartydurian', 'heartyblueshellsnail', 'bigheartytruffle'],
    ['bigheartyradish'],
    ['rawbirdthigh', 'rawprimemeat'],
    ['frozenbirdthigh', 'icyprimemeat'],
    ['staminokabass'],
    ['heartybass'],
    ['bokoblinguts', 'keeseeyeball', 'hinoxtoenail'],
    ['sankecarp'],
    ['roastedenduracarrot'],
    ['heartylizard'],
    ['tirelessfrog'],
    ['octorokeyeball', 'moblinguts'],
    ['lizalfostail'],
    ['ancientgear', 'moldugafin'],
    ['enduracarrot'],
    ['redlizalfostail', 'yellowlizalfostail', 'icylizalfostail', 'hinoxtooth'],
    ['rawgourmetmeat', 'rawwholebird'],
    ['searedgourmetsteak', 'roastedwholebird'],
    ['energeticrhinobeetle'],
    ['icygourmetmeat', 'frozenwholebird'],
    ['ancientshaft', 'lynelhorn'],
    ['lynelhoof'],
    ['ancientcore', 'hinoxguts'],
    ['moldugaguts'],
    ['lynelguts', 'giantancientcore'],
    ["farosh'sscale"],
    ["naydra'sscale"],
    ["dinraal'sscale"],
    ["farosh'sclaw"],
    ["naydra'sclaw"],
    ["dinraal'sclaw"],
    ["shardoffarosh'sfang"],
    ["shardofnaydra'sfang"],
    ["shardofdinraal'sfang"],
    ["shardoffarosh'shorn"],
    ["shardofnaydra'shorn"],
    ["shardofdinraal'shorn"],
    ['starfragment'],
    ['flint', 'amber', 'opal', 'luminousstone', 'topaz', 'ruby', 'sapphire', 'diamond']
]

FAIRY_TONIC = [
    ['Fairy'],
    ['Fairy', 'Monster'],
    ['Fairy', 'Material'],
    ['Fairy', 'Insect'],
    ['Fairy', 'Gem'],
    ['Fairy', 'Material', 'Monster'],
    ['Fairy', 'Food', 'Monster'],
    ['Fairy', 'Insect', 'Monster'],
    ['Fairy', 'Gem', 'Monster'],
    ['Fairy', 'Insect', 'Material'],
    ['Fairy', 'Gem', 'Material'],
    ['Fairy', 'Food', 'Insect'],
    ['Fairy', 'Food', 'Gem'],
    ['Fairy', 'Gem', 'Insect'],
    ['Fairy', 'Food', 'Material', 'Monster'],
    ['Fairy', 'Insect', 'Material', 'Monster'],
    ['Fairy', 'Gem', 'Material', 'Monster'],
    ['Fairy', 'Food', 'Insect', 'Monster'],
    ['Fairy', 'Food', 'Gem', 'Monster'],
    ['Fairy', 'Gem', 'Insect', 'Monster'],
    ['Fairy', 'Food', 'Insect', 'Material'],
    ['Fairy', 'Food', 'Gem', 'Material'],
    ['Fairy', 'Gem', 'Insect', 'Material'],
    ['Fairy', 'Food', 'Gem', 'Insect'],
    ['Fairy', 'Food', 'Insect', 'Material', 'Monster'],
    ['Fairy', 'Food', 'Gem', 'Material', 'Monster'],
    ['Fairy', 'Gem', 'Insect', 'Material', 'Monster'],
    ['Fairy', 'Food', 'Gem', 'Insect', 'Monster'],
    ['Fairy', 'Food', 'Gem', 'Insect', 'Material'],
    ['Fairy', 'Food', 'Gem', 'Insect', 'Material', 'Monster']
]

SPECIAL_INGREDIENTS = ['courserbeehoney', 'acorn', 'chickalootreenut']
NUT_DUBIOUS_LOOKUP = [['acorn'], ['chickalootreenut'], ['courserbeehoney'], ['acorn', 'courserbeehoney'] , ['chickalootreenut', 'courserbeehoney']]
