import discord
from discord.ext import commands

from ikalib import *

token = " "
resource_list = ["", "<:wine:511607612161130506>", "<:stone:511607611758739457>", "<:crystal:511607612039757824>", "<:sulfur:511607612178038794>"]

######################################################################
bot = commands.Bot(command_prefix="?", description="description here")
bot.remove_command("help")


@bot.event
async def on_ready():
    print("Logged in as " + bot.user.name)
    print("Bot is ready. Enter your command")


@bot.command()
# Description of command goes here.
async def intro():
    await bot.say("This is Ikariam bot")


@bot.command()
async def echo(*args):
    output = ""
    for word in args:
        output += word
        output += " "
    await bot.say(output)


@bot.command(pass_context=True)
async def clear(ctx, amount=100):
    channel = ctx.message.channel
    messages = []
    async for message in bot.logs_from(channel, limit=int(amount) + 1):
        messages.append(message)
    await bot.delete_messages(messages)
    await bot.say("Messages deleted.")


@bot.command(pass_context=True)
async def help(ctx):
    channel = ctx.message.channel
    # author = ctx.message.author
    embed = discord.Embed(
        title="Help",
        color=discord.Color.orange()
    )
    embed.add_field(name="?help", value="This command", inline=False)
    embed.add_field(name="?intro", value="Bot intro", inline=False)
    embed.add_field(name="?echo", value="Echo what you said", inline=False)
    embed.add_field(name="?clear [number]", value="Clear #number of last messages", inline=False)
    await bot.send_message(channel, embed=embed)
    # await bot.send_message(author, embed=embed


@bot.command(pass_context=True)
async def find(ctx, *args):
    global resource_list
    channel = ctx.message.channel
    playername = ""
    for word in args:
        playername += word
        playername += " "
    playername.strip()

    player_id = getPlayerId(playername)

    player_towns = getPlayerInfo(player_id)

    embed = discord.Embed(
        title="Towns information:",
        color=discord.Color.blue()
    )
    embed.set_footer(text="ika-search.com", icon_url="https://i.imgur.com/MBLT0wt.png")
    embed.set_author(name=playername, icon_url="https://i.imgur.com/6a7pOOv.png")
    for town in player_towns:
        embed.add_field(
            name="{} - {}({}) - {} {}".format(town["coord"], town["name"], town["level"], town["wonder_id"], resource_list[town["resource_id"]]), value="-", inline=False)
    await bot.send_message(channel, embed=embed)


######################################################################

bot.run(token)
