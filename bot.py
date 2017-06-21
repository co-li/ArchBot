# Import what's needed by the bot
import discord
from discord.ext import commands
import asyncio
import json
import datetime
import logging

import archcommands

# Set up logging
logging.basicConfig(level=logging.INFO)

# Set bot description
description = '''ArchBot is a Discord bot written in Python for searching the ArchWiki, Arch Linux package repositories, and AUR'''

# Open configuration file
with open('./config.json', 'r') as configjson:
    config = json.load(configjson)

# Set prefix
prefix = config["prefix_settings"]["prefix"]
if config["prefix_settings"]["use_space"] == True:
    prefix = prefix + ' '

# Create bot
bot = commands.Bot(command_prefix=prefix, description=description)

# Create a variable for the time the bot is launched
gametimestarted = datetime.datetime.now()

@bot.event
async def on_ready():
        print('Logged in as ')
        print(bot.user.name)
        print(bot.user.id)
        print('Bot prefix is set to ' + prefix + '\n')
        await bot.change_presence(game=discord.Game(name='with systemd'))

@bot.command()
async def uptime():
        """Check bot uptime."""
        global gametimestarted
        await bot.say(timedelta_str(datetime.datetime.now() - gametimestarted))

@bot.command()
async def source():
        """Get the bot's source code"""
        await bot.say("https://github.com/kingofinfo/ArchBot")

def timedelta_str(dt):
        days = dt.days
        hours, r = divmod(dt.seconds, 3600)
        minutes, sec = divmod(r, 60)

        if minutes == 1 and sec == 1:
            return '{0} days, {1} hours, {2} minute and {3} second.'.format(days,hours,minutes,sec)
        elif minutes > 1 and sec == 1:
            return '{0} days, {1} hours, {2} minutes and {3} second.'.format(days,hours,minutes,sec)
        elif minutes == 1 and sec > 1:
            return '{0} days, {1} hours, {2} minute and {3} seconds.'.format(days,hours,minutes,sec)
        else:
            return '{0} days, {1} hours, {2} minutes and {3} seconds.'.format(days,hours,minutes,sec)

bot.add_cog(archcommands.General(bot,config))

bot.run(config['token'])
