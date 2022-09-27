import discord
from quart import Quart, render_template, url_for, redirect, request
from quart_discord import DiscordOAuth2Session, requires_authorization, Unauthorized
import os

from main import bot

from dotenv import load_dotenv
load_dotenv()

app = Quart(__name__)

# config discord
app.secret_key = os.environ.get("session")
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "true"
app.config["DISCORD_CLIENT_ID"] = os.environ.get("CLIENT_ID")
app.config["DISCORD_CLIENT_SECRET"] = os.environ.get("CLIENT_SECRET")
app.config["DISCORD_REDIRECT_URI"] = os.environ.get("RI")
app.config["DISCORD_BOT_TOKEN"] = os.environ.get("TOKEN")

discordd = DiscordOAuth2Session(app)

# index page


@app.route("/")
async def index():
    logged = ""
    if await discordd.authorized:
        logged = True
    return await render_template("index.html", logged=logged)

# show servers


@app.route("/info")
async def info():
    user = await discordd.fetch_user()
    guilds = await user.fetch_guilds()
    return await render_template("info.html", user=user, guilds=guilds)

# login via discord


@app.route("/login/")
async def login():
    return await discordd.create_session(scope=["identify", "guilds"])

# logout


@app.route("/logout/")
async def logout():
    discordd.revoke()
    return redirect(url_for(".index"))

# redirect to main page after logged in


@app.route("/me/")
@requires_authorization
async def me():
    return redirect(url_for(".index"))


@app.route("/callback/")
async def callback():
    await discordd.callback()
    try:
        return redirect(bot.url)
    except:
        return redirect(url_for(".me"))

# handle uauthorized error


@app.errorhandler(Unauthorized)
async def redirect_unauthorized(e):
    bot.url = request.url
    return redirect(url_for(".login"))

if __name__ == "__main__":
    app.run(debug=True)
