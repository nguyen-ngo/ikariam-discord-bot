import os
import re
import json
import requests

with open("data{}island.json".format(os.sep), "r") as island_file:
    island_data = json.load(island_file)
    island_file.close()

islands = island_data["islands"]

url_base = 'http://ika-search.com/getSite.py'


def getNews():
    pass


def getServerConfigs(config_file):
    try:
        if os.path.exists(config_file):
            with open(config_file, "r") as config_file:
                config_data = json.load(config_file)
                config_file.close()
                return config_data
        else:
            print("{} doesn't exist.".format(config_file))
            return -1
    except Exception as e:
        return e


def getChannelConfigs(config_file, channel_id):
    try:
        if os.path.exists(config_file):
            with open(config_file, "r") as config_file:
                config_data = json.load(config_file)
                config_file.close()
    except Exception as e:
        return e
    server_region = config_data["region"]
    if config_data["mode"] == "server":
        ikariam_world = config_data["world"]
    elif config_data["mode"] == "channel":
        ikariam_world = config_data["channels"][channel_id]
    return server_region, ikariam_world


def updateConfigs(config_file, config_data):
    config_data = str(config_data)
    config_data = config_data.replace('\'', '"')
    try:
        with open(config_file, "w+") as config_file:
            config_file.write(config_data)
            config_file.close()
            return 0
    except Exception as e:
        return e


def getIslandId(x, y):
    for island in islands:
        if x in island["x"] and y in island["y"]:
            return int(island["id"])
    return 0


def getIslandInfo(region, server, island_id):
    params = {"action": "islandCities",
              "iso": region,
              "server": server,
              "islandId": island_id
              }
    rq = requests.post(url_base, params)
    island_info = rq.json()
    return island_info


def getPlayerData(region, server):
    params = {'action': 'autocompleteList',
              'iso': region,
              'server': server
              }
    rq = requests.post(url_base, params)
    server_data = rq.json()
    player_data = server_data['player']
    return player_data


def getPlayerId(region, server, player_name):
    player_data = getPlayerData(region, server)

    for player in player_data:
        if re.match(r"^" + player_name + "$", player['pseudo']):
            return player['id']
    return 0


def getPlayerTown(region, server, player_id):
    params = {"action": "playerInfo",
              "iso": region,
              "server": server,
              "playerId": player_id
              }

    rq = requests.post(url_base, params)

    player_data = rq.json()

    player_tag = player_data["player"]["tag"]
    town_data = player_data["cities"]

    player_towns = [player_tag]
    for town in town_data:
        player_towns.append(
            {"coord": "[" + str(town["x"]) + ":" + str(town["y"]) + "]", "name": town["name"], "level": town["level"],
             "resource_id": town["resource_id"], "wonder_id": town["wonder_id"]})
    return player_towns


def getPlayerInfo(region, server, player_id):
    params = {"action": "playerInfo",
              "iso": region,
              "server": server,
              "playerId": player_id
              }

    rq = requests.post(url_base, params)

    player_data = rq.json()
    return player_data


def getAllyData(region, server):
    params = {'action': 'autocompleteList',
              'iso': region,
              'server': server
              }
    rq = requests.post(url_base, params)
    server_data = rq.json()
    ally_data = server_data['ally']
    return ally_data


def getAllyId(region, server, ally_name):
    alliances = getAllyData(region, server)
    for alliance in alliances:
        if re.match(r"^" + ally_name + "$", alliance["tag"]) or re.match(r"^" + ally_name + "$", alliance["name"]):
            return alliance["id"]
    return 0


def getAllyInfo(region, server, ally_id):
    params = {"action": "allyInfo",
              "iso": region,
              "server": server,
              "allyId": ally_id
              }
    rq = requests.post(url_base, params)

    ally_data = rq.json()
    return ally_data


def getPlayerGrowth(region, server, search_criteria=[]):
    player_id = search_criteria[0]
    score_type = "score"
    date_num = "7"
    if len(search_criteria) == 2:
        score_type = search_criteria[1]
    if len(search_criteria) == 3:
        score_type = search_criteria[1]
        date_num = search_criteria[2]
    params = {"action": "getScores",
              "iso": region,
              "server": server,
              "type": "player",
              "index": player_id,
              "scoreType": score_type,
              "dateNum": date_num,
              "dateType": "DAY",
              }
    
    rq = requests.post(url_base, params)
    player_growth_info = rq.json()
    return player_growth_info
