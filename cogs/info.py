import discord
from discord import app_commands
from discord.ext import commands

import random


class Information(commands.Cog):
    def __init__(self, client) -> None:
        self.bot = client
        self.colors = [0x7700fe, 0x340e72, 0xfdb706]

    # server information - command
    @app_commands.command(name="serverinfo", description="Show information about the server.")
    async def serverinfo(self, ctx: discord.Interaction):
        guild = ctx.guild

        ### Guild Information Variable ###
        guild_roles = "\n".join(f"{i}. {j}" for i, j in enumerate(
            [f"{role}" for role in guild.roles][::-1], 1))  # fetch guild roles
        guild_name = guild.name
        guild_id = guild.id
        guild_owner = guild.owner
        guild_owner_id = guild.owner_id
        # guild_region = str(guild.region).capitalize()
        guild_description = guild.description
        guild_icon = str(guild.icon.url)
        guild_created_at = (guild.created_at).strftime("%a, %d-%b-%Y %I:%M %p")

        ### Member count ###
        members = guild.member_count
        humans = len([i for i in guild.members if not i.bot])
        bots = members - humans
        #### Channels ####
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
            value=f"{guild_owner.mention}",
            inline=False)
        info_em.add_field(
            name="Owner ID",
            value=f"```\n{guild_owner_id}\n```",
            inline=False)
        info_em.add_field(
            name="Server Created At",
            value=f"```\n{guild_created_at}\n```",
            inline=False)
        if guild_description:
            info_em.add_field(
                name="Guild Description",
                value=f"{guild_description}",
                inline=False)
        info_em.add_field(
            name=f"Members [{members}]",
            value=f"```\nHumans: {humans}\nBots: {bots}\n```", inline=False)
        info_em.add_field(
            name="Channels and Categories",
            value=f"```\nCategories: {guild_categories}\n\tChannels: {guild_channels}\n\t\tText Channels: {guild_text_channels}\n\t\tVoice Channels: {guild_voice_channels}\n\tStage Channels: {guild_stage_channels}\n```",
            inline=False)
        info_em.add_field(
            name="Roles",
            value=f"```\n{guild_roles}\n```",
            inline=False)

        info_em.set_thumbnail(url=f"{guild_icon}")
        info_em.set_footer(
            text=f"Requested by {ctx.user} | Programming Hero ")
        await ctx.response.send_message(embed=info_em)


async def setup(bot):
    await bot.add_cog(Information(bot))
