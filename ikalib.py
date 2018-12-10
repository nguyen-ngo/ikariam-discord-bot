import re
import json
import requests

f = open("island.json","r")
island_data = json.loads(f.read())
f.close()

islands = island_data["islands"]

url_base = 'http://ika-search.com/getSite.py'
region = 'us'
server = 'Eirene'


def getNews():
    pass


def getPlayerData():
    params = {'action': 'autocompleteList',
              'iso': region,
              'server': server
              }
    rq = requests.post(url_base, params)
    server_data = rq.json()
    player_data = server_data['player']
    return player_data


def getAllyData():
    params = {'action': 'autocompleteList',
              'iso': region,
              'server': server
              }
    rq = requests.post(url_base, params)
    server_data = rq.json()
    ally_data = server_data['ally']
    return ally_data


def getPlayerId(playername):
    player_data = getPlayerData()

    for player in player_data:
        if re.match(r"^"+playername+"$", player['pseudo']):
            return player['id']
    return 0


def getPlayerTown(playerId):
    params = {"action": "playerInfo",
              "iso": region,
              "server": server,
              "playerId": playerId
              }

    rq = requests.post(url_base, params)

    player_data = rq.json()

    player_tag = player_data["player"]["tag"]
    town_data = player_data["cities"]

    player_towns = [player_tag]
    for town in town_data:
        player_towns.append({"coord": "[" + str(town["x"]) + ":" + str(town["y"]) + "]", "name": town["name"], "level": town["level"], "resource_id": town["resource_id"], "wonder_id": town["wonder_id"]})
    return player_towns


def getPlayerInfo(playerId):
    params = {"action": "playerInfo",
              "iso": region,
              "server": server,
              "playerId": playerId
              }

    rq = requests.post(url_base, params)

    player_data = rq.json()
    return player_data


def getIslandId(x, y):
    for island in islands:
        if x in island["x"] and y in island["y"]:
            return int(island["id"])
    return 0


def getIslandInfo(islandId):
    params = {"action": "islandCities",
              "iso": region,
              "server": server,
              "islandId": islandId
              }
    rq = requests.post(url_base, params)
    island_data = rq.json()
    return island_data


def getAllyId(allyname):
    alliances = getAllyData()
    for alliance in alliances:
        if re.match(r"^"+allyname+"$", alliance["tag"]) or re.match(r"^"+allyname+"$", alliance["name"]):
            return alliance["id"]
    return 0


def getAllyInfo(allyId):
    params = {"action": "allyInfo",
              "iso": region,
              "server": server,
              "allyId": allyId
              }
    rq = requests.post(url_base, params)

    ally_data = rq.json()
    return ally_data