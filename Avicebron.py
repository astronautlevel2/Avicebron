#!/usr/bin/env python3

import yaml
import asyncio
import os

import discord
from discord.ext import commands

try:
    with open("config.yaml") as c:
        config = yaml.safe_load(c)
except FileNotFoundError:
    print("Config file not found - please copy config.yaml.example to config.yaml")

bot = commands.Bot(command_prefix=config['prefix'], description=config['description'], max_messages=config['max_messages'])

@bot.event
async def on_ready():
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

bot.run(config['token'])