import boto3
import discord
import json
import os
from discord.ext import commands
from discord_slash import SlashCommand
from dotenv import load_dotenv

def create_bot():

    #Variables For get_prefix
    load_dotenv() # Will load environment variables from a .env file
    ACCESS_ID = os.getenv("ACCESS_ID")
    ACCESS_KEY = os.getenv("ACCESS_KEY")
    REGION = os.getenv("REGION")
    s3_resource = boto3.resource('s3', aws_access_key_id=ACCESS_ID, aws_secret_access_key=ACCESS_KEY, region_name=REGION)
    prefixes = s3_resource.Object('carrotbotprefixes', 'prefixes.json')
    s3_resource.Object('carrotbotprefixes', 'prefixes.json').download_file('prefixes.json')
    
    #Define prefix for given server
    def get_prefix(client, message):
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)
        return prefixes[str(message.guild.id)]

    bot = commands.Bot(command_prefix=get_prefix, case_insensitive=True)

    #Remove Default Help Command
    bot.remove_command("help")

    #When Bot Is Ready
    @bot.event
    async def on_ready():
        await bot.change_presence(status=discord.Status.online, 
                                  activity=discord.Activity(type=discord.ActivityType.watching, 
                                                            name='&help'))
        print('Bot is ready')

    #Creat Slash Commands
    slash = SlashCommand(bot, sync_commands=True, override_type=True)

    #Load Cogs
    for filename in os.listdir('CarrotBot/cogs'):
        if filename.endswith('.py'):
            bot.load_extension(f'cogs.{filename[:-3]}')



    return bot