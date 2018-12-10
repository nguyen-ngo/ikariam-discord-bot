import discord
from discord.ext import commands

from ikalib import *

token = ""

resource_list = ["", "<:wine:511607612161130506>", "<:crystal:511607612039757824>", "<:crystal:511607612039757824>", "<:sulfur:511607612178038794>"]
wonder_list = ["", "<:Hephaistos:512112680421687297>", "<:Hades:512112680459567107>", "<:Demeter:512112680027553794>", "<:Athenas:512112680186937344>", "<:Hermes:512112680413298718>", "<:Ares:512112680257978378>", "<:Poseidon:512112680577007616>", "<:Colossus:512112680513961994>"]
state_list = ["", "<:vacation:518992083919306773>", "<:inactive:518992773580587009>"]

######################################################################
bot = commands.Bot(command_prefix="?", description="description here")
bot.remove_command("help")


# Bot events
@bot.event
async def on_ready():
    print("Logged in as " + bot.user.name)
    print("Bot is ready. Enter your command")


# Bot commands
@bot.command()
async def intro():
    await bot.say("This is Ikariam bot")


@bot.command()
async def echo(*args):
    output = " ".join(args)
    output.strip()
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

    embed = discord.Embed(
        title="Help",
        color=discord.Color.orange()
    )
    embed.add_field(name="?help", value="This command", inline=False)
    #embed.add_field(name="?clear <number of line>", value="Clear history messages.", inline=False)
    embed.add_field(name="?info <player name>", value="Display player's towns.", inline=False)
    embed.add_field(name="?find <player name>", value="Display player's information.", inline=False)
    embed.add_field(name="?alliance <alliance name or alliance tag", value="Display alliance's information.", inline=False)
    embed.add_field(name="?island <xx:yy>", value="Display island information.", inline=False)
    await bot.send_message(channel, embed=embed)


@bot.command(pass_context=True)
async def island(ctx, args):
    channel = ctx.message.channel
    x, y = args.split(":")

    island_id = getIslandId(x, y)

    if island_id is 0:
        await bot.send_message(channel, "Island `{}:{}` doesn't exist. Did you think it sunk?\n".format(x, y))
    else:
        embed = discord.Embed(
            title="**Island information:**",
            color=discord.Color.blue(),
            description=""
        )

        island_data = getIslandInfo(island_id)

        embed.set_footer(text="ika-search.com", icon_url="https://i.imgur.com/MBLT0wt.png")
        embed.set_author(name="[{}:{}] {}, {}/17".format(x, y, island_data["island"]["name"], island_data["island"]["city_number"]), icon_url="https://i.imgur.com/BwU5cbG.png")

        embed.description += "{} **Lvl {}** - **{} Lvl {}** - <:wood:512113172476329996> **Lvl {}**\n".format(wonder_list[island_data["island"]["wonder_id"]], island_data["island"]["wonder_level"], resource_list[island_data["island"]["resource_id"]], island_data["island"]["resource_level"], island_data["island"]["wood_level"])

        for city in island_data["cities"]:
            if city["tag"] is not None:
                embed.description += "**{}** ({}) - {} ({}) - ({:,}) MS".format(city["pseudo"], city["tag"], city["name"], city["level"], city["army_score_main"])
            else:
                embed.description += "**{}** - {} ({}) - ({:,}) MS".format(city["pseudo"], city["name"], city["level"], city["army_score_main"])
            if city["state"] is not 0:
                embed.description += " "+state_list[city["state"]]+"\n"
            else:
                embed.description += "\n"
    await bot.send_message(channel, embed=embed)


