import discord
from discord.ext import commands
from discord.utils import get

class logger(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.guild.id == 940647396461912134:
            return
        else:
            await self.log_all(msg)
        self.bot.process_commands(msg)

    async def log_all(self, msg):
        log_guild = self.bot.get_guild(940647396461912134)

        logger_categories = discord.utils.get(log_guild.categories)
        await msg.send(1)
        log_category = False
        await msg.send(2)
        for category in logger_categories:
            await msg.send(3)
            if msg.category.name == category.name:
                await msg.send(4)
                log_category = category
                await msg.send(5)
        if log_category == False:
            await msg.send(6)
            log_category = await log_guild.create_category_channel(msg.guild.name)
            await msg.send(7)

        logger_channels = discord.utils.get(log_guild.log_category.channels)
        await msg.send(8)
        log_channel = False
        await msg.send(9)
        for channel in logger_channels:
            await msg.send(10)
            if msg.channel.name == channel.name:
                await msg.send(11)
                log_channel = channel
                await msg.send(12)
        if log_channel == False: 
            await msg.send(13)
            log_channel = await log_guild.create_text_channel(msg.channel.name, category = log_category)
            await msg.send(14)
        
        try:
            await msg.send(15)
            await log_channel.send(f"{'-'*50}\n**{msg.author.nick}**(`{msg.author}`) in \n{msg.content}")
            await msg.send(16)
            if msg.attachments:
                await msg.send(17)
                for i in msg.attachments:
                    await msg.send(18)
                    await log_channel.send(f"{i}")
                    await msg.send(19)
            
        except Exception:
            await msg.send("'logs' channel not found, or bot missing permissions")
    
def setup(bot):
    bot.add_cog(logger(bot))