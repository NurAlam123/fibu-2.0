# imports
import discord
from discord import app_commands
from discord.ext import commands
import os


from dotenv import load_dotenv
load_dotenv()


# const variable
MY_GUILD = discord.Object(int(os.getenv("GUILD")))
TOKEN = os.getenv("TOKEN")

# client class [copied from discord.py examples repo]


class BotClient(commands.Bot):
    def __init__(self, *, prefix: str, intents: discord.Intents) -> None:
        super().__init__(command_prefix=prefix, intents=intents)

    async def setup_hook(self):
        cogs = [
            'info'
        ]
        for cog in cogs:
            await self.load_extension(f"cogs.{cog}")

        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)
#####


# bot intents
intents = discord.Intents.default()
intents.members = True

# bot client
bot = BotClient(prefix="/", intents=intents)

# Bot variable
bot.TEAM = [
    838836138537648149,  # Nur
    664550550527803405,  # Tamim
    728260210464129075,  # Rishikesh
    693375549686415381,  # Soren
    555452986885668886  # Karim
]  # our team's discord ids
bot.version = 'v2.0'  # version


########################
#### on ready event ####
@bot.event
async def on_ready():
    print(f"Logged in {bot.user}")
    print("------")

#### ping command ####


@bot.tree.command(name="ping", description="Pong!")
async def ping(ctx: discord.Interaction):
    embed_message = discord.Embed(
        title="Pong :ping_pong:",
        description=f"{round(bot.latency*1000)} _ms_!",
        color=0xffdf08)
    await ctx.response.send_message(embed=embed_message, ephemeral=True)
#### Sync commands ###


@bot.tree.command()
async def sync_command(ctx: discord.Interaction):
    await bot.unload_extension(f"cogs.info")
    await bot.load_extension(f"cogs.info")
    bot.tree.copy_global_to(guild=MY_GUILD)
    await bot.tree.sync(guild=MY_GUILD)
    await ctx.response.send_message("Synced!!", ephemeral=True)
#####


def is_me():
    def predicate(interaction: discord.Interaction) -> bool:
        return interaction.user.id == 838836138537648149
    return app_commands.check(predicate)

#### Load and Unload ####


@bot.tree.command(name="load")
@is_me()
async def _load(ctx: discord.Interaction, extension_name: str = None) -> None:
    if extension_name:
        await bot.load_extension(f"cog.{extension_name}")
    else:
        for _file in os.listdir("./cogs"):
            if _file.endswith(".py"):
                await bot.load_extension(f"cogs.{_file[:-3]}")
    await ctx.response.send_message("Extension Loaded!")


@bot.tree.command(name="unload")
@is_me()
async def _unload(ctx: discord.Interaction, extension_name: str = None) -> None:
    if extension_name:
        await bot.unload_extension(f"cog.{extension_name}")
    else:
        for _file in os.listdir("./cogs"):
            if _file.endswith(".py"):
                bot.unload_extension(f"cogs.{_file[:-3]}")
    await ctx.response.send_message("Extension UnLoaded!")

# @bot.tree.context_menu(name="Avatar", guild=MY_GUILD)
# async def _avatar_context(ctx: discord.Interaction, member: discord.Member) -> None:
#     from cogs.info import Information
#     info = Information._avatar(bot, ctx, member)

# hehe!! lets run the boy!! :D
bot.run(TOKEN)
