import discord
from discord.ext import commands
from discord.utils import get

CHANNEL_ID = 918550313693245470
ROLE_ID = 759257697954037790 #Public member


class GuildJoin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="GuildJoin", 
                      descripition="Request to join the guild")
    async def GuildJoin(self, ctx, *message):
        role = get(ctx.guild.roles, id=ROLE_ID)
        if not role in ctx.author.roles:
            await ctx.send(f'{ctx.author.mention} You must be a Public Member to do this. If you think you are, please do !verify (ign) to rectify this issue.')
            return
        for i in range(0, len(message)):
            for j in range(0, len(message[i])):
                if message[i][j] == "@":
                    await ctx.send(f'{ctx.author.mention} You may not use an @ in your message.')
                    return
        message = " ".join(message)
        messages = message.split('/')
        try:
            x = messages[4]
        except:
            await ctx.send(f"{ctx.author.mention} You must seperate arguments with a '/'.")
            await CTX.send("Please also make sure you have all 5 categories, ign, aliases, age, discovered guild, and about you.")
            return
        embed = discord.Embed(
            title = f'IGN: {messages[0]}',
            colour = discord.Colour.blurple(),
            type='article')
        
        embed.set_author(name='Carrot Bot', 
                         icon_url='https://images-ext-1.discordapp.net/external/NpXCm8rHLPUP0jk-lrskAJPwGDF-LIZ-Kq6SQ6lO5EQ/%3Fsize%3D256/https/cdn.discordapp.com/avatars/825359434602512388/c884bc5b69225f2319af41207a62c5d9.png')
        embed.add_field(name='Aliases:', 
                        value=f"{messages[1]}",
                        inline=False)
        embed.add_field(name='Age:', 
                        value=f"{messages[2]}",
                        inline=False)
        embed.add_field(name='Discovered guild:', 
                        value=f"{messages[3]}"),
                        inline=False)
        embed.add_field(name='About me:', 
                        value=f"{messages[4]}"),
                        inline=False)
        CHANNEL = self.bot.get_channel(CHANNEL_ID)
        await CHANNEL.send(ctx.author.mention)
        msg = await CHANNEL.send(embed=embed)
        emoji1 = get(ctx.guild.emojis, name="agree")
        emoji2 = get(ctx.guild.emojis, name="disagree")
        await msg.add_reaction(emoji1)
        await msg.add_reaction(emoji2)
        #await msg.add_reaction("<:agree:962855687103344690>")
        #await msg.add_reaction("<:disagree:962855799602970687>")

def setup(bot):
    bot.add_cog(GuildJoin(bot))

# @commands.has_role("Guild Staff")
