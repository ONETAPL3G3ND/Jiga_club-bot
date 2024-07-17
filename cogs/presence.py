import disnake
from disnake.ext import commands
import config

class presence(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_connect(self):
        await self.bot.change_presence(status=disnake.Status.online, activity=disnake.Game("Хасанит на шахе"))

def setup(bot):
    bot.add_cog(presence(bot))