import discord
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
    async def spam(self, ctx, channel: discord.TextChannel,  member: typing.Optional[discord.Member], *, msg=None):
        if member is not None:
            self.spaming.start(channel=channel, spam_msg=f"<@!{member.id}>")
            await ctx.send("Spam has been started!")
        elif msg is not None:
            self.spaming.start(channel=channel, spam_msg=msg)
            await ctx.send("Spam has been started!")
        elif msg and member is not None:
            self.spaming.start(channel=channel, spam_msg=f"<@!{member.id}> {msg}")
            await ctx.send("Spam has been started!")
        else:
            await ctx.send("That is unsupported")

    @spam.command()
    @not_blacklisted()
    async def stop(self, ctx):
        self.spaming.stop()
        await ctx.send("Spam Stopped")

    @tasks.loop(seconds=15)
    async def spaming(self, channel: discord.TextChannel, spam_msg: str):
        await channel.send(spam_msg)


def setup(bot):
    bot.add_cog(Random(bot))
