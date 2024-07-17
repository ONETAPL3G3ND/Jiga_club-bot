import disnake
from disnake.ext import commands
import os

import config

intents = disnake.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents, test_guilds=[1186031118554767400])

@bot.event
async def on_ready():
    print("[LOG] bot is ready")

for file in os.listdir("./cogs"):
    if file.endswith(".py"):
        bot.load_extension(f"cogs.{file[:-3]}")

bot.run(config.TOKEN)