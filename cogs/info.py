from email.mime import application
from ssl import get_default_verify_paths
import discord
from discord import app_commands
from discord.ext import commands

import random
from datetime import datetime as time
# import pymongo


class Information(commands.Cog):
    def __init__(self, client) -> None:
        self.bot = client
        self.colors = [0x7700fe, 0x340e72, 0xfdb706]

    # server information - command
    @app_commands.command(name="server", description="Show information about the server.")
    async def serverinfo(self, ctx: discord.Interaction) -> None:
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
            text=f"Requested by {ctx.user}\nFibu | Programming Hero ")
        await ctx.response.send_message(embed=info_em)

    # fibu information - command
    @app_commands.command(name="info", description="Displays information about the bot.")
    async def _botinfo(self, ctx: discord.Interaction) -> None:
        msg = discord.Embed(
            title="My information",
            description="Hey there! I am **Fibu**. Your friend and a friendly bot. I am from Programming Hero",
            color=0xffdf08,
            timestamp=time.now())
        msg.add_field(
            name="Version",
            value=f"{self.bot.version}",
            inline=False)
        msg.add_field(
            name="Released on",
            value="<t:1609480800:D>",
            inline=False)
        msg.add_field(
            name="Built in",
            value="**Language:** Python3\n**API Wrapper:** discord.py",
            inline=False)
        msg.add_field(
            name="Developer Team",
            value="**1. Nur Alam\n2. Tamim Vaiya\n3. Rishikesh\n4. Soren_Blank\n5. Shajedul Karim**",
            inline=False)
        msg.add_field(
            name="PH Website",
            value="[Programming Hero](https://www.programming-hero.com/)\n[Blog](https://www.programming-hero.com/blog/)",
            inline=False)
        msg.add_field(
            name="PH Application",
            value="[Android App](https://is.gd/z11RUg)\n[Iphone Version](https://is.gd/eVH92i)",
            inline=False)
        msg.add_field(
            name="PH Social Media",
            value="[Facebook Page](https://m.facebook.com/programmingHero/)\n[Facebook Group](https://www.facebook.com/groups/programmingheroapp/)\n[Instagram](https://is.gd/6m3hgd)\n[Twitter](https://twitter.com/ProgrammingHero?s=09)\n[Youtube](https://is.gd/EulQLJ)\n[Pinterest](https://www.pinterest.com/programminghero1/)",
            inline=False)
        msg.set_author(
            name=f"{self.bot.user.name}",
            url="https://www.programming-hero.com/",
            icon_url=f"{self.bot.user.avatar.url}")
        msg.set_thumbnail(url=f"{self.bot.user.avatar.url}")
        msg.set_footer(
            text=f"Requested by {ctx.user}\nFibu | Programming Hero ")
        await ctx.response.send_message(embed=msg, ephemeral=True)

    # user information - command
    @app_commands.command(name="user", description="Displays information about the user")
    @app_commands.describe(member="The member you want to get the information of.")
    async def userinfo(self, ctx: discord.Interaction, member: discord.Member = None) -> None:
        member = member or ctx.user
        ## Connect with database ##
        # con_fibu = pymongo.MongoClient(os.getenv("DB"))
        # db = con_fibu["fibu"]
        # #tb = db["challenge_data"]
        # tb = db["all_about_challenge"]

        # find_user = tb.find_one(
        #     {"user_id": member.id, "guild_id": member.guild.id})
        roles = []
        for role in member.roles:
            if role.name != "@everyone":
                role_format = f"{role}"
                roles.append(role_format)

            #### Information Variables ####
        roles_format = "\n".join(f"{i}. {j}" for i, j in enumerate(
            roles, 1)) if len(roles) != 0 else "No Roles"
        guild = member.guild
        user_id = member.id
        user_name = member.name
        user_tag = member.discriminator
        user_nickname = member.nick
        user_status = str(member.status)
        bot_user = member.bot
        user_avatar = str(member.avatar.url)
        status_emoji = {
            "online": "<:online:848818909292658729>",
            "offline": "<:offline:848818930830016533>",
            "invisible": "<:offline:848818930830016533>",
            "idle": "<:idle:848818891446681620>",
            "dnd": "<:dnd:848819104446283806>",
            "do_not_disturb": "<:dnd:848819104446283806>",
        }
        badges_value = {
            0: None,
            1 << 0: "Discord Employee",
            1 << 1: "Partnered Server Owner",
            1 << 2: "HypeSquad Events",
            1 << 3: "Bug Hunter Level 1",
            1 << 6: "House Bravery",
            1 << 7: "House Brilliance",
            1 << 8: "House Balance",
            1 << 9: "Early Supporter",
            1 << 10: "Team User",
            1 << 14: "Bug Hunter Level 2",
            1 << 16: "Verified Bot",
            1 << 17: "Early Verified Bot Developer",
            1 << 18: "Discord Certified Moderator"
        }

        user_activities = member.activities
        status = user_status.capitalize() if user_status != "dnd" else user_status.upper()

        user_badges = ""
        user_all_badges = member.public_flags.all()
        for no, badge in enumerate(user_all_badges, 1):
            value = badge.value
            user_badges += f"{no}. {badges_value[value]}\n"
        joined_guild = (member.joined_at).strftime("%a, %d-%b-%Y %I:%M %p")
        created_acc = (member.created_at).strftime("%a, %d-%b-%Y %I:%M %p")

        suf = "Bot " if bot_user else ""

        #### Embed Part ####
        info_em = discord.Embed(
            title=f"{suf}User Information",
            color=random.choice(self.colors))
        info_em.add_field(
            name="Name",
            value=f"```\n{user_name}\n```",
            inline=True)
        info_em.add_field(
            name="Tag",
            value=f"```\n#{user_tag}\n```",
            inline=True)
        info_em.add_field(
            name="ID",
            value=f"```\n{user_id}\n```",
            inline=False)
        if user_nickname:
            info_em.add_field(
                name="Nickname",
                value=f"```\n{user_nickname}\n```",
                inline=False)
            info_em.add_field(
                name="Status",
                value=f"{status_emoji[user_status]} ─ **{status}**",
                inline=False)
            info_em.add_field(
                name=f"Joined {guild.name} at",
                value=f"```\n{joined_guild}\n```",
                inline=False)
            info_em.add_field(
                name="Account Created at",
                value=f"```\n{created_acc}\n```",
                inline=False)
            info_em.add_field(
                name="Badges",
                value=user_badges,
                inline=False) if not user_badges else None
        #    #### challenge"s information ####
        #     if find_user:
        #         output = f"Level: {find_user['level']}\nXP: {find_user['xp']}/{find_user['need_xp']}"
        #         info_em.add_field(name="Challenge Profile",
        #                           value=output, inline=False)
        #         challenges_name = find_user["challenges"]
        #         if challenges_name:
        #             all_challenges = ""
        #             for no, challenge_name in enumerate(challenges_name, 1):
        #                 all_challenges += f"{no}. {challenge_name}\n"
        #             info_em.add_field(
        #                 name="Solved Challenges", value=f"```\n{all_challenges}\n```", inline=False)
            ########
            info_em.add_field(
                name=f"Roles [{len(roles)}]",
                value=f"```\n{roles_format}\n```",
                inline=False)
            info_em.set_thumbnail(url=f"{user_avatar}")
            info_em.set_footer(
                text=f"Requested by {ctx.user}\nFibu | Programming Hero ")

            await ctx.response.send_message(embed=info_em)
    # avatar

    @app_commands.command(name="avatar", description="Displays user avatar.")
    async def _av(self, ctx: discord.Interaction, member: discord.Member = None):
        member = member or ctx.user
        avatar = discord.Embed(
            title="Avatar",
            color=0xffdf08)
        avatar.set_image(url=member.avatar.url)
        await ctx.response.send_message(embed=avatar, ephemeral=True)


async def setup(bot):
    await bot.add_cog(Information(bot))
