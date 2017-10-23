import discord


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
        member = message.mentions[0]
    except IndexError:
        member = message.guild.get_member_named(user)
    if not member:
        try:
            member = message.guild.get_member(int(user))
        except ValueError:
            pass
    if not member:
        return None
    return member
