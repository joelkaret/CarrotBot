import os
import discord
from discord.ext import commands
from discord.utils import get
from discord_slash import SlashCommand, SlashContext

client = commands.Bot(command_prefix='&&')
slash = SlashCommand(client, sync_commands=True)
guild_ids = [713646548436910116]
client.remove_command("help")

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game('&&ping To @da boiz'))
    print('Bot is ready')

@client.command()
async def help(ctx):
    await ctx.send("This is a temporary help command")

@slash.slash(name="help", guild_ids=guild_ids, description="Displays the help menu")
async def helpSlash(ctx):
    await ctx.send("This is a temporary help command")


@client.command(name="ping", description="pings da boiz")
async def ping(ctx, *message):
    daboiz = 799036164057071636
    role = get(ctx.guild.roles, id=daboiz)
    for i in range(0, len(message)):
        for j in range(0, len(message[i])):
            if message[i][j] == "@":
                role = "this is not a role"
    if role in ctx.author.roles:
        await ctx.send(role.mention + ctx.author.mention + " says " + " ".join(message))

#@slash.slash(name="pingDaBoiz", guild_ids=guild_ids, description="This will ping da boiz")
#async def pingSlash(ctx, *message):
#    daboiz = 799036164057071636
#    role = get(ctx.guild.roles, id=daboiz)
#    for i in range(0, len(message)):
#        for j in range(0, len(message[i])):
#            if message[i][j] == "@":
#                role = "this is not a role"
#    if role in ctx.author.roles:
#        await ctx.send(role.mention + ctx.author.mention + " says " + " ".join(message))


@client.command(name="Whoop", description="This will WHOOP your ass!")
async def Whoop(ctx, *message):
    await ctx.send(ctx.author.mention + " WHOOP!")


@slash.slash(name="testWhoop", guild_ids=guild_ids, description="This will WHOOP your ass!")
async def WhoopSlash(ctx):
    await ctx.send(ctx.author.mention + " WHOOP!")


client.run(os.getenv("PRIVATE_KEY"))
