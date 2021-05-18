import discord
from discord.ext import commands
from discord.utils import get
from discord_slash import cog_ext, SlashContext



class daboiz(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="daboiz", 
                      description="pings da boiz")
    @commands.has_role("da boiz")
    async def daboiz(self, ctx, *message):
        role = get(ctx.guild.roles, name="da boiz")
        allowed = True
        for i in range(0, len(message)):
            for j in range(0, len(message[i])):
                if message[i][j] == "@":
                    allowed = False
        if allowed:
            await ctx.send(f'{role.mention} {ctx.author.mention}  says {" ".join(message)}')
        else:
            await ctx.send(f'{ctx.author.mention} You may not use an @ in your message.')

def setup(bot):
    bot.add_cog(daboiz(bot))