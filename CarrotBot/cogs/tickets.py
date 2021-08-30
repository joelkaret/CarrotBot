import discord
import os
import boto3
import json
from dotenv import load_dotenv
from discord import channel
from discord.ext import commands



class tickets(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    load_dotenv() # Will load environment variables from a .env file
    ACCESS_ID = os.getenv("ACCESS_ID")
    ACCESS_KEY = os.getenv("ACCESS_KEY")
    REGION = os.getenv("REGION")
    s3_resource = boto3.resource('s3', aws_access_key_id=ACCESS_ID, aws_secret_access_key=ACCESS_KEY, region_name=REGION)
    prefixFile = s3_resource.Object('carrottickets', 'tickets.json')
    s3_resource.Object('carrottickets', 'tickets.json').download_file('tickets.json')

    @commands.has_role("Guild Staff")
    @commands.command(name="CreateTicketStart", 
                      description="Adds the original Ticket")
    async def CreateTicketStart(self, ctx):
        embed = discord.Embed(
            title = 'Skillless Support',
            colour = discord.Colour.darker_gray(),
            type='article')

        embed.set_author(name='Skillless Support', 
                         icon_url='https://cdn.discordapp.com/icons/713646548436910116/a_272362c28065387d2cda1c55139d9f80.gif?size=128')
        embed.add_field(name='React with <:Skillless:764176281628704798> to create a ticket', 
                        value='⠀', 
                        inline=False)
        embed.add_field(name='Reasons to make a ticket', 
                        value='Deserve a Role (eg. veteran)\nReport someone\nRequire assistance/specific questions\nFor nitro booster roles, state the name and the hex code.', 
                        inline=False)
        ticket = await ctx.send(embed=embed)
        await ticket.add_reaction('<:Skillless:764176281628704798>')

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        channel = self.bot.get_channel(835942212188897343)
        reaction_message = await self.bot.get_channel(836263057838702592).fetch_message(855919153092493372)
        if payload.message_id == reaction_message.id:
            await channel.send("hi")
        else:
            await channel.send((payload.user_id))


def setup(bot):
    bot.add_cog(tickets(bot))