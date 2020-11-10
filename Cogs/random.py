import discord
import requests
import asyncio
import typing
from discord.ext import commands, tasks

blacklisted_users = [402939508615544832]


def not_blacklisted():
    def predicate(ctx):
        if ctx.author.id in blacklisted_users:
            return False
        else:
            return True

    return commands.check(predicate)


def guild_owner():
    def predicate(ctx):
        return ctx.author.id == ctx.guild.owner_id

    return commands.check(predicate)


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

    @commands.group(invoke_without_command=True)
    @not_blacklisted()
    async def spam(self, ctx, channel: discord.TextChannel, *, msg):
        self.spaming.start(channel=channel, spam_msg=msg)
        await ctx.send("Spam has been started!")

    @spam.command()
    @not_blacklisted()
    async def stop(self, ctx):
        self.spaming.stop()
        await ctx.send("Spam Stopped")

    @tasks.loop(seconds=15)
    async def spaming(self, channel: discord.TextChannel, spam_msg: str):
        await channel.send(spam_msg)

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

    @commands.command()
    async def get(self, ctx, url: str):
        request = requests.get(url)
        print(request.text)

    @commands.command()
    @guild_owner()
    async def test(self, ctx):
        self.bot.load_extension("Cogs.test")
        await ctx.send("Done!")


def setup(bot):
    bot.add_cog(Random(bot))
