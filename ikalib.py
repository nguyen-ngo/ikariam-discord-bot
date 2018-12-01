import requests

url_base = "http://ika-search.com/getSite.py"
iso = "us"
server = "Eirene"


def getPlayerData():
    params = {"action": "autocompleteList",
              "iso": iso,
              "server": server
              }
    rq1 = requests.post(url_base, params)
    server_data = rq1.json()
    player_data = server_data["player"]
    return player_data


def getAllyData():
    params = {"action": "autocompleteList",
              "iso": iso,
              "server": server
              }
    rq1 = requests.post(url_base, params)
    server_data = rq1.json()
    ally_data = server_data["ally"]
    return ally_data


def getPlayerId(playername):
    params = {"action": "autocompleteList",
              "iso": iso,
              "server": server
              }
    rq1 = requests.post(url_base, params)
    server_data = rq1.json()
    player_data = server_data["player"]

    for player in player_data:
        if playername in player["pseudo"]:
            return player["id"]
    return 0


def getPlayerInfo(playerId):
    params = {"action": "playerInfo",
              "iso": iso,
              "server": server,
              "playerId": playerId
              }

    rq2 = requests.post(url_base, params)

    player_data = rq2.json()

    town_data = player_data["cities"]

    player_towns = []
    for town in town_data:
        player_towns.append({"coord": "[" + str(town["x"]) + ":" + str(town["y"]) + "]", "name": town["name"], "level": town["level"], "resource_id": town["resource_id"], "wonder_id": town["wonder_id"]})
    return player_towns


def getAllyId(allytag):
    params = {"action": "autocompleteList",
              "iso": iso,
              "server": server
              }
    rq1 = requests.post(url_base, params)
    server_data = rq1.json()
    ally_data = server_data["ally"]

    for ally in ally_data:
        if allytag in ally["tag"]:
            return ally["id"]
        return 0


def getAllyInfo(allytag):
    allyId = getAllyId(allytag)
    params = {"action": "allyInfo",
              "iso": iso,
              "server": server,
              "allyId": allyId
              }
    rq1 = requests.post(url_base, params)
    player_data = rq1.json()
    member_data = player_data["members"]

    member_list = []
    for member in member_data:
        member_list.append({"name": member["pseudo"], "state": member["state"], "score": member["score"], "army_score": member["army_score_main"]})
    return member_list
