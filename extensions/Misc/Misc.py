import datetime
import os
import sqlite3

import discord
import yaml
from discord.ext import commands

from Utilities.get_helper import get_channel, get_user


class Misc:

    def __init__(self, bot):
        self.bot = bot
        self.role_db = sqlite3.connect('Database/role.db')
        self.role_db_cursor = self.role_db.cursor()

        path = os.path.dirname(os.path.abspath(__file__))
        try:
            with open("{}/config.yaml".format(path)) as c:
                config = yaml.safe_load(c)
        except FileNotFoundError as e:
            print("Not loading Misc extension due to missing config.yaml - Please copy and adjust config.yaml.example")
            raise e

        self.toggleable_channels = config['toggleable_channels']
        self.log_channel = self.bot.command_log_channel

    @commands.command()
    async def ping(self, ctx):
        """Check ping of bot"""
        msgtime = ctx.message.created_at
        start = datetime.datetime.now()
        message = await ctx.send("Pong! Ping time: {} ms; heartbeat time (Calculating)".format((start - msgtime).microseconds / 1000))
        end = message.created_at
        await message.edit(content="Pong! Ping time: {} ms; heartbeat time: {} ms".format((start - msgtime).microseconds / 1000, (end - msgtime).microseconds / 1000))

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
                        if self.log_channel:
                            await self.log_channel.send("<@{}> has left {}".format(ctx.author.id, channel.mention))
                    else:
                        user_roles.append(toggle_role)
                        if self.log_channel:
                            await self.log_channel.send("<@{}> has joined {}".format(ctx.author.id, channel.mention))
                    await ctx.author.edit(roles=user_roles)
            else:
                all_channels = list(self.toggleable_channels.values())
                all_channels = {channel: role for dictionary in all_channels for channel, role in dictionary.items()}
                if toggle in all_channels.keys():
                    channel = discord.utils.get(ctx.guild.channels, name=toggle)
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
            await ctx.send("{} currently has {} members".format(ctx.guild.name, ctx.guild.member_count))

    @commands.has_permissions(manage_roles=True)
    @commands.command()
    async def customrole(self, ctx, member, rolename):
        """Connects a role to a member so they can use color(), as so: .customrole @member rolename"""
        member = get_user(ctx.message, member)
        if member:
            role = discord.utils.get(ctx.guild.roles, name=rolename)
            if role:
                self.role_db.cursor().execute("CREATE TABLE IF NOT EXISTS roles (userid TEXT PRIMARY KEY, roleid TEXT)")
                exists = self.role_db_cursor.execute("SELECT * FROM roles WHERE userid={}".format(member.id)).fetchone()
                if exists:
                    return await ctx.send("Member already has custom role")
                self.role_db.cursor().execute("INSERT INTO roles VALUES(?, ?)", (member.id, role.id))
                self.role_db.commit()
                await ctx.send("Added role {} to member {}".format(role.name, member.name))
            else:
                await ctx.send("Invalid roleid")
        else:
            await ctx.send("Invalid member")

    @commands.has_permissions(manage_roles=True)
    @commands.command()
    async def removecustomrole(self, ctx, member):
        """Removes custom roleid from member, if any exists"""
        member = get_user(ctx.message, member)
        if member:
            table = self.role_db_cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name = 'roles'").fetchone()

            if table:
                role = self.role_db_cursor.execute("SELECT roleid FROM roles WHERE userid={}".format(member.id))

                if role:
                    self.role_db_cursor.execute("DELETE from roles WHERE userid={}".format(member.id))
                    self.role_db.commit()
                else:
                    await ctx.send("Member has no custom roles")
            else:
                await ctx.send("No custom roles have been added yet")
        else:
            await ctx.send("Invalid member")

    @commands.command(aliases=["colour"])
    async def color(self, ctx, color):
        """Changes color of custom role, if able. Color is in hex, in format 0x..."""
        user = ctx.author.id
        table = self.role_db_cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name = 'roles'").fetchone()

        if table:
            roleid = self.role_db_cursor.execute("SELECT roleid FROM roles WHERE userid={}".format(user)).fetchone()
            if roleid:
				role = discord.utils.get(ctx.guild.roles, id=roleid)
				if role:
					try:
						color = discord.Colour(int(color, 16))
						await discord.Client.edit_role(ctx.message.server, role, colour=color)
					except ValueError:
						await ctx.send("Invalid role colour")
				else:
					await ctx.send("Role not found")
            else:
                await ctx.send("You dont have a custom role!")
        else:
            await ctx.send("No custom roles have been added yet")


def setup(bot):
    bot.add_cog(Misc(bot))
