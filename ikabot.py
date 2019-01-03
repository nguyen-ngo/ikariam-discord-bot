import discord
from discord.ext import commands

from ikalib import *

prefix = "?"
bot = commands.Bot(command_prefix=prefix)
bot.remove_command("help")

TOKEN = ""

admin_role = "Administrator"
resource_list = ["", "<:wine:511607612161130506>", "<:crystal:511607612039757824>", "<:crystal:511607612039757824>",
                 "<:sulfur:511607612178038794>"]
wonder_list = ["", "<:Hephaistos:512112680421687297>", "<:Hades:512112680459567107>", "<:Demeter:512112680027553794>",
               "<:Athenas:512112680186937344>", "<:Hermes:512112680413298718>", "<:Ares:512112680257978378>",
               "<:Poseidon:512112680577007616>", "<:Colossus:512112680513961994>"]
state_list = ["", "<:vacation:518992083919306773>", "<:inactive:518992773580587009>"]


# Bot events
@bot.event
async def on_ready():
    print("Bot is ready, waiting for your command.")


@bot.event
async def on_server_join(server):
    server_id = server.id
    server_name = server.name
    server_config_file = "servers{}{}.json".format(os.sep, server_id)
    if not os.path.exists(server_config_file):
        with open(server_config_file, "w+") as file:
            file_content = '{"name": "' + server_name + '", "region": "us", "world": "Eirene", "mode": "server", "channels": {}}'
            file.write(file_content)
            file.close()


@bot.event
async def on_member_join(member):
    channels = list(member.server.channels)
    for channel in channels:
        if channel.name == "general":
            await bot.send_message(channel,
                                   ":fireworks: :fireworks: :fireworks: @everyone !! Please send a warm welcome to our new member, {} :fireworks: :fireworks: :fireworks:".format(
                                       member.mention))


# Server configuration commands
@bot.command(pass_context=True)
async def mode(ctx, input_mode=None):
    top_role = ctx.message.author.top_role.name
    channel = ctx.message.channel
    run_as_administrator = True if ctx.message.author.server_permissions.administrator or top_role == admin_role else False
    if not run_as_administrator:
        await bot.send_message(channel, "It looks like you don't have permission to use this command.")
    else:
        if input_mode is None or (input_mode != "server" and input_mode != "channel"):
            await bot.send_message(channel,
                                   "You didn't input valid mode. To set server mode using command `?mode [server/channel]`")
        else:
            server_mode = input_mode.strip()
            server_id = ctx.message.server.id
            server_config_file = "servers{}{}.json".format(os.sep, server_id)
            server_configs = getServerConfigs(server_config_file)
            server_configs["mode"] = server_mode
            updateConfigs(server_config_file, server_configs)
            if input_mode == "server":
                await bot.send_message(channel,
                                       "Server mode is set to `server`. Current world is `{}`.\nTo change server mode using command `?mode [server/channel]`.\nTo change world using command `?ikaworld [world]`.".format(
                                           server_configs["world"]))
            else:
                await bot.send_message(channel,
                                       "Server mode is set to `channel`.\nTo change server mode using command `?mode [server/channel]`.\nTo set world for this channel using command `?ikaworld [world]`.")


@bot.command(pass_context=True)
async def region(ctx, input_region=None):
    top_role = ctx.message.author.top_role.name
    channel = ctx.message.channel
    run_as_administrator = True if ctx.message.author.server_permissions.administrator or top_role == admin_role else False
    if not run_as_administrator:
        await bot.send_message(channel, "It looks like you don't have permission to use this command.")
    else:
        if input_region is None:
            await bot.send_message(channel,
                                   "You didn't input region name in command. To set server region using `?region [region]`")
        else:
            server_region = input_region.strip()
            server_id = ctx.message.server.id

            server_config_file = "servers{}{}.json".format(os.sep, server_id)
            server_configs = getServerConfigs(server_config_file)
            server_configs["region"] = server_region
            updateConfigs(server_config_file, server_configs)
            await bot.send_message(channel,
                                   "Server region is set to `{}`. To change server region using `?region [region]`".format(
                                       server_region))


