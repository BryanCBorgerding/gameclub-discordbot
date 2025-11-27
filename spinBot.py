import discord
from discord.ext import commands
from spinner import wheelSpin
from msgParser import messageConstructor
import os
import argparse


# Determine the database path to use
parser = argparse.ArgumentParser(description="A tool to do random wheel spins")
parser.add_argument("-t","--test", action="store_true", help ="sets the bot to use the test database")
args = parser.parse_args()
if args.test:
    print("Running in test/debug mode!")
    dbPath = "./testDB"
    msgPath = "./msgTestDB"
else:
    dbPath = "./spinDB"
    msgPath = "./msgDB"

# Outside of application: Need to Define an environment variable with name SPINBOT_TOKEN that has a value of the bot token given by discord 
TOKEN_NAME = "SPINBOT_TOKEN"

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix= '!', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot is online as {bot.user}')


#TODO: Could add multiple subcommands
@bot.group()
async def GameClub(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send("Please specify a subcommand. Try '!GameClub help' for a list of subcommands")

@GameClub.command()
async def help(ctx):
    cmdlist = {
        "help": "Displays this message; a list of commands",
        "spin": "Spins the wheel to determine the next GM"
    }
    await ctx.send("Feed me one of the following commands!")
    for key, value in cmdlist.items():
        await ctx.send(f"{key} : {value}")

@GameClub.command()
async def spin(ctx):
    result = wheel.spinTheWheel()
    userID = msg.findUserID(result)
    if userID == False:
        user = result
        winner = result
    else:
        user = await bot.fetch_user(userID)
        winner = user.mention
    message = msg.constructMessage(winner)
    await ctx.send(message)

token = os.getenv(TOKEN_NAME)
if not token:
    raise ValueError(f"{TOKEN_NAME} is not set in environment! please export a valid token")
wheel = wheelSpin(dbPath, Verbose = False)
msg = messageConstructor(msgPath, Verbose= False)
bot.run(token)