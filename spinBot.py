import discord
from discord.ext import commands
from spinner import wheelSpin
import os

dbPath = "./spinDB"
TOKEN_NAME = "SPINBOT_TOKEN"

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix= '!', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot is online as {bot.user}')

@bot.command()
async def spin(ctx):
    
    result = wheel.spinTheWheel()
    await ctx.send(f"And the winner is... {result}!")
token = os.getenv(TOKEN_NAME)
if not token:
    raise ValueError(f"{TOKEN_NAME} is not set in environment! please export a valid token")
wheel = wheelSpin(dbPath, Verbose= True)
bot.run(token)