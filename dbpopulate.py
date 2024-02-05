from pymongo import MongoClient
import requests

client = MongoClient("mongodb+srv://Kolo:leceki73@skins.dpdrssl.mongodb.net/?retryWrites=true&w=majority")
db = client['CommunityDragon']
collection = db['List_of_Skins']
dbList = []

def load_static_data_champions():
    champ_list = {}

    url = 'https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/champion-summary.json'
    response = requests.get(url)
    response.raise_for_status()
    result = response.json()

    for k in result:
        if(k['name'] == "None"):
            continue
        champ_list[k['id']] = {k['name']}
    return champ_list

def load_static_data_champions_specific(champ_id):
    eliminate = ["alias", "tacticalInfo", "playstyleInfo", "squarePortraitPath", "stingerSfxPath", "chooseVoPath", "banVoPath", "roles", "recommendedItemDefaults", "passive", "spells", "spellbookOverride"]
    
    url = f'https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/champions/{champ_id}.json'
    response = requests.get(url)
    response.raise_for_status()
    result = response.json()

    for key in eliminate:
        if "skins" in result and isinstance(result["skins"], list):
            new_skins_list = [{"id": item["id"], "name": item["name"], "description": item["description"], "splashPath": item["splashPath"], "tilePath": item["tilePath"], "loadScreenPath": item["loadScreenPath"]} for item in result["skins"] if isinstance(item, dict) and "id" in item and "name" in item and "description" in item and "splashPath" in item and "tilePath" in item and "loadScreenPath" in item]
        result["skins"] = new_skins_list
        result.pop(key, None)

    return result

def change_paths(obj):
    replacement_patterns = {
        "splashPath": ('/lol-game-data/assets/', '/rcp-be-lol-game-data/global/default/'),
        "tilePath": ('/lol-game-data/assets/', '/rcp-be-lol-game-data/global/default/'),
        "loadScreenPath": ('/lol-game-data/assets/', '/rcp-be-lol-game-data/global/default/')
    }

    for skin in obj.get("skins", []):
        for key in skin:
            if key in replacement_patterns:
                old_pattern, new_pattern = replacement_patterns[key]
                skin[key] = skin[key].replace(old_pattern, new_pattern).lower()

    return obj

champ_list = load_static_data_champions()
for k in champ_list:
    dbList.append(change_paths(load_static_data_champions_specific(k)))
collection.insert_many(dbList)