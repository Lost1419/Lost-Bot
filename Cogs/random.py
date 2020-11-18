import discord
import asyncio
import typing
from discord.ext import commands, tasks


class Random(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def say(self, ctx, *, message):
        if any(word in message.lower() for word in self.bot.banned_words):
            await ctx.message.delete()
            await ctx.send("Don't say those words please.")
        else:
            msg_embed = discord.Embed(title=f"{ctx.author}", description=message)
            await ctx.send(embed=msg_embed)

    @commands.command()
    async def math(self, ctx, number_1: float, operator: str, number_2: float):
        if operator == '*':
            await ctx.send(f"{number_1}*{number_2}={number_1 * number_2}")
        elif operator == '/':
            await ctx.send(f"{number_1}/{number_2}={number_1 / number_2}")
        elif operator == '+':
            await ctx.send(f"{number_1}+{number_2}={number_1 + number_2}")
        elif operator == '-':
            await ctx.send(f"{number_1}-{number_2}={number_1 - number_2}")
        else:
            await ctx.send("Unsupported Type")

    @commands.command()
    async def type(self, ctx, channel: typing.Optional[discord.TextChannel], time: int, *, msg):
        if channel is None:
            channel = ctx.channel

        async with channel.typing():
            await asyncio.sleep(time)
            await channel.send(msg)


def setup(bot):
    bot.add_cog(Random(bot))
