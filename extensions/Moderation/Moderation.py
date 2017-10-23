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
        self.warn_db_cursor = self.warn_db.cursor()
        self.log_channel = self.bot.moderation_log_channel

    @commands.has_permissions(kick_members=True)
    @commands.command()
    async def kick(self, ctx, member, *, reason=""):
        """
        Kick the specified member
        Usage: [p]kick <mention, ID, or name> [reason]
        """
        try:
            member = get_user(ctx.message, member)
            if member:
                if ctx.author.top_role <= member.top_role:
                    return await ctx.send("You cannot kick {}!".format(member))
                try:
                    await member.send("You have been kicked from SSSv4stro! Reason: {}".format(reason if reason else "No reason provided"))
                except discord.errors.Forbidden:
                    print("DMing user failed.")
                await member.kick(reason=reason + "\nResponsible moderator: {}".format(ctx.author))
                await ctx.send("{} has been kicked".format(member))
                if self.log_channel:
                    embed = discord.Embed()
                    embed.color = discord.Color.orange()
                    embed.set_author(name=str(ctx.message.author) + " moderator action", icon_url=ctx.message.author.avatar_url)
                    embed.add_field(name="Action type", value="Kick", inline=False)
                    embed.add_field(name="Target", value=member.mention + " ({})".format(member), inline=False)
                    embed.add_field(name="Reason", value=reason if reason else "No reason provided", inline=False)
                    await self.log_channel.send(embed=embed)

            else:
                await ctx.send("Please enter a valid member!")
        except discord.errors.Forbidden:
            await ctx.send("That member cannot be kicked!")

    @commands.has_permissions(ban_members=True)
    @commands.command()
    async def ban(self, ctx, member, *, reason=""):
        """
        Ban the specified member
        Usage: [p]ban <mention, ID, or name> [reason]
        """
        try:
            member = get_user(ctx.message, member)
            if member:
                if ctx.author.top_role <= member.top_role:
                    return await ctx.send("You cannot ban {}!".format(member))
                try:
                    await member.send("You have been banned from SSSv4stro! Reason: {}".format(reason if reason else "No reason provided"))
                except discord.errors.Forbidden:
                    print("DMing user failed.")
                await member.ban(reason=reason + "\nResponsible moderator: {}".format(ctx.author), delete_message_days=0)
                await ctx.send("{} has been banned".format(member))
                if self.log_channel:
                    embed = discord.Embed()
                    embed.color = discord.Color.dark_red()
                    embed.set_author(name=str(ctx.message.author) + " moderator action", icon_url=ctx.message.author.avatar_url)
                    embed.add_field(name="Action type", value="Ban", inline=False)
                    embed.add_field(name="Target", value=member.mention + " ({})".format(member), inline=False)
                    embed.add_field(name="Reason", value=reason if reason else "No reason provided", inline=False)
                    await self.log_channel.send(embed=embed)

            else:
                await ctx.send("Please enter a valid member!")
        except discord.errors.Forbidden:
            await ctx.send("That member cannot be banned!")

    @commands.has_permissions(kick_members=True)
    @commands.command()
    async def warn(self, ctx, member, *, reason):
        """
        Warn the specific member.
        Usage: [p]warn <mention, ID, or name> <reason>
        """
        member = get_user(ctx.message, member)
        if member:
            if member.top_role >= ctx.message.author.top_role:
                return await ctx.send("You cannot warn this member!")
            self.warn_db_cursor.execute("CREATE TABLE IF NOT EXISTS _{} (datetime timestamp, invoker text, reason text, revoked integer, key integer PRIMARY KEY)"
                                        .format(str(member.id)))
            self.warn_db_cursor.execute("SELECT * FROM _{}".format(str(member.id)))
            warns = self.warn_db_cursor.fetchall()
            warncount = 0
            for _, _, _, revoked, _ in warns:
                warncount += revoked
            self.warn_db_cursor.execute("INSERT INTO _{} VALUES (?, ?, ?, 0, {})".format(str(member.id), len(warns) + 1),
                                        (datetime.datetime.now(), str(ctx.message.author.id), reason))
            self.warn_db.commit()
            await ctx.send("Warned member {}!".format(member))
            try:
                await member.send("You have been warned on SSSv4stro! Reason: {}".format(reason))
            except discord.errors.Forbidden:
                print("DMing user failed.")
            if self.log_channel:
                embed = discord.Embed()
                embed.color = discord.Color.gold()
                embed.set_author(name=str(ctx.message.author) + " moderator action", icon_url=ctx.message.author.avatar_url)
                embed.add_field(name="Action type", value="Warn", inline=False)
                embed.add_field(name="Target", value=member.mention + " ({})".format(member), inline=False)
                embed.add_field(name="Reason", value=reason, inline=False)
                await self.log_channel.send(embed=embed)
        else:
            await ctx.send("Please enter a valid member!")

    @commands.has_permissions(kick_members=True)
    @commands.command()
    async def listwarns(self, ctx, member):
        """
        List warns for a specified member
        Usage: [p]listwarns <mention, ID, or name>
        """
        member = get_user(ctx.message, member)
        if member:
            exists = self.warn_db_cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='_{}'"
                                                 .format(member.id)).fetchone()
            if exists:
                warns = self.warn_db_cursor.execute("SELECT * FROM _{}".format(str(member.id))).fetchall()
                embed = discord.Embed(title="Warns for {}".format(member))
                for timestamp, invoker, reason, revoked, key in warns:
                    invoker = ctx.guild.get_member(int(invoker))
                    if not revoked:
                        embed.add_field(name="{}: {}".format(key, timestamp), value="{}\nWarned by: {}"
                                        .format(reason, invoker), inline=False)
                    else:
                        embed.add_field(name="~~{}: {}~~".format(key, timestamp), value="~~{}\nWarned by: {}~~"
                                        .format(reason, invoker), inline=False)
                await ctx.send(embed=embed)
            else:
                await ctx.send("No warns found!")
        else:
            await ctx.send("Please enter a valid member!")

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def clearwarns(self, ctx, member):
        """
        Clear warns for a member permanently
        Usage: [p]clearwarns <member>
        """
        member = get_user(ctx.message, member)
        if member == ctx.message.author:
            await ctx.send("You can't clear your own warns!")
        elif member.top_role >= ctx.message.author.top_role:
            await ctx.send("You can't clear this member's warns!")
        elif member:
            self.warn_db_cursor.execute("DROP TABLE IF EXISTS _{}".format(member.id))
            await ctx.send("Warns for {} cleared!".format(member))
            if self.log_channel:
                embed = discord.Embed()
                embed.color = discord.Color.green()
                embed.set_author(name=str(ctx.message.author) + " moderator action", icon_url=ctx.message.author.avatar_url)
                embed.add_field(name="Action type", value="Clearwarns", inline=False)
                embed.add_field(name="Target", value=member.mention + " ({})".format(member), inline=False)
                await self.log_channel.send(embed=embed)

        else:
            await ctx.send("Please mention a valid member!")

    @commands.has_permissions(kick_members=True)
    @commands.command()
    async def delwarn(self, ctx, member, warn):
        """
        Revoke a specific warn for a member
        Usage: [p]delwarn <mention, ID, or name> <warn #>
        """
        member = get_user(ctx.message, member)
        if member:
            self.warn_db_cursor.execute("UPDATE _{} SET revoked = 1 WHERE key={}".format(member.id, warn))
            await ctx.send("Warn {} for {} cleared!".format(warn, member))
            if self.log_channel:
                embed = discord.Embed()
                embed.color = discord.Color.teal()
                embed.set_author(name=str(ctx.message.author) + " moderator action", icon_url=ctx.message.author.avatar_url)
                embed.add_field(name="Action type", value="Delete Warn", inline=False)
                embed.add_field(name="Target", value=member.mention + " ({})".format(member), inline=False)
                embed.add_field(name="Warn revoked", value=warn, inline=False)
                await self.log_channel.send(embed=embed)

        else:
            await ctx.send("Please enter a valid member!")

    @commands.has_permissions(manage_messages=True)
    @commands.command()
    async def lockdown(self, ctx):
        """
        Lock down a channel
        Usage: [p]lockdown
        """
        channel = ctx.channel
        await channel.set_permissions(ctx.guild.default_role, send_messages=False)
        await channel.send("Channel has been locked down to non-administrators.")
        if self.log_channel:
            embed = discord.Embed()
            embed.color = discord.Color.dark_orange()
            embed.set_author(name=str(ctx.message.author) + " moderator action", icon_url=ctx.message.author.avatar_url)
            embed.add_field(name="Action type", value="Lockdown", inline=False)
            embed.add_field(name="Target", value=channel.mention + " ({})".format(channel), inline=False)
            await self.log_channel.send(embed=embed)


    @commands.has_permissions(manage_messages=True)
    @commands.command()
    async def unlock(self, ctx):
        """
        Unlock a locked channel
        Usage: [p]unlock
        """
        channel = ctx.channel
        await channel.set_permissions(ctx.guild.default_role, send_messages=None)
        await channel.send("Channel has been unlocked.")
        if self.log_channel:
            embed = discord.Embed()
            embed.color = discord.Color.blue()
            embed.set_author(name=str(ctx.message.author) + " moderator action", icon_url=ctx.message.author.avatar_url)
            embed.add_field(name="Action type", value="Unlockdown", inline=False)
            embed.add_field(name="Target", value=channel.mention + " ({})".format(channel), inline=False)
            await self.log_channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Moderation(bot))
