import discord
import json
import time
import threading
import asyncio
from datetime import datetime, time, timedelta
from discord.ext import commands
from discord.utils import get
from discord_slash import SlashCommand

def create_bot():
    #Define prefix for given server
    def get_prefix(client, message):
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)
        return prefixes[str(message.guild.id)]

    bot = commands.Bot(command_prefix=get_prefix, case_insensitive=True)
    slash = SlashCommand(bot, sync_commands=True)
    bot.remove_command("help")
    WHEN = time(3, 59, 0)

    #When Bot Is Ready
    @bot.event
    async def on_ready():
        await bot.change_presence(status=discord.Status.online, activity=discord.Game('&ping To @da boiz'))
        print('Bot is ready')

    #Prefixes
    @bot.event
    async def on_guild_join(guild):
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)
        prefixes[str(guild.id)] = '&'
        with open('prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)

    @bot.event
    async def on_guild_remove(guild):
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)
        prefixes.pop(str(guild.id))
        with open('prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)

    @bot.command()
    async def changeprefix(ctx, prefix):
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)
        prefixes[str(ctx.guild.id)] = prefix
        with open('prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)
        await ctx.send("Prefix has been changed to " + prefix)

    #Help
    @bot.command()
    async def help(ctx):
        author = ctx.message.author

        embed = discord.Embed(
            colour = discord.Colour.purple()
        )

        embed.set_author(name='CarrotBot Help')
        embed.add_field(name='daboiz', value='Pings daboiz', inline=False)
        embed.add_field(name='whoop', value='Pings you, with funky message attached.', inline=False)
        embed.add_field(name='Staff Only', value='#############', inline=False)
        embed.add_field(name='VCBlock', value='Will VC Block Someone', inline=False)
        embed.add_field(name='VCUnblock', value='Will VC Unblock Someone', inline=False)

        await ctx.send(embed=embed)

    @slash.slash(name="help", description="Displays the help menu")
    async def helpSlash(ctx):
        await ctx.send("ping - pings da boiz role\nwhoop - pings you")

    #ping da boiz
    @bot.command(name="daboiz", description="pings da boiz")
    @commands.has_role("da boiz")
    async def daboiz(ctx, *message):
        role = get(ctx.guild.roles, name="da boiz")
        allowed = True
        for i in range(0, len(message)):
            for j in range(0, len(message[i])):
                if message[i][j] == "@":
                    allowed = False
        if allowed:
            await ctx.send(role.mention + ctx.author.mention + " says " + " ".join(message))

    #Whoop
    @bot.command(name="Whoop", description="This will ping you!")
    async def Whoop(ctx, *message):
        await ctx.send(ctx.author.mention + " WHOOP!")

    @slash.slash(name="Whoop", description="This will ping you!")
    async def WhoopSlash(ctx):
        await ctx.send(ctx.author.mention + " WHOOP!")

    #Say
    @bot.command(name="Say", descripition="Carrot will say this.")
    async def Say(ctx, *message):
        if ctx.author.id == 506884005195677696: #My Discord id - For Testing purposes only.
            await ctx.send(" ".join(message))
    
    #VCBlock
    @bot.command(name="VCBlock", descripition="Will VCBlock Someone")
    @commands.has_role("Guild Staff")
    async def VCBlock(ctx, user: discord.Member):
        role = get(ctx.guild.roles, name="VC Channel Blocked")
        await user.add_roles(role)
        await ctx.send(ctx.user.mention + " has been VC Channel Blocked")

    #VCUnblock
    @bot.command(name="VCUnblock", descripition="Will VCUnblock Someone")
    @commands.has_role("Guild Staff")
    async def VCUnblock(ctx, user: discord.Member):
        role = get(ctx.guild.roles, name="VC Channel Blocked")
        await user.remove_roles(role)
        await ctx.send(ctx.user.mention + " has been VC Channel Unblocked")

    return bot 