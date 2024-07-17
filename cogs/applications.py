import disnake
from disnake.ext import commands
import config

class applicationsModal(disnake.ui.Modal):
    def __init__(self):
        components = [disnake.ui.TextInput(label="Ваш игровой ник:", placeholder="Введите ваш ник", custom_id="nickname"),
                      disnake.ui.TextInput(label="Ваш игровой лвл:", placeholder="Введите ваш лвл", custom_id="lvl"),
                      disnake.ui.TextInput(label="Готовы ли вы соблюдать правила клуба?", placeholder="Да/Нет", custom_id="gamerule"),
                      disnake.ui.TextInput(label="Ваша машина и ее тюнинг:", placeholder="Введите вашу марку машини и ее тюнинг", custom_id="auto")]
        super().__init__(title="Заявка в клуб", components=components, custom_id="applicationsModal")
    async def callback(self, interaction: disnake.ModalInteraction) -> None:
        nickname = interaction.text_values["nickname"]
        lvl = interaction.text_values["lvl"]
        gamerule = interaction.text_values["gamerule"]
        auto = interaction.text_values["auto"]
        categories = disnake.utils.get(interaction.guild.categories, id=config.categories_applications)
        guild = interaction.guild
        channel = await guild.create_text_channel(f"Заявка игрока {interaction.author.name}", category=categories)
        await channel.set_permissions(interaction.author, speak=False, send_messages=True, read_message_history=True,
                                      read_messages=True)
        await channel.send(interaction.author.mention)
        embed = disnake.Embed(color=0x2F3136)
        embed.set_author(name=f"Заявка в клуб, игрока: {nickname}")
        embed.description = f'''▬▬▬▬▬▬▬▬▬▬▬~ஜ۩۞۩ஜ~▬▬▬▬▬▬▬▬▬▬▬▬▬▬
Ваш игровой ник: {nickname}
Ваш игровой лвл: {lvl}
Готовы ли вы соблюдать правила клуба?: {gamerule}
Ваша машина и ее тюнинг: {auto}'''
        await channel.send(embed=embed)
        await interaction.send("Заявка создана!", ephemeral=True)

class ButtonView(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @disnake.ui.button(label="👴Подать заявку", style=disnake.ButtonStyle.green, custom_id="applications")
    async def applicationsButton(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        await interaction.response.send_modal(applicationsModal())


class ButtonsApplications(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.persistents_views_added = True
    @commands.command()
    async def applicationsSend(self, ctx):
        if ctx.author.id in config.Admin_id:
            view = ButtonView()
            embed = disnake.Embed(color=0x2F3136)
            embed.set_author(name="Заявка в клуб:")
            embed.description = f'''▬▬▬▬▬▬▬▬▬▬▬~ஜ۩۞۩ஜ~▬▬▬▬▬▬▬▬▬▬▬▬▬▬
        Привет, путник!
    Ты находишься в Жигули CLUB!
    Для вступления, тебе надо:
    1. Нажать кнопку ":older_man:Подать заявку"
    2. Оставить заявку
    3. Ожидать одобрения'''
            await ctx.send(embed=embed, view=view)

    @commands.Cog.listener()
    async def on_connect(self):
        self.bot.add_view(ButtonView(), message_id=1187049238715174942
                          )

def setup(bot):
    bot.add_cog(ButtonsApplications(bot))