@bot.command(pass_context=True)
async def ikaworld(ctx, input_world=None):
    top_role = ctx.message.author.top_role.name
    channel = ctx.message.channel
    run_as_administrator = True if ctx.message.author.server_permissions.administrator or top_role == admin_role else False
    if not run_as_administrator:
        await bot.send_message(channel, "It looks like you don't have permission to use this command.")
    else:
        if input_world is None:
            await bot.send_message(channel,
                                   "You didn't input world name in command. To set server world using command `?ikaworld [world]`")
        else:
            server_world = input_world.strip()
            server_id = ctx.message.server.id

            server_config_file = "servers{}{}.json".format(os.sep, server_id)
            server_configs = getServerConfigs(server_config_file)
            if server_configs["mode"] == "server":
                server_configs["world"] = server_world
                updateConfigs(server_config_file, server_configs)
                await bot.send_message(channel,
                                       "Server world is set to `{}`. To change the world using command `?ikaworld [world]`".format(
                                           server_world))
            elif server_configs["mode"] == "channel":
                channel_id = channel.id
                server_configs["channels"][channel_id] = server_world
                updateConfigs(server_config_file, server_configs)
                await bot.send_message(channel,
                                       "Channel world is set to `{}`. To change the world using command `?ikaworld [world]`".format(
                                           server_world))
            else:
                await bot.send_message(channel,
                                       "Server mode is not set. To set server mode using command `?ikaworld [world]`".format(
                                           server_world))


# Bot commands
@bot.command(pass_context=True)
async def help(ctx):
    channel = ctx.message.channel

    embed = discord.Embed(
        title="Help",
        color=discord.Color.orange(),
        description="{prefix}help - This command.\n{prefix}info <player name> - Display player's towns.\n{prefix}find <player's name> - Display player's information.\n{prefix}alliance <alliance name or alliance tag> - Display alliance's information.\n{prefix}island <x:y> - Display island's information.".format(
            prefix=prefix)
    )
    await bot.send_message(channel, embed=embed)


@bot.command(pass_context=True)
async def island(ctx, coordinate):
    server_id = ctx.message.server.id
    channel = ctx.message.channel
    channel_id = channel.id
    server_config_file = "servers{}{}.json".format(os.sep, server_id)
    server_region, world = getChannelConfigs(server_config_file, channel_id)

    x, y = coordinate.split(":")

    island_id = getIslandId(x, y)

    if island_id is 0:
        await bot.send_message(channel, "Island `{}:{}` doesn't exist. Did you think it sunk?".format(x, y))
    else:
        embed = discord.Embed(
            title="**Island information:**",
            color=discord.Color.blue(),
            description=""
        )

        island_info = getIslandInfo(server_region, world, island_id)

        embed.set_footer(text="ika-search.com", icon_url="https://i.imgur.com/MBLT0wt.png")
        embed.set_author(
            name="[{}:{}] {}, {}/17".format(x, y, island_info["island"]["name"], island_info["island"]["city_number"]),
            icon_url="https://i.imgur.com/BwU5cbG.png")

        embed.description += "{} **Lvl {}** - **{} Lvl {}** - <:wood:512113172476329996> **Lvl {}**\n".format(
            wonder_list[island_info["island"]["wonder_id"]], island_info["island"]["wonder_level"],
            resource_list[island_info["island"]["resource_id"]], island_info["island"]["resource_level"],
            island_info["island"]["wood_level"])

        for city in island_info["cities"]:
            if city["tag"] is not None:
                embed.description += "**{}** ({}) - {} ({}) - ({:,}) MS".format(city["pseudo"], city["tag"],
                                                                                city["name"], city["level"],
                                                                                city["army_score_main"])
            else:
                embed.description += "**{}** - {} ({}) - ({:,}) MS".format(city["pseudo"], city["name"], city["level"],
                                                                           city["army_score_main"])
            if city["state"] is not 0:
                embed.description += " " + state_list[city["state"]] + "\n"
            else:
                embed.description += "\n"
    await bot.send_message(channel, embed=embed)


