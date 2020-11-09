mport discord
import traceback
import sys
from discord.ext import commands


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Logged in as: {self.bot.user}\nName: {self.bot.user.name}\nDiscriminator:{self.bot.user.discriminator}\nId: {self.bot.user.id}")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if hasattr(ctx.command, 'on_error'):
            return

        cog = ctx.cog
        if cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return

        ignored = (commands.CommandNotFound,)
        error = getattr(error, 'original', error)
        if isinstance(error, ignored):
            return

        if isinstance(error, commands.CheckFailure):
            await ctx.send('You have been blacklisted')
        elif isinstance(error, commands.ExtensionNotLoaded):
            unsuccessful_emoji = self.bot.get_emoji(758518136525422615)
            unsuccessful_embed = discord.Embed(
                title="Unsuccessful",
                description=f"{unsuccessful_emoji}| Could not find that module.",
                color=self.bot.lost_color
            )
            await ctx.send(embed=unsuccessful_embed)
        else:
            print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

def setup(bot):
    bot.add_cog(Events(bot))
