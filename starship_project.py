import pymongo
import requests

client = pymongo.MongoClient()
db = client['starwars']


def get_all_jsons(api_link):

    """
    Reads API link and returns list of all JSON files associated with it through the "next" keyword
    Returns full JSON file
    """
    full_jsons = []

    while True:
        resp = requests.get(api_link).json()
        full_jsons += resp["results"]
        if resp["next"] is None:
            break
        api_link = resp["next"]

    print("Returned all JSON files...")
    return full_jsons


def api_url_to_id(api_link):
    """
    Helper function that takes in character API link and returns their ID
    Returns: name of character
    """

    name = requests.get(api_link).json()["name"]
    pilot_id = db.characters.find_one({"name": name}, {"_id"})["_id"]
    print(type(pilot_id))
    return pilot_id


def update_jsons(jsons):
    """
    Loops through JSON files
    Changes pilot data from API link to pilot ID
    Returns: Updated list of jsons
    """

    for json_dict in jsons:
        json_dict["pilots"] = [api_url_to_id(url) for url in json_dict["pilots"]]

    print("Pilot API url converted to ID...")
    return jsons


def upload_jsons(jsons):
    """
    Uploads each JSON file individually
    Creates starships collection if it doesn't already exist
    Returns: nothing

    """
    for starship in jsons:
        db.starships.insert_one(starship)

    print("Uploaded to MongoDB database.")
    return None


if __name__ == "__main__":

    db.starships.drop()

    # Execution
    starship_jsons = get_all_jsons("https://swapi.dev/api/starships")       # Get all JSONs
    id_jsons = update_jsons(starship_jsons)                                  # Update JSONs
    upload_jsons(id_jsons)                                                   # Upload modified JSONs to starships collection