@bot.command(pass_context=True)
async def find(ctx, *args):
    server_id = ctx.message.server.id
    channel = ctx.message.channel
    channel_id = channel.id
    server_config_file = "servers{}{}.json".format(os.sep, server_id)
    server_region, world = getChannelConfigs(server_config_file, channel_id)

    player_name = " ".join(args)
    player_name.strip()

    player_id = getPlayerId(server_region, world, player_name)
    if player_id == 0:
        await bot.send_message(channel, "Player `{}` doesn't exist. Did you mistype?".format(player_name))
    else:
        embed = discord.Embed(
            title="**Towns information:**",
            color=discord.Color.blue(),
            description=""
        )

        player_towns = getPlayerTown(server_region, world, player_id)

        embed.set_footer(text="ika-search.com", icon_url="https://i.imgur.com/MBLT0wt.png")
        if player_towns[0] is None:
            embed.set_author(name=player_name, icon_url="https://i.imgur.com/6a7pOOv.png")
        else:
            embed.set_author(name=player_name + " (" + player_towns[0] + ")",
                             icon_url="https://i.imgur.com/6a7pOOv.png")

        for town in player_towns[1:]:
            embed.description += "**{}** - {}({}) - {} {}\n".format(town["coord"], town["name"], town["level"],
                                                                    wonder_list[town["wonder_id"]],
                                                                    resource_list[town["resource_id"]])
        await bot.send_message(channel, embed=embed)


@bot.command(pass_context=True)
async def info(ctx, *args):
    server_id = ctx.message.server.id
    channel = ctx.message.channel
    channel_id = channel.id
    server_config_file = "servers{}{}.json".format(os.sep, server_id)
    server_region, world = getChannelConfigs(server_config_file, channel_id)

    player_name = " ".join(args)
    player_name.strip()

    player_id = getPlayerId(server_region, world, player_name)
    if player_id == 0:
        await bot.send_message(channel, "Player `{}` doesn't exist. Did you mistype?".format(player_name))
    else:
        embed = discord.Embed(
            title="**Player information:**",
            color=discord.Color.blue(),
            description=""
        )

        player_data = getPlayerInfo(server_region, world, player_id)
        player = player_data["player"]
        embed.set_footer(text="ika-search.com", icon_url="https://i.imgur.com/MBLT0wt.png")

        embed_player_name = player_name
        if player["tag"] is not None:
            embed_player_name += " (" + player["tag"] + ")"

        embed.set_author(name=embed_player_name, icon_url="https://i.imgur.com/hasGiOH.png")

        embed.description += "**Total Score:** {:,} (#{})\n \
                              **Military Score:** {:,} (#{})\n \
                              **Gold Stock:** {:,} (#{}))\n \
                              **Offensive Points:** {:,} (#{})\n \
                              **Defence Points:** {:,} (#{})\n \
                              **Capture Points:** {:,} (#{})\n \
                              **Donations:** {:,} (#{})\n".format(player["score"], player["score_rank"],
                                                                  player["army_score_main"],
                                                                  player["army_score_main_rank"],
                                                                  player["trader_score_secondary"],
                                                                  player["trader_score_secondary_rank"],
                                                                  player["offense"], player["offense_rank"],
                                                                  player["defense"], player["defense_rank"],
                                                                  player["piracy"], player["piracy_rank"],
                                                                  player["donations"], player["donations_rank"])
        await bot.send_message(channel, embed=embed)


@bot.command(pass_context=True)
async def alliance(ctx, *args):
    server_id = ctx.message.server.id
    channel = ctx.message.channel
    channel_id = channel.id
    server_config_file = "servers{}{}.json".format(os.sep, server_id)
    server_region, world = getChannelConfigs(server_config_file, channel_id)

    ally_name = " ".join(args)
    ally_name.strip()

    ally_id = getAllyId(server_region, world, ally_name)
    if ally_id == 0:
        await bot.send_message(channel, "Alliance `{}` doesn't exist. Did you mistype?".format(ally_name))
    else:
        ally_data = getAllyInfo(server_region, world, ally_id)
        ally_info = ally_data["ally"]
        member_info = ally_data["members"]
        embed = discord.Embed(
            title="**Alliance information:**\n{:,} ({}), {} Members\n".format(ally_info["avg_score"],
                                                                              ally_info["score_rank"],
                                                                              ally_info["members"]),
            color=discord.Color.blue(),
            description=""
        )

        embed.set_footer(text="ika-search.com", icon_url="https://i.imgur.com/MBLT0wt.png")
        embed.set_author(name="{} ({})\n".format(ally_info["name"], ally_info["tag"]),
                         icon_url="http://ika-search.com/style/images/alliance.png")

        for member in member_info:
            if len(embed.description) < 1900:
                if member["state"] is not 0:
                    embed.description += "**{}** (#{}) - {:,} MS {}\n".format(member["pseudo"], member["score_rank"],
                                                                              member["army_score_main"],
                                                                              state_list[member["state"]])
                else:
                    embed.description += "**{}** (#{}) - {:,} MS\n".format(member["pseudo"], member["score_rank"],
                                                                           member["army_score_main"])
            else:
                embed.set_footer()
                await bot.send_message(channel, embed=embed)
                embed.description = ""
                embed.set_author(name="")
                embed.title = ""
                embed.set_footer(text="ika-search.com", icon_url="https://i.imgur.com/MBLT0wt.png")
        await bot.send_message(channel, embed=embed)


