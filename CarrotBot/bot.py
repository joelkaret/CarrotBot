import discord
import json
import time
import threading
import asyncio
import csv
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
        await ctx.send(f"{user.mention} has been VC Channel Blocked")

    #VCUnblock
    @bot.command(name="VCUnblock", descripition="Will VCUnblock Someone")
    @commands.has_role("Guild Staff")
    async def VCUnblock(ctx, user: discord.Member):
        role = get(ctx.guild.roles, name="VC Channel Blocked")
        await user.remove_roles(role)
        await ctx.send(f"{user.mention} has been VC Channel Unblocked")

    #Leaderboards
    @bot.command(name="UpdateLeaderboard", description="Will update the leaderboard", aliases=["UpdLdb"])
    @commands.has_role("Guild Staff")
    async def UpdateLeaderboard(ctx):
        channel = bot.get_channel(836258539806654544)
        await ctx.channel.purge(limit=1)
        overall = readCSV("leaderboard_overall.csv")
        solos = readCSV("leaderboard_solos.csv")
        doubles = readCSV("leaderboard_doubles.csv")
        threes = readCSV("leaderboard_threes.csv")
        fours = readCSV("leaderboard_fours.csv")
        fourVSfour = readCSV("leaderboard_4v4.csv")
        await channel.send(f"""
__Overall Winstreak__
        {ArrayToString(overall)}
__Solo Winstreak__
        {ArrayToString(solos)}
__Doubles Winstreak__
        {ArrayToString(doubles)}
__3s Winstreak__
        {ArrayToString(threes)}
__4s Winstreak__
        {ArrayToString(fours)}
__4v4 Winstreak__
        {ArrayToString(fourVSfour)}
        """)
        await ctx.send("Bedwars Winstreak Leaderboard Updated")
        
    def ArrayToString(array):
        string = ""
        count = 1
        for i in range (0,len(array)):
            values = array[i].split(',')
            string = f"{string}{count}. `{values[0]}` - {values[1]}\n        "
            count += 1
        return string

    def readCSV(filename):
        file = open(filename, 'rt')
        lines = file.read().splitlines()
        return lines

    def csvToArray(csvLines):
        array = []
        numberOfLines = len(csvLines)
        for i in range (0,numberOfLines):
            line = csvLines[i]
            values = line.split(',')
            array.append(values)
        return array

    def writeCSV(filename, array):
        with open(filename, 'w', newline='') as file:
            csv.writer(file, delimiter=',').writerows(array)

    def addToLeaderboard(file, ign, winstreak):
        leaderboard = csvToArray(readCSV(file))
        entry = [ign, winstreak]
        for i in range (0, len(leaderboard)-1):
            if entry[0] == leaderboard[i][0]:
                leaderboard.pop(i)
        leaderboard.append(entry)
        #BubbleSort
        swapped = True
        while swapped:
            swapped = False
            for i in range (0, len(leaderboard)-1):
                print(leaderboard)#TEST
                if int(leaderboard[i][1]) > int(leaderboard[i+1][1]):
                    temp = leaderboard[i]
                    leaderboard[i] = leaderboard[i+1]
                    leaderboard[i+1] = temp
                    swapped = True
        writeCSV(file, leaderboard)

    @bot.command(name="SolosAdd", description="Will add a winstreak to the solos leaderboard")
    @commands.has_role("Guild Staff")
    async def SolosAdd(ctx, ign, winstreak):
        print("1")#TEST
        addToLeaderboard("leaderboard_solos.csv", ign, winstreak)
        UpdateLeaderboard(ctx)
        print("2")#TEST

        



    return bot 