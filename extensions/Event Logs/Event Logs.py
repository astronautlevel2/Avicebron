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

    async def on_message_edit(self, old, message):
        if old.content != message.content:
            embed = discord.Embed()
            embed.set_author(name="{} has edited their message".format(message.author), icon_url=message.author.avatar_url)
            embed.add_field(name="Channel", value="{} ({})".format(message.channel.mention, message.channel), inline=False)
            embed.add_field(name="Old", value=old.content, inline=False)
            embed.add_field(name="New", value=message.content, inline=False)
            await self.log_channel.send(embed=embed)

    async def on_message_delete(self, message):
        embed = discord.Embed()
        embed.set_author(name="{} has deleted their message".format(message.author), icon_url=message.author.avatar_url)
        embed.add_field(name="Channel", value="{} ({})".format(message.channel.mention, message.channel), inline=False)
        embed.add_field(name="Message", value=message.content, inline=False)
        await self.log_channel.send(embed=embed)


def setup(bot):
    bot.add_cog(EventLogs(bot))