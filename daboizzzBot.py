import discord
from discord.ext import commands
from discord.utils import get

client = commands.Bot(command_prefix='&&')


@client.event
async def on_ready():
    print('Bot is ready')


@client.command()
async def ping(ctx, *, message="hi"):
    daboiz = 799036164057071636
    role = get(ctx.guild.roles, id=daboiz)
    if role in ctx.author.roles:
        await ctx.send(role.mention + ctx.author.mention + " says " + message)


client.run("ODI1MzU5NDM0NjAyNTEyMzg4.YF8x3w.8MzJhl2xYl6lnIOlG0WGNxosaNQ")
