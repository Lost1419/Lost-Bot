import discord
from discord.ext import commands


class GetHelp(commands.HelpCommand):
    commands.HelpCommand.show_hidden = False

    COLOUR = 0x8f1f21

    def get_ending_note(self):
        return f"<> Means that it requiried and [] means it's optinal | {self.clean_prefix}{self.invoked_with} [command] for command help."

    def get_command_signature(self, command):
        return f'{command.qualified_name} {command.signature}'

    async def send_bot_help(self, mapping):
        embed = discord.Embed(title='Commands', colour=self.COLOUR)
        description = self.context.bot.description
        if description:
            embed.description = description

        for cog, commands in mapping.items():
            name = 'No Category' if cog is None else cog.qualified_name
            filtered = await self.filter_commands(commands, sort=True)
            if filtered:
                value = ' '.join(f"`{c.name}`" for c in commands)
                if cog and cog.description:
                    value = f'{cog.description}\n{value}'

                embed.add_field(name=name, value=value, inline=False)

        embed.set_footer(text=self.get_ending_note())
        destination = self.get_destination()
        await destination.send(embed=embed)

    async def send_cog_help(self, cog):
        embed = discord.Embed(title='{0.qualified_name} Commands'.format(cog), colour=self.COLOUR)
        if cog.description:
            embed.description = cog.description

        filtered = await self.filter_commands(cog.get_commands(), sort=True)
        for command in filtered:
            embed.add_field(name=self.get_command_signature(command), value=command.description or '...', inline=False)

        embed.set_footer(text=self.get_ending_note())
        destination = self.get_destination()
        await destination.send(embed=embed)

    async def send_group_help(self, group):
        embed = discord.Embed(title=f"Help for {group.qualified_name}", colour=self.COLOUR)

        if group.help:
            embed.description = group.help

        if isinstance(group, commands.Group):
            filtered = await self.filter_commands(group.commands, sort=True)
            for command in filtered:
                embed.add_field(name=self.get_command_signature(command), value=command.description or '...',
                                inline=False)

        embed.set_footer(text=self.get_ending_note())
        destination = self.get_destination()
        await destination.send(embed=embed)

    send_command_help = send_group_help


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._original_help_command = bot.help_command
        bot.help_command = GetHelp()
        bot.help_command.cog = self

    def cog_unload(self):
        self.bot.help_command = self._original_help_command


def setup(bot):
    bot.add_cog(Help(bot))
