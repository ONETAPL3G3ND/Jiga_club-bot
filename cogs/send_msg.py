import disnake
from disnake.ext import commands
import config

class Send_msg(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def send_msg(self, iteraction: disnake.CommandInteraction):
        if iteraction.author.id in config.Admin_id:
            await iteraction.response.send_message(".")

def setup(bot):
    bot.add_cog(Send_msg(bot))