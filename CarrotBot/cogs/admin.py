import os
import discord
from discord.ext import commands



class admin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    #Check
    async def is_me(ctx):
        return ctx.author.id == 506884005195677696 #MyID

    #Say
    @commands.command(name="Say", 
                      descripition="Carrot will say this.")
    @commands.check(is_me)
    async def Say(self, ctx, *message):
        await ctx.send(" ".join(message))

    #RulesEmbed
    @commands.command()
    @commands.check(is_me)
    async def RulesEmbed(self, ctx):
        embed = discord.Embed(
            title = 'Skillless Rules',
            colour = discord.Colour.dark_theme(),
            type='article')

        embed.set_author(name='Skillless Rules', 
                         icon_url='https://cdn.discordapp.com/icons/713646548436910116/a_272362c28065387d2cda1c55139d9f80.gif?size=128')
        embed.add_field(name='All punishment lengths/severity will be at staff members discretion', 
                        value='''NSFW Content is not allowed. Talking about NSFW topics may also be punished., 
Discrimination (including slurs) is not allowed. Instant 3 day mute mininum.
Hate Symbols/Speech is not allowed. 
KYS comments, in any regard, is not allowed.
Flame wars and other harsh comments are not allowed. Take arguments to dms.
Political discussion is not allowed.
Drama to do with the guild is not allowed. This can be punished no matter where it took place. 
Advertising is only allowed in #media. Excessive advertising may still be punished.
Creepy or sexualising remarks to anybody, without their consent, is not allowed.
Please speak primarily English. It's fine if you speak another language a little, but it's impossible for us to moderate all languages, and it also makes it easier for other people to join in.''', 
                        inline=False)
        embed.add_field(name='These will result in severe punishments, including blacklisting and banning.', 
                        value='''Impersonation of staff.
Alting, both accounts may be banned. 
Evading punishment.
Doxxing/Threatening to doxx.''', 
                        inline=False)
        embed.add_field(name='To Clarify On Some Rules',
                        value='''Jokes do not guarentee exemption from mutes.
Some jokes may be punished more heavily than others.

You are allowed to have civil discussions about certain topics, but flamewars will be punished.
Spreading Misinformation Is Discouraged.

If you want to say a joke that can be seen as discriminatory, think about how others will read it, if it's actually funny, if it is clearly intended as a joke, and if it could be crossing the line. That decision is up to you, but if a staff member deems that it has crossed the line, you'll be muted and you can't complain. Remember that this is a minecraft discord server, and although we all find certain jokes funny, the bar will be lower than that of in a personal friend group.''',
                        inline=False)
        embed.add_field(name='⠀',
                        value='''Any N Word, F Slur (Not Fuck, The Other One), No Matter The Context, Will Result In An Instant Mute.

Using "Gay" As An Insult Will Result In A 1 day warn.

Eg1. "Oh Freddie Mercury From Queen Was Gay" (Although He Was Actually Bi)
 - Not a mute
Eg2. "Hypixel Is Sooo Gay Man, All These Lagbacks Are Soo Gay"
 - mute

Don't sexually harass anyone. We all have in jokes, and find making comic sex jokes about each other, but don't do it to someone you just met, or if they ask you to stop.''',
                        inline=False)
        embed.add_field(name='Extra important info',
                        value='''If You Believe That A Staff Member Is Abusing Their Admin Privileges, Contact Owenator#8710
If you do something stupid, that isn't in the rules, a staff member can still warn/mute/ban you.''',
                        inline=False)


        await ctx.send(embed=embed)
    #Cogs
    @commands.command()
    @commands.check(is_me)
    async def load(self, ctx, extension):
        self.bot.load_extension(f'cogs.{extension}')

    @commands.command()
    @commands.check(is_me)
    async def unload(self, ctx, extension):
        self.bot.unload_extension(f'cogs.{extension}')

    @commands.command(name='Terminate', 
                      description='Ends All Cogs',
                      aliases=['end'])
    @commands.check(is_me)
    async def terminate(self, ctx):
        for filename in os.listdir('CarrotBot/cogs'):
            if filename.endswith('.py'):
                self.bot.unload_extension(f'cogs.{filename[:-3]}')

    @commands.command(name='reinstate',
                      description='Starts all Cogs',
                      aliases=['unterminate','start'])
    @commands.check(is_me)
    async def reinstate(self, ctx):
        for filename in os.listdir('CarrotBot/cogs'):
            if filename.endswith('.py'):
                self.bot.load_extension(f'cogs.{filename[:-3]}')

    @commands.command(name='purge',
                      description='Purge all',
                      aliases=['del'])
    @commands.check(is_me)
    async def purge(self, ctx, num = 1):
        num += 1
        await ctx.channel.purge(limit=num)
        
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.user_id != 506884005195677696:
            return
        if payload.emoji == '🏮':
            channel = self.bot.get_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            await payload.message.delete()
        

def setup(bot):
    bot.add_cog(admin(bot))
