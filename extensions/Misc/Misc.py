import discord
from discord.ext import commands
import os
import datetime
import yaml

class Misc:

    def __init__(self, bot):
        self.bot = bot

        path = os.path.dirname(os.path.abspath(__file__))
        with open("{}/config.yaml".format(path)) as c:
            config = yaml.safe_load(c)

        self.toggleable_channels = config['toggleable_channels']

    @commands.command()
    async def ping(self, ctx):
        """Chick ping of bot"""
        start = datetime.datetime.now()
        message = await ctx.send("Pong! Response time: (Calculating)")
        end = message.created_at.now()
        await message.edit(content="Pong! Response time: {} ms".format((end - start).microseconds / 1000))

    @commands.command()
    async def togglechannel(self, ctx, toggle=""):
        """Add or remove yourself from a channel. Exclude channel argument to list all channels"""
        if toggle == "":
            embed_description = ""
            for group, channels in self.toggleable_channels.items():
                embed_description += "**{}\n**".format(group)
                for channel in channels:
                    embed_description += "• {}\n".format(channel)
            embed = discord.Embed(title="Toggleable Channels", description=embed_description)
            await ctx.send(embed=embed)
        elif toggle == "Ungrouped":
            return await ctx.send("You can't toggle Ungrouped!")
        else:
            if toggle in self.toggleable_channels.keys():
                for channel, role in self.toggleable_channels[toggle].items():
                    channel = discord.utils.get(ctx.guild.channels, name=channel)
                    toggle_role = discord.utils.get(ctx.guild.roles, name=role)
                    user_roles = ctx.author.roles
                    if toggle_role in user_roles:
                        user_roles.remove(toggle_role)
                        await channel.send("<@{}> has left the channel".format(ctx.author.id))
                    else:
                        user_roles.append(toggle_role)
                        await channel.send("<@{}> has joined the channel".format(ctx.author.id))
                    await ctx.author.edit(roles=user_roles)
            else:
                all_channels = list(self.toggleable_channels.values())
                all_channels = { channel: role for dict in all_channels for channel, role in dict.items() }
                if toggle in all_channels.keys():
                    channel = discord.utils.get(ctx.guild.channels, name=toggle)
                    toggle_role = discord.utils.get(ctx.guild.roles, name=all_channels[toggle])
                    user_roles = ctx.author.roles
                    if toggle_role in user_roles:
                        user_roles.remove(toggle_role)
                        await channel.send("<@{}> has left the channel".format(ctx.author.id))
                    else:
                        await channel.send("<@{}> has joined the channel".format(ctx.author.id))
                        user_roles.append(toggle_role)
                    await ctx.author.edit(roles=user_roles)


def setup(bot):
    bot.add_cog(Misc(bot))
