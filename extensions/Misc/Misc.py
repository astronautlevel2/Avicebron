from discord.ext import commands
import os
import datetime

class Misc:

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        start = datetime.datetime.now()
        message = await ctx.send("Pong! Response time: (Calculating)")
        end = message.created_at.now()
        await message.edit(content="Pong! Response time: {} ms".format((end - start).microseconds / 1000))

def setup(bot):
    bot.add_cog(Misc(bot))