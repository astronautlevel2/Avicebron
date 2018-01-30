import discord


class EventLogs:
    def __init__(self, bot):
        self.bot = bot
        self.log_channel = bot.event_log_channel

    async def on_member_remove(self, member):
        embed = discord.Embed()
        embed.set_author(name="User {} has left the server!".format(member), icon_url=member.avatar_url)
        await self.log_channel.send(embed=embed)

    async def on_member_join(self, member):
        embed = discord.Embed()
        embed.set_author(name="User {} has joined the server!".format(member), icon_url=member.avatar_url)
        await self.log_channel.send(embed=embed)

def setup(bot):
    bot.add_cog(EventLogs(bot))
