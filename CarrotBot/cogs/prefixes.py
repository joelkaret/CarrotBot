import boto3
import json
import os
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from dotenv import load_dotenv



class Prefixes(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    load_dotenv() # Will load environment variables from a .env file
    ACCESS_ID = os.getenv("ACCESS_ID")
    ACCESS_KEY = os.getenv("ACCESS_KEY")
    REGION = os.getenv("REGION")
    s3_resource = boto3.resource('s3', aws_access_key_id=ACCESS_ID, aws_secret_access_key=ACCESS_KEY, region_name=REGION)
    prefixFile = s3_resource.Object('carrotbotprefixes', 'prefixes.json')
    s3_resource.Object('carrotbotprefixes', 'prefixes.json').download_file('prefixes.json')
    guild_ids=[634134183773732864,835942211635773472,713646548436910116]

    def get_prefix(client, message):
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)
        return prefixes[str(message.guild.id)]

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)
        prefixes[str(guild.id)] = '&'
        with open('prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)
        self.prefixFile.upload_file('prefixes.json')

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)
        prefixes.pop(str(guild.id))
        with open('prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)
        self.prefixFile.upload_file('prefixes.json')

    @commands.command(name='ChangePrefix',
                      description='Changes Prefix')
    async def changeprefix(self, ctx, prefix):
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)
        prefixes[str(ctx.guild.id)] = prefix
        with open('prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)
        self.prefixFile.upload_file('prefixes.json')
        await ctx.send("Prefix has been changed to " + prefix)        

def setup(bot):
    bot.add_cog(Prefixes(bot))