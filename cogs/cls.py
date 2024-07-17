from disnake.ext import commands
import asyncio
import config

class Cls(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def cls(self, iteraction, amount: int):
        if iteraction.author.id in config.Admin_id:
            await iteraction.channel.purge(limit=amount + 1)
            await iteraction.response.send_message(f"Удалено {amount} собщений", ephemeral=True)
def setup(bot):
    bot.add_cog(Cls(bot))