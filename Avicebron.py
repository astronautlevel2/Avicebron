#!/usr/bin/env python3

import yaml
import os
import sys

import discord
from discord.ext import commands

try:
    with open("config.yaml") as c:
        config = yaml.safe_load(c)
except FileNotFoundError:
    print("Config file not found - please copy config.yaml.example to config.yaml")
    sys.exit()

bot = commands.Bot(command_prefix=config['prefix'],
                   description=config['description'],
                   max_messages=config['max_messages'])


@bot.event
async def on_ready():
    bot.command_log_channel = discord.utils.get(bot.guilds[0].channels, name=config["command_log_channel"])
    print("Bot ready, loading extensions")
    # Extension loading code adapted from appu1232/discord-selfbot
    for entry in os.listdir("extensions"):
        if os.path.isdir("extensions/{}".format(entry)):
            for extension in os.listdir("extensions/{}".format(entry)):
                if extension.endswith('.py'):
                    try:
                        bot.load_extension("extensions.{}.{}".format(entry, extension[:-3]))
                    except Exception as e:
                        print('Failed to load extension {}/{}\n{}: {}'.format(entry, extension, type(e).__name__, e))
        elif os.path.isfile("extensions/{}".format(entry)) and entry.endswith('.py'):
            try:
                bot.load_extension("extensions.{}".format(entry[:-3]))
            except Exception as e:
                print('Failed to load extension {}\n{}: {}'.format(entry, type(e).__name__, e))

    print("Bot ready!")

    # Check if a channel name is passed via argv to output restart message on
    if len(sys.argv) > 1:
        try:
            channel = bot.get_channel(int(sys.argv[1]))
            await channel.send("Bot has restarted")
        except:
            pass


@commands.has_permissions(administrator=True)
@bot.command(hidden=True)
async def restart(ctx):
    """Restart the bot"""
    await ctx.send("Restarting bot")
    os.execv(__file__, [__file__, str(ctx.channel.id)])

bot.run(config['token'])
