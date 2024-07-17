import time

import disnake
from disnake.ext import commands
import config
import asyncio

connect_id = []
time_start_g = ""
race_number_g = ""
prize = 0

class RaceModal(disnake.ui.Modal):
    def __init__(self, bot):
        self.bot = bot
        components = [disnake.ui.TextInput(label="Номер трассы:", placeholder="Введите номер трассы", custom_id="race_number"),
                      disnake.ui.TextInput(label="Призовой фонд:", placeholder="Введите призовой фонд", custom_id="prize_fund"),
                      disnake.ui.TextInput(label="Гонка начнеться:", placeholder="время | дата", custom_id="race_start"),
                      disnake.ui.TextInput(label="Регистрация закончиться:", placeholder="время | дата", custom_id="reg_finish")]
        super().__init__(title="Создать гонку:", components=components, custom_id="RaceModal")
    async def callback(self, interaction: disnake.ModalInteraction) -> None:
        global time_start_g
        global race_number_g
        global prize

        await interaction.response.defer()

        race_number = interaction.text_values["race_number"]
        prize_fund = interaction.text_values["prize_fund"]
        race_start = interaction.text_values["race_start"]
        reg_finish = interaction.text_values["reg_finish"]
        prize = prize_fund

        if interaction.author.id in config.Admin_id:
            time_start_g = race_start
            race_number_g = race_number
            view = ButtonView()
            embed = disnake.Embed(color=0x2F3136)
            embed.set_author(name="Вступить в гонку:")
            embed.description = f'''▬▬▬▬▬▬▬▬▬▬▬~ஜ۩۞۩ஜ~▬▬▬▬▬▬▬▬▬▬▬▬▬▬
        Добро пожаловать на грандиозную гонку! Сегодня нас ждет захватывающее соревнование на трассе № {race_number}. Невероятные скорости, острые повороты и невероятные эмоции - все это ждет наших гонщиков!

        Гонка начнется в {race_start}. Регистрация продлится до {reg_finish}. Поторопитесь, чтобы принять участие в этом захватывающем спортивном событии!

        Призовой фонд этой увлекательной гонки составляет {prize_fund}$. За победу борются не только за звание лучшего гонщика, но и за значительные денежные награды!

        Готовы ли вы почувствовать адреналин и стать частью этой захватывающей гонки? Пускай лучший выиграет!'''
            channel = interaction.guild.get_channel(config.channel_race_reg)
            msg = await channel.send(embed=embed, view=view)

            config.race_message = msg.id

            view = ButtonAdminView(self.bot)
            embed = disnake.Embed(color=0x2F3136)
            embed.set_author(name="Вступить в гонку:")
            embed.description = f'''▬▬▬▬▬▬▬▬▬▬▬~ஜ۩۞۩ஜ~▬▬▬▬▬▬▬▬▬▬▬▬▬▬
                    Добро пожаловать на грандиозную гонку! Сегодня нас ждет захватывающее соревнование на трассе № {race_number}. Невероятные скорости, острые повороты и невероятные эмоции - все это ждет наших гонщиков!

                    Гонка начнется в {race_start}. Регистрация продлится до {reg_finish}. Поторопитесь, чтобы принять участие в этом захватывающем спортивном событии!

                    Призовой фонд этой увлекательной гонки составляет {prize_fund}$. За победу борются не только за звание лучшего гонщика, но и за значительные денежные награды!

                    Готовы ли вы почувствовать адреналин и стать частью этой захватывающей гонки? Пускай лучший выиграет!'''

            channel = interaction.guild.get_channel(config.channel_admin_panel)
            msg = await channel.send(embed=embed, view=view)

            config.race_admin_massage = msg.id

class GiveModal(disnake.ui.Modal):
    def __init__(self):
        components = [disnake.ui.TextInput(label="Айди победителя:", placeholder="Введите айди победителя", custom_id="winner_id"),
                      disnake.ui.TextInput(label="Призовой фонд:", placeholder="Введите призовой фонд", custom_id="prize_fund"),]
        super().__init__(title="Выдать победу:", components=components, custom_id="RaceModal")
    async def callback(self, interaction: disnake.ModalInteraction) -> None:
        global time_start_g
        global race_number_g

        await interaction.response.defer()

        winner_id = interaction.text_values["winner_id"]
        prize_fund = interaction.text_values["prize_fund"]


        if interaction.author.id in config.Admin_id:
            embed = disnake.Embed(color=0x2F3136)
            embed.set_author(name="Итоги набора:")
            embed.description = f'''▬▬▬▬▬▬▬▬▬▬▬~ஜ۩۞۩ஜ~▬▬▬▬▬▬▬▬▬▬▬▬▬▬
Дорогие гонщики и болельщики!

С огромной радостью объявляем победителя нашей захватывающей гонки! Поздравляем <@{winner_id}> с захватывающей победой! Его умение, мастерство и решимость принесли ему заслуженную победу!

Этот день принадлежит <@{winner_id}>! Его упорство и отличные навыки сделали его лидером этой гонки, а его имя войдет в историю нашего соревнования.

<@{winner_id}>, вам теперь принадлежит гордое звание лучшего гонщика нашего события! Ваше мастерство было вознаграждено призовым фондом в размере {prize_fund}$. Поздравляем вас с этим заслуженным успехом!

Спасибо всем участникам за участие и борьбу на трассе! Надеемся увидеть вас снова на следующих соревнованиях!

Пусть этот день будет запомнен как день вашей победы, <@{winner_id}>! Поздравляем вас с этим замечательным достижением!

Для получения приза, пожалуйста, напишите <@896846570018967602> или <@722502474715627590>'''
            channel = interaction.guild.get_channel(config.channel_race_info)
            await channel.purge(limit=100)
            await channel.send(embed=embed)

