import discord
import asyncpg
import random
import asyncio
from discord.ext import commands


class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def register(self, ctx):
        try:
            await self.bot.conn.execute('''INSERT INTO economy(id, bank, wallet) VALUES($1, $2, $3)''', ctx.author.id, 100, 0)
            await ctx.send(f"You have been registered.")
        except asyncpg.exceptions.UniqueViolationError:
            await ctx.send(f"Your already registered.")

    @commands.command(aliases=['bal'])
    async def balance(self, ctx):
        bal = await self.bot.conn.fetchrow('SELECT * FROM economy WHERE id=$1', ctx.author.id)

        bal_embed = discord.Embed(title=f"{ctx.author.name}'s Balance",description=f"Wallet: {bal['wallet']}\nBank: {bal['bank']}")
        bal_embed.set_thumbnail(url=ctx.author.avatar_url)
        bal_embed.set_footer(text=f'You can get more money by using {ctx.prefix}work!')
        await ctx.send(embed=bal_embed)

    @commands.command()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def work(self, ctx):
        balance = await self.bot.conn.fetchrow('SELECT * FROM economy WHERE id=$1', ctx.author.id)

        amount = random.randrange(50, 500)
        add_amount = amount + balance['wallet']

        await self.bot.conn.execute('''UPDATE economy SET wallet=$1 WHERE id=$2''', add_amount, ctx.author.id)

        work_embed = discord.Embed(title=f"You worked and got `${amount}`", color=self.bot.lost_color)
        await ctx.send(embed=work_embed)

    @commands.group(aliases=['dep'], invoke_without_command=True)
    async def deposit(self, ctx, amount: int):
        balance = await self.bot.conn.fetchrow('SELECT * FROM economy WHERE id=$1', ctx.author.id)
        if amount <= balance['wallet']:

            with_amount = balance['wallet'] - amount
            dep_amount = balance['bank'] + amount

            await self.bot.conn.execute('''UPDATE economy SET wallet=$1 WHERE id=$2''', with_amount, ctx.author.id)
            await self.bot.conn.execute('''UPDATE economy SET bank=$1 WHERE id=$2''', dep_amount, ctx.author.id)

            await ctx.send(f"You have deposited `${amount}` into your bank.")

        else:
            await ctx.send("You don't have that much money.")

    @deposit.command(name='all')
    async def _name(self, ctx):
        balance = await self.bot.conn.fetchrow('SELECT * FROM economy WHERE id=$1', ctx.author.id)
        dep_amount = balance['wallet']
        if dep_amount != 0:
            await self.bot.conn.execute('''UPDATE economy SET wallet=$1 WHERE id=$2''', 0, ctx.author.id)
            await self.bot.conn.execute('''UPDATE economy SET bank=$1 WHERE id=$2''', dep_amount, ctx.author.id)

            await ctx.send(f"You have deposited `${balance['wallet']}` into your bank.")
        else:
            await ctx.send("You have nothing to deposit.")

    @commands.group(aliases=['with'], invoke_without_command=True)
    async def withdraw(self, ctx, amount: int):
        balance = await self.bot.conn.fetchrow('SELECT * FROM economy WHERE id=$1', ctx.author.id)
        if amount <= balance['bank']:

            with_amount = balance['bank'] - amount
            dep_amount = balance['wallet'] + amount

            await self.bot.conn.execute('''UPDATE economy SET wallet=$1 WHERE id=$2''', dep_amount, ctx.author.id)
            await self.bot.conn.execute('''UPDATE economy SET bank=$1 WHERE id=$2''', with_amount, ctx.author.id)
            balance = await self.bot.conn.fetchrow('SELECT * FROM economy WHERE id=$1', ctx.author.id)

            await ctx.send(f"You have withdrew `${amount}` from your bank.")

        else:
            await ctx.send("You don't have that much money.")

    @withdraw.command(name='all')
    async def _all(self, ctx):
        balance = await self.bot.conn.fetchrow('SELECT * FROM economy WHERE id=$1', ctx.author.id)
        dep_amount = balance['bank']
        if dep_amount != 0:
            dep_amount = balance['bank'] + balance['wallet']
            await self.bot.conn.execute('''UPDATE economy SET wallet=$1 WHERE id=$2''', dep_amount, ctx.author.id)
            await self.bot.conn.execute('''UPDATE economy SET bank=$1 WHERE id=$2''', 0, ctx.author.id)

            await ctx.send(f"You have withdrew `${balance['bank']}` from your bank.")
        else:
            await ctx.send("You have nothing to withdraw.")


def setup(bot):
    bot.add_cog(Economy(bot))
