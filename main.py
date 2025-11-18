import os
import discord
from discord.ext import tasks, commands
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))  # where the message should be sent

intents = discord.Intents.default()
intents.guilds = True
intents.guild_messages = True
intents.message_content = True
intents.members = True  # needed to access roles

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    send_daily_message.start()  # start the daily task

@tasks.loop(hours=24)
async def send_daily_message():
    now = datetime.utcnow()  # use UTC time
    day = now.day
    if day > 28:
        return  # skip 29–31

    guild = bot.guilds[0]  # assumes you only run this in one server
    role_name = f"Day {day}"
    role = discord.utils.get(guild.roles, name=role_name)
    channel = bot.get_channel(CHANNEL_ID)

    if role and channel:
        await channel.send(
            f"{role.mention} — Today is your day to post your creations! "
            "In the appropriate channels, post a fic or piece of art (and add a little blurb about it if you'd like)!"
        )

@send_daily_message.before_loop
async def before_daily_message():
    await bot.wait_until_ready()
    # Calculate seconds until next midnight UTC
    now = datetime.utcnow()
    next_midnight = datetime.combine(now.date() + timedelta(days=1), datetime.min.time())
    await discord.utils.sleep_until(next_midnight)

bot.run(TOKEN)