class ButtonView(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @disnake.ui.button(label="👴Вступить в гонку", style=disnake.ButtonStyle.green, custom_id="applicationsRace")
    async def applicationsRaceButton(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        global connect_id
        await interaction.response.defer()
        if interaction.author.id not in connect_id:
            connect_id.append(interaction.author.id)
            channel = interaction.guild.get_channel(config.channel_race_info)
            await channel.send(f"<@{interaction.author.id}> присоединился к гонке!")
        else:
            await interaction.send("Ты уже участвуешь в гонке!", ephemeral=True)
class ButtonAdminView(disnake.ui.View):
    def __init__(self, bot):
        self.bot = bot
        super().__init__(timeout=None)

    @disnake.ui.button(label="❌Закончить набор", style=disnake.ButtonStyle.green, custom_id="applications_end")
    async def applicationsButton(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        if interaction.author.id in config.Admin_id:
            global connect_id

            channel = interaction.guild.get_channel(config.channel_admin_panel)
            await channel.purge(limit=100)
            channel = interaction.guild.get_channel(config.channel_race_reg)
            await channel.purge(limit=100)
            channel = interaction.guild.get_channel(config.channel_race_info)
            await channel.purge(limit=100)
            text = ""
            for item in connect_id:
                text += f"\n<@{item}> Участвует в гонке!"
            embed = disnake.Embed(color=0x2F3136)
            embed.set_author(name="Итоги набора:")
            embed.description = f'''▬▬▬▬▬▬▬▬▬▬▬~ஜ۩۞۩ஜ~▬▬▬▬▬▬▬▬▬▬▬▬▬▬
    Уважаемые участники гонки!
    
    Регистрация на нашу захватывающую гонку завершена. Спасибо всем, кто проявил интерес и зарегистрировался! Вот список участников, готовых сразиться за победу на трассе:
    {text}
    
    И это только часть нашей захватывающей гонки! С нетерпением ждем начала соревнований, которые пройдут в {time_start_g} на трассе № {race_number_g}.
    
    Желаем удачи всем участникам и пусть победит сильнейший'''
            await channel.send(embed=embed)
            options = [
                disnake.SelectOption(label=(await self.bot.get_guild(config.guild_ids[0]).fetch_member(i)).name,
                                     value=str(i))
                for i in connect_id]
            view = disnake.ui.View(timeout=None)
            view.add_item(UserSelector(options=options))
            await interaction.send("Выбери победителя", view=view)


class UserSelector(disnake.ui.Select):
    def __init__(self, options):
        print(options)
        super().__init__(placeholder="Выбери победителя", options=options, custom_id="Winner", min_values=0, max_values=len(options))


    async def callback(self, interaction: disnake.MessageInteraction):
        if interaction.values:
            global time_start_g
            global race_number_g
            global prize
            await interaction.response.defer()

            winner_id = interaction.values[0]
            prize_fund = prize

            if interaction.author.id in config.Admin_id:
                embed = disnake.Embed(color=0x2F3136)
                embed.set_author(name="Итоги набора:")
                embed.description = f'''▬▬▬▬▬▬▬▬▬▬▬~ஜ۩۞۩ஜ~▬▬▬▬▬▬▬▬▬▬▬▬▬▬
            Дорогие гонщики и болельщики!

            С огромной радостью объявляем победителя нашей захватывающей гонки! Поздравляем <@{winner_id}> с захватывающей победой! Его умение, мастерство и решимость принесли ему заслуженную победу!

            Этот день принадлежит <@{winner_id}>! Его упорство и отличные навыки сделали его лидером этой гонки, а его имя войдет в историю нашего соревнования.

            <@{winner_id}>, вам теперь принадлежит гордое звание лучшего гонщика нашего события! Ваше мастерство было вознаграждено призовым фондом в размере {prize_fund}$. Поздравляем вас с этим заслуженным успехом!

            Спасибо всем участникам за участие и борьбу на трассе! Надеемся увидеть вас снова на следующих соревнованиях!

            Пусть этот день будет запомнен как день вашей победы, <@{winner_id}>! Поздравляем вас с этим замечательным достижением!

            Для получения приза, пожалуйста, напишите <@896846570018967602> или <@722502474715627590>'''
                channel = interaction.guild.get_channel(config.channel_race_info)
                await channel.purge(limit=100)
                await channel.send(embed=embed)
                channel = interaction.guild.get_channel(config.channel_admin_panel)
                await channel.purge(limit=100)



class RaceApplications(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="Запуск гонки")
    async def start_race(self, interaction):
        global time_start_g
        global race_number_g


        if interaction.author.id in config.Admin_id:
            await interaction.response.send_modal(RaceModal(self.bot))

    @commands.slash_command(description="Выбрать победителя")
    async def stop_race(self, interaction):
        if interaction.author.id in config.Admin_id:
            await interaction.response.send_modal(GiveModal())









def setup(bot):
    bot.add_cog(RaceApplications(bot))