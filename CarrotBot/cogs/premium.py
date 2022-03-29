import discord
from discord.ext import commands
from discord.utils import get




class PremiumTickets(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
 
    #VCBlock
    @commands.command(name="premium", 
                      descripition="Make a vote for premium")
    async def premium(self, ctx, user: discord.Member, *message):
        for i in range(0, len(message)):
            for j in range(0, len(message[i])):
                if message[i][j] == "@":
                    await ctx.send(f'{ctx.author.mention} You may not use an @ in your message.')
                    return
        embed = discord.Embed(
            title = 'Command List',
            colour = discord.Colour.dark_theme(),
            type='article')

        embed.set_author(name='Carrot Bot', 
                         icon_url='https://images-ext-1.discordapp.net/external/NpXCm8rHLPUP0jk-lrskAJPwGDF-LIZ-Kq6SQ6lO5EQ/%3Fsize%3D256/https/cdn.discordapp.com/avatars/825359434602512388/c884bc5b69225f2319af41207a62c5d9.png')
        embed.add_field(name=f'@{user.name}', 
                        value=" ".join(message))
        CHANNEL = self.bot.get_channel(958491773825585172)
        msg = await CHANNEL.send(embed=embed)
        await msg.add_reaction(self.bot.get_emoji(958509779918151690))
        await msg.add_reaction(self.bot.get_emoji(958509815259332608))

def setup(bot):
    bot.add_cog(PremiumTickets(bot))

# @commands.has_role("Guild Staff")