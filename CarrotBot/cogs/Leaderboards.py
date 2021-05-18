from discord.ext import commands
from dotenv import load_dotenv
import os
import boto3
import csv



class leaderboards(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    #Variables
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
    
    
    
    #Check
    async def is_me(ctx):
        return ctx.author.id == 506884005195677696 #My ID
    

    
    #Functions
    def readCSV(self, filename):
        file = open(filename, 'rt')
        lines = file.read().splitlines()
        return lines

    def csvToArray(self, csvLines):
        array = []
        numberOfLines = len(csvLines)
        for i in range (0,numberOfLines):
            line = csvLines[i]
            values = line.split(',')
            array.append(values)
        return array

    def writeCSV(self, filename, array, nameS3):
        with open(filename, 'w', newline='') as file:
            csv.writer(file, delimiter=',').writerows(array)
        nameS3.upload_file(filename)

    def addToLeaderboard(self, file, ign, winstreak, nameS3):
        leaderboard = self.csvToArray(self.readCSV(file))
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
                if int(leaderboard[i][1]) < int(leaderboard[i+1][1]):
                    temp = leaderboard[i]
                    leaderboard[i] = leaderboard[i+1]
                    leaderboard[i+1] = temp
                    swapped = True
        self.writeCSV(file, leaderboard, nameS3)
    
    def removeFromLeaderboard(self, file, ign, nameS3):
        leaderboard = self.csvToArray(self.readCSV(file))
        for i in range (0, len(leaderboard)-1):
            if leaderboard[i][0] == ign:
                leaderboard.pop(i)
        self.writeCSV(file, leaderboard, nameS3)



    #Commands
    @commands.command(name="UpdateLeaderboard", 
                      descripition="Updates the leaderboard", 
                      aliases=["UpdLdb","LdbUpd"])
    @commands.check(is_me)
    async def UpdateLeaderboard(self, ctx):
        channel = commands.get_channel(836258539806654544)
        await channel.purge(limit=1)
        overall = self.readCSV("leaderboard_overall.csv")
        solos = self.readCSV("leaderboard_solos.csv")
        doubles = self.readCSV("leaderboard_doubles.csv")
        threes = self.readCSV("leaderboard_threes.csv")
        fours = self.readCSV("leaderboard_fours.csv")
        fourVSfour = self.readCSV("leaderboard_4v4.csv")
        await channel.send(f"""
**Overall Winstreak**
{self.ArrayToString(overall)}
**Solo Winstreak**
{self.ArrayToString(solos)}
**Doubles Winstreak**
{self.ArrayToString(doubles)}
**3s Winstreak**
{self.ArrayToString(threes)}
**4s Winstreak**
{self.ArrayToString(fours)}
**4v4 Winstreak**
{self.ArrayToString(fourVSfour)}
        """)
        await ctx.send("Bedwars Winstreak Leaderboard Updated")

    @commands.command(name="LeaderboardAdd", 
                      descripition="Add a winstreak to any leaderboard", 
                      aliases=["LdbAdd","AddLdb"])
    @commands.has_role("Guild Staff")
    async def LeaderboardAdd(self, ctx, mode, ign, winstreak):
        mode = mode.lower()
        nameS3 = "Error"
        if mode == "overall":
            nameS3 = self.overallS3
            leaderboardFile = "leaderboard_overall.csv"
        elif mode == "solos":
            nameS3 = self.solosS3
            leaderboardFile = "leaderboard_solos.csv"
        elif mode == "doubles":
            nameS3 = self.doublesS3
            leaderboardFile = "leaderboard_doubles.csv"
        elif mode == "threes":
            nameS3 = self.threesS3
            leaderboardFile = "leaderboard_threes.csv"
        elif mode == "fours":
            nameS3 = self.foursS3
            leaderboardFile = "leaderboard_fours.csv"
        elif mode == "4v4":
            nameS3 = self.fourVSfourS3
            leaderboardFile = "leaderboard_4v4.csv"
        if nameS3 != "Error":
            self.addToLeaderboard(leaderboardFile, ign, winstreak, nameS3)
            await self.UpdateLeaderboard(ctx)
        else:
            await ctx.send("Command Failed")

    @commands.command(name="LeaderboardRemove", 
                      descripition="Add a winstreak to any leaderboard", 
                      aliases=["LdbDel","DelLdb","LdbRem","RemLdb"])
    @commands.has_role("Guild Staff")
    async def LeaderboardRemove(self, ctx, mode, ign):
        mode = mode.lower()
        nameS3 = "Error"
        if mode == "overall":
            nameS3 = self.overallS3
            leaderboardFile = "leaderboard_overall.csv"
        elif mode == "solos":
            nameS3 = self.solosS3
            leaderboardFile = "leaderboard_solos.csv"
        elif mode == "doubles":
            nameS3 = self.doublesS3
            leaderboardFile = "leaderboard_doubles.csv"
        elif mode == "threes":
            nameS3 = self.threesS3
            leaderboardFile = "leaderboard_threes.csv"
        elif mode == "fours":
            nameS3 = self.foursS3
            leaderboardFile = "leaderboard_fours.csv"
        elif mode == "4v4":
            nameS3 = self.fourVSfourS3
            leaderboardFile = "leaderboard_4v4.csv"
        if nameS3 != "Error":
            self.removeFromLeaderboard(leaderboardFile, ign, nameS3)
            await self.UpdateLeaderboard(ctx)
        else:
            await ctx.send("Command Failed")

def setup(bot):
    bot.add_cog(leaderboards(bot))