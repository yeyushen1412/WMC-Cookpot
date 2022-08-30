import os
from discord.ext import commands

from cookpot import cook
from recipe_finder import find

TOKEN = os.getenv('DISCORD_TOKEN')
client = commands.Bot(command_prefix='?')

def help_message():
    return '''Cook command:
? cook ingredient1, [ingredient2, ingredient3, ingredient4, ingredient5] ....
Use , to separate ingredients

Some shortcut examples:
Dragon parts:
- ? cook farosh horn
- ? cook 3 distinct dragon horn
- ? cook ice dragon fang

Use multiple same ingredients:
- ? cook apple x3, fairy x2
- ? cook dragon hornx3, palm fruit, fairy

Fuzzy matching:
- farry, faiiy => fairy
- rice, wheat, salt, star and more

Find command:
? find m: [mod1, mod2, mod3...] v: cure_value

Examples:
? find m: amzQ v: 120
=> to find a recipe with a [attack up], m[motishot] and without Q[quickshot] and cure HP value of 120
m: initial letters of the modifiers, lower case => include, upper case => exclude

Modifier lookup:
a: Attack up\t\td: Durability up\tc: Critical hit\t\tl: Long throw\t\tm: Multishot
z: Zoom\t\t\t\tq: Quickshot\t\ts: Surf up\t\tg: Guard up

Contribute:
https://github.com/yeyushen1412/WMC-Cookpot.git
'''


@client.event
async def on_ready():
    print(f'client ready')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.author.bot:
        return
    if '?' not in message.content:
        return
    if 'help' in message.content:
        response = help_message()
    elif 'find' in message.content:
        response = find(message.content)
    else:
        response = cook(message.content)
    await message.channel.send(response)

client.run(TOKEN)
