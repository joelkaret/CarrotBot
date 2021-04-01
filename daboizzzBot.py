import os
import discord
import json
from discord.ext import commands
from discord.utils import get
from discord_slash import SlashCommand, SlashContext


#Define prefix for given server
def get_prefix(client, message):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    return prefixes[str(message.guild.id)]



client = commands.Bot(command_prefix=get_prefix)
slash = SlashCommand(client, sync_commands=True)
guild_ids = [713646548436910116]
client.remove_command("help")



#When Bot Is Ready
@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game('&ping To @da boiz'))
    print('Bot is ready')



#Prefixes
@client.event
async def on_guild_join(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = '&'

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

@client.event
async def on_guild_remove(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes.pop(str(guild.id))

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

@client.command()
async def changeprefix(ctx, prefix):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = prefix

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

    await ctx.send("Prefix has been changed to " + prefix)



#Help
@client.command()
async def help(ctx):
    await ctx.send("This is a temporary help command")

@slash.slash(name="help", guild_ids=guild_ids, description="Displays the help menu")
async def helpSlash(ctx):
    await ctx.send("This is a temporary help command")



#ping da boiz
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



#Whoop
@client.command(name="Whoop", description="This will WHOOP your ass!")
async def Whoop(ctx, *message):
    await ctx.send(ctx.author.mention + " WHOOP!")


@slash.slash(name="Whoop", guild_ids=guild_ids, description="This will WHOOP your ass!")
async def WhoopSlash(ctx):
    await ctx.send(ctx.author.mention + " WHOOP!")



#Run Bot
client.run(os.getenv("PRIVATE_KEY"))
