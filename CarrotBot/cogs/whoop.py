import discord
from discord import guild
from discord.ext import commands
from discord_slash import cog_ext, SlashContext



class whoop(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="Whoop", 
                      description="This will ping you!")
    async def Whoop(self, ctx, *message):
        await ctx.send(ctx.author.mention + " WHOOP!")

    @cog_ext.cog_slash(name="Whoop", 
                       description="This will ping you! test woo",)
    async def WhoopSlash(self, ctx: SlashContext):
        await ctx.send(ctx.author.mention + " WHOOP!")

def setup(bot):
    bot.add_cog(whoop(bot))