import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext



class help(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="help",
                      description="Displays the help menu")
    async def help(self, ctx):
        role = discord.utils.get(ctx.guild.roles, name="Guild Staff")
        embed = discord.Embed(
            title = 'Command List',
            colour = discord.Colour.dark_theme(),
            type='article')

        embed.set_author(name='Carrot Bot', 
                         icon_url='https://images-ext-1.discordapp.net/external/NpXCm8rHLPUP0jk-lrskAJPwGDF-LIZ-Kq6SQ6lO5EQ/%3Fsize%3D256/https/cdn.discordapp.com/avatars/825359434602512388/c884bc5b69225f2319af41207a62c5d9.png')
        embed.add_field(name='Command \nhelp \ndaboiz \nwhoop \nGuildJoin', 
                        value='⠀', 
                        inline=True)
        embed.add_field(name='Description', 
                        value='Sends this message \n Pings da boiz.\nPings you, with funky message attached. \nCreate an embed to join the guild', 
                        inline=True)
        embed.add_field(name='Paramaters', 
                            value='None \nMessage (no @) \nNone \nIGN / Aliases / Age / Discovered Guild (Include / and if None type None).',
                            inline=True)
        if role in ctx.author.roles:
            embed.add_field(name='⠀', 
                            value='⠀', 
                            inline=True)
            embed.add_field(name='⠀', 
                            value='⠀', 
                            inline=False)
            embed.add_field(name='Staff Commands \nVCBlock \nVCUnblock \nLeaderboardAdd \nLeaderboardRemove', 
                            value='⠀', inline=True)
            embed.add_field(name='Description', 
                            value='Will VC Block Someone \nWill VC Unblock Someone \nWill add someone to the leaderboard \n Will remove someone from the leaderboard', 
                            inline=True)
            embed.add_field(name='Paramaters', 
                            value='User \nUser \nMode | Ign | Winstreak \nMode | Ign',
                            inline=True)

        await ctx.send(embed=embed)

    @cog_ext.cog_slash(name="help", 
                       description="Displays the help menu")
    async def helpSlash(self, ctx: SlashContext):
        role = discord.utils.get(ctx.guild.roles, name="Guild Staff")
        embed = discord.Embed(
            title = 'Command List',
            colour = discord.Colour.dark_theme(),
            type='article')

        embed.set_author(name='Carrot Bot', 
                         icon_url='https://images-ext-1.discordapp.net/external/NpXCm8rHLPUP0jk-lrskAJPwGDF-LIZ-Kq6SQ6lO5EQ/%3Fsize%3D256/https/cdn.discordapp.com/avatars/825359434602512388/c884bc5b69225f2319af41207a62c5d9.png')
        embed.add_field(name='Command \nhelp \ndaboiz \nwhoop', 
                        value='⠀', 
                        inline=True)
        embed.add_field(name='Description', 
                        value='Sends this message \n Pings da boiz.\nPings you, with funky message attached.', 
                        inline=True)
        if role in ctx.author.roles:
            embed.add_field(name='⠀', 
                            value='⠀', 
                            inline=True)
            embed.add_field(name='⠀', 
                            value='⠀', 
                            inline=False)
            embed.add_field(name='Staff Commands \nVCBlock \nVCUnblock \nLeaderboardAdd \nLeaderboardRemove', 
                            value='⠀', inline=True)
            embed.add_field(name='Description', 
                            value='Will VC Block Someone \nWill VC Unblock Someone \nWill add someone to the leaderboard \n Will remove someone from the leaderboard', 
                            inline=True)
            embed.add_field(name='Paramaters', 
                            value='User \nUser \nMode | Ign | Winstreak \nMode | Ign',
                            inline=True)

        await ctx.send(embed=embed) 

def setup(bot):
    bot.add_cog(help(bot))
