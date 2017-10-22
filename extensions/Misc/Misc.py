import datetime
import os

import discord
import yaml
from discord.ext import commands

from Utilities.get_helper import get_channel


class Misc:

    def __init__(self, bot):
        self.bot = bot

        path = os.path.dirname(os.path.abspath(__file__))
        with open("{}/config.yaml".format(path)) as c:
            config = yaml.safe_load(c)

        self.toggleable_channels = config['toggleable_channels']
        self.log_channel = self.bot.command_log_channel

    @commands.command()
    async def ping(self, ctx):
        """Check ping of bot"""
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
                        await self.log_channel.send("<@{}> has left {}".format(ctx.author.id, channel.mention))
                    else:
                        user_roles.append(toggle_role)
                        await self.log_channel.send("<@{}> has joined {}".format(ctx.author.id, channel.mention))
                    await ctx.author.edit(roles=user_roles)
            else:
                all_channels = list(self.toggleable_channels.values())
                all_channels = {channel: role for dictionary in all_channels for channel, role in dictionary.items()}
                if toggle in all_channels.keys():
                    channel = discord.utils.get(ctx.guild.channels, name=all_channels[toggle])
                    toggle_role = discord.utils.get(ctx.guild.roles, name=all_channels[toggle])
                    user_roles = ctx.author.roles
                    if toggle_role in user_roles:
                        user_roles.remove(toggle_role)
                        await self.log_channel.send("<@{}> has left {}".format(ctx.author.id, channel.mention))
                    else:
                        await self.log_channel.send("<@{}> has joined {}".format(ctx.author.id, channel.mention))
                        user_roles.append(toggle_role)
                    await ctx.author.edit(roles=user_roles)

    @commands.command(aliases=["mc", "members"])
    async def membercount(self, ctx, channel=""):
        """Returns member count in the specified channel, or the server if not specified"""
        if channel:
            channel = get_channel(ctx.guild.channels, channel)
            if not channel:
                await ctx.send("That channel doesn't exist!")
            elif not ctx.author.permissions_in(channel).read_messages:
                await ctx.send("You cannot view the member count in this channel")
            else:
                await ctx.send("There are {} members in {}".format(len(channel.members), channel.name))
        else:
            await ctx.send("SSSv4stro currently has {} members".format(ctx.guild.member_count))


def setup(bot):
    bot.add_cog(Misc(bot))
