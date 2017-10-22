#!/usr/bin/env/python3

import datetime
import sqlite3

import discord
from discord.ext import commands

from Utilities.get_helper import get_user


class Moderation:

    def __init__(self, bot):
        self.bot = bot
        self.warn_db = sqlite3.connect('Databases/warn.db')
        self.warn_db_cursor = self. warn_db.cursor()

    @commands.has_permissions(kick_members=True)
    @commands.command()
    async def kick(self, ctx, member, *, reason=""):
        """Kick the specified member"""
        try:
            member = ctx.message.mentions[0]
            if ctx.message.author.top_role <= member.top_role:
                await ctx.send("You cannot kick {}".format(member))
                return
            try:
                await member.send("You have been kicked from SSSv4stro! Reason: {}".format(reason if reason else "No reason provided"))
            except discord.errors.Forbidden:
                print("DMing user failed")
            await member.kick(reason=reason + "\nResponsible moderator: {}".format(ctx.author))
            await ctx.send("{} has been kicked".format(member))
        except IndexError:
            await ctx.send("Please mention a member")
        except discord.errors.Forbidden:
            await ctx.send("That member cannot be kicked")

    @commands.has_permissions(ban_members=True)
    @commands.command()
    async def ban(self, ctx, member, *, reason=""):
        """Ban the specified member"""
        try:
            member = ctx.message.mentions[0]
            if ctx.message.author.top_role <= member.top_role:
                await ctx.send("You cannot ban {}".format(member))
                return
            try:
                await member.send("You have been banned from SSSv4stro! Reason: {}".format(reason if reason else "No reason provided"))
            except discord.errors.Forbidden:
                print("DMing user failed.")
            await member.ban(reason=reason + "\nResponsible moderator: {}".format(ctx.author), delete_message_days=0)
            await ctx.send("{} has been banned".format(member))
        except IndexError:
            await ctx.send("Please mention a member")
        except discord.errors.Forbidden:
            await ctx.send("That member cannot be banned")

    @commands.has_permissions(kick_members=True)
    @commands.command()
    async def warn(self, ctx, member, *, reason):
        member = get_user(ctx.message, member)
        if member:
            if member.top_role >= ctx.message.author.top_role:
                return await ctx.send("You cannot warn this member!")
            self.warn_db_cursor.execute("CREATE TABLE IF NOT EXISTS _{} (datetime timestamp, invoker text, reason text, revoked integer, key integer PRIMARY KEY)"
                                        .format(str(member.id)))
            self.warn_db_cursor.execute("SELECT * FROM _{}".format(str(member.id)))
            warns = self.warn_db_cursor.fetchall()
            warncount = len(warns)
            self.warn_db_cursor.execute("INSERT INTO _{} VALUES (?, ?, ?, 0, {})".format(str(member.id), warncount + 1), (datetime.datetime.now(), str(ctx.message.author.id), reason))
            self.warn_db.commit()
            await ctx.send("Warned member {}!".format(member))
        else:
            await ctx.send("Please enter a valid member!")

    @commands.has_permissions(kick_members=True)
    @commands.command()
    async def listwarns(self, ctx, member):
        member = get_user(ctx.message, member)
        if member:
            exists = self.warn_db_cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='_{}'".format(member.id)).fetchone()
            if exists:
                warns = self.warn_db_cursor.execute("SELECT * FROM _{}".format(str(member.id))).fetchall()
                embed = discord.Embed(title="Warns for {}".format(member))
                for timestamp, invoker, reason, revoked, key in warns:
                    invoker = ctx.guild.get_member(int(invoker))
                    if not revoked:
                        embed.add_field(name="{}: {}".format(key, timestamp), value="{}\nWarned by: {}".format(reason, invoker), inline=False)
                    else:
                        embed.add_field(name="~~{}: {}~~".format(key, timestamp), value="~~{}\nWarned by: {}~~".format(reason, invoker), inline=False)
                await ctx.send(embed=embed)
            else:
                await ctx.send("No warns found!")
        else:
            await ctx.send("Please mention a valid member!")

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def clearwarns(self, ctx, member):
        member = get_user(ctx.message, member)
        if member:
            self.warn_db_cursor.execute("DROP TABLE IF EXISTS _{}".format(member.id))
            await ctx.send("Warns for {} cleared!".format(member))
        else:
            await ctx.send("Please mention a valid member!")

    @commands.has_permissions(kick_members=True)
    @commands.command()
    async def delwarn(self, ctx, member, warn):
        member = get_user(ctx.message, member)
        if member:
            self.warn_db_cursor.execute("UPDATE _{} SET revoked = 1 WHERE key={}".format(member.id, warn))
            await ctx.send("Warn {} for {} cleared!".format(warn, member))
        else:
            await ctx.send("Please mention a valid member!")


def setup(bot):
    bot.add_cog(Moderation(bot))
