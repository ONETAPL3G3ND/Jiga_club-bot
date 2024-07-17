from disnake.ext import commands
import disnake
import asyncio
import config

class applicationsAddRole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        channel: disnake.ChannelType = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        emoji = payload.emoji.name
        guild = self.bot.get_guild(payload.guild_id)


        if channel.category.name == "заявки в клуб":
            if payload.user_id in config.Admin_id:
                if emoji == "✅":
                    for member in channel.members:
                        if not member.bot:  # Проверяем, что это не бот
                            if len(member.roles) == 1:  # Если у пользователя нет ролей
                                role = guild.get_role(1186724019802738698)  # ID вашей роли
                                if role:
                                    await member.add_roles(role)
                                    embed = disnake.Embed(color=0x2F3136)
                                    embed.set_author(name="Приветствуем вас!")
                                    embed.description = f'''▬▬▬▬▬▬▬▬▬▬▬~ஜ۩۞۩ஜ~▬▬▬▬▬▬▬▬▬▬▬▬▬▬
                                    <@{member.id}> Приветствуем тебя в нашем клубе с открытыми объятиями! Мы рады приветствовать новых членов, и ты — важное дополнение к нашей команде.
    
    Ты играешь ключевую роль в нашем клубе. Твоя энергия и уникальные способности делают тебя незаменимым участником. Мы уверены, что ты отлично войдешь в роль "{role.name}"
    
    Твое присутствие и вклад ценны для нас. Мы настоятельно приглашаем тебя принимать участие в наших мероприятиях и дискуссиях, делиться своими идеями и исследованиями.
    
    Не стесняйся обращаться к любому из нас с вопросами или предложениями. Ты важен для нас, и мы хотим, чтобы ты почувствовался как дома в нашей дружной команде.
    
    Добро пожаловать в наш клуб! Мы уверены, что ты принесешь в него свежие идеи и энтузиазм.
    '''
                                    await channel.send(embed=embed)
                elif emoji == "🚘":
                    for member in channel.members:
                        if not member.bot:  # Проверяем, что это не бот
                            if len(member.roles) == 1:  # Если у пользователя нет ролей
                                role = guild.get_role(1186723921098186873)  # ID вашей роли
                                if role:
                                    await member.add_roles(role)
                                    embed = disnake.Embed(color=0x2F3136)
                                    embed.set_author(name="Приветствуем вас!")
                                    embed.description = f'''▬▬▬▬▬▬▬▬▬▬▬~ஜ۩۞۩ஜ~▬▬▬▬▬▬▬▬▬▬▬▬▬▬
                                    <@{member.id}> Приветствуем тебя в нашем клубе с открытыми объятиями! Мы рады приветствовать новых членов, и ты — важное дополнение к нашей команде.
    
    Ты играешь ключевую роль в нашем клубе. Твоя энергия и уникальные способности делают тебя незаменимым участником. Мы уверены, что ты отлично войдешь в роль "{role.name}"
    
    Твое присутствие и вклад ценны для нас. Мы настоятельно приглашаем тебя принимать участие в наших мероприятиях и дискуссиях, делиться своими идеями и исследованиями.
    
    Не стесняйся обращаться к любому из нас с вопросами или предложениями. Ты важен для нас, и мы хотим, чтобы ты почувствовался как дома в нашей дружной команде.
    
    Добро пожаловать в наш клуб! Мы уверены, что ты принесешь в него свежие идеи и энтузиазм.
    '''
                                    await channel.send(embed=embed)
                else:
                    print(emoji)


def setup(bot):
    bot.add_cog(applicationsAddRole(bot))