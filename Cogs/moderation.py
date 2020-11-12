import discord
from discord.ext import commands


# From R.Danny by Danny (Raptz). https://github.com/Rapptz/RoboDanny
class BannedMember(commands.Converter):
    async def convert(self, ctx, argument):
        if argument.isdigit():
            member_id = int(argument, base=10)
            try:
                return await ctx.guild.fetch_ban(discord.Object(id=member_id))
            except discord.NotFound:
                raise commands.BadArgument('This member has not been banned before.') from None

        ban_list = await ctx.guild.bans()
        entity = discord.utils.find(lambda u: str(u.user) == argument, ban_list)

        if entity is None:
            raise commands.BadArgument('This member has not been banned before.')
        return entity


class Moderation(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_guild_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        if ctx.author.top_role < member.top_role:
            await ctx.send("You can't ban someone with a higher role than you.")
            return

        await ctx.guild.kick(member, reason=f"**{member}**: Kicked for **{reason}**\n**By**: {ctx.author}")

        kick_embed = discord.Embed(
            title=f"Kicked {member.display_name}",
            description=f"{member}: Kicked for {reason}\nBy: {ctx.author}",
            color=self.bot.lost_color)

        await ctx.send(embed=kick_embed)

    @commands.command()
    @commands.has_guild_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        if ctx.author.top_role < member.top_role:
            await ctx.send("You can't ban someone with a higher role than you.")
            return

        if reason is None:
            reason = f"{ctx.author} banned {member}"

        await ctx.guild.ban(member, reason=f"{member}: Banned for {reason}\nBy: {ctx.author}")

        ban_embed = discord.Embed(
            title=f"Banned {member.display_name}",
            description=f"{member}: Banned for {reason}\nBy: {ctx.author}",
            color=self.bot.lost_color)

        await ctx.send(embed=ban_embed)

    @commands.command()
    @commands.has_guild_permissions(ban_members=True)
    async def unban(self, ctx, member: BannedMember, *, reason=None):
        await ctx.guild.unban(member, reason=f"{member}: Unbanned for {reason}\nBy: {ctx.author}")

        ban_embed = discord.Embed(
            title=f"Unbanned {member}",
            description=f"{member}: Unbanned for {reason}\nBy: {ctx.author}",
            color=self.bot.lost_color)

        await ctx.send(embed=ban_embed)


def setup(bot):
    bot.add_cog(Moderation(bot))
