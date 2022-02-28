from discord.ext import commands
from dotenv import load_dotenv
import os
import boto3
import csv
import requests



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
    def usernameToUuid(self, username):
        try:
            url = f'https://api.mojang.com/users/profiles/minecraft/{username}?'
            response = requests.get(url)
            uuid = response.json()['id']
        except:
            uuid = username
        return uuid

    def uuidToUsername(self, uuid):
        try:
            url = f'https://api.mojang.com/user/profiles/{uuid}/names'
            response = requests.get(url)
            username = response.json()[-1]['name']
        except:
            username = uuid
        return username

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
        uuid = self.usernameToUuid(ign)
        entry = [uuid, winstreak]
        try:
            for i in range (0, len(leaderboard)-1):
                if entry[0] == leaderboard[i][0]:
                    leaderboard.pop(i)
        except:
            pass #didnt want to indent code :/
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
        uuid = self.usernameToUuid(ign)
        if isinstance(file, list):
            for j in range(0, len(file):
                leaderboard = self.csvToArray(self.readCSV(file[j]))
                try:
                for i in range (0, len(leaderboard)):
                    if leaderboard[i][0] == uuid:
                        leaderboard.pop(i)
                except:
                    self.writeCSV(file, leaderboard, nameS3[j])
        else:    
            leaderboard = self.csvToArray(self.readCSV(file))
            try:
                for i in range (0, len(leaderboard)):
                    if leaderboard[i][0] == uuid:
                        leaderboard.pop(i)
            except:
                self.writeCSV(file, leaderboard, nameS3)

    def ArrayToString(self, array):
        string = ''
        count = 1
        UpTo = len(array)
        if len(array) > 10:
            UpTo = 10
        i = 0
        while i < UpTo:
            values = array[i].split(',')
            values2 = ['False&^%',-69]
            if len(array) > i+1:
                values2 = array[i+1].split(',')
                username2 = self.uuidToUsername(values2[0])
            username = self.uuidToUsername(values[0])
            winstreak = values[1]
            if username == 'Minimum':
                string = f'{string}*{username} - {winstreak}*\n'
            elif values[1] == values2[1] and username2 != 'Minimum':
                string = f'{string}{count}. `{username}` & `{username2}` - {winstreak}\n'
                array.pop(i+1)
                if len(array) < UpTo:
                    UpTo -= 1
            else:
                string = f'{string}{count}. `{username}` - {winstreak}\n'
            count += 1
            i += 1
        return string
    
    #Commands
    @commands.command(name="UpdateLeaderboard", 
                      descripition="Updates the leaderboard", 
                      aliases=["UpdLdb","LdbUpd"])
    @commands.has_role("Guild Staff")
    async def UpdateLeaderboard(self, ctx):
        channel = self.bot.get_channel(836258539806654544)
        await channel.purge(limit=10)
        overall = self.readCSV("leaderboard_overall.csv")
        solos = self.readCSV("leaderboard_solos.csv")
        doubles = self.readCSV("leaderboard_doubles.csv")
        threes = self.readCSV("leaderboard_threes.csv")
        fours = self.readCSV("leaderboard_fours.csv")
        fourVSfour = self.readCSV("leaderboard_4v4.csv")
        await channel.send(f'**Overall Winstreak**\n{self.ArrayToString(overall)}')
        await channel.send(f'**Solo Winstreak**\n{self.ArrayToString(solos)}')
        await channel.send(f'**Doubles Winstreak**\n{self.ArrayToString(doubles)}')
        await channel.send(f'**3s Winstreak**\n{self.ArrayToString(threes)}')
        await channel.send(f'**4s Winstreak**\n{self.ArrayToString(fours)}')
        await channel.send(f'**4v4 Winstreak**\n{self.ArrayToString(fourVSfour)}')
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
#             await self.UpdateLeaderboard(ctx)
        else:
            await ctx.send("Command Failed")

    @commands.command(name="LeaderboardRemove", 
                      descripition="Add a winstreak to any leaderboard", 
                      aliases=["LdbDel","DelLdb","LdbRem","RemLdb"])
    @commands.has_role("Guild Staff")
    async def LeaderboardRemove(self, ctx, mode, ign):
        mode = mode.lower()
        nameS3 = "Error"
        if mode == "all":
            nameS3 = [self.overallS3, 
                      self.solosS3, 
                      self.doublesS3, 
                      self.threesS3, 
                      self.foursS3, 
                      self.fourVSfourS3]
            leaderboardFile = ["leaderboard_overall.csv", 
                               "leaderboard_solos.csv", 
                               "leaderboard_doubles.csv", 
                               "leaderboard_threes.csv", 
                               "leaderboard_fours.csv", 
                               "leaderboard_4v4.csv"]
        elif mode == "overall":
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
#             await self.UpdateLeaderboard(ctx)
        else:
            await ctx.send("Command Failed")

            

def setup(bot):
    bot.add_cog(leaderboards(bot))
