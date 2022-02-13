import discord
from discord.ext import commands
from discord.utils import get



class VCBlocking(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
 
    #VCBlock
    @commands.command(name="VCBlock", 
                      descripition="Will VCBlock Someone")
    @commands.has_role("Guild Staff")
    async def VCBlock(self, ctx, user: discord.Member):
        role = get(ctx.guild.roles, name="VC Channel Blocked")
        await user.add_roles(role)
        await ctx.send(f"{user.mention} has been VC Channel Blocked")

    #VCUnblock
    @commands.command(name="VCUnblock", descripition="Will VCUnblock Someone")
    @commands.has_role("Guild Staff")
    async def VCUnblock(self, ctx, user: discord.Member):
        role = get(ctx.guild.roles, name="VC Channel Blocked")
        await user.remove_roles(role)
        await ctx.send(f"{user.mention} has been VC Channel Unblocked")

def setup(bot):
    bot.add_cog(VCBlocking(bot))