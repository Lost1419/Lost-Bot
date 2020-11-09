import os
import discord
from discord.ext import commands

client = commands.Bot(
    command_prefix=commands.when_mentioned_or('l!'),
    description="A small bot made for practice.",
    activity=discord.Game(name="SAO"),
    status=discord.Status.idle,
    help_command=None
)

client.lost_color = 0x8f1f21

os.chdir('.')
for file in os.listdir('.\Cogs'):
    if file.endswith('.py'):
        client.load_extension(f"Cogs.{file.removesuffix('.py')}")

client.run('')
