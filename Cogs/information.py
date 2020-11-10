import discord
import typing
from discord.ext import commands


class Information(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def profile(self, ctx, member: typing.Optional[discord.Member]):
        if member is None:
            member = ctx.author

        profile_embed = discord.Embed(title=f"{member}", color=member.color)
        profile_embed.add_field(name="Name", value=member.name, inline=True)
        profile_embed.add_field(name="Id", value=member.id, inline=True)
        profile_embed.add_field(name="Discriminator", value=member.discriminator, inline=True)
        profile_embed.add_field(name="Nickname", value=member.display_name, inline=True)
        await ctx.send(embed=profile_embed)


def setup(bot):
    bot.add_cog(Information(bot))
