import os
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
                self.bot.unload_extension(f'cogs.{filename[:-3]}')
        


def setup(bot):
    bot.add_cog(admin(bot))