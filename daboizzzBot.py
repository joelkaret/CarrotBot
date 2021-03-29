import os
import discord
from discord.ext import commands
from discord.utils import get

client = commands.Bot(command_prefix='&&')


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game('&&ping To @da boiz'))    
    print('Bot is ready')


@client.command()
async def ping(ctx, *message):
    daboiz = 799036164057071636
    role = get(ctx.guild.roles, id=daboiz)
    for i in range(0, len(message)):
        for j in range(0, len(message[i])):
            if message[i][j] == "@":
                role = "this is not a role"
    if role in ctx.author.roles:
        await ctx.send(role.mention + ctx.author.mention + " says " + " ".join(message))
    

client.run(os.getenv("PRIVATE_KEY"))
