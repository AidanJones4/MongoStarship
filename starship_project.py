import pymongo
import requests
from pprint import pprint as pp

client = pymongo.MongoClient()
db = client['starwars']

db.starships.drop()


def get_all_json(api_link):

    """
    Reads API link and returns list of all JSON files associated with it through the next keyword
    Returns list of JSONs
    """
    list_of_jsons = []

    while True:
        resp = requests.get(api_link).json()
        list_of_jsons.append(resp["results"])
        if resp["next"] is None:
            break
        api_link = resp["next"]

    return list_of_jsons


def api_link_to_name(api_link):
    """
    Helper function that takes in character API link and returns their name
    Returns: name of character
    """

    resp = requests.get(api_link).json()
    return resp["name"]


# Following 2 functions could easily be grouped into 1

def change_pilot_api_links(list_of_jsons):
    """
    Loops through list of json files
    Changes pilot data from API link to pilot name
    Returns: Updated list of jsons, list of names of the pilots with no duplicates
    """
    list_of_pilots = []

    for i in range(len(list_of_jsons)):                                                                 # Loop through list of JSON file
        for j in range(len(list_of_jsons[i])):                                                          # Loop through elements within JSON file
            for k in range(len(list_of_jsons[i][j]["pilots"])):                                         # Loop through list of pilot data
                list_of_jsons[i][j]["pilots"][k] = api_link_to_name(list_of_jsons[i][j]["pilots"][k])   # Update pilot list with name (API link --> Name)
                list_of_pilots.append(list_of_jsons[i][j]["pilots"][k])                                 # Append pilot name to list
    return list_of_jsons, list(set(list_of_pilots))                                                     # Return updated jsons and list of pilot names (removed dupes)


def change_pilot_name_to_id(list_of_jsons):
    """
    Loops through list of json files
    Changes pilot data from name to object ID by querying the "characters" collection
    Returns: Updated list of jsons
    """

    # Same nested loop structure as above
    for i in range(len(list_of_jsons)):
        for j in range(len(list_of_jsons[i])):
            for k in range(len(list_of_jsons[i][j]["pilots"])):
                pilot_name = list_of_jsons[i][j]["pilots"][k]
                pilot_id = db.characters.find_one({"name":pilot_name},{"_id"})["_id"]   # Query characters collection for the ID of the pilot
                list_of_jsons[i][j]["pilots"][k] = pilot_id                             # Update JSON file

    return list_of_jsons


def upload_jsons(list_of_jsons):
    """
    Uploads each JSON element within list of JSONS one at a time into starships collection
    Creates starships collection if doesn't already exist
    Returns: nothing

    """
    for json in list_of_jsons:
        for starship in json:
            db.starships.insert_one(starship)

    return None


# Execution
jsons = get_all_json("https://swapi.dev/api/starships")     # Get all JSONs
name_jsons, pilots = change_pilot_api_links(jsons)          # Update JSONs to include Pilot name instead of API link
pp(pilots)                                                  # Print list of pilots, notice Jek Tono Porkins, have a laugh
id_jsons = change_pilot_name_to_id(name_jsons)              # Update JSONs to include character ID instead of pilot name
upload_jsons(id_jsons)                                      # Upload modified JSONs to starships collection
