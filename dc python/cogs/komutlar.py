import discord
from discord.ext import commands
import random


class Komutlar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.activities = {}

    @commands.command()
    async def cekilis(self, ctx):
        await ctx.send(random.choice(self.bot.guilds[0].members))

    @commands.command()
    async def change_status(self, ctx, activity, *, text):
        self.bind_text(text)
        await self.bot.change_presence(**self.activities.get(activity))  # activity=discord.Game(name=text)

    def bind_text(self, text, url=''):
        self.activities = {
            "1": {"activity": discord.Game(name=text)},
            "2": {"activity": discord.Activity(type=discord.ActivityType.listening, name=text)},
            "3": {"activity": discord.Activity(type=discord.ActivityType.watching, name=text)},
            "4": {"activity": discord.Streaming(name=text, url=url)},
        }


def setup(bot):
    bot.add_cog(Komutlar(bot))