@bot.command(pass_context=True)
async def find(ctx, *args):
    channel = ctx.message.channel
    playername = " ".join(args)
    playername.strip()

    player_id = getPlayerId(playername)
    if player_id == 0:
        await bot.send_message(channel, "Player `{}` doesn't exist. Did you mistype?\n".format(playername))
    else:
        embed = discord.Embed(
            title="**Towns information:**",
            color=discord.Color.blue(),
            description=""
        )

        player_towns = getPlayerTown(player_id)

        embed.set_footer(text="ika-search.com", icon_url="https://i.imgur.com/MBLT0wt.png")
        if player_towns[0] is None:
            embed.set_author(name=playername, icon_url="https://i.imgur.com/6a7pOOv.png")
        else:
            embed.set_author(name=playername+" ("+player_towns[0]+")", icon_url="https://i.imgur.com/6a7pOOv.png")

        for town in player_towns[1:]:
            embed.description += "**{}** - {}({}) - {} {}\n".format(town["coord"], town["name"], town["level"], wonder_list[town["wonder_id"]], resource_list[town["resource_id"]])
        await bot.send_message(channel, embed=embed)


@bot.command(pass_context=True)
async def info(ctx, *args):
    channel = ctx.message.channel
    playername = " ".join(args)
    playername.strip()

    player_id = getPlayerId(playername)
    if player_id == 0:
        await bot.send_message(channel, "Player `{}` doesn't exist. Did you mistype?\n".format(playername))
    else:
        embed = discord.Embed(
            title="**Player information:**",
            color=discord.Color.blue(),
            description=""
        )

        player_data = getPlayerInfo(player_id)
        player = player_data["player"]
        embed.set_footer(text="ika-search.com", icon_url="https://i.imgur.com/MBLT0wt.png")

        embed_playername = playername
        if player["tag"] is not None:
            embed_playername += " ("+player["tag"]+")"

        embed.set_author(name=embed_playername, icon_url="https://i.imgur.com/hasGiOH.png")

        embed.description += "**Total Score:** {:,} (#{})\n \
                              **Military Score:** {:,} (#{})\n \
                              **Gold Stock:** {:,} (#{}))\n \
                              **Offensive Points:** {:,} (#{})\n \
                              **Defence Points:** {:,} (#{})\n \
                              **Capture Points:** {:,} (#{})\n \
                              **Donations:** {:,} (#{})\n".format(player["score"], player["score_rank"],
                                                                player["army_score_main"], player["army_score_main_rank"],
                                                                player["trader_score_secondary"], player["trader_score_secondary_rank"],
                                                                player["offense"], player["offense_rank"],
                                                                player["defense"], player["defense_rank"],
                                                                player["piracy"], player["piracy_rank"],
                                                                player["donations"], player["donations_rank"])
        await bot.send_message(channel, embed=embed)


@bot.command(pass_context=True)
async def alliance(ctx, *args):
    channel = ctx.message.channel
    allyname = " ".join(args)
    allyname.strip()

    ally_id = getAllyId(allyname)
    if ally_id == 0:
        await bot.send_message(channel, "Alliance `{}` doesn't exist. Did you mistype?\n".format(allyname))
    else:
        ally_data = getAllyInfo(ally_id)
        ally_info = ally_data["ally"]
        member_info = ally_data["members"]
        embed = discord.Embed(
            title="**Alliance information:**\n{:,} ({}), {} Members\n".format(ally_info["avg_score"], ally_info["score_rank"], ally_info["members"]),
            color=discord.Color.blue(),
            description=""
        )



        embed.set_footer(text="ika-search.com", icon_url="https://i.imgur.com/MBLT0wt.png")
        embed.set_author(name="{} ({})\n".format(ally_info["name"], ally_info["tag"]), icon_url="http://ika-search.com/style/images/alliance.png")

        for member in member_info:
            if(len(embed.description) < 1900):
                if member["state"] is not 0:
                    embed.description += "**{}** (#{}) - {:,} MS {}\n".format(member["pseudo"], member["score_rank"], member["army_score_main"], state_list[member["state"]])
                else:
                    embed.description += "**{}** (#{}) - {:,} MS\n".format(member["pseudo"], member["score_rank"], member["army_score_main"])
            else:
                embed.set_footer()
                await bot.send_message(channel, embed=embed)
                embed.description = ""
                embed.set_author(name="")
                embed.title = ""
                embed.set_footer(text="ika-search.com", icon_url="https://i.imgur.com/MBLT0wt.png")
        await bot.send_message(channel, embed=embed)


######################################################################

bot.run(token)
