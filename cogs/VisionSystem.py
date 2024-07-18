import disnake
from disnake.ext import commands
import config
import aiohttp
from io import BytesIO


inf = {}

class NextButton(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @disnake.ui.button(label="Следующий шаг", style=disnake.ButtonStyle.green, custom_id="NextButton")
    async def NextB(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        if inf.get(interaction.author.id) == None:
            await interaction.send("Ошибка, начните заново!", ephemeral=True)
            return
        await interaction.response.send_modal(NextModal())


class NextModal(disnake.ui.Modal):
    def __init__(self):
        components = [
            disnake.ui.TextInput(label="Уровень прокачки подвески:", placeholder="Введите уровень прокачки подвески ", custom_id="pendants"),
            disnake.ui.TextInput(label="Есть ли турбонаддув?", placeholder="Да/Нет", custom_id="turbo"),
            disnake.ui.TextInput(label="Чипы: ", placeholder="Введите все ваши чипы", custom_id="chip")
        ]
        super().__init__(title="Опубликовать машину", components=components, custom_id="PublicNextAuto")

    async def callback(self, interaction: disnake.ModalInteraction) -> None:
        global inf
        nameAuto: str = inf.get(interaction.author.id).get("NameAuto")
        url = inf.get(interaction.author.id).get("url")
        Engine = inf.get(interaction.author.id).get("Engine")
        Transmissions = inf.get(interaction.author.id).get("Transmissions")
        breakes = inf.get(interaction.author.id).get("breakes")
        pendants = interaction.text_values["pendants"]
        turbo = interaction.text_values["turbo"]
        chip = interaction.text_values["chip"]

        embed = disnake.Embed(color=0x2F3136)
        embed.set_author(name=interaction.author.name, icon_url=interaction.author.avatar.url)
        embed.description = f'''{interaction.author.mention}
        ▬▬▬▬▬▬▬▬▬▬▬~ஜ۩۞۩ஜ~▬▬▬▬▬▬▬▬▬▬▬▬▬▬
        **{nameAuto}**
        
        Уровень прокачки двигателя: {Engine}
        Уровень прокачки трансмиссии: {Transmissions}
        Уровень прокачки тормозов: {breakes}
        Уровень прокачки подвески: {pendants}
        Есть ли турбонаддув: {turbo}
        Чипы: {chip}'''
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    image_bytes = await resp.read()
                    image_file = BytesIO(image_bytes)
                    file = disnake.File(image_file, filename=f"image.png")
                    embed.set_image(file=file)
                    channel = interaction.guild.get_channel(1186046754228015124)
                    await channel.send(embed=embed)
                    await interaction.send("Удачно!", ephemeral=True)
                else:
                    await interaction.send("Не удалось загрузить изображение", ephemeral=True)
        del inf[interaction.author.id]


class Modal(disnake.ui.Modal):
    def __init__(self):
        components = [
            disnake.ui.TextInput(label="Название машины:", placeholder='Введите название машины', custom_id="NameAuto"),
            disnake.ui.TextInput(label="Введите ссылку на фото машину:", placeholder="ссылка", custom_id="url"),
            disnake.ui.TextInput(label="Уровень прокачки двигателя:", placeholder="Введите уровень прокачки двигателя", custom_id="Engine"),
            disnake.ui.TextInput(label="Уровень прокачки трансмиссии:", placeholder="Введите уровень прокачки трансмиссии", custom_id="Transmissions"),
            disnake.ui.TextInput(label="Уровень прокачки тормозов:", placeholder="Введите уровень прокачки Тормозов", custom_id="breakes"),
        ]
        super().__init__(title="Опубликовать машину",components=components, custom_id="PublicAuto")

    async def callback(self, interaction: disnake.ModalInteraction) -> None:
        global inf
        nameAuto: str = interaction.text_values["NameAuto"]
        url = interaction.text_values["url"]
        Engine = interaction.text_values["Engine"]
        Transmissions = interaction.text_values["Transmissions"]
        breakes = interaction.text_values["breakes"]
        inf[interaction.author.id] = {"NameAuto": nameAuto, "url": url, "Engine":Engine, "Transmissions": Transmissions, "breakes":breakes}
        # pendants = interaction.text_values["pendants"]
        # turbo = interaction.text_values["turbo"]

        await interaction.send("Перейдите к следующему шагу", view=NextButton(), ephemeral=True)


class View(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @disnake.ui.button(label="🚗Опубликовать машину", style=disnake.ButtonStyle.danger, custom_id="PublicAuto")
    async def VisionButton(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        global inf
        if inf.get(interaction.author.id) == None:
            await interaction.response.send_modal(Modal())
            return
        await interaction.send("Перейдите к следующему шагу", view=NextButton(), ephemeral=True)





class VisionSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def send_vision(self, iteraction: disnake.CommandInteraction):
        if iteraction.author.id in config.Admin_id:
            embed = disnake.Embed(color=0x2F3136)
            embed.set_author(name="Выставить машину:")
            embed.description = '''▬▬▬▬▬▬▬▬▬▬▬~ஜ۩۞۩ஜ~▬▬▬▬▬▬▬▬▬▬▬▬▬▬
            Я здесь, чтобы помочь вам опубликовать вашу машину на выставке. 
            Нажмите на кнопку 'Опубликовать машину' ниже этого сообщения, чтобы предоставить информацию о вашем автомобиле для участия в выставке. 
            Это шанс привлечь внимание и показать ваш проект миру. 
            Спасибо за участие!'''

            view = View()

            await iteraction.send(embed=embed, view=view)

    @commands.Cog.listener()
    async def on_connect(self):
        self.bot.add_view(View(), message_id=1187883386908442715)

def setup(bot):
    bot.add_cog(VisionSystem(bot))
