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
        await ctx.send("ping - pings da boiz role\nwhoop - pings you")

    @slash.slash(name="help", description="Displays the help menu")
    async def helpSlash(ctx):
        await ctx.send("ping - pings da boiz role\nwhoop - pings you")

    #ping da boiz
    @bot.command(name="ping", description="pings da boiz")
    async def ping(ctx, *message):
        daboiz = 799036164057071636
        role = get(ctx.guild.roles, id=daboiz)
        for i in range(0, len(message)):
            for j in range(0, len(message[i])):
                if message[i][j] == "@":
                    role = "this is not a role"
        if role in ctx.author.roles:
            await ctx.send(role.mention + ctx.author.mention + " says " + " ".join(message))

    #Whoop
    @bot.command(name="Whoop", description="This will ping you!")
    async def Whoop(ctx, *message):
        await ctx.send(ctx.author.mention + " WHOOP!")

    @slash.slash(name="Whoop", description="This will ping you!")
    async def WhoopSlash(ctx):
        await ctx.send(ctx.author.mention + " WHOOP!")

    @bot.command(name="Say", descripition="Carrot will say this.")
    async def Say(ctx, *message):
        if ctx.author.id == 506884005195677696: #My Discord id
            await ctx.send(" ".join(message))


    async def called_once_a_day():  # Fired every day (at 3:59 UTC)
        channel = bot.get_guild(713646548436910116).get_channel(718527252970733659)
        await channel.send(".gexp")
        await asyncio.sleep(60)
        await channel.send(".refresh")

    async def background_task(): #Taken from Stack Overflow. https://stackoverflow.com/questions/63769685/discord-py-how-to-send-a-message-everyday-at-a-specific-time
        now = datetime.utcnow()
        if now.time() > WHEN:
            tomorrow = datetime.combine(now.date() + timedelta(days=1), time(0))
            seconds = (tomorrow - now).total_seconds()  # Seconds until tomorrow (midnight)
            await asyncio.sleep(seconds)   # Sleep until tomorrow and then the loop will start 
        while True:
            now = datetime.utcnow()
            target_time = datetime.combine(now.date(), WHEN)
            seconds_until_target = (target_time - now).total_seconds()
            await asyncio.sleep(seconds_until_target)  # Sleep until we hit the target time
            await called_once_a_day()  # Call the helper function that sends the message
            tomorrow = datetime.combine(now.date() + timedelta(days=1), time(0))
            seconds = (tomorrow - now).total_seconds()  # Seconds until tomorrow (midnight)
            await asyncio.sleep(seconds)   # Sleep until tomorrow and then the loop will start a new iteration

    bot.loop.create_task(background_task())
    return bot 