# discord imports
from code import compile_command
import discord
from discord import app_commands
from discord.ext import commands
# other imports
import os
from dotenv import load_dotenv
load_dotenv()

# const variable
MY_GUILD = discord.Object(839126064621027329)
TOKEN = os.getenv("TOKEN")

# client class [copied from discord.py examples repo]


class BotClient(commands.Bot):
    def __init__(self, *, prefix: str, intents: discord.Intents) -> None:
        super().__init__(command_prefix=prefix, intents=intents)

    async def setup_hook(self):
        await self.load_extension(f"cogs.info")

        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)
#####


# bot client
intents = discord.Intents.default()
bot = BotClient(prefix="!", intents=intents)

# Bot variable
# Team
bot.TEAM = [
    838836138537648149,  # Nur
    664550550527803405,  # Tamim
    728260210464129075,  # Rishikesh
    693375549686415381,  # Soren
    555452986885668886  # Karim
]  # our team's discord ids

# version
bot.version = 'v0.4.8'
#####

# on ready event


@bot.event
async def on_ready():
    print(f"Logged in {bot.user}")
    print("------")

# ping command


@bot.tree.command()
async def ping(ctx: discord.Interaction):
    embed_message = discord.Embed(
        title="Pong :ping_pong:",
        description=f"{round(bot.latency*1000)} _ms_!",
        color=0xffdf08)
    await ctx.response.send_message(embed=embed_message, ephemeral=True)


# hehe!! lets run the boy!! :D
bot.run(TOKEN)