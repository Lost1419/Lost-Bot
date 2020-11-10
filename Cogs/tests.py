from discord.ext import commands


class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='other-test')
    async def _name(self, ctx):
        await ctx.send("Test Successful")


def setup(bot):
    bot.add_cog(Test(bot))
