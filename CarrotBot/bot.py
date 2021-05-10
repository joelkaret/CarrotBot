import discord
import json
import threading
import asyncio
import csv
import boto3
import os
from dotenv import load_dotenv
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
    load_dotenv() # Will load environment variables from a .env file
    ACCESS_ID = os.getenv("ACCESS_ID")
    ACCESS_KEY = os.getenv("ACCESS_KEY")
    REGION = os.getenv("REGION")
    s3_resource = boto3.resource('s3', aws_access_key_id=ACCESS_ID, aws_secret_access_key=ACCESS_KEY, region_name=REGION)
    overallS3 = s3_resource.Object('bedwarswinstreakleaderboard', 'leaderboard_overall.csv')
    solosS3 = s3_resource.Object('bedwarswinstreakleaderboard', 'leaderboard_solos.csv')
    doublesS3 = s3_resource.Object('bedwarswinstreakleaderboard', 'leaderboard_doubles.csv')
    threesS3 = s3_resource.Object('bedwarswinstreakleaderboard', 'leaderboard_threes.csv')
    foursS3 = s3_resource.Object('bedwarswinstreakleaderboard', 'leaderboard_fours.csv')
    fourVSfourS3 = s3_resource.Object('bedwarswinstreakleaderboard', 'leaderboard_4v4.csv')
    s3_resource.Object('bedwarswinstreakleaderboard', 'leaderboard_overall.csv').download_file('leaderboard_overall.csv')
    s3_resource.Object('bedwarswinstreakleaderboard', 'leaderboard_solos.csv').download_file('leaderboard_solos.csv')
    s3_resource.Object('bedwarswinstreakleaderboard', 'leaderboard_doubles.csv').download_file('leaderboard_doubles.csv')
    s3_resource.Object('bedwarswinstreakleaderboard', 'leaderboard_threes.csv').download_file('leaderboard_threes.csv')
    s3_resource.Object('bedwarswinstreakleaderboard', 'leaderboard_fours.csv').download_file('leaderboard_fours.csv')
    s3_resource.Object('bedwarswinstreakleaderboard', 'leaderboard_4v4.csv').download_file('leaderboard_4v4.csv')

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
    @bot.command(name="UpdateLeaderboard", descripition="Updates the leaderboard", aliases=["UpdLdb"])
    @commands.has_role("Guild Staff")
    async def UpdateLeaderboard(ctx):
        channel = bot.get_channel(836258539806654544)
        await channel.purge(limit=1)
        overall = readCSV("leaderboard_overall.csv")
        solos = readCSV("leaderboard_solos.csv")
        doubles = readCSV("leaderboard_doubles.csv")
        threes = readCSV("leaderboard_threes.csv")
        fours = readCSV("leaderboard_fours.csv")
        fourVSfour = readCSV("leaderboard_4v4.csv")
        await channel.send(f"""
**Overall Winstreak**
{ArrayToString(overall)}
**Solo Winstreak**
{ArrayToString(solos)}
**Doubles Winstreak**
{ArrayToString(doubles)}
**3s Winstreak**
{ArrayToString(threes)}
**4s Winstreak**
{ArrayToString(fours)}
**4v4 Winstreak**
{ArrayToString(fourVSfour)}
        """)
        await ctx.send("Bedwars Winstreak Leaderboard Updated")
        
    def ArrayToString(array):
        string = ""
        count = 1
        UpTo = len(array)
        if len(array) > 10:
            UpTo = 10
        for i in range (0,UpTo):
            values = array[i].split(',')
            if values[0] == "Minimum":
                string = f"{string}*{values[0]} - {values[1]}*\n"
            else:
                string = f"{string}{count}. `{values[0]}` - {values[1]}\n"
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

    def writeCSV(filename, array, nameS3):
        with open(filename, 'w', newline='') as file:
            csv.writer(file, delimiter=',').writerows(array)
        nameS3.upload_file(filename)

    def addToLeaderboard(file, ign, winstreak, nameS3):
        leaderboard = csvToArray(readCSV(file))
        entry = [ign, winstreak]
        for i in range (0, len(leaderboard)):
            if entry[0] == leaderboard[i][0]:
                leaderboard.pop(i)
        leaderboard.append(entry)
        #BubbleSort
        swapped = True
        while swapped:
            swapped = False
            for i in range (0, len(leaderboard)-1):
                if int(leaderboard[i][1]) < int(leaderboard[i+1][1]):
                    temp = leaderboard[i]
                    leaderboard[i] = leaderboard[i+1]
                    leaderboard[i+1] = temp
                    swapped = True
        writeCSV(file, leaderboard, nameS3)
    
    def removeFromLeaderboard(file, ign, nameS3):
        leaderboard = csvToArray(readCSV(file))
        for i in range (0, len(leaderboard)):
            if leaderboard[i][0] == ign:
                leaderboard.pop(i)
        writeCSV(file, leaderboard, nameS3)

    @bot.command(name="LeaderboardAdd", descripition="Add a winstreak to any leaderboard", aliases=["LdbAdd"])
    @command.has_role("Guild Staff")
    async def LeaderboardAdd(ctx, mode, ign, winstreak):
        mode = mode.lower()
        nameS3 = "Error"
        if mode == "overall":
            nameS3 = overallS3
        elif mode == "solos":
            nameS3 = solosS3
        elif mode == "doubles":
            nameS3 = doublesS3
        elif mode == "threes":
            nameS3 = threesS3
        elif mode == "fours":
            nameS3 = foursS3
        elif mode == "4v4":
            nameS3 = fourVSfourS3
        if nameS3 != "Error":
            addToLeaderboard("leaderboard_overall.csv", ign, winstreak, nameS3)
        else:
            await ctx.send("Command Failed")

    @bot.command(name="LeaderboardRemove", descripition="Add a winstreak to any leaderboard", aliases=["LdbDel"])
    @command.has_role("Guild Staff")
    async def LeaderboardRemove(ctx, mode, ign):
        mode = mode.lower()
        nameS3 = "Error"
        if mode == "overall":
            nameS3 = overallS3
        elif mode == "solos":
            nameS3 = solosS3
        elif mode == "doubles":
            nameS3 = doublesS3
        elif mode == "threes":
            nameS3 = threesS3
        elif mode == "fours":
            nameS3 = foursS3
        elif mode == "4v4":
            nameS3 = fourVSfourS3
        if nameS3 != "Error":
            removeFromLeaderboard("leaderboard_overall.csv", ign, nameS3)
        else:
            await ctx.send("Command Failed")

    return bot 