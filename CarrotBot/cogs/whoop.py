from discord.ext import commands
from discord_slash import cog_ext, SlashContext



class whoop(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    guild_ids=[634134183773732864,835942211635773472,713646548436910116]

    @commands.command(name="Whoop", 
                      description="This will ping you!")
    async def Whoop(self, ctx, *message):
        await ctx.send(ctx.author.mention + " WHOOP!")

    @cog_ext.cog_slash(name="Whoop", 
                       description="This will ping you! test woo",
                       guild_ids=guild_ids)
    async def WhoopSlash(self, ctx: SlashContext):
        await ctx.send(ctx.author.mention + " WHOOP!")

def setup(bot):
    bot.add_cog(whoop(bot))