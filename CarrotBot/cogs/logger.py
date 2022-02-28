import discord
from discord.ext import commands
from discord.utils import get
from sqlalchemy import null

class logger(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, msg):
#         await self.bot.process_commands(msg)
        if msg.guild.id == 940647396461912134:
            return
        else:
            await self.log_all(msg)

    async def log_all(self, msg):
        log_guild = self.bot.get_guild(940647396461912134)

        logger_categories = log_guild.categories
        log_category = False
        log_category_2 = False
        for categoryi in logger_categories:
            if msg.guild.name == categoryi.name:
                log_category = categoryi
            if f'{msg.guild.name} 2' == categoryi.name:
                log_category_2 = categoryi
        if log_category == False:
            log_category = await log_guild.create_category(msg.guild.name)

        if len(log_category.channels) > 49 and not log_category_2:
            await log_guild.create_category(f'{msg.guild.name} 2')

        logger_channels = log_category.channels
        log_channel = False
        log_channel_2 = False
        for channeli in logger_channels:
            if msg.channel.name == channeli.name:
                log_channel = channeli
        if log_channel == False: 
            if log_category_2 != False:
                logger_channels_2 = log_category_2.channels
                for channeli_2 in logger_channels_2:
                    if msg.channel.name == channeli_2.name:
                        log_channel_2 = channeli_2
                        log_channel = channeli_2
                if log_channel_2 == False:
                    log_channel = await log_guild.create_text_channel(msg.channel.name, category = log_category_2)
            else:
                log_channel = await log_guild.create_text_channel(msg.channel.name, category = log_category)
        
        try:
            user_mentions = msg.mentions
            role_mentions = msg.role_mentions
            channel_mentions = msg.channel_mentions
            content = str(msg.system_content)
            for i in user_mentions:
                pingmsg = f"<@!{i.id}>"
                content = content.replace(pingmsg, f'***Ping-User:{i.name}***')
            for i in role_mentions:
                pingmsg = f"<@&{i.id}>"
                content = content.replace(pingmsg, f'***Ping-Role:{i.name}***')
            for i in channel_mentions:
                pingmsg = f"<@#{i.id}>"
                content = content.replace(pingmsg, f'***Channel:{i.name}***')
            content = content.replace('@','***PING: EVERYONE***')
            if msg.reference:
                await log_channel.send(f"{'-'*50}\n```reply to {msg.reference.resolved.author}: {msg.reference.resolved.system_content}:```")
            else:
                await log_channel.send(f"{'-'*50}")
            try:
                await log_channel.send(f"**{msg.author.nick}**(`{msg.author}`)\n{content}")
            except:
                await log_channel.send(f"**No Nick**(`{msg.author}`)\n{content}")
            for i in msg.attachments:
                await log_channel.send(i)
            for i in msg.embeds:
                await log_channel.send(embed=i)
            
        except Exception as e:
            print(msg.system_content, msg.author)
            print("'logs' channel not found, or bot missing permissions")
            print(e)
    
def setup(bot):
    bot.add_cog(logger(bot))