@bot.command(pass_context=True)
async def growth(ctx, *args):
    server_id = ctx.message.server.id
    channel = ctx.message.channel
    channel_id = channel.id
    config_file = "servers{}{}.json".format(os.sep, server_id)
    server_region, world = getChannelConfigs(config_file, channel_id)

    categories = {
        "army_score_main": ["military"],
        "trader_score_secondary": ["gold", "gold stock"],
        "offense": ["offense"],
        "defense": ["defense"],
        "donations": ["donate", "donation", "donates", "donations"]
    }

    arg_list = " ".join(args).split(", ")

    # Check command syntax
    if arg_list[0] == "" or len(arg_list) > 3:
        await bot.send_message(channel,
                               "Command not correct. Correct syntax: `{}growth <player name>, [category], [time in days]`.".format(
                                   prefix))
    else:
        # Check if player exists
        player_id = getPlayerId(server_region, world, arg_list[0])
        if player_id == 0:  # Player doesn't exist
            await bot.send_message(channel, "Player `{}` doesn't exist. Did you mistype?".format(arg_list[0]))
        else:  # Player exists
            arg_list[0] = player_id
            player_growth_info = []

            # Check arguments
            if len(arg_list) == 1:
                player_growth_info = getPlayerGrowth(server_region, world, arg_list)

            if 1 < len(arg_list) <= 3:
                # Check if input category correct
                category_found = 0  # category found or not
                search_category = arg_list[1].lower()
                for category in categories:
                    if search_category in categories[category]:
                        arg_list[1] = category
                        category_found = 1  # category found (correct)
                        break
                if not category_found:
                    await bot.send_message(channel, "Can't find a score category.")
                else:
                    player_growth_info = getPlayerGrowth(server_region, world, arg_list)

            if player_growth_info:
                player_info = getPlayerInfo(server_region, world, player_id)
                player_name = player_info["player"]["pseudo"]
                player_tag = player_info["player"]["tag"]

                embed = discord.Embed(
                    title="**Player score information:**\n",
                    color=discord.Color.blue(),
                    description=""
                )

                embed.set_footer(text="ika-search.com", icon_url="https://i.imgur.com/MBLT0wt.png")
                if player_tag:
                    embed.set_author(name="{} ({})".format(player_name, player_tag),
                                     icon_url="https://i.imgur.com/hasGiOH.png")
                else:
                    embed.set_author(name="{}".format(player_name),
                                     icon_url="https://i.imgur.com/hasGiOH.png")

                score_change = player_growth_info[len(player_growth_info) - 1]["v"] - player_growth_info[0]["v"]
                rank_change = player_growth_info[len(player_growth_info) - 1]["r"] - player_growth_info[0]["r"]
                embed.description += "**{:,} --> {:,} ({:,})**\n".format(player_growth_info[0]["v"],
                                                                         player_growth_info[
                                                                             len(player_growth_info) - 1]["v"],
                                                                         score_change)
                embed.description += "**#{:,} --> #{:,} ({})**\n".format(abs(player_growth_info[0]["r"]),
                                                                         abs(player_growth_info[
                                                                                 len(player_growth_info) - 1]["r"]),
                                                                         rank_change)

                await bot.send_message(channel, embed=embed)


# ------------------------------------------------------
if __name__ == "__main__":
    bot.run(TOKEN)
