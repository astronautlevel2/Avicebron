#!/usr/bin/env/python3

from discord.ext import commands


class Memes:

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def t3ch(self, ctx, *, arg="server, sss, weeb, shack mod, trap role, channel, shitposting, cancerous"):
        """
        Prints the T3CHNOLOGIC copypasta.
        With no or missing arguments, defaults to the original pasta (or a modified original).
        Usage: [p]t3ch [server], [sss], [weeb], [shack mod], [trap role], [channel], [shitposting], [cancerous]
        The spaces are important!
        """
        original = ["server", "sss", "weeb", "shack mod", "trap role", "channel", "shitposting", "cancerous"]
        replacements = arg.split(', ')
        del replacements[8:]
        if len(replacements) < 8:
            replacements = replacements + original[len(replacements):]

        await ctx.send(await commands.clean_content().convert(ctx, """
y'know, i was trying to keep my cool and be a part of this {0}, but i cant force myself here any longer. \
this isnt {1}. too much {2} shit, owned by a {3} and a former {3}, no {4}, \
a {5} where people get warned for {6} when part of the spirit of {1} is {6}, \
and overall just more {7} than {1} was ever meant to be. goodbye.
        """.format(*replacements)))

    @commands.command()
    async def lenny(self, ctx):
        """Print lenny face ( ͡° ͜ʖ ͡°)"""
        await ctx.send("( ͡° ͜ʖ ͡°)")

    #@commands.command(aliases=[])
    #async def rip(self, ctx):


def setup(bot):
    bot.add_cog(Memes(bot))
