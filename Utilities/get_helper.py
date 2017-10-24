import discord
import re


def get_channel(channel_list, text):  # Adapted from appu's discord selfbot
    if text.isdigit():
        found_channel = discord.utils.get(channel_list, id=int(text))
    elif text.startswith("<#") and text.endswith(">"):
        found_channel = discord.utils.get(channel_list, id=int(text.replace("<", "").replace(">", "").replace("#", "")))
    elif text.startswith("#"):
        found_channel = discord.utils.get(channel_list, name=text.replace("#", ""))
    else:
        found_channel = discord.utils.get(channel_list, name=text)
    return found_channel


def get_user(message, user):
    try:
        uid = int(re.match(r"<@!?(\d+)>", user).groups()[0])
    except AttributeError:
        try:
            uid = int(user)
        except ValueError:
            return message.guild.get_member_named(user)
    return message.guild.get_member(uid)
