import os
import logging
import discord
from config import Config
from discord.ext import commands

config = Config()


async def get_prefix(client, message):
    try:
        prefix = await config.conn.fetchrow('SELECT * FROM guilds WHERE id=$1', message.guild.id)
        return prefix['prefix']
    except:
        return 'l!'


client = commands.Bot(
    command_prefix=get_prefix,
    description="A small bot made for practice.",
    activity=discord.Game(name="being Lost"),
    status=discord.Status.idle,
    help_command=None
)

client.lost_color = config.color
client.conn = config.conn

os.chdir('.')
for file in os.listdir('.\Cogs'):
    if file.endswith('.py'):
        client.load_extension(f"Cogs.{file[:-3]}")

client.run(config.token)
