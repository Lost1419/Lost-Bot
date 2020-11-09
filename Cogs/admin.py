import discord
from discord.ext import commands


class Admin(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def reload(self, ctx, *, module):
        success_emoji = self.bot.get_emoji(758517607912439909)
        module_name = f"Cogs.{module.lower()}"

        self.bot.unload_extension(module_name)
        self.bot.load_extension(module_name)
        reload_embed = discord.Embed(
            title="Successful Reload",
            description=f"{success_emoji}| Successfully reloaded {module.title()} module.",
            color=self.bot.lost_color)

        await ctx.send(embed=reload_embed)

    @reload.command()
    async def all(self, ctx):
        success_emoji = self.bot.get_emoji(758517607912439909)
        modules = []
        for module in self.bot.extensions:
            modules.append(module)

        for module in modules:
            self.bot.unload_extension(module)
            self.bot.load_extension(module)

        reload_embed = discord.Embed(
            title="Successful of all Modules",
            description=f"{success_emoji}| Successfully reloaded all modules.",
            color=self.bot.lost_color)

        await ctx.send(embed=reload_embed)

    @commands.command()
    async def load(self, ctx, *, module):
        success_emoji = self.bot.get_emoji(758517607912439909)
        module_name = f"Cogs.{module.lower()}"

        self.bot.load_extension(module_name)
        load_embed = discord.Embed(
            title="Successful Load",
            description=f"{success_emoji}| Successfully loaded {module.title()} module.",
            color=self.bot.lost_color
        )

        await ctx.send(embed=load_embed)

    @commands.command()
    async def unload(self, ctx, *, module):
        success_emoji = self.bot.get_emoji(758517607912439909)
        module_name = f"Cogs.{module.lower()}"

        self.bot.unload_extension(module_name)
        unload_embed = discord.Embed(
            title="Successful Load",
            description=f"{success_emoji}| Successfully unloaded {module.title()} module.",
            color=self.bot.lost_color
        )

        await ctx.send(embed=unload_embed)


def setup(bot):
    bot.add_cog(Admin(bot))
