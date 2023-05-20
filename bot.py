import discord
import os
from discord.ext import commands, tasks

from cookpot import cook
from recipe_finder import find


from keep_alive import keep_alive

keep_alive()

TOKEN = os.getenv('DISCORD_TOKEN')
client = commands.Bot(command_prefix='?')

from itertools import cycle

status = cycle(['Learning react', 'Coding python'])


@client.event
async def on_ready():
    change_status.start()
    print(f'client ready')


@tasks.loop(seconds=600)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))


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
m: initial letters of the modifiers, lower case => include, upper case => exclude

Examples:
? find m: amQ v: 10
=> to find a recipe with a [attack up], m[multishot] and without Q[quickshot] and cure HP value >= 10

Advanced mode:
Use "M:a" instead of "m:a" to strictly search for recipes with modifier of "a (attack up)"
Use "V:10" instead of "v:10" to strictly search for recipes with cure HP value of "10"
Add "H" in modifier filter, e.g. "? find m:Ha v:105" to search for non-HPE recipes
Add "h" in modifier filter, e.g. "? find m:ha v:105" to search for only HPE-recipes

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
    if '? help' in message.content or '?help' in message.content:
        response = help_message()
    elif '? find' in message.content or '?find' in message.content:
        response = find(message.content)
    elif '? cook' in message.content or '?cook' in message.content:
        response = cook(message.content)
    await message.channel.send(response)

client.run(TOKEN)
