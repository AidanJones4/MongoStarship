import pymongo
import requests
from pprint import pprint as pp

client = pymongo.MongoClient()
db = client['starwars']

db.starships.drop()


def get_all_json(api_link):

    """
    Reads API link and returns list of all JSON files associated with it through the "next" keyword
    Returns list of JSONs
    """
    list_of_jsons = []

    while True:
        resp = requests.get(api_link).json()
        list_of_jsons += resp["results"]
        if resp["next"] is None:
            break
        api_link = resp["next"]

    print("List of all JSON files created...")
    return list_of_jsons


def api_url_to_id(api_link):
    """
    Helper function that takes in character API link and returns their name
    Returns: name of character
    """

    name = requests.get(api_link).json()["name"]
    pilot_id = db.characters.find_one({"name": name}, {"_id"})["_id"]
    return pilot_id


def update_json(list_of_jsons):
    """
    Loops through list of json files
    Changes pilot data from API link to pilot ID
    Returns: Updated list of jsons
    """

    for json_dict in list_of_jsons:
        json_dict["pilots"] = [api_url_to_id(url) for url in json_dict["pilots"]]

    print("Pilot API links changed to character name...")
    return list_of_jsons


def upload_jsons(list_of_jsons):
    """
    Uploads each JSON element within list of JSONS one at a time into starships collection
    Creates starships collection if doesn't already exist
    Returns: nothing

    """
    for starship in list_of_jsons:
        db.starships.insert_one(starship)

    print("Uploaded to MongoDB database")
    return None


# Execution
jsons = get_all_json("https://swapi.dev/api/starships")     # Get all JSONs
id_json = update_json(jsons)                                # Update JSONs
upload_jsons(id_json)                                       # Upload modified JSONs to starships collection
