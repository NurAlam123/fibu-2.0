import discord
from discord import app_commands
from discord.ext import commands

import random


class Information(commands.Cog):
    def __init__(self, client) -> None:
        self.bot = client
        self.colors = [0x7700fe, 0x340e72, 0xfdb706]

    @app_commands.command()
    async def info(self, ctx: discord.Interaction):
        # await ctx.response.send_message("hello!")
        guild = ctx.guild

        ### Information Variable ###
        guild_roles = "\n".join(f"{i}. {j}" for i, j in enumerate(
            [f"{role}" for role in guild.roles][::-1], 1))  # fetch guild roles
        guild_name = guild.name
        guild_id = guild.id
        guild_owner = guild.owner
        guild_owner_id = guild.owner_id
        # guild_region = str(guild.region).capitalize()
        guild_description = guild.description
        guild_icon = str(guild.icon_url)
        guild_created_at = (guild.created_at).strftime("%a, %d-%b-%Y %I:%M %p")

        ### Member count ###
        members = guild.member_count
        humans = 0
        online = 0
        offline = 0
        idle = 0
        dnd = 0
        for m in guild.members:
            status = str(m.status)
            if not m.bot:
                humans += 1
            if status == "online":
                online += 1
            elif status == "offline" or status == "invisible":
                offline += 1
            elif status == "idle":
                idle += 1
            elif status == "dnd" or status == "do_not_disturb":
                dnd += 1
        bots = members - humans
        ######

        guild_text_channels = len(guild.text_channels)
        guild_voice_channels = len(guild.voice_channels)
        guild_stage_channels = len(guild.stage_channels)
        guild_channels = guild_text_channels + guild_voice_channels
        guild_categories = len(guild.categories)

        ### Embed Part ###
        info_em = discord.Embed(
            title="Server Information",
            color=random.choice(self.colors))
        info_em.add_field(
            name="Name",
            value=f"{guild_name}",
            inline=False)
        info_em.add_field(
            name="Guild ID",
            value=f"```\n{guild_id}\n```",
            inline=False)
        info_em.add_field(
            name="Owner",
            value=f"{guild_owner}",
            inline=False)
        info_em.add_field(
            name="Owner ID",
            value=f"```\n{guild_owner_id}\n```",
            inline=False)
        info_em.add_field(
            name="Server Created At",
            value=f"```\n{guild_created_at}\n```")
        info_em.add_field(
            name="Region",
            value=f"{guild_region}",
            inline=False)
        if guild_description:
            info_em.add_field(
                name="Guild Description",
                value=f"{guild_description}",
                inline=False)
        info_em.add_field(
            name=f"Members [{members}]",
            value=f"```\nHumans: {humans}\nBots: {bots}\n--------------------\nOnline: {online}\nOffline: {offline}\nIdle: {idle}\nDND: {dnd}\n```", inline=False)
        info_em.add_field(
            name="Channels and Categories",
            value=f"```\nCategories: {guild_categories}\n│\n└── Channels: {guild_channels}\n    ├── Text Channels: {guild_text_channels}\n    ├── Voice Channels: {guild_voice_channels}\n└── Stage Channels: {guild_stage_channels}\n```",
            inline=False)
        info_em.add_field(
            name="Roles",
            value=f"```\n{guild_roles}\n```",
            inline=False)

        info_em.set_thumbnail(url=f"{guild_icon}")
        info_em.set_footer(
            text=f"Requested by {ctx.author} | Programming Hero ")
        await ctx.response.send_message(embed=info_em)


async def setup(bot):
    await bot.add_cog(Information(bot))
