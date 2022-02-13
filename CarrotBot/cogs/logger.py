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
        loggerguild = self.bot.get_guild(940647396461912134)

        logger_categories = discord.utils.get(loggerguild.categories)
        log_category = False
        for category in logger_categories:
            if msg.category.name == category.name:
                log_category = category.name
        if not category:
            log_category = await loggerguild.create_category(category)

        logger_channels = discord.utils.get(loggerguild.logger_category.channels)
        log_channel = False
        for channel in logger_channels:
            if msg.channel.name == channel.name:
                log_channel = channel.name
        if log_channel: 
            log_channel = await loggerguild.create_text_channel(msg.channel.name, category = log_category)
        
        try:
            await log_channel.send(f"{'-'*50}\n**{msg.author.nick}**(`{msg.author}`) in \n{msg.content}")
            if msg.attachments:
                for i in msg.attachments:
                    await log_channel.send(f"{i}")
            
        except Exception:
            print("'logs' channel not found, or bot missing permissions")
    
def setup(bot):
    bot.add_cog(logger(bot))